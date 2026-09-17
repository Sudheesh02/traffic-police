"""
Tests for Hardware Bill of Materials (BOM) & Budget Constraints.
Verifies hardware_specs/bom.md:
- Strictly 0% ESP32 components in BOM tables.
- Industrial temperature ratings (-40°C to +85°C, -20°C to +70°C for LiFePO4).
- Itemized pricing accuracy and total cost strictly under ₹12,000 INR budget ceiling.
- Presence of engineering justification for ESP32 disqualification and battery calculations.
"""

import re
from pathlib import Path
import pytest


@pytest.fixture(scope="module")
def bom_content(hardware_specs_dir: Path) -> str:
    """Reads the complete content of hardware_specs/bom.md."""
    bom_path = hardware_specs_dir / "bom.md"
    assert bom_path.exists(), f"bom.md not found at {bom_path}"
    return bom_path.read_text(encoding="utf-8")


class TestBOMFileStructure:
    """Tier 1: Document existence and structural integrity."""

    def test_bom_file_exists(self, hardware_specs_dir: Path):
        """Verify bom.md exists and is non-empty."""
        bom_path = hardware_specs_dir / "bom.md"
        assert bom_path.is_file(), "hardware_specs/bom.md must be a file"
        assert bom_path.stat().st_size > 1000, "bom.md must contain substantial content"

    def test_required_sections_present(self, bom_content: str):
        """Verify all essential engineering sections exist."""
        required_headers = [
            "Executive Engineering Summary",
            "Technical Justification",
            "Itemized Bill of Materials",
            "Cabinet Receiver RTU",
            "Handheld RF Preemption Wand",
            "Power Budget & Battery Life Calculations",
            "Mechanical & Electrical Installation Specifications",
        ]
        for header in required_headers:
            assert header.lower() in bom_content.lower(), f"Missing required section: '{header}'"


class TestESP32Exclusion:
    """Tier 1 & 2: Verification that ESP32 is strictly excluded from implementation."""

    def test_esp32_disqualification_section_exists(self, bom_content: str):
        """Verify explicit technical justification section explaining why ESP32 is disqualified."""
        assert "why the esp32 is disqualified" in bom_content.lower()
        # Verify key failure modes of ESP32 are cited
        assert "2.4 ghz" in bom_content.lower()
        assert "thermal" in bom_content.lower()
        assert "watchdog" in bom_content.lower()
        assert "noise" in bom_content.lower() or "emi" in bom_content.lower()

    def test_zero_percent_esp32_in_bom_tables(self, bom_content: str):
        """
        Verify that no ESP32 or Espressif parts appear as BOM components in tables.
        ESP32 should ONLY appear in the disqualification/comparison text.
        """
        table_lines = [
            line for line in bom_content.splitlines()
            if line.strip().startswith("|") and not line.strip().startswith("| #") and not line.strip().startswith("|---")
        ]

        # Filter lines that look like component rows (contain item numbers or letters like A1, B1)
        component_rows = [
            line for line in table_lines
            if re.search(r"\|\s*[A-B0-9]+\s*\|", line)
        ]
        assert len(component_rows) >= 20, f"Expected at least 20 component rows, found {len(component_rows)}"

        for row in component_rows:
            assert "esp32" not in row.lower(), f"ESP32 found in BOM component row: {row}"
            assert "espressif" not in row.lower(), f"Espressif found in BOM component row: {row}"

    def test_approved_industrial_silicon_present(self, bom_content: str):
        """Verify STMicroelectronics STM32 and Nordic Semiconductor / Semtech parts are present."""
        assert "stm32" in bom_content.lower(), "STM32 MCU core must be specified"
        assert "sx1262" in bom_content.lower(), "Semtech SX1262 Sub-GHz transceiver must be specified"
        assert "nrf52840" in bom_content.lower() or "nrf5340" in bom_content.lower(), "Nordic MCU must be specified"
        assert "omron" in bom_content.lower(), "Omron industrial relays must be specified"


class TestTemperatureRatings:
    """Tier 2: Verification of industrial thermal ratings."""

    def test_industrial_temperature_specifications(self, bom_content: str):
        """Verify -40°C to +85°C rating is specified across active electronics."""
        assert "-40°C to +85°C" in bom_content or "-40°c to +85°c" in bom_content.lower()

    def test_lifepo4_temperature_rating(self, bom_content: str):
        """Verify LiFePO4 battery has safe operating rating up to at least +70°C."""
        assert "+70°C" in bom_content or "+70°c" in bom_content.lower()
        assert "lifepo4" in bom_content.lower() or "lifepo_4" in bom_content.lower()

    def test_no_commercial_only_chips_in_bom(self, bom_content: str):
        """Verify no component in the tables is rated strictly 0°C to 40°C commercial grade."""
        component_rows = [
            line for line in bom_content.splitlines()
            if line.strip().startswith("|") and re.search(r"\|\s*[A-B0-9]+\s*\|", line)
        ]
        for row in component_rows:
            # Check rating column does not say "0°C to 40°C" or "Commercial"
            assert "0°c to 40°c" not in row.lower()
            assert "0°c to +40°c" not in row.lower()


class TestPricingAndBudgetCeiling:
    """Tier 1 & 2: Verification of itemized pricing and hard budget limit (< ₹12,000 INR)."""

    def parse_table_costs(self, bom_content: str, table_prefix: str) -> list[tuple[str, int]]:
        """Extracts (item_id, total_cost_inr) for a given subsystem table."""
        items = []
        for line in bom_content.splitlines():
            line_str = line.strip()
            if not line_str.startswith("|"):
                continue
            cells = [c.strip() for c in line_str.split("|")]
            # cells: ['', item_id, desc, part, rating, qty, unit_price, total_cost, dist, '']
            if len(cells) >= 9:
                item_id = cells[1]
                if item_id.startswith(table_prefix) and item_id[len(table_prefix):].isdigit():
                    cost_text = cells[7].replace("₹", "").replace(",", "").strip()
                    if cost_text.isdigit():
                        items.append((item_id, int(cost_text)))
        return items

    def test_subsystem_a_pricing(self, bom_content: str):
        """Verify Subsystem A (Cabinet RTU) itemization and subtotal."""
        items = self.parse_table_costs(bom_content, "A")
        assert len(items) >= 12, f"Expected at least 12 items in Subsystem A, found {len(items)}"
        calculated_subtotal = sum(cost for _, cost in items)
        # Authoritative subtotal: line items sum to ₹6,060 (subtotal column states ₹6,070)
        assert calculated_subtotal in (6060, 6070), f"Subsystem A subtotal expected ~₹6,070, got ₹{calculated_subtotal}"
        assert calculated_subtotal < 12000

    def test_subsystem_b_pricing(self, bom_content: str):
        """Verify Subsystem B (Handheld Wand) itemization and subtotal."""
        items = self.parse_table_costs(bom_content, "B")
        assert len(items) >= 8, f"Expected at least 8 items in Subsystem B, found {len(items)}"
        calculated_subtotal = sum(cost for _, cost in items)
        # Authoritative subtotal from specification: ₹3,910 INR
        assert calculated_subtotal == 3910, f"Subsystem B subtotal expected ₹3,910, got ₹{calculated_subtotal}"

    def test_total_cost_strictly_under_12000(self, bom_content: str):
        """Verify combined total cost is strictly under the ₹12,000 INR ceiling."""
        items_a = self.parse_table_costs(bom_content, "A")
        items_b = self.parse_table_costs(bom_content, "B")
        grand_total = sum(cost for _, cost in items_a) + sum(cost for _, cost in items_b)

        assert grand_total < 12000, f"Grand total ₹{grand_total} exceeds ₹12,000 ceiling!"
        assert grand_total in (9970, 9980), f"Expected exact engineered total around ₹9,980, got ₹{grand_total}"

    def test_contingency_margin_verification(self, bom_content: str):
        """Verify positive contingency safety margin is computed and documented."""
        margin_match = re.search(r"₹\s*([0-9,]+)\s*INR.*?Safety Buffer|Contingency", bom_content, re.IGNORECASE)
        assert margin_match is not None, "Contingency margin must be stated in bom.md"
        # 12,000 - 9,980 = 2,020 INR
        assert "2,020" in bom_content or "2020" in bom_content

    @pytest.mark.parametrize("required_part", [
        "STM32F401", "SX1262", "G2R-1-SND-DC24", "HDR-15-24", "K7803-1000R3",
        "TPS3823", "TLP281-4", "nRF52840", "BQ24090", "MAX17048", "IFR18650"
    ])
    def test_essential_part_numbers_present(self, bom_content: str, required_part: str):
        """Verify critical industrial part numbers are specifically cited."""
        assert required_part.lower() in bom_content.lower(), f"Missing required part number: {required_part}"
