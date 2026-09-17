# Original User Request

## 2026-09-17T01:12:07Z

Build "SynchroClear-ITS", a hybrid Edge-AI and Sub-GHz RF manual override system for emergency vehicle preemption, specifically tailored for the Raipur Police Commissionerate Traffic Hackathon. The solution must be low-cost and easily integrable with existing Raipur ICCC servers.

Working directory: c:/Users/Asus/Desktop/Misc _Projects/Traffic Police
Integrity mode: demo

## Requirements

### R1. Hackathon Pitch Deck & Documentation
Create the content for a 6-slide pitch deck (as outlined in the master prompt) and a comprehensive `README.md`. The documentation must highlight the Raipur-specific advantages: zero cost overhead (leveraging existing CCTV), challan protection via synchronized logging, and low-cost STM32/Relay retrofits (under ₹12,000 per junction).

### R2. Edge-AI Pipeline Prototype
Develop a functional Python prototype for the AI pipeline (`ai_pipeline/`). This must include a script that uses YOLO (for detecting ambulances/fire trucks) and an OCR library (for license plate logging). It should output a structured JSON log simulating a push to the Raipur Police Commissionerate traffic server via MQTT.

### R3. Firmware Skeletons & Hardware Specs
Write firmware skeleton code (`firmware/`) for both the Handheld RF Transmitter (e.g., Nordic nRF/Sub-GHz logic) and the Cabinet Receiver (STM32 with fail-safe relay interlocks). Include a Bill of Materials (`hardware_specs/bom.md`) focusing on industrial-grade, cost-effective components suitable for Raipur's climate and infrastructure.

### R4. System Diagrams
Generate system architecture and state machine (inter-green safety clearance) diagrams, saved in the `docs/` directory.

## Acceptance Criteria

### Documentation & Pitch
- [ ] `README.md` exists and contains the Executive Summary, Problem Statement, and Raipur-specific impact.
- [ ] A `pitch_deck.md` or similar file contains the exact text and structure for the 6 required slides.

### AI Pipeline
- [ ] `ai_pipeline/detect_emergency.py` (or similar) runs without syntax errors and processes a sample image/video or mock data to output a JSON log.
- [ ] The output JSON log strictly follows the schema provided (junction_id, timestamp, vehicle_detected, license_plate, etc.).

### Firmware & Hardware
- [ ] Firmware stubs exist for both transmitter and receiver with clear inline comments explaining the state machine logic (Green -> Yellow -> All-Red -> Priority Green).
- [ ] `bom.md` lists specific industrial components (not ESP32) with estimated costs in INR, keeping the per-junction budget under ₹12,000.

### Diagrams
- [ ] Architecture and state machine diagrams are generated and saved in `docs/` (using Mermaid markdown or standard image generation).
