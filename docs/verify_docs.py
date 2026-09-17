"""
Verification script for docs/:
- Validates Markdown structure and required sections
- Validates Mermaid syntax and structure
- Validates SVG artifacts and XML well-formedness
"""
import os
import re
import xml.etree.ElementTree as ET

DOCS_DIR = os.path.abspath(os.path.dirname(__file__))

def verify_system_architecture_md():
    filepath = os.path.join(DOCS_DIR, "system_architecture.md")
    assert os.path.exists(filepath), f"File not found: {filepath}"
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Check 4-layer Mermaid architecture flowchart
    assert "```mermaid" in content, "Missing mermaid block"
    assert "flowchart TD" in content, "Missing flowchart TD"
    
    # Check required layers
    required_layers = [
        "Layer 1: Field Layer",
        "Layer 2: Cabinet & Junction RTU Layer",
        "Layer 3: Edge-AI Vision Layer",
        "Layer 4: Central Command Layer"
    ]
    for layer in required_layers:
        assert layer in content, f"Missing layer in markdown: {layer}"
    
    # Check required components
    required_components = [
        "Handheld RF Transmitter",
        "Emergency Vehicle",
        "Citizen Motorists",
        "STM32",
        "Semtech SX1262",
        "Form-C",
        "Traffic Controller",
        "Signal Heads",
        "IP Camera",
        "RTSP",
        "YOLOv8",
        "Strobe",
        "ANPR",
        "Raipur",
        "ICCC",
        "e-Challan Exemption Gateway",
        "NIC"
    ]
    for comp in required_components:
        assert comp.lower() in content.lower(), f"Missing component mention: {comp}"
    
    # Check sequences
    required_sequences = [
        "Sequence 1: Ground Sub-GHz RF Override Trigger",
        "Sequence 2: Edge-AI Optical & Computer Vision Pipeline",
        "Sequence 3: Hardware Interlock & Signal Head Actuation",
        "Sequence 4: Central Command Telemetry & Citizen Challan Exemption"
    ]
    for seq in required_sequences:
        assert seq in content, f"Missing sequence: {seq}"
    
    print("PASS: docs/system_architecture.md verified successfully.")

def verify_state_machine_md():
    filepath = os.path.join(DOCS_DIR, "state_machine.md")
    assert os.path.exists(filepath), f"File not found: {filepath}"
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Check stateDiagram-v2
    assert "stateDiagram-v2" in content, "Missing stateDiagram-v2"
    
    # Check sequenceDiagram
    assert "sequenceDiagram" in content, "Missing sequenceDiagram"
    
    # Check millisecond-level transitions
    timing_checks = [
        "3,500 ms",
        "2,000 ms",
        "STATE_ACTIVE_AMBER",
        "STATE_ALL_RED_CLEARANCE",
        "STATE_PRIORITY_GREEN",
        "STATE_RECOVERY_AMBER",
        "STATE_RECOVERY_ALL_RED",
        "STATE_NORMAL_CYCLE",
        "Form-C",
        "IRC:SP:12"
    ]
    for check in timing_checks:
        assert check in content, f"Missing timing/safety element: {check}"
        
    # Check interlock matrix table
    assert "Fail-Safe Interlock State Matrix Table" in content, "Missing interlock state matrix"
    assert "Relay K1" in content and "Relay K6" in content, "Missing relay designations"
    assert "Break-Before-Make" in content, "Missing Break-Before-Make description"
    
    print("PASS: docs/state_machine.md verified successfully.")

def verify_svg_files():
    svgs = [
        "system_architecture.svg",
        "state_machine.svg",
        "timing_sequence.svg"
    ]
    for svg_name in svgs:
        filepath = os.path.join(DOCS_DIR, svg_name)
        assert os.path.exists(filepath), f"SVG missing: {svg_name}"
        tree = ET.parse(filepath)
        root = tree.getroot()
        assert root.tag.endswith("svg"), f"Root is not svg in {svg_name}"
        width = root.attrib.get("width")
        height = root.attrib.get("height")
        viewbox = root.attrib.get("viewBox")
        assert width and height and viewbox, f"Missing dimensions in {svg_name}"
        num_elements = len(list(root.iter()))
        assert num_elements > 50, f"SVG seems too sparse: {num_elements} elements in {svg_name}"
        print(f"PASS: {svg_name} ({width}x{height}, viewBox='{viewbox}', {num_elements} elements) verified.")

def verify_mermaid_blocks():
    md_files = ["system_architecture.md", "state_machine.md"]
    for md_file in md_files:
        filepath = os.path.join(DOCS_DIR, md_file)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        blocks = re.findall(r"```mermaid\s*\n(.*?)```", content, re.DOTALL)
        assert len(blocks) >= 1, f"No mermaid blocks found in {md_file}"
        for i, b in enumerate(blocks):
            lines = [line.strip() for line in b.strip().split("\n") if line.strip()]
            header = lines[0]
            # Check for bracket matching
            assert b.count("[") == b.count("]"), f"Mismatched [] in {md_file} block {i}"
            assert b.count("(") == b.count(")"), f"Mismatched () in {md_file} block {i}"
            assert b.count("{") == b.count("}"), f"Mismatched {{}} in {md_file} block {i}"
            print(f"PASS: {md_file} mermaid block {i+1} ({header}, {len(lines)} lines) syntax balanced.")

if __name__ == "__main__":
    verify_system_architecture_md()
    verify_state_machine_md()
    verify_svg_files()
    verify_mermaid_blocks()
    print("\nALL DOCS AND DIAGRAM VERIFICATIONS PASSED!")
