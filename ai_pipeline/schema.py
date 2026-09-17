"""
Preemption Event Schema Definition.

Compliant with Pydantic v2 and Raipur Police Commissionerate ITMS.
Validates the exact 8-field MQTT JSON schema:
1. junction_id
2. timestamp
3. override_source
4. vehicle_detected
5. license_plate
6. confidence
7. lane_cleared
8. preemption_duration_sec
"""

from datetime import datetime, timezone
from enum import Enum
import json
from typing import Annotated, Any, Dict, Optional, Union
from pydantic import BaseModel, ConfigDict, Field, StringConstraints, field_validator


class VehicleTypeEnum(str, Enum):
    """Supported emergency vehicle classifications."""
    AMBULANCE = "AMBULANCE"
    FIRE_TRUCK = "FIRE_TRUCK"
    POLICE_CRUISER = "POLICE_CRUISER"


class LaneDirectionEnum(str, Enum):
    """Traffic corridor approach headings."""
    NORTH_BOUND = "NORTH_BOUND"
    SOUTH_BOUND = "SOUTH_BOUND"
    EAST_BOUND = "EAST_BOUND"
    WEST_BOUND = "WEST_BOUND"


# Regular expressions for validation
JUNCTION_ID_REGEX = r"^[A-Z0-9_]+$"
TIMESTAMP_ISO8601_REGEX = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$"
OVERRIDE_SOURCE_REGEX = r"^[A-Z0-9_]+$"
# Matches standard Indian plates (e.g., CG04MB1234, DL01A1234) or BH series (e.g., 22BH1234AA)
LICENSE_PLATE_REGEX = r"^[A-Z]{2}[0-9]{1,2}[A-Z]{1,3}[0-9]{4}$|^[0-9]{2}BH[0-9]{4}[A-Z]{1,2}$"


class PreemptionEventPayload(BaseModel):
    """
    Standardized Preemption Event Telemetry Payload for Raipur ITMS.
    Strictly adheres to the 8-field specification required by the
    Raipur Police Commissionerate ICCC traffic server.
    """
    model_config = ConfigDict(
        extra="forbid",
        use_enum_values=True,
        json_schema_extra={
            "example": {
                "junction_id": "RPR_GE_ROAD_04",
                "timestamp": "2026-09-17T06:15:22Z",
                "override_source": "HANDHELD_RF_UNIT_02",
                "vehicle_detected": "AMBULANCE",
                "license_plate": "CG04MB1234",
                "confidence": 0.94,
                "lane_cleared": "NORTH_BOUND",
                "preemption_duration_sec": 22,
            }
        }
    )

    junction_id: Annotated[
        str,
        StringConstraints(min_length=3, max_length=32, pattern=JUNCTION_ID_REGEX)
    ] = Field(
        ...,
        description="Unique identifier for traffic junction in Raipur ITMS network (e.g. RPR_GE_ROAD_04)",
        examples=["RPR_GE_ROAD_04"]
    )

    timestamp: Annotated[
        str,
        StringConstraints(pattern=TIMESTAMP_ISO8601_REGEX)
    ] = Field(
        ...,
        description="ISO-8601 UTC timestamp of preemption event (e.g. 2026-09-17T06:15:22Z)",
        examples=["2026-09-17T06:15:22Z"]
    )

    override_source: Annotated[
        str,
        StringConstraints(min_length=3, max_length=32, pattern=OVERRIDE_SOURCE_REGEX)
    ] = Field(
        ...,
        description="Hardware or software unit initiating preemption (e.g. HANDHELD_RF_UNIT_02, EDGE_AI_CCTV_CAM01)",
        examples=["HANDHELD_RF_UNIT_02", "EDGE_AI_CCTV_CAM01"]
    )

    vehicle_detected: VehicleTypeEnum = Field(
        ...,
        description="Classified emergency vehicle category (AMBULANCE, FIRE_TRUCK, POLICE_CRUISER)",
        examples=[VehicleTypeEnum.AMBULANCE]
    )

    license_plate: Annotated[
        str,
        StringConstraints(pattern=LICENSE_PLATE_REGEX)
    ] = Field(
        ...,
        description="Extracted and normalized Indian registration plate (e.g. CG04MB1234 or 22BH1234AA)",
        examples=["CG04MB1234"]
    )

    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Combined detection and strobe optical beacon confidence metric in range [0.0, 1.0]",
        examples=[0.94]
    )

    lane_cleared: LaneDirectionEnum = Field(
        ...,
        description="Approach corridor granted emergency priority green phase",
        examples=[LaneDirectionEnum.NORTH_BOUND]
    )

    preemption_duration_sec: int = Field(
        ...,
        ge=5,
        le=120,
        description="Duration in seconds of active priority green phase (range: 5 to 120)",
        examples=[22]
    )

    @field_validator("confidence")
    @classmethod
    def round_confidence(cls, v: float) -> float:
        """Round confidence to two decimal places for clean telemetry."""
        return round(float(v), 2)

    def to_mqtt_json(self, indent: Optional[int] = None) -> str:
        """Serializes payload to exact MQTT JSON string."""
        return self.model_dump_json(indent=indent)

    def to_dict(self) -> Dict[str, Any]:
        """Returns payload as a standard Python dictionary."""
        return self.model_dump()

    @classmethod
    def create_now(
        cls,
        junction_id: str,
        override_source: str,
        vehicle_detected: Union[VehicleTypeEnum, str],
        license_plate: str,
        confidence: float,
        lane_cleared: Union[LaneDirectionEnum, str],
        preemption_duration_sec: int,
    ) -> "PreemptionEventPayload":
        """Factory helper creating an event with the current UTC timestamp."""
        now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        return cls(
            junction_id=junction_id,
            timestamp=now_utc,
            override_source=override_source,
            vehicle_detected=VehicleTypeEnum(vehicle_detected),
            license_plate=license_plate,
            confidence=confidence,
            lane_cleared=LaneDirectionEnum(lane_cleared),
            preemption_duration_sec=preemption_duration_sec,
        )


def validate_preemption_payload(data: Union[str, Dict[str, Any]]) -> PreemptionEventPayload:
    """
    Validates arbitrary dictionary or JSON string against the PreemptionEventPayload schema.
    Raises pydantic.ValidationError on schema mismatch.
    """
    if isinstance(data, str):
        raw = json.loads(data)
    else:
        raw = data
    return PreemptionEventPayload.model_validate(raw)


if __name__ == "__main__":
    # Self-test when executed directly
    sample = {
        "junction_id": "RPR_GE_ROAD_04",
        "timestamp": "2026-09-17T06:15:22Z",
        "override_source": "HANDHELD_RF_UNIT_02",
        "vehicle_detected": "AMBULANCE",
        "license_plate": "CG04MB1234",
        "confidence": 0.94,
        "lane_cleared": "NORTH_BOUND",
        "preemption_duration_sec": 22,
    }
    event = validate_preemption_payload(sample)
    print("Schema validation successful!")
    print(event.to_mqtt_json(indent=2))
