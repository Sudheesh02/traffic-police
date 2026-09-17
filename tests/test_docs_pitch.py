"""
Tests for Hackathon Pitch Deck (pitch_deck.md) & Documentation (README.md).
Verifies:
- All 6 required slides exist with exact structure (Takeaway, Judges Need to Know, Proof/Metrics, Visual Layout, 30s Spoken Pitch).
- 5-second scan rule compliance with bold concept anchors.
- Absolute exclusion of banned AI buzzwords (delve, tapestry, seamlessly, empowers, etc.).
- Raipur-specific impact sections (Jaistambh Chowk, Ghadi Chowk, Mekahara Hospital, e-Challan whitelisting).
- Comprehensive README.md sections (Executive Summary, Problem, Impact Matrix, Repo Tree, Quickstart).
"""

import re
from pathlib import Path
import pytest


# List of banned AI buzzwords according to hackathon presentation guidelines
BANNED_AI_WORDS = [
    "delve",
    "tapestry",
    "seamlessly",
    "empowers",
    "beacon of hope",
    "revolutionary game-changer",
    "testament",
    "plethora",
    "moreover",
    "furthermore",
]


@pytest.fixture(scope="module")
def pitch_deck_text(repo_root: Path) -> str:
    """Reads the pitch deck file."""
    pitch_path = repo_root / "pitch_deck.md"
    assert pitch_path.exists(), f"pitch_deck.md not found at {pitch_path}"
    return pitch_path.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def readme_text(repo_root: Path) -> str:
    """Reads the root README file."""
    readme_path = repo_root / "README.md"
    assert readme_path.exists(), f"README.md not found at {readme_path}"
    return readme_path.read_text(encoding="utf-8")


class TestPitchDeckStructure:
    """Tier 1: 6-Slide Executive Deck Structure."""

    def test_all_six_slides_exist(self, pitch_deck_text: str):
        """Verify all 6 slides are clearly delimited with headers."""
        for i in range(1, 7):
            pattern = rf"###\s*Slide\s*{i}:"
            assert re.search(pattern, pitch_deck_text, re.IGNORECASE) is not None, f"Slide {i} header missing!"

    @pytest.mark.parametrize("slide_num", [1, 2, 3, 4, 5, 6])
    def test_slide_mandatory_components(self, pitch_deck_text: str, slide_num: int):
        """Every slide must feature Key Takeaway, Judges Need to Know, Metrics, Layout, and Spoken Pitch."""
        # Find the slice for this slide
        pattern = rf"(###\s*Slide\s*{slide_num}:.*?)(?=###\s*Slide|\Z)"
        match = re.search(pattern, pitch_deck_text, re.DOTALL | re.IGNORECASE)
        assert match is not None, f"Failed to extract Slide {slide_num}"
        slide_content = match.group(1)

        # 1. 5-Second Scan Key Takeaway
        assert "Key Takeaway" in slide_content, f"Slide {slide_num} missing 'Key Takeaway'"
        # 2. What Judges Need to Know
        assert "What Judges Need to Know" in slide_content, f"Slide {slide_num} missing 'What Judges Need to Know'"
        # 3. Hard Proof & Metrics
        assert "Hard Proof & Metrics" in slide_content, f"Slide {slide_num} missing 'Hard Proof & Metrics'"
        # 4. Recommended Visual Layout
        assert "Recommended Visual Layout" in slide_content, f"Slide {slide_num} missing 'Recommended Visual Layout'"
        # 5. 30-Second Spoken Pitch
        assert "30-Second Spoken Pitch" in slide_content, f"Slide {slide_num} missing '30-Second Spoken Pitch'"

    @pytest.mark.parametrize("slide_num", [1, 2, 3, 4, 5, 6])
    def test_spoken_script_is_substantial(self, pitch_deck_text: str, slide_num: int):
        """Verify the 30-second spoken pitch is a complete monologue (>30 words)."""
        pattern = rf"###\s*Slide\s*{slide_num}:.*?(?:####\s*4\.\s*30-Second Spoken Pitch|30-Second Spoken Pitch)\s*\"?(.*?)(?:\"?\s*---|\Z)"
        match = re.search(pattern, pitch_deck_text, re.DOTALL | re.IGNORECASE)
        assert match is not None, f"Could not find spoken script in Slide {slide_num}"
        script_text = match.group(1).strip().strip('"')
        word_count = len(script_text.split())
        assert word_count >= 30, f"Slide {slide_num} spoken pitch too short ({word_count} words; expected >=30)"


class TestNoBannedAIWords:
    """Tier 2: Scan for prohibited AI buzzwords."""

    @pytest.mark.parametrize("word", BANNED_AI_WORDS)
    def test_pitch_deck_free_of_banned_words(self, pitch_deck_text: str, word: str):
        """Verify banned buzzwords are absent in pitch_deck.md."""
        pattern = rf"\b{re.escape(word)}\b"
        matches = re.findall(pattern, pitch_deck_text, re.IGNORECASE)
        assert len(matches) == 0, f"Banned word '{word}' found in pitch_deck.md: {len(matches)} occurrence(s)"

    @pytest.mark.parametrize("word", ["delve", "tapestry", "seamlessly", "empowers"])
    def test_readme_free_of_banned_words(self, readme_text: str, word: str):
        """Verify core banned buzzwords are absent in README.md."""
        pattern = rf"\b{re.escape(word)}\b"
        matches = re.findall(pattern, readme_text, re.IGNORECASE)
        assert len(matches) == 0, f"Banned word '{word}' found in README.md: {len(matches)} occurrence(s)"


class TestRaipurSpecificImpact:
    """Tier 1 & 4: Raipur-specific operational and geographical validation."""

    @pytest.mark.parametrize("keyword", [
        "Jaistambh",
        "Ghadi Chowk",
        "Mekahara",
        "e-Challan",
        "Sub-GHz",
        "STM32",
    ])
    def test_pitch_deck_mentions_raipur_context(self, pitch_deck_text: str, keyword: str):
        """Verify Raipur locations and technical specifics are emphasized in pitch_deck.md."""
        assert keyword.lower() in pitch_deck_text.lower(), f"Keyword '{keyword}' missing from pitch_deck.md"

    @pytest.mark.parametrize("keyword", [
        "Jaistambh Chowk",
        "Ghadi Chowk",
        "Mekahara",
        "e-Challan",
        "12,000",
        "IRC",
    ])
    def test_readme_mentions_raipur_context(self, readme_text: str, keyword: str):
        """Verify Raipur locations and constraints are emphasized in README.md."""
        assert keyword.lower() in readme_text.lower(), f"Keyword '{keyword}' missing from README.md"


class TestReadmeCompleteness:
    """Tier 1: Comprehensive README structure."""

    def test_readme_mandatory_sections(self, readme_text: str):
        """Verify README contains all required sections from Master Prompt & R1."""
        required_headers = [
            "Executive Summary",
            "Problem Statement",
            "Cognitive Dissonance",
            "Raipur-Specific Impact",
            "System Architecture",
            "Repository Structure",
        ]
        for header in required_headers:
            assert header.lower() in readme_text.lower(), f"README.md missing section: '{header}'"
        assert "quickstart" in readme_text.lower() or "quick start" in readme_text.lower()

    def test_readme_quickstart_commands_present(self, readme_text: str):
        """Verify actionable runnable commands exist in Quick Start Guide."""
        assert "detect_emergency.py" in readme_text
        assert "requirements.txt" in readme_text
        assert "python" in readme_text

    def test_readme_sample_json_present(self, readme_text: str):
        """Verify example JSON telemetry is displayed in README.md."""
        assert "junction_id" in readme_text
        assert "license_plate" in readme_text
        assert "override_source" in readme_text
