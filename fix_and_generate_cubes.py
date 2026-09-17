import os

slide_icons_dir = r"c:\Users\akgam\Downloads\Traffic Police\slide_icons"
os.makedirs(slide_icons_dir, exist_ok=True)

# 1. Redraw workflow_03_anpr_ocr.svg with pure vector shapes for the plate and letters
anpr_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
  <!-- Optical ANPR Scan Bracket Corners -->
  <path d="M4 14V6h8M44 14V6h-8M4 34v8h8M44 34v8h-8" stroke-width="3"/>
  
  <!-- License Plate Frame -->
  <rect x="7" y="15" width="34" height="18" rx="3" fill="white" fill-opacity="0.15" stroke-width="2"/>
  
  <!-- IND Left Blue/White Stripe -->
  <line x1="12" y1="15" x2="12" y2="33" stroke="white" stroke-width="1.5"/>
  <circle cx="9.5" cy="20" r="1" fill="white"/>

  <!-- Pure Vector Glyphs for "CG 04" (No font dependency, 100% centered in box) -->
  <!-- 'C' -->
  <path d="M19 20h-3v8h3" stroke-width="2.2"/>
  <!-- 'G' -->
  <path d="M26 20h-3v8h3v-4h-1.5" stroke-width="2.2"/>
  <!-- '0' -->
  <rect x="29.5" y="20" width="3.5" height="8" rx="1.5" stroke-width="2.2"/>
  <!-- '4' -->
  <path d="M38 20v8M35 20v4h3" stroke-width="2.2"/>

  <!-- Scanline sweep bar -->
  <line x1="7" y1="24" x2="41" y2="24" stroke="white" stroke-width="1" stroke-dasharray="2 2" stroke-opacity="0.6"/>
</svg>"""

with open(os.path.join(slide_icons_dir, "workflow_03_anpr_ocr.svg"), "w", encoding="utf-8") as f:
    f.write(anpr_svg.strip())

# 2. Slide 2: 3D Cube Stack Icons (01, 02, 03)
cube_icons = {
    # Cube 01: Instant Sub-GHz Preemption (RF tower + 42ms lightning speed)
    "cube_01_instant_rf_preemption.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
  <!-- Radio Antenna / Tower with Signal Waves -->
  <path d="M24 18v22M18 40h12" stroke-width="3"/>
  <circle cx="24" cy="16" r="3.5" fill="white"/>
  <!-- Expanding 868 MHz RF Wave Arcs -->
  <path d="M16 10a11 11 0 0 1 16 0" stroke-width="2.5"/>
  <path d="M10 4a19 19 0 0 1 28 0" stroke-width="2.5"/>
  <!-- Lightning Bolt for 42ms Instant Trigger -->
  <path d="M34 22l-6 10h5l-4 8" fill="white" stroke-width="1.5"/>
</svg>""",

    # Cube 02: Dual-Stage Edge-AI Verification (CCTV Camera + Strobe Frequency Wave)
    "cube_02_dual_stage_ai_strobe.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
  <!-- Smart City Pole CCTV Camera -->
  <path d="M6 14h18l10-8v22l-10-8H6a2 2 0 0 1-2-2V16a2 2 0 0 1 2-2z" fill="white" fill-opacity="0.25"/>
  <circle cx="14" cy="19" r="3.5" fill="white"/>
  <path d="M10 27v7M6 34h8"/>
  <!-- Strobe Frequency Waveform & Optical Rays -->
  <path d="M24 38l3-6 4 12 4-8 3 4" stroke-width="2.5"/>
  <path d="M38 10l5-2M40 18h5M38 26l5 2" stroke-width="2"/>
</svg>""",

    # Cube 03: Automated Good Samaritan Protection (Shield + Citizen Exemption Checkmark)
    "cube_03_good_samaritan_shield.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
  <!-- Protective Legal Shield -->
  <path d="M24 4L8 10v12c0 12 7 20 16 22 9-2 16-10 16-22V10L24 4z" fill="white" fill-opacity="0.25"/>
  <!-- Checkmark for 100% Exemption Waiver -->
  <path d="M16 22l6 6 11-11" stroke-width="3.5"/>
  <!-- Citizen vehicle outline underneath -->
  <path d="M12 40h24" stroke-width="2" stroke-dasharray="3 3"/>
</svg>"""
}

for filename, content in cube_icons.items():
    with open(os.path.join(slide_icons_dir, filename), "w", encoding="utf-8") as f:
        f.write(content.strip())

print("Successfully updated ANPR SVG and generated 3D cube stack icons.")
