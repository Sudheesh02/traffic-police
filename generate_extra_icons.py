import os

extra_icons = {
    "roadmap_phase1_pilot.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
  <!-- Pilot Junction Document & Pin -->
  <rect x="8" y="8" width="26" height="34" rx="4" fill="white" fill-opacity="0.25"/>
  <path d="M14 16h14M14 22h14M14 28h8"/>
  <circle cx="34" cy="32" r="5" fill="white" fill-opacity="0.3"/>
  <path d="M34 32v6l3-3"/>
</svg>""",

    "roadmap_phase2_expansion.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
  <!-- City-wide Network Grid Expansion -->
  <circle cx="12" cy="14" r="5" fill="white" fill-opacity="0.25"/>
  <circle cx="36" cy="14" r="5" fill="white" fill-opacity="0.25"/>
  <circle cx="24" cy="34" r="6" fill="white"/>
  <line x1="16" y1="17" x2="21" y2="30" stroke-width="2.5"/>
  <line x1="32" y1="17" x2="27" y2="30" stroke-width="2.5"/>
  <line x1="17" y1="14" x2="31" y2="14" stroke-width="2"/>
</svg>""",

    "roadmap_phase3_scale.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
  <!-- State-wide Corridor Growth / Cloud & Highway Scale -->
  <path d="M10 32c-3.5 0-6-2.5-6-6 0-3 2-5.5 5-6 1-5 5.5-8 11-8 6 0 10.5 4 11.5 9.5 3 .5 5.5 3 5.5 6.5 0 3.5-3 6-7 6H10z" fill="white" fill-opacity="0.25"/>
  <path d="M18 42l6-6 6 6M24 36v10" stroke-width="3"/>
</svg>""",

    "impact_failsafe_purity.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
  <!-- Engineering Integrity / Fail-Safe Lock -->
  <rect x="12" y="18" width="24" height="22" rx="4" fill="white" fill-opacity="0.25"/>
  <path d="M18 18v-6a6 6 0 0 1 12 0v6" stroke-width="3"/>
  <circle cx="24" cy="28" r="3" fill="white"/>
  <path d="M24 31v4"/>
</svg>""",

    "impact_rapid_retrofit.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
  <!-- 45-Min Plug-and-Play Clock & Wrench -->
  <circle cx="22" cy="24" r="14" fill="white" fill-opacity="0.2"/>
  <path d="M22 16v8l5 5"/>
  <!-- Lightning bolt / rapid plug -->
  <path d="M34 10l-4 8h6l-5 10 2-7h-5z" fill="white"/>
</svg>""",

    "impact_transit_efficiency.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
  <!-- Cleared Green Corridor Flow / Emergency Path -->
  <path d="M6 38L18 10h12l12 28H6z" fill="white" fill-opacity="0.2"/>
  <line x1="24" y1="16" x2="24" y2="24" stroke-width="3"/>
  <line x1="24" y1="30" x2="24" y2="36" stroke-width="3"/>
  <path d="M20 6l4-4 4 4" stroke-width="2"/>
</svg>""",

    "impact_legal_protection.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
  <!-- Shield with Citizen Checkmark (Good Samaritan Protection) -->
  <path d="M24 4L10 10v12c0 10 6 18 14 20 8-2 14-10 14-20V10L24 4z" fill="white" fill-opacity="0.25"/>
  <path d="M17 22l5 5 9-9" stroke-width="3.5"/>
</svg>"""
}

out_dir = r"c:\Users\akgam\Downloads\Traffic Police\slide_icons"
for filename, content in extra_icons.items():
    path = os.path.join(out_dir, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip())

print(f"Generated {len(extra_icons)} additional SVGs in {out_dir}")
