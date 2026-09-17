"""
Pytest configuration and shared fixtures for SynchroClear-ITS test suite.
"""

import sys
from pathlib import Path
import pytest

# Ensure repository root is on sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


@pytest.fixture(scope="session")
def repo_root() -> Path:
    """Returns absolute path to the repository root."""
    return REPO_ROOT


@pytest.fixture(scope="session")
def docs_dir(repo_root: Path) -> Path:
    """Returns path to docs directory."""
    return repo_root / "docs"


@pytest.fixture(scope="session")
def hardware_specs_dir(repo_root: Path) -> Path:
    """Returns path to hardware_specs directory."""
    return repo_root / "hardware_specs"


@pytest.fixture(scope="session")
def firmware_dir(repo_root: Path) -> Path:
    """Returns path to firmware directory."""
    return repo_root / "firmware"


@pytest.fixture(scope="session")
def ai_pipeline_dir(repo_root: Path) -> Path:
    """Returns path to ai_pipeline directory."""
    return repo_root / "ai_pipeline"


@pytest.fixture
def sample_valid_payload_dict():
    """Returns an authoritative valid 8-field MQTT payload dictionary."""
    return {
        "junction_id": "RPR_GE_ROAD_04",
        "timestamp": "2026-09-17T06:15:22Z",
        "override_source": "HANDHELD_RF_UNIT_02",
        "vehicle_detected": "AMBULANCE",
        "license_plate": "CG04MB1234",
        "confidence": 0.94,
        "lane_cleared": "NORTH_BOUND",
        "preemption_duration_sec": 22,
    }


@pytest.fixture
def sample_bh_payload_dict():
    """Returns an authoritative valid payload with Bharat (BH) series plate."""
    return {
        "junction_id": "RPR_JAISTAMBH_01",
        "timestamp": "2026-09-17T08:30:00Z",
        "override_source": "EDGE_AI_CCTV_CAM01",
        "vehicle_detected": "FIRE_TRUCK",
        "license_plate": "22BH1234AA",
        "confidence": 0.98,
        "lane_cleared": "EAST_BOUND",
        "preemption_duration_sec": 30,
    }
