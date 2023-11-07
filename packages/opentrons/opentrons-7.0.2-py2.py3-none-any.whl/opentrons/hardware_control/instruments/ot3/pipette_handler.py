"""Shared code for managing pipette configuration and storage."""
from dataclasses import dataclass
import logging
from typing import (
    Callable,
    Dict,
    Optional,
    Tuple,
    Any,
    cast,
    List,
    Sequence,
    Iterator,
    TypeVar,
)
from typing_extensions import Final
import numpy
from opentrons_shared_data.pipette.dev_types import UlPerMmAction

from opentrons_shared_data.errors.exceptions import (
    CommandPreconditionViolated,
    CommandParameterLimitViolated,
)
from opentrons_shared_data.pipette.pipette_definition import (
    liquid_class_for_volume_between_default_and_defaultlowvolume,
)

from opentrons import types as top_types
from opentrons.hardware_control.types import (
    CriticalPoint,
    HardwareAction,
    Axis,
    OT3Mount,
)
from opentrons.hardware_control.errors import (
    TipAttachedError,
    NoTipAttachedError,
)
from opentrons.hardware_control.constants import (
    SHAKE_OFF_TIPS_SPEED,
    SHAKE_OFF_TIPS_PICKUP_DISTANCE,
    DROP_TIP_RELEASE_DISTANCE,
    SHAKE_OFF_TIPS_DROP_DISTANCE,
)

from opentrons.hardware_control.dev_types import PipetteDict
from .pipette import Pipette
from .instrument_calibration import (
    PipetteOffsetSummary,
    PipetteOffsetByPipetteMount,
    check_instrument_offset_reasonability,
)


MOD_LOG = logging.getLogger(__name__)

# TODO both pipette handlers should be combined once the pipette configurations
# are unified AND we separate out the concept of changing pipette state versus static state
HOME_POSITION: Final[float] = 230.15

MountType = TypeVar("MountType", top_types.Mount, OT3Mount)
InstrumentsByMount = Dict[MountType, Optional[Pipette]]
PipetteHandlingData = Tuple[Pipette, OT3Mount]


@dataclass(frozen=True)
class LiquidActionSpec:
    axis: Axis
    volume: float
    plunger_distance: float
    speed: float
    acceleration: float
    instr: Pipette
    current: float


# TODO during refactor we should figure out if
# we still need these dataclasses


@dataclass(frozen=True)
class PickUpTipPressSpec:
    relative_down: top_types.Point
    relative_up: top_types.Point
    current: Dict[Axis, float]
    speed: float


@dataclass(frozen=True)
class TipMotorPickUpTipSpec:
    tiprack_down: top_types.Point
    tiprack_up: top_types.Point
    pick_up_distance: float
    speed: float
    currents: Dict[Axis, float]
    # FIXME we should throw this in a config
    # file of some sort
    home_buffer: float = 0


@dataclass(frozen=True)
class PickUpTipSpec:
    plunger_prep_pos: float
    plunger_currents: Dict[Axis, float]
    presses: List[PickUpTipPressSpec]
    shake_off_list: List[Tuple[top_types.Point, Optional[float]]]
    retract_target: float
    pick_up_motor_actions: Optional[TipMotorPickUpTipSpec]


@dataclass(frozen=True)
class DropTipMove:
    target_position: float
    current: Dict[Axis, float]
    speed: Optional[float]
    home_after: bool = False
    home_after_safety_margin: float = 0
    home_axes: Sequence[Axis] = tuple()
    is_ht_tip_action: bool = False
    # FIXME we should throw this in a config
    # file of some sort
    home_buffer: float = 0


@dataclass(frozen=True)
class DropTipSpec:
    drop_moves: List[DropTipMove]
    shake_moves: List[Tuple[top_types.Point, Optional[float]]]
    ending_current: Dict[Axis, float]


class OT3PipetteHandler:
    IHP_LOG = MOD_LOG.getChild("InstrumentHandler")

    def __init__(self, attached_instruments: InstrumentsByMount[OT3Mount]):
        assert attached_instruments
        self._attached_instruments: InstrumentsByMount[OT3Mount] = attached_instruments
        self._ihp_log = self.__class__.IHP_LOG

    def reset_instrument(self, mount: Optional[OT3Mount] = None) -> None:
        """
        Reset the internal state of a pipette by its mount, without doing
        any lower level reconfiguration. This is useful to make sure that no
        settings changes from a protocol persist.

        :param mount: If specified, reset that mount. If not specified,
                      reset both
        """

        # need to have a reset function on the pipette
        def _reset(m: OT3Mount) -> None:
            self._ihp_log.info(f"Resetting configuration for {m}")
            p = self._attached_instruments[m]
            if not p:
                return
            p.reset_pipette_offset(OT3Mount.from_mount(m), to_default=False)
            p.reload_configurations()
            p.reset_state()

        if not mount:
            for m in type(list(self._attached_instruments.keys())[0]):
                _reset(m)
        else:
            _reset(mount)

    def get_instrument_offset(self, mount: OT3Mount) -> Optional[PipetteOffsetSummary]:
        """Get the specified pipette's offset."""
        assert mount != OT3Mount.GRIPPER, "Wrong mount type to fetch pipette offset"
        try:
            pipette = self.get_pipette(mount)
        except top_types.PipetteNotAttachedError:
            return None
        return self._return_augmented_offset_data(
            pipette, mount, pipette.pipette_offset
        )

    def reset_instrument_offset(self, mount: OT3Mount, to_default: bool) -> None:
        """
        Temporarily reset the pipette offset to default values.
        :param mount: Modify the given mount.
        """
        pipette = self.get_pipette(mount)
        pipette.reset_pipette_offset(mount, to_default)

    def save_instrument_offset(
        self, mount: OT3Mount, delta: top_types.Point
    ) -> PipetteOffsetSummary:
        """
        Save a new instrument offset the pipette offset to a particular value.
        :param mount: Modify the given mount.
        :param delta: The offset to set for the pipette.
        """
        pipette = self.get_pipette(mount)
        offset_data = pipette.save_pipette_offset(mount, delta)
        return self._return_augmented_offset_data(pipette, mount, offset_data)

    def _return_augmented_offset_data(
        self,
        pipette: Pipette,
        mount: OT3Mount,
        offset_data: PipetteOffsetByPipetteMount,
    ) -> PipetteOffsetSummary:
        if mount == OT3Mount.LEFT:
            other_pipette = self._attached_instruments.get(OT3Mount.RIGHT, None)
            if other_pipette:
                other_offset = other_pipette.pipette_offset.offset
            else:
                other_offset = top_types.Point(0, 0, 0)
            reasonability = check_instrument_offset_reasonability(
                offset_data.offset, other_offset
            )
        else:
            other_pipette = self._attached_instruments.get(OT3Mount.LEFT, None)
            if other_pipette:
                other_offset = other_pipette.pipette_offset.offset
            else:
                other_offset = top_types.Point(0, 0, 0)
            reasonability = check_instrument_offset_reasonability(
                other_offset, offset_data.offset
            )
        return PipetteOffsetSummary(
            offset=offset_data.offset,
            source=offset_data.source,
            status=offset_data.status,
            last_modified=offset_data.last_modified,
            reasonability_check_failures=reasonability,
        )

    # TODO(mc, 2022-01-11): change returned map value type to `Optional[PipetteDict]`
    # instead of potentially returning an empty dict
    # For compatibility purposes only right now. We should change this
    # as soon as we can modify the /pipettes endpoint.
    def get_attached_instruments(self) -> Dict[OT3Mount, PipetteDict]:
        """Get the status dicts of the cached attached instruments.

        Also available as :py:meth:`get_attached_instruments`.

        This returns a dictified version of the
        :py:class:`hardware_control.instruments.pipette.Pipette` as a dict keyed by
        the :py:class:`top_types.Mount` to which the pipette is attached.
        If no pipette is attached on a given mount, the mount key will
        still be present but will have the value ``None``.

        Note that this is only a query of a cached value; to actively scan
        for changes, use :py:meth:`cache_instruments`. This process deactivates
        the motors and should be used sparingly.
        """
        return {
            m: self.get_attached_instrument(m)
            for m in self._attached_instruments.keys()
        }

    # TODO(mc, 2022-01-11): change return type to `Optional[PipetteDict]` instead
    # of potentially returning an empty dict
    def get_attached_instrument(self, mount: OT3Mount) -> PipetteDict:
        # TODO (lc 12-05-2022) Kill this code ASAP
        instr = self._attached_instruments[mount]
        result: Dict[str, Any] = {}
        if instr:
            configs = [
                "name",
                "aspirate_flow_rate",
                "dispense_flow_rate",
                "pipette_id",
                "current_volume",
                "display_name",
                "tip_length",
                "model",
                "blow_out_flow_rate",
                "working_volume",
                "tip_overlap",
                "available_volume",
                "return_tip_height",
                "default_aspirate_flow_rates",
                "default_blow_out_flow_rates",
                "default_dispense_flow_rates",
                "back_compat_names",
                "supported_tips",
            ]

            instr_dict = instr.as_dict()
            # TODO (spp, 2021-08-27): Revisit this logic. Why do we need to build
            #  this dict newly every time? Any why only a few items are being updated?
            for key in configs:
                result[key] = instr_dict[key]

            result["min_volume"] = instr.liquid_class.min_volume
            result["max_volume"] = instr.liquid_class.max_volume
            result["channels"] = instr._max_channels
            result["has_tip"] = instr.has_tip
            result["tip_length"] = instr.current_tip_length
            result["aspirate_speed"] = self.plunger_speed(
                instr, instr.aspirate_flow_rate, "aspirate"
            )
            result["dispense_speed"] = self.plunger_speed(
                instr, instr.dispense_flow_rate, "dispense"
            )
            result["blow_out_speed"] = self.plunger_speed(
                instr, instr.blow_out_flow_rate, "dispense"
            )
            result["ready_to_aspirate"] = instr.ready_to_aspirate

            result["default_blow_out_speeds"] = {
                alvl: self.plunger_speed(instr, fr, "blowout")
                for alvl, fr in instr.blow_out_flow_rates_lookup.items()
            }

            result["default_dispense_speeds"] = {
                alvl: self.plunger_speed(instr, fr, "dispense")
                for alvl, fr in instr.dispense_flow_rates_lookup.items()
            }
            result["default_aspirate_speeds"] = {
                alvl: self.plunger_speed(instr, fr, "aspirate")
                for alvl, fr in instr.aspirate_flow_rates_lookup.items()
            }
            result[
                "default_push_out_volume"
            ] = instr.active_tip_settings.default_push_out_volume
        return cast(PipetteDict, result)

    @property
    def attached_instruments(self) -> Dict[OT3Mount, PipetteDict]:
        return self.get_attached_instruments()

    @property
    def hardware_instruments(self) -> InstrumentsByMount[OT3Mount]:
        """Do not write new code that uses this."""
        return self._attached_instruments

    def set_current_tiprack_diameter(
        self, mount: OT3Mount, tiprack_diameter: float
    ) -> None:
        instr = self.get_pipette(mount)
        self._ihp_log.info(
            "Updating tip rack diameter on pipette mount: "
            f"{mount}, tip diameter: {tiprack_diameter} mm"
        )
        instr.current_tiprack_diameter = tiprack_diameter

    def set_working_volume(self, mount: OT3Mount, tip_volume: float) -> None:
        instr = self.get_pipette(mount)
        if not instr:
            raise top_types.PipetteNotAttachedError(
                "No pipette attached to {} mount".format(mount.name)
            )
        self._ihp_log.info(
            "Updating working volume on pipette mount:"
            f"{mount}, tip volume: {tip_volume} ul"
        )
        instr.working_volume = tip_volume

    def calibrate_plunger(
        self,
        mount: OT3Mount,
        top: Optional[float] = None,
        bottom: Optional[float] = None,
        blow_out: Optional[float] = None,
        drop_tip: Optional[float] = None,
    ) -> None:
        """
        Set calibration values for the pipette plunger.
        This can be called multiple times as the user sets each value,
        or you can set them all at once.
        :param top: Touching but not engaging the plunger.
        :param bottom: Must be above the pipette's physical hard-stop, while
        still leaving enough room for 'blow_out'
        :param blow_out: Plunger is pushed down enough to expel all liquids.
        :param drop_tip: Position that causes the tip to be released from the
        pipette
        """
        instr = self.get_pipette(mount)
        pos_dict: Dict[str, float] = {
            "top": instr.plunger_positions.top,
            "bottom": instr.plunger_positions.bottom,
            "blow_out": instr.plunger_positions.blow_out,
            "drop_tip": instr.plunger_positions.drop_tip,
        }
        if top is not None:
            pos_dict["top"] = top
        if bottom is not None:
            pos_dict["bottom"] = bottom
        if blow_out is not None:
            pos_dict["blow_out"] = blow_out
        if drop_tip is not None:
            pos_dict["drop_tip"] = drop_tip
        instr.update_config_item(pos_dict)

    def set_flow_rate(
        self,
        mount: OT3Mount,
        aspirate: Optional[float] = None,
        dispense: Optional[float] = None,
        blow_out: Optional[float] = None,
    ) -> None:
        this_pipette = self.get_pipette(mount)
        if aspirate:
            this_pipette.aspirate_flow_rate = aspirate
        if dispense:
            this_pipette.dispense_flow_rate = dispense
        if blow_out:
            this_pipette.blow_out_flow_rate = blow_out

    def set_pipette_speed(
        self,
        mount: OT3Mount,
        aspirate: Optional[float] = None,
        dispense: Optional[float] = None,
        blow_out: Optional[float] = None,
    ) -> None:
        this_pipette = self.get_pipette(mount)
        if aspirate:
            this_pipette.aspirate_flow_rate = self.plunger_flowrate(
                this_pipette, aspirate, "aspirate"
            )
        if dispense:
            this_pipette.dispense_flow_rate = self.plunger_flowrate(
                this_pipette, dispense, "dispense"
            )
        if blow_out:
            this_pipette.blow_out_flow_rate = self.plunger_flowrate(
                this_pipette, blow_out, "blowout"
            )

    def instrument_max_height(
        self,
        mount: OT3Mount,
        retract_distance: float,
        critical_point: Optional[CriticalPoint],
    ) -> float:
        """Return max achievable height of the attached instrument
        based on the current critical point
        """
        cp = self.critical_point_for(mount, critical_point)

        max_height = HOME_POSITION - retract_distance + cp.z

        return max_height

    async def reset(self) -> None:
        self._attached_instruments = {
            k: None for k in self._attached_instruments.keys()
        }

    async def add_tip(self, mount: OT3Mount, tip_length: float) -> None:
        instr = self._attached_instruments[mount]
        attached = self.attached_instruments
        instr_dict = attached[mount]
        if instr and not instr.has_tip:
            instr.add_tip(tip_length=tip_length)
            # TODO (spp, 2021-08-27): These items are being updated in a local copy
            #  of the PipetteDict, which gets thrown away. Fix this.
            instr_dict["has_tip"] = True
            instr_dict["tip_length"] = tip_length
        else:
            self._ihp_log.warning(
                "attach tip called while tip already attached to {instr}"
            )

    async def remove_tip(self, mount: OT3Mount) -> None:
        instr = self._attached_instruments[mount]
        attached = self.attached_instruments
        instr_dict = attached[mount]
        if instr and instr.has_tip:
            instr.remove_tip()
            # TODO (spp, 2021-08-27): These items are being updated in a local copy
            #  of the PipetteDict, which gets thrown away. Fix this.
            instr_dict["has_tip"] = False
            instr_dict["tip_length"] = 0.0
        else:
            self._ihp_log.warning("detach tip called with no tip")

    def critical_point_for(
        self, mount: OT3Mount, cp_override: Optional[CriticalPoint] = None
    ) -> top_types.Point:
        """Return the current critical point of the specified mount.

        The mount's critical point is the position of the mount itself, if no
        pipette is attached, or the pipette's critical point (which depends on
        tip status).

        If `cp_override` is specified, and that critical point actually exists,
        it will be used instead. Invalid `cp_override`s are ignored.
        """
        pip = self._attached_instruments[OT3Mount.from_mount(mount)]
        if pip is not None and cp_override != CriticalPoint.MOUNT:
            return pip.critical_point(cp_override)
        else:
            return top_types.Point(0, 0, 0)

    def ready_for_tip_action(self, target: Pipette, action: HardwareAction) -> None:
        if not target.has_tip:
            raise NoTipAttachedError(f"Cannot perform {action} without a tip attached")
        if (
            action == HardwareAction.ASPIRATE
            and target.current_volume == 0
            and not target.ready_to_aspirate
        ):
            raise RuntimeError("Pipette not ready to aspirate")
        self._ihp_log.debug(f"{action} on {target.name}")

    def plunger_position(
        self, instr: Pipette, ul: float, action: "UlPerMmAction"
    ) -> float:
        mm = ul / instr.ul_per_mm(ul, action)
        position = instr.plunger_positions.bottom - mm
        return round(position, 6)

    def plunger_speed(
        self, instr: Pipette, ul_per_s: float, action: "UlPerMmAction"
    ) -> float:
        mm_per_s = ul_per_s / instr.ul_per_mm(instr.working_volume, action)
        return round(mm_per_s, 6)

    def plunger_flowrate(
        self, instr: Pipette, mm_per_s: float, action: "UlPerMmAction"
    ) -> float:
        ul_per_s = mm_per_s * instr.ul_per_mm(instr.working_volume, action)
        return round(ul_per_s, 6)

    def plunger_acceleration(self, instr: Pipette, ul_per_s_per_s: float) -> float:
        # using nominal ul/mm, to make sure accelerations are always the same
        # regardless of volume being aspirated/dispensed
        mm_per_s_per_s = ul_per_s_per_s / instr.config.shaft_ul_per_mm
        return round(mm_per_s_per_s, 6)

    def plan_check_aspirate(
        self,
        mount: OT3Mount,
        volume: Optional[float],
        rate: float,
    ) -> Optional[LiquidActionSpec]:
        """Check preconditions for aspirate, parse args, and calculate positions.

        While the mechanics of issuing an aspirate move itself are left to child
        classes, determining things like aspiration volume from the allowed argument
        types is invariant between machines, and this method gathers that functionality.

        Coalesce
        - Optional volumes

        Check
        - Aspiration volumes compared to max and remaining

        Calculate
        - Plunger distances (possibly calling an overridden plunger_volume)
        """
        instrument = self.get_pipette(mount)
        self.ready_for_tip_action(instrument, HardwareAction.ASPIRATE)
        if volume is None:
            self._ihp_log.debug(
                "No aspirate volume defined. Aspirating up to "
                "max_volume for the pipette"
            )
            asp_vol = instrument.available_volume
        else:
            asp_vol = volume

        if asp_vol == 0:
            return None

        assert instrument.ok_to_add_volume(
            asp_vol
        ), "Cannot aspirate more than pipette max volume"

        dist = self.plunger_position(
            instrument, instrument.current_volume + asp_vol, "aspirate"
        )
        speed = self.plunger_speed(
            instrument, instrument.aspirate_flow_rate * rate, "aspirate"
        )
        acceleration = self.plunger_acceleration(
            instrument, instrument.flow_acceleration
        )

        return LiquidActionSpec(
            axis=Axis.of_main_tool_actuator(mount),
            volume=asp_vol,
            plunger_distance=dist,
            speed=speed,
            acceleration=acceleration,
            instr=instrument,
            current=instrument.plunger_motor_current.run,
        )

    def plan_check_dispense(
        self,
        mount: OT3Mount,
        volume: Optional[float],
        rate: float,
        push_out: Optional[float],
    ) -> Optional[LiquidActionSpec]:
        """Check preconditions for dispense, parse args, and calculate positions.

        While the mechanics of issuing a dispense move itself are left to child
        classes, determining things like dispense volume from the allowed argument
        types is invariant between machines, and this method gathers that functionality.

        Coalesce
        - Optional volumes

        Check
        - Dispense volumes compared to max and remaining

        Calculate
        - Plunger distances (possibly calling an overridden plunger_volume)
        """

        instrument = self.get_pipette(mount)
        self.ready_for_tip_action(instrument, HardwareAction.DISPENSE)

        if volume is None:
            disp_vol = instrument.current_volume
            self._ihp_log.debug(
                "No dispense volume specified. Dispensing all "
                "remaining liquid ({}uL) from pipette".format(disp_vol)
            )
        else:
            disp_vol = volume

        # Ensure we don't dispense more than the current volume
        disp_vol = min(instrument.current_volume, disp_vol)
        is_full_dispense = numpy.isclose(instrument.current_volume - disp_vol, 0)

        if disp_vol == 0:
            return None

        if is_full_dispense:
            if push_out is None:
                push_out_ul = instrument.push_out_volume
            else:
                push_out_ul = push_out
        else:
            if push_out is not None and push_out != 0:
                raise CommandPreconditionViolated(
                    message="Cannot push_out on a dispense that does not leave the pipette empty",
                    detail={
                        "command": "dispense",
                        "remaining-volume": instrument.current_volume - disp_vol,
                    },
                )
            push_out_ul = 0

        push_out_dist_mm = push_out_ul / instrument.ul_per_mm(push_out_ul, "blowout")

        if not instrument.ok_to_push_out(push_out_dist_mm):
            raise CommandParameterLimitViolated(
                command_name="dispense",
                parameter_name="push_out",
                limit_statement="less than pipette max blowout volume",
                actual_value=str(push_out_ul),
            )

        dist = self.plunger_position(
            instrument, instrument.current_volume - disp_vol, "dispense"
        )
        speed = self.plunger_speed(
            instrument, instrument.dispense_flow_rate * rate, "dispense"
        )
        acceleration = self.plunger_acceleration(
            instrument, instrument.flow_acceleration
        )
        return LiquidActionSpec(
            axis=Axis.of_main_tool_actuator(mount),
            volume=disp_vol,
            plunger_distance=dist + push_out_dist_mm,
            speed=speed,
            acceleration=acceleration,
            instr=instrument,
            current=instrument.plunger_motor_current.run,
        )

    def plan_check_blow_out(
        self, mount: OT3Mount, volume: Optional[float] = None
    ) -> LiquidActionSpec:
        """Check preconditions and calculate values for blowout."""
        instrument = self.get_pipette(mount)
        self.ready_for_tip_action(instrument, HardwareAction.BLOWOUT)
        speed = self.plunger_speed(instrument, instrument.blow_out_flow_rate, "blowout")
        acceleration = self.plunger_acceleration(
            instrument, instrument.flow_acceleration
        )
        max_distance = (
            instrument.plunger_positions.blow_out - instrument.plunger_positions.bottom
        )
        if volume is None:
            distance_mm = max_distance
        else:
            ul = volume
            distance_mm = ul / instrument.ul_per_mm(ul, "blowout")
            if distance_mm > max_distance:
                raise CommandParameterLimitViolated(
                    command_name="blow_out",
                    parameter_name="volume",
                    limit_statement="less than the available distance for the plunger to move",
                    actual_value=str(volume),
                )

        return LiquidActionSpec(
            axis=Axis.of_main_tool_actuator(mount),
            volume=0,
            plunger_distance=distance_mm,
            speed=speed,
            acceleration=acceleration,
            instr=instrument,
            current=instrument.plunger_motor_current.run,
        )

    @staticmethod
    def _build_pickup_shakes(
        instrument: Pipette,
    ) -> List[Tuple[top_types.Point, Optional[float]]]:
        def build_one_shake() -> List[Tuple[top_types.Point, Optional[float]]]:
            shake_dist = float(SHAKE_OFF_TIPS_PICKUP_DISTANCE)
            shake_speed = float(SHAKE_OFF_TIPS_SPEED)
            return [
                (top_types.Point(-shake_dist, 0, 0), shake_speed),  # left
                (top_types.Point(2 * shake_dist, 0, 0), shake_speed),  # right
                (top_types.Point(-shake_dist, 0, 0), shake_speed),  # center
                (top_types.Point(0, -shake_dist, 0), shake_speed),  # front
                (top_types.Point(0, 2 * shake_dist, 0), shake_speed),  # back
                (top_types.Point(0, -shake_dist, 0), shake_speed),  # center
                (top_types.Point(0, 0, DROP_TIP_RELEASE_DISTANCE), None),  # up
            ]

        return []

    def plan_check_pick_up_tip(
        self,
        mount: OT3Mount,
        tip_length: float,
        presses: Optional[int],
        increment: Optional[float],
    ) -> Tuple[PickUpTipSpec, Callable[[], None]]:
        # Prechecks: ready for pickup tip and press/increment are valid
        instrument = self.get_pipette(mount)
        if instrument.has_tip:
            raise TipAttachedError("Cannot pick up tip with a tip attached")
        self._ihp_log.debug(f"Picking up tip on {mount.name}")

        def add_tip_to_instr() -> None:
            instrument.add_tip(tip_length=tip_length)
            instrument.set_current_volume(0)

        if presses is None or presses < 0:
            checked_presses = instrument.pick_up_configurations.presses
        else:
            checked_presses = presses

        if not increment or increment < 0:
            check_incr = instrument.pick_up_configurations.increment
        else:
            check_incr = increment

        pick_up_speed = instrument.pick_up_configurations.speed

        def build_presses() -> Iterator[Tuple[float, float]]:
            # Press the nozzle into the tip <presses> number of times,
            # moving further by <increment> mm after each press
            for i in range(checked_presses):
                # move nozzle down into the tip
                press_dist = (
                    -1.0 * instrument.pick_up_configurations.distance
                    + -1.0 * check_incr * i
                )
                # move nozzle back up
                backup_dist = -press_dist
                yield (press_dist, backup_dist)

        if instrument.channels == 96:
            return (
                PickUpTipSpec(
                    plunger_prep_pos=instrument.plunger_positions.bottom,
                    plunger_currents={
                        Axis.of_main_tool_actuator(
                            mount
                        ): instrument.plunger_motor_current.run,
                    },
                    presses=[],
                    shake_off_list=[],
                    retract_target=instrument.pick_up_configurations.distance,
                    pick_up_motor_actions=TipMotorPickUpTipSpec(
                        # Move onto the posts
                        tiprack_down=top_types.Point(0, 0, -7),
                        tiprack_up=top_types.Point(0, 0, 2),
                        pick_up_distance=instrument.pick_up_configurations.distance,
                        speed=instrument.pick_up_configurations.speed,
                        currents={Axis.Q: instrument.pick_up_configurations.current},
                        home_buffer=10,
                    ),
                ),
                add_tip_to_instr,
            )
        return (
            PickUpTipSpec(
                plunger_prep_pos=instrument.plunger_positions.bottom,
                plunger_currents={
                    Axis.of_main_tool_actuator(
                        mount
                    ): instrument.plunger_motor_current.run
                },
                presses=[
                    PickUpTipPressSpec(
                        current={
                            Axis.by_mount(
                                mount
                            ): instrument.pick_up_configurations.current
                        },
                        speed=pick_up_speed,
                        relative_down=top_types.Point(0, 0, press_dist),
                        relative_up=top_types.Point(0, 0, backup_dist),
                    )
                    for press_dist, backup_dist in build_presses()
                ],
                shake_off_list=self._build_pickup_shakes(instrument),
                retract_target=instrument.pick_up_configurations.distance
                + check_incr * checked_presses
                + 2,
                pick_up_motor_actions=None,
            ),
            add_tip_to_instr,
        )

    @staticmethod
    def _shake_off_tips_drop(
        tiprack_diameter: float,
    ) -> List[Tuple[top_types.Point, Optional[float]]]:
        # tips don't always fall off, especially if resting against
        # tiprack or other tips below it. To ensure the tip has fallen
        # first, shake the pipette to dislodge partially-sealed tips,
        # then second, raise the pipette so loosened tips have room to fall
        shake_off_dist = SHAKE_OFF_TIPS_DROP_DISTANCE
        if tiprack_diameter > 0.0:
            shake_off_dist = min(shake_off_dist, tiprack_diameter / 4)
        shake_off_dist = max(shake_off_dist, 1.0)
        speed = SHAKE_OFF_TIPS_SPEED
        return [
            (top_types.Point(-shake_off_dist, 0, 0), speed),  # left
            (top_types.Point(2 * shake_off_dist, 0, 0), speed),  # right
            (top_types.Point(-shake_off_dist, 0, 0), speed),  # center
            (top_types.Point(0, 0, DROP_TIP_RELEASE_DISTANCE), None),  # top
        ]

    def _droptip_sequence_builder(
        self,
        bottom_pos: float,
        droptip_pos: float,
        plunger_currents: Dict[Axis, float],
        drop_tip_currents: Dict[Axis, float],
        speed: float,
        home_after: bool,
        home_axes: Sequence[Axis],
        is_ht_pipette: bool = False,
    ) -> Callable[[], List[DropTipMove]]:
        def build() -> List[DropTipMove]:
            base = [
                DropTipMove(
                    target_position=bottom_pos, current=plunger_currents, speed=None
                ),
                DropTipMove(
                    target_position=droptip_pos,
                    current=drop_tip_currents,
                    speed=speed,
                    home_after=home_after,
                    home_after_safety_margin=abs(bottom_pos - droptip_pos),
                    home_axes=home_axes,
                    is_ht_tip_action=is_ht_pipette,
                    home_buffer=10 if is_ht_pipette else 0,
                ),
                DropTipMove(  # always finish drop-tip at a known safe plunger position
                    target_position=bottom_pos, current=plunger_currents, speed=None
                ),
            ]
            return base

        return build

    def plan_check_drop_tip(
        self,
        mount: OT3Mount,
        home_after: bool,
    ) -> Tuple[DropTipSpec, Callable[[], None]]:
        instrument = self.get_pipette(mount)
        self.ready_for_tip_action(instrument, HardwareAction.DROPTIP)

        is_96_chan = instrument.channels == 96

        bottom = instrument.plunger_positions.bottom
        droptip = (
            instrument.drop_configurations.distance
            if is_96_chan
            else instrument.plunger_positions.drop_tip
        )
        speed = instrument.drop_configurations.speed
        shakes: List[Tuple[top_types.Point, Optional[float]]] = []

        def _remove_tips() -> None:
            instrument.set_current_volume(0)
            instrument.current_tiprack_diameter = 0.0
            instrument.remove_tip()

        drop_tip_current_axis = (
            Axis.Q if is_96_chan else Axis.of_main_tool_actuator(mount)
        )
        seq_builder_ot3 = self._droptip_sequence_builder(
            bottom,
            droptip,
            {Axis.of_main_tool_actuator(mount): instrument.plunger_motor_current.run},
            {drop_tip_current_axis: instrument.drop_configurations.current},
            speed,
            home_after,
            (Axis.of_main_tool_actuator(mount),),
            is_96_chan,
        )

        seq_ot3 = seq_builder_ot3()
        return (
            DropTipSpec(
                drop_moves=seq_ot3,
                shake_moves=shakes,
                ending_current={
                    Axis.of_main_tool_actuator(
                        mount
                    ): instrument.plunger_motor_current.run
                },
            ),
            _remove_tips,
        )

    def has_pipette(self, mount: OT3Mount) -> bool:
        return bool(self._attached_instruments[mount])

    def get_pipette(self, mount: OT3Mount) -> Pipette:
        pip = self._attached_instruments[mount]
        if not pip:
            raise top_types.PipetteNotAttachedError(
                f"No pipette attached to {mount.name} mount"
            )
        return pip

    async def set_liquid_class(self, mount: OT3Mount, liquid_class: str) -> None:
        pip = self.get_pipette(mount)
        pip.set_liquid_class_by_name(liquid_class)

    async def configure_for_volume(self, mount: OT3Mount, volume: float) -> None:
        pip = self.get_pipette(mount)
        if pip.current_volume > 0:
            # Switching liquid classes can't happen when there's already liquid
            return
        new_class_name = liquid_class_for_volume_between_default_and_defaultlowvolume(
            volume,
            pip.liquid_class_name,
            pip.config.liquid_properties,
        )
        pip.set_liquid_class_by_name(new_class_name.name)
