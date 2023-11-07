"""Load pipette command request, result, and implementation models."""
from __future__ import annotations
from pydantic import BaseModel, Field
from typing import TYPE_CHECKING, Optional, Type, Union, Tuple
from typing_extensions import Literal

from opentrons_shared_data.pipette.dev_types import PipetteNameType
from opentrons.types import MountType

from .command import (
    AbstractCommandWithPrivateResultImpl,
    BaseCommand,
    BaseCommandCreate,
)
from .configuring_common import PipetteConfigUpdateResultMixin

if TYPE_CHECKING:
    from ..execution import EquipmentHandler


LoadPipetteCommandType = Literal["loadPipette"]


class LoadPipettePrivateResult(PipetteConfigUpdateResultMixin):
    """The not-to-be-exposed results of a load pipette call."""

    ...


class LoadPipetteParams(BaseModel):
    """Payload needed to load a pipette on to a mount."""

    # TODO (tz, 11-23-22): remove Union when refactoring load_pipette for 96 channels.
    # https://opentrons.atlassian.net/browse/RLIQ-255
    pipetteName: Union[PipetteNameType, Literal["p1000_96"]] = Field(
        ...,
        description="The load name of the pipette to be required.",
    )
    mount: MountType = Field(
        ...,
        description="The mount the pipette should be present on.",
    )
    pipetteId: Optional[str] = Field(
        None,
        description="An optional ID to assign to this pipette. If None, an ID "
        "will be generated.",
    )


class LoadPipetteResult(BaseModel):
    """Result data for executing a LoadPipette."""

    pipetteId: str = Field(
        ...,
        description="An ID to reference this pipette in subsequent commands.",
    )


class LoadPipetteImplementation(
    AbstractCommandWithPrivateResultImpl[
        LoadPipetteParams, LoadPipetteResult, LoadPipettePrivateResult
    ]
):
    """Load pipette command implementation."""

    def __init__(self, equipment: EquipmentHandler, **kwargs: object) -> None:
        self._equipment = equipment

    async def execute(
        self, params: LoadPipetteParams
    ) -> Tuple[LoadPipetteResult, LoadPipettePrivateResult]:
        """Check that requested pipette is attached and assign its identifier."""
        loaded_pipette = await self._equipment.load_pipette(
            pipette_name=params.pipetteName,
            mount=params.mount,
            pipette_id=params.pipetteId,
        )

        return LoadPipetteResult(
            pipetteId=loaded_pipette.pipette_id
        ), LoadPipettePrivateResult(
            pipette_id=loaded_pipette.pipette_id,
            serial_number=loaded_pipette.serial_number,
            config=loaded_pipette.static_config,
        )


class LoadPipette(BaseCommand[LoadPipetteParams, LoadPipetteResult]):
    """Load pipette command model."""

    commandType: LoadPipetteCommandType = "loadPipette"
    params: LoadPipetteParams
    result: Optional[LoadPipetteResult]

    _ImplementationCls: Type[LoadPipetteImplementation] = LoadPipetteImplementation


class LoadPipetteCreate(BaseCommandCreate[LoadPipetteParams]):
    """Load pipette command creation request model."""

    commandType: LoadPipetteCommandType = "loadPipette"
    params: LoadPipetteParams

    _CommandCls: Type[LoadPipette] = LoadPipette
