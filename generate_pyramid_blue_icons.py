import os

color = "#1e3b81"

pyramid_icons = {
    # Tier 1 (Top): Guaranteed Golden Hour
    "pyramid_01_golden_hour.svg": f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48" fill="none" stroke="{color}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
  <!-- Protective Lifeline Shield -->
  <path d="M24 4L8 10v12c0 12 7 20 16 22 9-2 16-10 16-22V10L24 4z" fill="{color}" fill-opacity="0.15"/>
  <!-- Bold Medical Cross -->
  <path d="M24 13v16M16 21h16" stroke-width="3.5"/>
  <!-- Sparkles for guaranteed priority -->
  <path d="M36 8l1.5 3 3 1.5-3 1.5-1.5 3-1.5-3-3-1.5 3-1.5z" fill="{color}" stroke="none"/>
</svg>""",

    # Tier 1 Alternate: Lifeline Pulse
    "pyramid_01_lifeline_pulse.svg": f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48" fill="none" stroke="{color}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
  <!-- Shield with ECG Pulse -->
  <path d="M24 4L8 10v12c0 12 7 20 16 22 9-2 16-10 16-22V10L24 4z" fill="{color}" fill-opacity="0.15"/>
  <path d="M12 23h6l3-7 5 14 4-9 3 2h3" stroke-width="3"/>
</svg>""",

    # Tier 2 (Middle): Deterministic Clearance
    "pyramid_02_deterministic_clearance.svg": f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48" fill="none" stroke="{color}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
  <!-- Interlocking Safety Cycle Arrows -->
  <path d="M24 8a16 16 0 0 1 14 8l-4 1" stroke-width="3"/>
  <path d="M38 9v7h-7"/>
  <path d="M24 40a16 16 0 0 1-14-8l4-1" stroke-width="3"/>
  <path d="M10 39v-7h7"/>
  <!-- Center Signal Core with Green Light indicator -->
  <circle cx="24" cy="24" r="7" fill="{color}" fill-opacity="0.2"/>
  <circle cx="24" cy="24" r="3.5" fill="{color}"/>
</svg>""",

    # Tier 2 Alternate: Traffic Light Safety Interlock
    "pyramid_02_safety_interlock.svg": f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48" fill="none" stroke="{color}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
  <!-- Traffic Signal Housing -->
  <rect x="14" y="6" width="20" height="36" rx="6" fill="{color}" fill-opacity="0.15"/>
  <circle cx="24" cy="14" r="3"/>
  <circle cx="24" cy="24" r="3"/>
  <circle cx="24" cy="34" r="4" fill="{color}"/>
  <!-- Safety Checkmark Badge -->
  <circle cx="34" cy="14" r="6" fill="#ffffff" stroke="{color}" stroke-width="2"/>
  <path d="M31 14l2 2 4-4" stroke-width="2"/>
</svg>""",

    # Tier 3 (Bottom): Automated Challan Protection
    "pyramid_03_automated_challan.svg": f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48" fill="none" stroke="{color}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
  <!-- Audit Clipboard -->
  <rect x="8" y="8" width="26" height="34" rx="4" fill="{color}" fill-opacity="0.15"/>
  <path d="M16 8V5a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v3"/>
  <line x1="13" y1="16" x2="27" y2="16"/>
  <line x1="13" y1="22" x2="23" y2="22"/>
  <line x1="13" y1="28" x2="21" y2="28"/>
  <!-- Legal Immunity Shield Badge -->
  <g transform="translate(18, 14)">
    <path d="M16 2L6 6v7c0 8 5 13 10 15 5-2 10-7 10-15V6L16 2z" fill="#ffffff" stroke="{color}" stroke-width="2.2"/>
    <path d="M11 13l3.5 3.5 7.5-7.5" stroke-width="2.5"/>
  </g>
</svg>""",

    # Tier 3 Alternate: Good Samaritan Shield
    "pyramid_03_good_samaritan_shield.svg": f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48" fill="none" stroke="{color}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
  <!-- Citizen Protection Shield with Rupees zero / waiver -->
  <path d="M24 4L8 10v12c0 12 7 20 16 22 9-2 16-10 16-22V10L24 4z" fill="{color}" fill-opacity="0.15"/>
  <path d="M16 23l5 5 11-11" stroke-width="3.5"/>
  <!-- Document base -->
  <path d="M14 42h20" stroke-width="2.5"/>
</svg>"""
}

# Create folders
folders = [
    r"c:\Users\akgam\Downloads\Traffic Police\pyramids",
    r"c:\Users\akgam\Downloads\Traffic Police\slide_icons\pyramids"
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)
    for filename, content in pyramid_icons.items():
        with open(os.path.join(folder, filename), "w", encoding="utf-8") as f:
            f.write(content.strip())

print(f"Successfully generated {len(pyramid_icons)} icons in color {color} into {folders[0]}")
