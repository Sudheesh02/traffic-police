import os

icons = {
    "arc_02_visual_occlusion.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
  <!-- Blindspot / Eye Slashed by Commercial Vehicle Chassis -->
  <path d="M4 24C9 14 19 8 24 8c3 0 6 1 9 2.5M44 24c-5 10-15 16-20 16-3.5 0-7-1-10-3"/>
  <circle cx="24" cy="24" r="6" fill="white" fill-opacity="0.2"/>
  <circle cx="24" cy="24" r="2.5" fill="white"/>
  <!-- Diagonal occlusion slash -->
  <line x1="6" y1="42" x2="42" y2="6" stroke="#ffffff" stroke-width="3.5"/>
</svg>""",

    "arc_03_challan_penalty.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
  <!-- ANPR Traffic Camera + Challan Ticket -->
  <rect x="6" y="8" width="22" height="16" rx="3" fill="white" fill-opacity="0.2"/>
  <circle cx="17" cy="16" r="4" fill="white"/>
  <path d="M12 24l-4 12h18l-4-12"/>
  <!-- Challan fine receipt -->
  <rect x="26" y="16" width="16" height="24" rx="2" fill="white" fill-opacity="0.25"/>
  <line x1="30" y1="22" x2="38" y2="22"/>
  <line x1="30" y1="28" x2="38" y2="28"/>
  <line x1="30" y1="34" x2="35" y2="34"/>
  <circle cx="38" cy="34" r="2" fill="white"/>
</svg>""",

    "arc_04_golden_hour_hazard.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
  <!-- Emergency Stopwatch & Danger Triangle -->
  <circle cx="24" cy="26" r="16" fill="white" fill-opacity="0.2"/>
  <path d="M24 6v4M20 6h8M24 16v10l6 4"/>
  <!-- Warning triangle alert badge -->
  <path d="M37 31l5 9H32z" fill="#ffffff" stroke-width="1.5"/>
  <circle cx="37" cy="37" r="0.8" fill="#1A426F"/>
</svg>""",

    "pyramid_01_golden_hour.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
  <!-- Shield with Medical Cross (Lifeline protection) -->
  <path d="M24 4L8 10v12c0 12 7 20 16 22 9-2 16-10 16-22V10L24 4z" fill="white" fill-opacity="0.2"/>
  <path d="M24 14v14M17 21h14" stroke-width="3.5"/>
</svg>""",

    "pyramid_02_deterministic_clearance.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
  <!-- Interlocking Cycle / Safety Clearance Interlock -->
  <path d="M24 8a16 16 0 0 1 14 8l-4 1" stroke-width="3"/>
  <path d="M38 9v7h-7"/>
  <path d="M24 40a16 16 0 0 1-14-8l4-1" stroke-width="3"/>
  <path d="M10 39v-7h7"/>
  <!-- Center Signal Core -->
  <circle cx="24" cy="24" r="5" fill="white"/>
</svg>""",

    "pyramid_03_automated_challan.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
  <!-- Clipboard with Audit Shield and Checkmark -->
  <rect x="10" y="8" width="28" height="34" rx="4" fill="white" fill-opacity="0.2"/>
  <path d="M18 8V5a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v3"/>
  <path d="M17 25l5 5 10-11" stroke-width="3.5"/>
</svg>""",

    "radar_01_delay_reduction.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
  <!-- Speedometer / Transit Delay Reduction -->
  <path d="M8 32a18 18 0 1 1 32 0" stroke-width="3"/>
  <circle cx="24" cy="30" r="3" fill="white"/>
  <line x1="24" y1="30" x2="33" y2="18" stroke-width="3.5"/>
  <path d="M12 36h24"/>
</svg>""",

    "radar_02_safety_clearance.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
  <!-- Traffic Signal Housing with Green Active -->
  <rect x="14" y="6" width="20" height="36" rx="6" fill="white" fill-opacity="0.2"/>
  <circle cx="24" cy="14" r="3"/>
  <circle cx="24" cy="24" r="3"/>
  <circle cx="24" cy="34" r="3.5" fill="white"/>
</svg>""",

    "radar_03_subghz_rf.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
  <!-- 868 MHz Sub-GHz Radio Antenna & Penetrating Waves -->
  <line x1="24" y1="20" x2="24" y2="40" stroke-width="3.5"/>
  <circle cx="24" cy="18" r="4" fill="white"/>
  <path d="M16 12a12 12 0 0 1 16 0" stroke-width="2.5"/>
  <path d="M10 6a20 20 0 0 1 28 0" stroke-width="2.5"/>
  <path d="M18 40h12"/>
</svg>""",

    "radar_04_frugal_bom.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
  <!-- Industrial Microcontroller Chip / DIN-Rail RTU -->
  <rect x="12" y="12" width="24" height="24" rx="4" fill="white" fill-opacity="0.25"/>
  <rect x="18" y="18" width="12" height="12" rx="2" fill="white"/>
  <!-- Pins -->
  <path d="M18 6v6M24 6v6M30 6v6M18 36v6M24 36v6M30 36v6"/>
  <path d="M6 18h6M6 24h6M6 30h6M36 18h6M36 24h6M36 30h6"/>
</svg>""",

    # Slide 2: 6-Step Workflow Icons
    "workflow_01_rf_trigger.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
  <!-- Handheld Radio Remote / Industrial Wand Trigger -->
  <rect x="16" y="12" width="16" height="28" rx="4" fill="white" fill-opacity="0.25"/>
  <circle cx="24" cy="22" r="4" fill="white"/>
  <line x1="20" y1="32" x2="28" y2="32"/>
  <line x1="24" y1="4" x2="24" y2="12" stroke-width="3.5"/>
  <circle cx="24" cy="4" r="1.5" fill="white"/>
  <!-- RF Transmission waves -->
  <path d="M30 8a6 6 0 0 1 0 8M18 8a6 6 0 0 0 0 8"/>
</svg>""",

    "workflow_02_cctv_verification.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
  <!-- Smart City CCTV & Strobe Flasher Detection -->
  <path d="M8 14h20l8-6v20l-8-6H8a2 2 0 0 1-2-2V16a2 2 0 0 1 2-2z" fill="white" fill-opacity="0.25"/>
  <circle cx="16" cy="19" r="3" fill="white"/>
  <path d="M12 28v6M8 34h8"/>
  <!-- Flashing Strobe Rays -->
  <path d="M38 12l4-2M40 19h4M38 26l4 2"/>
</svg>""",

    "workflow_03_anpr_ocr.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
  <!-- License Plate ANPR Scanner / Target Framing -->
  <rect x="8" y="14" width="32" height="20" rx="3" fill="white" fill-opacity="0.2"/>
  <text x="14" y="28" font-family="monospace" font-size="10" font-weight="bold" fill="white" stroke="none">CG-04</text>
  <!-- OCR Scan Corners -->
  <path d="M4 12V6h6M44 12V6h-6M4 36v6h6M44 36v6h-6" stroke-width="3"/>
</svg>""",

    "workflow_04_intergreen_buffer.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
  <!-- Deterministic Inter-Green Timer (3.5s Yellow + 2.0s All-Red) -->
  <circle cx="24" cy="24" r="18" fill="white" fill-opacity="0.2"/>
  <path d="M24 12v12l8 4" stroke-width="3"/>
  <path d="M24 6v3M24 39v3M6 24h3M39 24h3"/>
  <circle cx="32" cy="16" r="2.5" fill="white"/>
</svg>""",

    "workflow_05_priority_green.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
  <!-- Form-C Interlocked Relay / Priority Green Corridor -->
  <path d="M8 24h10l6-10 6 20 6-10h4" stroke-width="3"/>
  <circle cx="8" cy="24" r="3" fill="white"/>
  <circle cx="40" cy="24" r="3" fill="white"/>
  <!-- Arrow indicating green clearance flow -->
  <path d="M28 8l8 0 0 8M36 8l-10 10" stroke-width="2.5"/>
</svg>""",

    "workflow_06_iccc_whitelist.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
  <!-- Raipur Commissionerate ICCC Server Sync & Whitelist Ledger -->
  <rect x="10" y="8" width="28" height="10" rx="3" fill="white" fill-opacity="0.25"/>
  <circle cx="16" cy="13" r="1.5" fill="white"/>
  <circle cx="22" cy="13" r="1.5" fill="white"/>
  <rect x="10" y="22" width="28" height="10" rx="3" fill="white" fill-opacity="0.25"/>
  <circle cx="16" cy="27" r="1.5" fill="white"/>
  <circle cx="22" cy="27" r="1.5" fill="white"/>
  <!-- Exemption Checkmark Badge -->
  <circle cx="36" cy="36" r="7" fill="white"/>
  <path d="M33 36l2 2 4-4" stroke="#1A426F" stroke-width="2"/>
</svg>"""
}

out_dir = r"c:\Users\akgam\Downloads\Traffic Police\slide_icons"
os.makedirs(out_dir, exist_ok=True)

for filename, content in icons.items():
    path = os.path.join(out_dir, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip())

print(f"Generated {len(icons)} SVGs in {out_dir}")
