import math
from datetime import datetime, timedelta

import bpkio_cli.utils.prompt as prompt
import click
import cloup
from bpkio_api.helpers.handlers import ContentHandler, factory
from bpkio_api.helpers.source_type import SourceTypeDetector
from bpkio_api.helpers.times import relative_time
from bpkio_api.models import (
    AssetSourceIn,
    LiveSourceIn,
    SourceType,
    VirtualChannelService,
    VirtualChannelSlotIn,
    VirtualChannelSlotType,
)
from bpkio_cli.core.app_context import AppContext
from bpkio_cli.core.config_provider import ConfigProvider
from bpkio_cli.core.resource_decorator import add_category_info
from bpkio_cli.utils.datetimes import (
    parse_date_expression_as_utc,
    parse_duration_expression,
)
from bpkio_cli.writers.colorizer import Colorizer as CL


def populate_virtual_channel_slots_command():
    # COMMAND: POPULATE
    @cloup.command(help="Populate the slots of a Virtual Channel service")
    @click.pass_obj
    def populate(obj: AppContext):
        vc_id = obj.resources.last()
        populate_virtual_channel_slots_with_prompts(obj, vc_id)

    return populate


def populate_virtual_channel_slots_with_prompts(context: AppContext, vc_id):
    api = context.api.services.virtual_channel
    vc: VirtualChannelService = api.retrieve(vc_id)

    all_sources = context.api.sources.list()

    # Define source list
    slot_sources = [
        s
        for s in all_sources
        if s.type in (SourceType.LIVE, SourceType.ASSET) and s.format == vc.format
    ]
    slot_sources = sorted(slot_sources, key=lambda s: s.id, reverse=True)
    slot_sources = context.cache.sort_resources_by_most_recently_accessed(slot_sources)
    source_choices = [
        dict(value=s.id, name=f"({s.id})  {s.name}  [{s.type.value}]")
        for s in slot_sources
    ]

    source_choices = [dict(value="BYURL", name="-- From URL --")] + source_choices

    if vc.adBreakInsertion is not None:
        source_choices = [dict(value="ADBREAK", name="-- Ad Break --")] + source_choices

    source_choices = [dict(value=None, name="-- End of schedule --")] + source_choices

    # Ask for a category
    categories = context.api.categories.list()
    categories = sorted(categories, key=lambda c: c.name)
    category_choices = [
        dict(value=c.id, name=f"({c.id})  {c.name}") for c in categories
    ]
    category_choices.insert(0, dict(value=None, name="-- No category --"))

    category_id = prompt.fuzzy(
        message="What category do you want to associate the schedule with?",
        choices=category_choices,
    )

    # Ask for a starting time
    starting_in = None
    while starting_in is None:
        starting_in = prompt.text(
            message="Starting time",
            default="now",
            filter=lambda t: parse_start_time_prompt(t, filter=True),
            transformer=lambda t: parse_start_time_prompt(t, filter=False),
            long_instruction="Use an exact time, or a time expression "
            "(eg. 'in 10 min', 'tomorrow 10am', 'now').  "
            "Or use 'slot' if you want to align with an existing future slot",
        )

        # Optionally select a slot to align with
        if starting_in == "SLOT":
            candidate_slots = api.slots.list(
                vc.id,
                from_time=datetime.now(),
                to_time=datetime.now() + timedelta(hours=4),
            )
            add_category_info(candidate_slots)
            if not candidate_slots:
                click.echo(CL.error("No present or future slot found"))
                starting_in = None  # ready to go back through the while loop
            else:
                slot_choices = [
                    dict(
                        value=sl.id,
                        name=f"from {sl.startTime} - ({sl.id}) {sl.type}"
                        f"{': ' + sl.replacement.name if sl.replacement else ''}"
                        f"{'  [cat: ' + sl.category.name + ']' if sl.category else ''}",
                    )
                    for sl in candidate_slots
                ]
                slot_id = prompt.fuzzy(
                    message="Select a slot to align with", choices=slot_choices
                )
                slot = next(s for s in candidate_slots if s.id == slot_id)

                starting_in = prompt.select(
                    message="What end of the slot do you want to align to?",
                    choices=[
                        dict(
                            value=slot.startTime,
                            name=f"Start - {relative_time(slot.startTime)}",
                        ),
                        dict(
                            value=slot.endTime,
                            name=f"End - {relative_time(slot.endTime)}",
                        ),
                    ],
                )
    # end while

    # Check if there are slots starting at that time (and in the next 4 hours)
    list_args = dict(
        from_time=starting_in,
        to_time=starting_in + timedelta(hours=4),
    )
    if category_id:
        list_args["categories"] = category_id

    existing_slots = api.slots.list(vc.id, **list_args)
    if existing_slots:
        clear = prompt.confirm(
            message="There are already slots in this channel for that category, and at that starting time. "
            "Would you like to clear all future slots for that category?",
            default=False,
        )

        if clear:
            for s in existing_slots:
                api.slots.delete(service_id=vc_id, slot_id=s.id)
        else:
            pass

    schedule = []
    t0 = starting_in

    click.secho("\nDefine schedule for the channel", fg="yellow")
    adbreak_default_duration = "2 min"
    while True:
        # Ask for a source
        msg = "Source to add" if len(schedule) == 0 else "Next source to add"
        source_id = prompt.fuzzy(message=msg, choices=source_choices)

        # Stop the loop if the user wants to end the schedule
        if source_id is None:
            break

        # retrieve the source from the source list
        source = None
        if isinstance(source_id, int) or source_id.isdigit():
            source = next(s for s in slot_sources if s.id == source_id)

        # allow new source
        if source_id == "BYURL":
            url = prompt.text(message="Source URL", level=1)

            source_type = SourceTypeDetector.determine_source_type(url)
            name = ".." + url[-30:] if len(url) > 30 else url

            match source_type:
                case SourceType.LIVE:
                    name = "Live Source for VC: .." + name
                    (source, status) = context.api.sources.live.upsert(
                        LiveSourceIn(name=name, url=url), if_exists="retrieve"
                    )
                    source_id = source.id
                case SourceType.ASSET:
                    name = "Source Asset for VC: .." + name
                    (source, status) = context.api.sources.asset.upsert(
                        AssetSourceIn(name=name, url=url), if_exists="retrieve"
                    )
                    source_id = source.id
                case _:
                    click.secho(
                        f"Source type not supported in VCs: {source_type}",
                        fg="red",
                    )
                    source_id = "SKIP"

            if source:
                click.secho(
                    f"     » Source {source.id}: {status.name.lower()}", fg="green"
                )
            if source.format != vc.format:
                click.secho(
                    f"     ! Source {source.id} has wrong format ({source.format} != {vc.format})",
                    fg="red",
                )
                source = None
                source_id = "SKIP"

        # set default duration for valid sources
        if source_id == "ADBREAK":
            default_duration = adbreak_default_duration

        if source:
            if source.type == SourceType.LIVE:
                default_duration = "10 min"
            else:
                handler: ContentHandler = factory.create_handler(
                    source.full_url, user_agent=ConfigProvider().get_user_agent()
                )
                default_duration = str(math.floor(handler.get_duration()))

        if source_id != "SKIP":
            # ask for duration to insert
            duration = prompt.text(
                message="Duration",
                default=default_duration,
                level=1,
                filter=lambda t: parse_duration_expression(t),
                transformer=lambda t: str(
                    timedelta(seconds=parse_duration_expression(t))
                ),
                long_instruction="Use a number (of seconds) or a duration expression (eg. 2h, 30m)",
            )

            if source_id == "ADBREAK":
                adbreak_default_duration = str(duration)

            schedule.append(dict(source_id=source_id, duration=duration, start=t0))

            t0 += timedelta(seconds=duration)

    schedule_duration = sum([s["duration"] for s in schedule])

    click.echo()

    # Ask if slots are to be repeated
    if len(schedule):
        repeat = prompt.number(
            message="How many times would you like to repeat this schedule?",
            default=1,
            min_allowed=1,
            max_allowed=20,
            filter=lambda i: int(i),
        )

        # Now create the slots
        slots = []
        for i in range(repeat):
            for sched in schedule:
                if sched["source_id"] == "ADBREAK":
                    slot = VirtualChannelSlotIn(
                        startTime=(
                            sched["start"] + timedelta(seconds=schedule_duration * i)
                        ),
                        duration=sched["duration"],
                        type=VirtualChannelSlotType.AD_BREAK,
                    )
                else:
                    slot = VirtualChannelSlotIn(
                        startTime=(
                            sched["start"] + timedelta(seconds=schedule_duration * i)
                        ),
                        duration=sched["duration"],
                        replacement=dict(id=sched["source_id"]),
                        type=VirtualChannelSlotType.CONTENT,
                    )
                if category_id:
                    slot.category = dict(id=category_id)

                slot = api.slots.create(vc.id, slot)
                slots.append(slot)

        # decorate with the full categories
        add_category_info(slots)

        context.response_handler.treat_list_resources(
            slots,
            select_fields=[
                "id",
                "name",
                "type",
                "relativeStartTime",
                "relativeEndTime",
                "duration",
                "replacement.id",
                "replacement.name",
                "category.id",
                "category.name",
            ],
        )


def parse_start_time_prompt(t: str, filter=False):
    if t.startswith("slot"):
        return "SLOT"

    try:
        if filter:
            # returned value
            return parse_date_expression_as_utc(t)
        else:
            # displayed value
            return relative_time(parse_date_expression_as_utc(t))
    except Exception as e:
        return None
