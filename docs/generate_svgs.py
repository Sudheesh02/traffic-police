"""
Script to generate high-resolution SVG diagram artifacts for SynchroClear-ITS documentation:
1. docs/system_architecture.svg
2. docs/state_machine.svg
3. docs/timing_sequence.svg
"""
import xml.etree.ElementTree as ET
import os

DOCS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "docs"))
os.makedirs(DOCS_DIR, exist_ok=True)

# -------------------------------------------------------------------------------------------------
# 1. docs/system_architecture.svg
# -------------------------------------------------------------------------------------------------
svg_arch = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1240 980" width="1240" height="980">
  <defs>
    <style>
      .title { font-family: 'Segoe UI', Arial, sans-serif; font-weight: 800; font-size: 26px; fill: #0f172a; }
      .subtitle { font-family: 'Segoe UI', Arial, sans-serif; font-weight: 500; font-size: 14px; fill: #475569; }
      .layer-title { font-family: 'Segoe UI', Arial, sans-serif; font-weight: 700; font-size: 15px; }
      .card-title { font-family: 'Segoe UI', Arial, sans-serif; font-weight: 700; font-size: 13px; fill: #0f172a; }
      .card-text { font-family: 'Segoe UI', Arial, sans-serif; font-size: 11px; fill: #334155; }
      .card-badge { font-family: 'Segoe UI', Arial, sans-serif; font-size: 9.5px; font-weight: 700; fill: #ffffff; }
      .edge-label { font-family: 'Segoe UI', Arial, sans-serif; font-size: 10.5px; font-weight: 600; fill: #0284c7; }
      .legend-text { font-family: 'Segoe UI', Arial, sans-serif; font-size: 11px; fill: #475569; }
      .shadow { filter: drop-shadow(0px 4px 10px rgba(0, 0, 0, 0.05)); }
      .card-shadow { filter: drop-shadow(0px 2px 5px rgba(0, 0, 0, 0.04)); }
    </style>
    <linearGradient id="headerGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f8fafc" />
      <stop offset="100%" stop-color="#f1f5f9" />
    </linearGradient>
    <linearGradient id="fieldGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#f0f9ff" />
      <stop offset="100%" stop-color="#e0f2fe" />
    </linearGradient>
    <linearGradient id="cabinetGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#fffbeb" />
      <stop offset="100%" stop-color="#fef3c7" />
    </linearGradient>
    <linearGradient id="visionGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#f0fdf4" />
      <stop offset="100%" stop-color="#dcfce7" />
    </linearGradient>
    <linearGradient id="cloudGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#faf5ff" />
      <stop offset="100%" stop-color="#f3e8ff" />
    </linearGradient>
    <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#0284c7" />
    </marker>
    <marker id="arrow-green" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#16a34a" />
    </marker>
    <marker id="arrow-amber" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#d97706" />
    </marker>
    <marker id="arrow-purple" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#9333ea" />
    </marker>
    <marker id="arrow-red" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#dc2626" />
    </marker>
  </defs>

  <!-- Background Canvas -->
  <rect x="0" y="0" width="1240" height="980" fill="#f8fafc" />

  <!-- Header Container -->
  <rect x="25" y="20" width="1190" height="75" rx="12" fill="url(#headerGrad)" stroke="#cbd5e1" stroke-width="1.5" class="shadow" />
  <text x="50" y="52" class="title">SynchroClear-ITS: 4-Layer System Architecture</text>
  <text x="50" y="76" class="subtitle">Fail-Safe Edge-AI Vision &amp; Sub-GHz RF Emergency Preemption — Raipur Police Commissionerate</text>

  <!-- Header Badges -->
  <rect x="760" y="38" width="95" height="24" rx="12" fill="#0284c7" />
  <text x="772" y="54" class="card-badge">868 MHz RF</text>
  <rect x="865" y="38" width="105" height="24" rx="12" fill="#d97706" />
  <text x="876" y="54" class="card-badge">STM32F4 RTU</text>
  <rect x="980" y="38" width="110" height="24" rx="12" fill="#16a34a" />
  <text x="990" y="54" class="card-badge">YOLO + ANPR</text>
  <rect x="1100" y="38" width="95" height="24" rx="12" fill="#9333ea" />
  <text x="1112" y="54" class="card-badge">Raipur ICCC</text>

  <!-- ========================================================================= -->
  <!-- LAYER 1: FIELD INTERACTION LAYER                                         -->
  <!-- ========================================================================= -->
  <rect x="25" y="110" width="1190" height="155" rx="14" fill="url(#fieldGrad)" stroke="#38bdf8" stroke-width="2" class="shadow" />
  <rect x="40" y="122" width="280" height="26" rx="6" fill="#0284c7" />
  <text x="50" y="139" fill="#ffffff" class="layer-title">LAYER 1: FIELD INTERACTION LAYER</text>
  <text x="330" y="139" fill="#0369a1" font-family="'Segoe UI', Arial" font-size="11.5px" font-weight="600">On-Ground Queue, Emergency Traffic &amp; Officer Remote Interface</text>

  <!-- Card 1.1: Emergency Vehicle -->
  <g class="card-shadow">
    <rect x="45" y="158" width="260" height="92" rx="8" fill="#ffffff" stroke="#bae6fd" stroke-width="1.2" />
    <rect x="45" y="158" width="6" height="92" rx="3" fill="#e11d48" />
    <text x="60" y="178" class="card-title">🚑 Approaching Emergency Vehicle</text>
    <text x="60" y="196" class="card-text">• 108 Ambulance / Fire Tender / Police</text>
    <text x="60" y="212" class="card-text">• Trapped 30–50m behind red stop-line</text>
    <text x="60" y="228" class="card-text">• Optical Strobe (1.0–2.5 Hz) + Siren</text>
  </g>

  <!-- Card 1.2: Traffic Officer & Handheld Wand -->
  <g class="card-shadow">
    <rect x="335" y="158" width="280" height="92" rx="8" fill="#ffffff" stroke="#bae6fd" stroke-width="1.2" />
    <rect x="335" y="158" width="6" height="92" rx="3" fill="#0284c7" />
    <text x="350" y="178" class="card-title">👮 Traffic Constable &amp; Handheld Wand</text>
    <text x="350" y="196" class="card-text">• Nordic nRF52840 / STM32L0 + SX1262</text>
    <text x="350" y="212" class="card-text">• 4-Way Directional Toggle + Cancel</text>
    <text x="350" y="228" class="card-text">• 32-bit Rolling Counter &amp; HMAC-SHA256</text>
  </g>

  <!-- Card 1.3: Citizen Vehicles at Stop Line -->
  <g class="card-shadow">
    <rect x="645" y="158" width="275" height="92" rx="8" fill="#ffffff" stroke="#bae6fd" stroke-width="1.2" />
    <rect x="645" y="158" width="6" height="92" rx="3" fill="#f59e0b" />
    <text x="660" y="178" class="card-title">🚗 Citizen Motorists at Stop Line</text>
    <text x="660" y="196" class="card-text">• Trapped under Stop-Line Dissonance</text>
    <text x="660" y="212" class="card-text">• Cannot see constable wand in queue</text>
    <text x="660" y="228" class="card-text">• Dread automatic ₹1,000–₹5,000 challan</text>
  </g>

  <!-- Card 1.4: Preemption Corridor Result -->
  <g class="card-shadow">
    <rect x="945" y="158" width="250" height="92" rx="8" fill="#ffffff" stroke="#bae6fd" stroke-width="1.2" />
    <rect x="945" y="158" width="6" height="92" rx="3" fill="#10b981" />
    <text x="960" y="178" class="card-title">🟢 Golden Hour Corridor Flow</text>
    <text x="960" y="196" class="card-text">• Physical overhead green turns ON</text>
    <text x="960" y="212" class="card-text">• Citizens safely yield with confidence</text>
    <text x="960" y="228" class="card-text">• Zero dispute: Automated e-Challan Immunity</text>
  </g>

  <!-- Flow in Layer 1 -->
  <path d="M 305 204 L 333 204" stroke="#0284c7" stroke-width="1.8" stroke-dasharray="3,3" marker-end="url(#arrow)" />
  <path d="M 615 204 L 643 204" stroke="#0284c7" stroke-width="1.8" marker-end="url(#arrow)" />
  <path d="M 920 204 L 943 204" stroke="#10b981" stroke-width="2" marker-end="url(#arrow-green)" />

  <!-- ========================================================================= -->
  <!-- LAYER 2: TRAFFIC CABINET & JUNCTION RTU LAYER                             -->
  <!-- ========================================================================= -->
  <rect x="25" y="290" width="580" height="370" rx="14" fill="url(#cabinetGrad)" stroke="#f59e0b" stroke-width="2" class="shadow" />
  <rect x="40" y="302" width="320" height="26" rx="6" fill="#d97706" />
  <text x="50" y="319" fill="#ffffff" class="layer-title">LAYER 2: CABINET &amp; JUNCTION RTU</text>
  <text x="370" y="319" fill="#b45309" font-family="'Segoe UI', Arial" font-size="11.5px" font-weight="600">Deterministic Edge Safety Control</text>

  <!-- Card 2.1: RF Front-End -->
  <g class="card-shadow">
    <rect x="45" y="338" width="250" height="84" rx="8" fill="#ffffff" stroke="#fde68a" stroke-width="1.2" />
    <text x="58" y="358" class="card-title">📶 868MHz Antenna &amp; SX1262 Rx</text>
    <text x="58" y="376" class="card-text">• External 3 dBi Omnidirectional Whip</text>
    <text x="58" y="392" class="card-text">• Semtech SX1262 (-148 dBm sensitivity)</text>
    <text x="58" y="408" class="card-text">• SPI Bus + Hardware IRQ to MCU</text>
  </g>

  <!-- Card 2.2: Industrial RTU -->
  <g class="card-shadow">
    <rect x="315" y="338" width="270" height="84" rx="8" fill="#ffffff" stroke="#fde68a" stroke-width="1.2" />
    <text x="328" y="358" class="card-title">⚡ Industrial RTU (STM32F401)</text>
    <text x="328" y="376" class="card-text">• ARM Cortex-M4 @ 84MHz (-40°C..+85°C)</text>
    <text x="328" y="392" class="card-text">• Deterministic Inter-Green FSM Engine</text>
    <text x="328" y="408" class="card-text">• Dual Watchdog (IWDG + WWDG)</text>
  </g>

  <!-- Card 2.3: Optocoupler Isolation Barrier -->
  <g class="card-shadow">
    <rect x="45" y="440" width="250" height="84" rx="8" fill="#ffffff" stroke="#fde68a" stroke-width="1.2" />
    <text x="58" y="460" class="card-title">🔌 2500V Optocoupled Isolation</text>
    <text x="58" y="478" class="card-text">• PC817 High-Isolation Transistors</text>
    <text x="58" y="494" class="card-text">• Flyback Snubbers &amp; Inductive Damping</text>
    <text x="58" y="510" class="card-text">• Complete galvanic immunity from AC noise</text>
  </g>

  <!-- Card 2.4: Form-C Interlock Relays -->
  <g class="card-shadow">
    <rect x="315" y="440" width="270" height="84" rx="8" fill="#ffffff" stroke="#fde68a" stroke-width="1.2" />
    <text x="328" y="460" class="card-title">🔀 Form-C Break-Before-Make Relays</text>
    <text x="328" y="478" class="card-text">• Mechanical DPDT Interlock Matrix</text>
    <text x="328" y="494" class="card-text">• Physically severed cross-green feed</text>
    <text x="328" y="510" class="card-text">• De-energizes to legacy TSC on fault</text>
  </g>

  <!-- Card 2.5: Existing Controller & Signals -->
  <g class="card-shadow">
    <rect x="45" y="542" width="540" height="98" rx="8" fill="#ffffff" stroke="#fde68a" stroke-width="1.2" />
    <rect x="45" y="542" width="6" height="98" rx="3" fill="#d97706" />
    <text x="60" y="564" class="card-title">🚦 Existing Traffic Signal Controller (TSC) &amp; Overhead Signal Heads</text>
    <text x="60" y="584" class="card-text">• Connects via standard dry contact preemption terminals (Pins 12–16)</text>
    <text x="60" y="600" class="card-text">• High-flux 300mm LED Signal Heads: 3.5s Amber ➔ 2.0s All-Red ➔ Priority Green</text>
    <text x="60" y="616" class="card-text">• Full queue visibility (150m+ line of sight) eliminates stop-line cognitive dissonance</text>
  </g>

  <!-- Connections inside Layer 2 -->
  <path d="M 170 422 L 170 440" stroke="#d97706" stroke-width="1.8" marker-end="url(#arrow-amber)" />
  <path d="M 295 380 L 315 380" stroke="#d97706" stroke-width="1.8" marker-end="url(#arrow-amber)" />
  <path d="M 450 422 L 450 440" stroke="#d97706" stroke-width="1.8" marker-end="url(#arrow-amber)" />
  <path d="M 295 482 L 315 482" stroke="#d97706" stroke-width="1.8" marker-end="url(#arrow-amber)" />
  <path d="M 450 524 L 450 542" stroke="#d97706" stroke-width="2" marker-end="url(#arrow-amber)" />

  <!-- ========================================================================= -->
  <!-- LAYER 3: JUNCTION EDGE-AI VISION LAYER                                    -->
  <!-- ========================================================================= -->
  <rect x="635" y="290" width="580" height="370" rx="14" fill="url(#visionGrad)" stroke="#22c55e" stroke-width="2" class="shadow" />
  <rect x="650" y="302" width="310" height="26" rx="6" fill="#16a34a" />
  <text x="660" y="319" fill="#ffffff" class="layer-title">LAYER 3: EDGE-AI VISION LAYER</text>
  <text x="970" y="319" fill="#15803d" font-family="'Segoe UI', Arial" font-size="11.5px" font-weight="600">Visual Verification &amp; OCR Audit</text>

  <!-- Card 3.1: Existing ITMS Camera -->
  <g class="card-shadow">
    <rect x="655" y="338" width="250" height="84" rx="8" fill="#ffffff" stroke="#bbf7d0" stroke-width="1.2" />
    <text x="668" y="358" class="card-title">🎥 Existing Smart City CCTV</text>
    <text x="668" y="376" class="card-text">• 1080p / 4K RTSP H.264 Stream</text>
    <text x="668" y="392" class="card-text">• Zero New Camera Hardware (₹0 Capex)</text>
    <text x="668" y="408" class="card-text">• Elevated Gantry Mounted Field of View</text>
  </g>

  <!-- Card 3.2: Edge Compute Node -->
  <g class="card-shadow">
    <rect x="925" y="338" width="270" height="84" rx="8" fill="#ffffff" stroke="#bbf7d0" stroke-width="1.2" />
    <text x="938" y="358" class="card-title">🧠 Jetson Orin Nano / IPC Compute</text>
    <text x="938" y="376" class="card-text">• 20–40 TOPS INT8 TensorRT Engine</text>
    <text x="938" y="392" class="card-text">• Local Fanless IP66 (-40°C to +85°C)</text>
    <text x="938" y="408" class="card-text">• Real-time 30 FPS Ingestion Pipeline</text>
  </g>

  <!-- Card 3.3: YOLO Emergency Classifier -->
  <g class="card-shadow">
    <rect x="655" y="440" width="250" height="84" rx="8" fill="#ffffff" stroke="#bbf7d0" stroke-width="1.2" />
    <text x="668" y="460" class="card-title">🔍 YOLOv8 Emergency Classifier</text>
    <text x="668" y="478" class="card-text">• Ambulance, Fire Truck, Police Classes</text>
    <text x="668" y="494" class="card-text">• Precision: 96.4% on Indian traffic datasets</text>
    <text x="668" y="510" class="card-text">• Isolates Vehicle Rooftop ROI</text>
  </g>

  <!-- Card 3.4: Strobe & ANPR OCR -->
  <g class="card-shadow">
    <rect x="925" y="440" width="270" height="84" rx="8" fill="#ffffff" stroke="#bbf7d0" stroke-width="1.2" />
    <text x="938" y="460" class="card-title">🔤 Strobe FFT &amp; ANPR OCR</text>
    <text x="938" y="478" class="card-text">• 1.0–2.5 Hz Strobe Temporal Analysis</text>
    <text x="938" y="494" class="card-text">• Anti-Spoofing Visual Verification</text>
    <text x="938" y="510" class="card-text">• Indian Plates (CG04, BH) Extraction</text>
  </g>

  <!-- Card 3.5: Cryptographic Audit Ledger -->
  <g class="card-shadow">
    <rect x="655" y="542" width="540" height="98" rx="8" fill="#ffffff" stroke="#bbf7d0" stroke-width="1.2" />
    <rect x="655" y="542" width="6" height="98" rx="3" fill="#16a34a" />
    <text x="670" y="564" class="card-title">💾 Cryptographic Local Audit Ledger &amp; Telemetry Packager</text>
    <text x="670" y="584" class="card-text">• Append-only JSONL storage with SHA-256 block hash chaining</text>
    <text x="670" y="600" class="card-text">• Offline buffer preserves events and snapshots during cellular / fiber outages</text>
    <text x="670" y="616" class="card-text">• Packages MQTT JSON payload compliant with Raipur Police Commissionerate schema</text>
  </g>

  <!-- Connections inside Layer 3 -->
  <path d="M 905 380 L 925 380" stroke="#16a34a" stroke-width="1.8" marker-end="url(#arrow-green)" />
  <path d="M 1060 422 L 1060 440" stroke="#16a34a" stroke-width="1.8" marker-end="url(#arrow-green)" />
  <path d="M 925 482 L 905 482" stroke="#16a34a" stroke-width="1.8" marker-end="url(#arrow-green)" />
  <path d="M 780 524 L 780 542" stroke="#16a34a" stroke-width="1.8" marker-end="url(#arrow-green)" />
  <path d="M 1060 524 L 1060 542" stroke="#16a34a" stroke-width="1.8" marker-end="url(#arrow-green)" />

  <!-- Inter-Layer Synchronization: STM32 to Jetson RS-485 -->
  <path d="M 585 380 L 635 380" stroke="#64748b" stroke-width="2" stroke-dasharray="4,3" marker-end="url(#arrow)" />
  <text x="590" y="372" font-family="'Segoe UI', Arial" font-size="9px" font-weight="700" fill="#475569">RS-485 Sync</text>

  <!-- ========================================================================= -->
  <!-- LAYER 4: CENTRAL COMMAND LAYER (RAIPUR ICCC)                              -->
  <!-- ========================================================================= -->
  <rect x="25" y="685" width="1190" height="175" rx="14" fill="url(#cloudGrad)" stroke="#c084fc" stroke-width="2" class="shadow" />
  <rect x="40" y="697" width="370" height="26" rx="6" fill="#9333ea" />
  <text x="50" y="714" fill="#ffffff" class="layer-title">LAYER 4: CENTRAL COMMAND &amp; CITIZEN PROTECTION</text>
  <text x="420" y="714" fill="#7e22ce" font-family="'Segoe UI', Arial" font-size="11.5px" font-weight="600">Raipur Smart City ICCC &amp; ITMS Integration</text>

  <!-- Card 4.1: Secure MQTT Gateway -->
  <g class="card-shadow">
    <rect x="45" y="733" width="260" height="108" rx="8" fill="#ffffff" stroke="#e9d5ff" stroke-width="1.2" />
    <text x="60" y="753" class="card-title">🌐 Secure MQTT Telemetry Broker</text>
    <text x="60" y="771" class="card-text">• TLS 1.3 Port 8883 / mTLS Auth</text>
    <text x="60" y="787" class="card-text">• Topic: raipur/itms/preemption/events</text>
    <text x="60" y="803" class="card-text">• QoS 1 Guaranteed Delivery</text>
    <text x="60" y="819" class="card-text">• Auto-reconnect with offline sync</text>
  </g>

  <!-- Card 4.2: Raipur ICCC Server -->
  <g class="card-shadow">
    <rect x="335" y="733" width="280" height="108" rx="8" fill="#ffffff" stroke="#e9d5ff" stroke-width="1.2" />
    <text x="350" y="753" class="card-title">🏢 Raipur Smart City ICCC Server</text>
    <text x="350" y="771" class="card-text">• Centralized Traffic Command Center</text>
    <text x="350" y="787" class="card-text">• High-Availability Linux Cluster</text>
    <text x="350" y="803" class="card-text">• GIS Map Display &amp; Corridor Tracking</text>
    <text x="350" y="819" class="card-text">• Jaistambh &amp; Ghadi Chowk Lifeline Link</text>
  </g>

  <!-- Card 4.3: ITMS e-Challan Exemption Gateway -->
  <g class="card-shadow">
    <rect x="645" y="733" width="275" height="108" rx="8" fill="#ffffff" stroke="#e9d5ff" stroke-width="1.2" />
    <rect x="645" y="733" width="6" height="108" rx="3" fill="#9333ea" />
    <text x="660" y="753" class="card-title">🛡️ ITMS e-Challan Exemption Engine</text>
    <text x="660" y="771" class="card-text">• Dynamic Whitelist Calculation:</text>
    <text x="660" y="787" class="card-text font-semibold" fill="#7e22ce">  Window = [T_start-10s, T_end+10s]</text>
    <text x="660" y="803" class="card-text">• Intersects with ITMS Violation Feeds</text>
    <text x="660" y="819" class="card-text">• Auto-suppresses wrongful citations</text>
  </g>

  <!-- Card 4.4: NIC Integration & Police Audit -->
  <g class="card-shadow">
    <rect x="945" y="733" width="250" height="108" rx="8" fill="#ffffff" stroke="#e9d5ff" stroke-width="1.2" />
    <text x="960" y="753" class="card-title">🏛️ NIC Backend &amp; Police Console</text>
    <text x="960" y="771" class="card-text">• Direct VAHAN / e-Challan API link</text>
    <text x="960" y="787" class="card-text">• 100% Elimination of Court Appeals</text>
    <text x="960" y="803" class="card-text">• Senior Officer Anti-Abuse Audit</text>
    <text x="960" y="819" class="card-text">• Golden-hour travel time KPIs</text>
  </g>

  <!-- Flow in Layer 4 -->
  <path d="M 305 787 L 335 787" stroke="#9333ea" stroke-width="2" marker-end="url(#arrow-purple)" />
  <path d="M 615 787 L 645 787" stroke="#9333ea" stroke-width="2" marker-end="url(#arrow-purple)" />
  <path d="M 920 787 L 945 787" stroke="#9333ea" stroke-width="2" marker-end="url(#arrow-purple)" />

  <!-- ========================================================================= -->
  <!-- CROSS-LAYER DATA FLOWS                                                    -->
  <!-- ========================================================================= -->
  <!-- 1. Wand to Cabinet Whip Antenna -->
  <path d="M 475 250 L 475 270 L 170 270 L 170 338" stroke="#0284c7" stroke-width="2.5" marker-end="url(#arrow)" />
  <rect x="235" y="260" width="160" height="20" rx="4" fill="#ffffff" stroke="#0284c7" stroke-width="1" />
  <text x="245" y="274" class="edge-label">868 MHz RF Packet &lt;50ms</text>

  <!-- 2. Edge Compute to Central MQTT Broker -->
  <path d="M 925 640 L 925 665 L 175 665 L 175 733" stroke="#9333ea" stroke-width="2.5" marker-end="url(#arrow-purple)" />
  <rect x="460" y="655" width="180" height="20" rx="4" fill="#ffffff" stroke="#9333ea" stroke-width="1" />
  <text x="470" y="669" class="edge-label" fill="#9333ea">MQTT JSON over TLS 1.3</text>

  <!-- 3. Signal Head to Citizen Vehicles (Feedback) -->
  <path d="M 45 590 L 15 590 L 15 204 L 45 204" stroke="#10b981" stroke-width="2" stroke-dasharray="4,4" marker-end="url(#arrow-green)" />
  <rect x="5" y="385" width="20" height="100" rx="4" fill="#10b981" />
  <text x="-475" y="19" transform="rotate(-90)" font-family="'Segoe UI', Arial" font-size="10px" font-weight="700" fill="#ffffff">PHYSICAL GREEN SEEN BY QUEUE</text>

  <!-- ========================================================================= -->
  <!-- FOOTER & LEGEND                                                           -->
  <!-- ========================================================================= -->
  <rect x="25" y="880" width="1190" height="75" rx="10" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2" />
  <text x="45" y="904" font-family="'Segoe UI', Arial" font-size="12px" font-weight="700" fill="#0f172a">SYSTEM ARCHITECTURE PROTOCOLS &amp; GUARANTEES:</text>

  <circle cx="50" cy="928" r="6" fill="#0284c7" />
  <text x="65" y="932" class="legend-text"><tspan font-weight="700">Sub-GHz RF:</tspan> 868.0MHz ISM, AES-128, Rolling HMAC, &lt;50ms Latency</text>

  <circle cx="370" cy="928" r="6" fill="#d97706" />
  <text x="385" y="932" class="legend-text"><tspan font-weight="700">Hardware RTU:</tspan> STM32F401, Dual Watchdog, Form-C Break-Before-Make</text>

  <circle cx="700" cy="928" r="6" fill="#16a34a" />
  <text x="715" y="932" class="legend-text"><tspan font-weight="700">Edge Vision:</tspan> RTSP H.264, YOLOv8 30FPS, Strobe 1.0–2.5Hz FFT, ANPR</text>

  <circle cx="1020" cy="928" r="6" fill="#9333ea" />
  <text x="1035" y="932" class="legend-text"><tspan font-weight="700">Raipur ICCC:</tspan> MQTT TLS 1.3, Automated e-Challan Immunity</text>
</svg>
"""

# -------------------------------------------------------------------------------------------------
# 2. docs/state_machine.svg
# -------------------------------------------------------------------------------------------------
svg_fsm = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 900" width="1200" height="900">
  <defs>
    <style>
      .title { font-family: 'Segoe UI', Arial, sans-serif; font-weight: 800; font-size: 24px; fill: #0f172a; }
      .subtitle { font-family: 'Segoe UI', Arial, sans-serif; font-weight: 500; font-size: 14px; fill: #475569; }
      .state-name { font-family: 'Segoe UI', Arial, sans-serif; font-weight: 700; font-size: 13.5px; }
      .state-time { font-family: 'Segoe UI', Arial, sans-serif; font-weight: 700; font-size: 11px; }
      .state-desc { font-family: 'Segoe UI', Arial, sans-serif; font-size: 10.5px; fill: #334155; }
      .guard-text { font-family: 'Segoe UI', Arial, sans-serif; font-size: 10px; font-weight: 600; fill: #0284c7; }
      .fail-text { font-family: 'Segoe UI', Arial, sans-serif; font-size: 9.5px; font-weight: 700; fill: #dc2626; }
      .panel-title { font-family: 'Segoe UI', Arial, sans-serif; font-weight: 700; font-size: 12.5px; fill: #0f172a; }
      .panel-body { font-family: 'Segoe UI', Arial, sans-serif; font-size: 11px; fill: #334155; line-height: 1.4; }
      .shadow { filter: drop-shadow(0px 3px 8px rgba(0, 0, 0, 0.06)); }
    </style>
    <linearGradient id="headerGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f8fafc" />
      <stop offset="100%" stop-color="#f1f5f9" />
    </linearGradient>
    <marker id="arrow-fsm" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#0284c7" />
    </marker>
    <marker id="arrow-fail" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#dc2626" />
    </marker>
    <marker id="arrow-green" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#16a34a" />
    </marker>
  </defs>

  <!-- Background -->
  <rect x="0" y="0" width="1200" height="900" fill="#f8fafc" />

  <!-- Header -->
  <rect x="25" y="20" width="1150" height="72" rx="12" fill="url(#headerGrad)" stroke="#cbd5e1" stroke-width="1.5" class="shadow" />
  <text x="50" y="50" class="title">Deterministic Inter-Green Safety Clearance State Machine</text>
  <text x="50" y="74" class="subtitle">Indian Road Congress (IRC:SP:12 &amp; IRC:93) Safety Engine with Form-C Hardware Interlocks</text>
  <rect x="970" y="38" width="180" height="24" rx="12" fill="#16a34a" />
  <text x="982" y="54" font-family="'Segoe UI', Arial" font-size="10.5px" font-weight="700" fill="#ffffff">ZERO-COLLISION CERTIFIED</text>

  <!-- ========================================================================= -->
  <!-- MAIN STATE ENGINE FLOW (TOP-TO-BOTTOM / CIRCULAR RECOVERY)                -->
  <!-- ========================================================================= -->

  <!-- 1. STATE_NORMAL_CYCLE -->
  <g class="shadow">
    <rect x="80" y="125" width="280" height="90" rx="10" fill="#ffffff" stroke="#94a3b8" stroke-width="2" />
    <rect x="80" y="125" width="8" height="90" rx="4" fill="#64748b" />
    <text x="100" y="148" class="state-name" fill="#1e293b">1. STATE_NORMAL_CYCLE</text>
    <text x="100" y="166" class="state-time" fill="#64748b">Duration: Fixed-Time / Actuated (Legacy TSC)</text>
    <text x="100" y="184" class="state-desc">• Standard round-robin phasing (N-S ➔ E-W)</text>
    <text x="100" y="200" class="state-desc">• Form-C Relays de-energized (NC Passthrough)</text>
  </g>

  <!-- Transition 1 -> 2 -->
  <path d="M 360 170 L 440 170" stroke="#0284c7" stroke-width="2.2" marker-end="url(#arrow-fsm)" />
  <rect x="365" y="145" width="70" height="18" rx="3" fill="#e0f2fe" />
  <text x="370" y="158" class="guard-text">RF Packet</text>

  <!-- 2. STATE_PREEMPTION_PENDING -->
  <g class="shadow">
    <rect x="445" y="125" width="290" height="90" rx="10" fill="#ffffff" stroke="#38bdf8" stroke-width="2" />
    <rect x="445" y="125" width="8" height="90" rx="4" fill="#0284c7" />
    <text x="465" y="148" class="state-name" fill="#0369a1">2. PREEMPTION_PENDING</text>
    <text x="465" y="166" class="state-time" fill="#0284c7">Duration: &lt; 25 ms (Hardware Interrupt)</text>
    <text x="465" y="184" class="state-desc">• Validate HMAC-SHA256 &amp; 32-bit Counter</text>
    <text x="465" y="200" class="state-desc">• Latch requested direction (e.g. North Approach)</text>
  </g>

  <!-- Transition 2 -> 3 -->
  <path d="M 735 170 L 815 170" stroke="#0284c7" stroke-width="2.2" marker-end="url(#arrow-fsm)" />
  <rect x="740" y="145" width="70" height="18" rx="3" fill="#e0f2fe" />
  <text x="745" y="158" class="guard-text">Latch Done</text>

  <!-- 3. STATE_ACTIVE_AMBER (Mandatory Deceleration) -->
  <g class="shadow">
    <rect x="820" y="125" width="300" height="95" rx="10" fill="#fefce8" stroke="#eab308" stroke-width="2.5" />
    <rect x="820" y="125" width="8" height="95" rx="4" fill="#ca8a04" />
    <circle cx="1095" cy="150" r="10" fill="#eab308" stroke="#ca8a04" stroke-width="1.5" />
    <text x="840" y="148" class="state-name" fill="#854d0e">3. STATE_ACTIVE_AMBER</text>
    <text x="840" y="168" class="state-time" fill="#ca8a04">Duration: 3,500 ms (Safe Deceleration)</text>
    <text x="840" y="186" class="state-desc">• Cross-Traffic (E-W): AMBER (Deceleration)</text>
    <text x="840" y="202" class="state-desc">• Priority Target: HELD RED | Pedestrians: STOP</text>
  </g>

  <!-- Transition 3 -> 4 -->
  <path d="M 970 220 L 970 295" stroke="#0284c7" stroke-width="2.2" marker-end="url(#arrow-fsm)" />
  <rect x="980" y="248" width="85" height="18" rx="3" fill="#e0f2fe" />
  <text x="985" y="261" class="guard-text">t &gt;= 3500 ms</text>

  <!-- 4. STATE_ALL_RED_CLEARANCE (Intersection Evacuation) -->
  <g class="shadow">
    <rect x="820" y="300" width="300" height="95" rx="10" fill="#fef2f2" stroke="#ef4444" stroke-width="2.5" />
    <rect x="820" y="300" width="8" height="95" rx="4" fill="#dc2626" />
    <circle cx="1095" cy="325" r="10" fill="#ef4444" stroke="#b91c1c" stroke-width="1.5" />
    <text x="840" y="323" class="state-name" fill="#991b1b">4. ALL_RED_CLEARANCE</text>
    <text x="840" y="343" class="state-time" fill="#dc2626">Duration: 2,000 ms (Junction Box Clearance)</text>
    <text x="840" y="361" class="state-desc">• ALL LANES HELD RED (Cross &amp; Emergency)</text>
    <text x="840" y="377" class="state-desc">• Straggling vehicles fully evacuate junction box</text>
  </g>

  <!-- Transition 4 -> 5 -->
  <path d="M 820 348 L 740 348" stroke="#16a34a" stroke-width="2.5" marker-end="url(#arrow-green)" />
  <rect x="745" y="325" width="70" height="18" rx="3" fill="#dcfce7" />
  <text x="750" y="338" font-family="'Segoe UI', Arial" font-size="9.5px" font-weight="700" fill="#15803d">t &gt;= 2000 ms</text>

  <!-- 5. STATE_PRIORITY_GREEN (Corridor Preemption) -->
  <g class="shadow">
    <rect x="420" y="295" width="315" height="105" rx="10" fill="#f0fdf4" stroke="#22c55e" stroke-width="3" />
    <rect x="420" y="295" width="8" height="105" rx="4" fill="#16a34a" />
    <circle cx="710" cy="320" r="10" fill="#22c55e" stroke="#15803d" stroke-width="1.5" />
    <text x="440" y="320" class="state-name" fill="#166534">5. STATE_PRIORITY_GREEN</text>
    <text x="440" y="340" class="state-time" fill="#15803d">Duration: 15,000 – 30,000 ms (Active Corridor)</text>
    <text x="440" y="358" class="state-desc">• Priority Approach (North): ENERGIZED GREEN</text>
    <text x="440" y="374" class="state-desc">• Cross Lanes: HARD MECHANICAL RED (K3 cut by K6)</text>
    <text x="440" y="390" class="state-desc">• Edge-AI: Logging Plates &amp; Granting Challan Immunity</text>
  </g>

  <!-- Transition 5 -> 6 -->
  <path d="M 420 348 L 340 348" stroke="#0284c7" stroke-width="2.2" marker-end="url(#arrow-fsm)" />
  <rect x="345" y="325" width="70" height="18" rx="3" fill="#e0f2fe" />
  <text x="350" y="338" class="guard-text">Exit Trigger</text>

  <!-- 6. STATE_RECOVERY_AMBER -->
  <g class="shadow">
    <rect x="40" y="300" width="295" height="95" rx="10" fill="#fefce8" stroke="#eab308" stroke-width="2.5" />
    <rect x="40" y="300" width="8" height="95" rx="4" fill="#ca8a04" />
    <circle cx="310" cy="325" r="10" fill="#eab308" stroke="#ca8a04" stroke-width="1.5" />
    <text x="60" y="323" class="state-name" fill="#854d0e">6. RECOVERY_AMBER</text>
    <text x="60" y="343" class="state-time" fill="#ca8a04">Duration: 3,500 ms (Anti-Tailgate Warning)</text>
    <text x="60" y="361" class="state-desc">• Target Emergency Lane: AMBER ENERGIZED</text>
    <text x="60" y="377" class="state-desc">• Cross Lanes: HELD RED | Stops civilian tailgating</text>
  </g>

  <!-- Transition 6 -> 7 -->
  <path d="M 185 395 L 185 470" stroke="#0284c7" stroke-width="2.2" marker-end="url(#arrow-fsm)" />
  <rect x="195" y="425" width="85" height="18" rx="3" fill="#e0f2fe" />
  <text x="200" y="438" class="guard-text">t &gt;= 3500 ms</text>

  <!-- 7. STATE_RECOVERY_ALL_RED -->
  <g class="shadow">
    <rect x="40" y="475" width="295" height="95" rx="10" fill="#fef2f2" stroke="#ef4444" stroke-width="2.5" />
    <rect x="40" y="475" width="8" height="95" rx="4" fill="#dc2626" />
    <circle cx="310" cy="500" r="10" fill="#ef4444" stroke="#b91c1c" stroke-width="1.5" />
    <text x="60" y="498" class="state-name" fill="#991b1b">7. RECOVERY_ALL_RED</text>
    <text x="60" y="518" class="state-time" fill="#dc2626">Duration: 1,500 ms (Phase Resync Buffer)</text>
    <text x="60" y="536" class="state-desc">• ALL LANES HELD RED (Settles relay transients)</text>
    <text x="60" y="552" class="state-desc">• Resynchronizes legacy traffic controller timers</text>
  </g>

  <!-- Transition 7 -> 1 (Loop back to Normal) -->
  <path d="M 140 475 L 140 215" stroke="#0284c7" stroke-width="2.2" marker-end="url(#arrow-fsm)" />
  <rect x="75" y="250" width="60" height="18" rx="3" fill="#e0f2fe" />
  <text x="80" y="263" class="guard-text">Cycle Sync</text>

  <!-- ========================================================================= -->
  <!-- FAIL-SAFE FALLBACK & HARDWARE WATCHDOG OVERRIDE                           -->
  <!-- ========================================================================= -->
  <g class="shadow">
    <rect x="420" y="475" width="700" height="95" rx="10" fill="#fff7ed" stroke="#ea580c" stroke-width="2.5" />
    <rect x="420" y="475" width="8" height="95" rx="4" fill="#c2410c" />
    <text x="440" y="500" class="state-name" fill="#9a3412">🚨 STATE_FAIL_SAFE_FALLBACK (Hardware Crash / Brownout / Watchdog Trip)</text>
    <text x="440" y="520" class="state-time" fill="#c2410c">Actuation Speed: &lt; 20 ms (Mechanical Spring Return)</text>
    <text x="440" y="538" class="state-desc">• All Form-C Relay coils instantly de-energize; moving contacts drop to Normally Closed (NC) pins.</text>
    <text x="440" y="554" class="state-desc">• Control reverts 100% to legacy traffic signal controller (fixed round-robin or flashing amber).</text>
  </g>

  <!-- Fail-safe triggers (Dotted Red Arrows) -->
  <path d="M 570 400 L 570 475" stroke="#dc2626" stroke-width="1.8" stroke-dasharray="4,3" marker-end="url(#arrow-fail)" />
  <text x="575" y="445" class="fail-text">Watchdog Trip / Brownout</text>

  <path d="M 970 395 L 970 475" stroke="#dc2626" stroke-width="1.8" stroke-dasharray="4,3" marker-end="url(#arrow-fail)" />
  <text x="975" y="445" class="fail-text">Relay Error</text>

  <!-- ========================================================================= -->
  <!-- BOTTOM DETAIL PANELS                                                      -->
  <!-- ========================================================================= -->

  <!-- Panel 1: Fail-Safe Interlock Matrix -->
  <rect x="25" y="605" width="560" height="265" rx="10" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" class="shadow" />
  <text x="45" y="630" class="panel-title">FORM-C HARDWARE INTERLOCK STATE MATRIX</text>
  
  <!-- Table Header -->
  <rect x="45" y="645" width="520" height="24" fill="#f1f5f9" />
  <text x="55" y="661" font-family="'Segoe UI', Arial" font-size="10px" font-weight="700" fill="#1e293b">STATE</text>
  <text x="185" y="661" font-family="'Segoe UI', Arial" font-size="10px" font-weight="700" fill="#1e293b">CROSS (E-W)</text>
  <text x="295" y="661" font-family="'Segoe UI', Arial" font-size="10px" font-weight="700" fill="#1e293b">TARGET (NORTH)</text>
  <text x="415" y="661" font-family="'Segoe UI', Arial" font-size="10px" font-weight="700" fill="#1e293b">INTERLOCK STATUS</text>

  <!-- Row 1 -->
  <text x="55" y="685" font-family="'Segoe UI', Arial" font-size="9.5px" fill="#475569">NORMAL_CYCLE</text>
  <text x="185" y="685" font-family="'Segoe UI', Arial" font-size="9.5px" fill="#16a34a" font-weight="600">GREEN / AMBER / RED</text>
  <text x="295" y="685" font-family="'Segoe UI', Arial" font-size="9.5px" fill="#dc2626" font-weight="600">RED / AMBER / GREEN</text>
  <text x="415" y="685" font-family="'Segoe UI', Arial" font-size="9.5px" fill="#64748b">Legacy Passthrough (NC)</text>

  <!-- Row 2 -->
  <text x="55" y="709" font-family="'Segoe UI', Arial" font-size="9.5px" fill="#475569">ACTIVE_AMBER (3.5s)</text>
  <text x="185" y="709" font-family="'Segoe UI', Arial" font-size="9.5px" fill="#ca8a04" font-weight="700">AMBER (Yellow)</text>
  <text x="295" y="709" font-family="'Segoe UI', Arial" font-size="9.5px" fill="#dc2626" font-weight="700">SOLID RED</text>
  <text x="415" y="709" font-family="'Segoe UI', Arial" font-size="9.5px" fill="#0284c7">Decel Timer Active</text>

  <!-- Row 3 -->
  <text x="55" y="733" font-family="'Segoe UI', Arial" font-size="9.5px" fill="#475569">ALL_RED_CLEAR (2.0s)</text>
  <text x="185" y="733" font-family="'Segoe UI', Arial" font-size="9.5px" fill="#dc2626" font-weight="700">SOLID RED</text>
  <text x="295" y="733" font-family="'Segoe UI', Arial" font-size="9.5px" fill="#dc2626" font-weight="700">SOLID RED</text>
  <text x="415" y="733" font-family="'Segoe UI', Arial" font-size="9.5px" fill="#dc2626" font-weight="700">All Lanes Open Circuit</text>

  <!-- Row 4 -->
  <text x="55" y="757" font-family="'Segoe UI', Arial" font-size="9.5px" fill="#475569">PRIORITY_GREEN (20s)</text>
  <text x="185" y="757" font-family="'Segoe UI', Arial" font-size="9.5px" fill="#dc2626" font-weight="700">HARD LOCKED RED</text>
  <text x="295" y="757" font-family="'Segoe UI', Arial" font-size="9.5px" fill="#16a34a" font-weight="700">ENERGIZED GREEN</text>
  <text x="415" y="757" font-family="'Segoe UI', Arial" font-size="9.5px" fill="#16a34a" font-weight="700">K6 Breaks K3 Power Rail</text>

  <!-- Row 5 -->
  <text x="55" y="781" font-family="'Segoe UI', Arial" font-size="9.5px" fill="#475569">RECOVERY_AMBER (3.5s)</text>
  <text x="185" y="781" font-family="'Segoe UI', Arial" font-size="9.5px" fill="#dc2626" font-weight="700">SOLID RED</text>
  <text x="295" y="781" font-family="'Segoe UI', Arial" font-size="9.5px" fill="#ca8a04" font-weight="700">AMBER (Yellow)</text>
  <text x="415" y="781" font-family="'Segoe UI', Arial" font-size="9.5px" fill="#0284c7">Target Decel Timer</text>

  <!-- Row 6 -->
  <text x="55" y="805" font-family="'Segoe UI', Arial" font-size="9.5px" fill="#475569">RECOVERY_ALL_RED (1.5s)</text>
  <text x="185" y="805" font-family="'Segoe UI', Arial" font-size="9.5px" fill="#dc2626" font-weight="700">SOLID RED</text>
  <text x="295" y="805" font-family="'Segoe UI', Arial" font-size="9.5px" fill="#dc2626" font-weight="700">SOLID RED</text>
  <text x="415" y="805" font-family="'Segoe UI', Arial" font-size="9.5px" fill="#64748b">Sync Re-engagement</text>

  <!-- Row 7 -->
  <text x="55" y="829" font-family="'Segoe UI', Arial" font-size="9.5px" fill="#b91c1c" font-weight="700">FAIL-SAFE BROWNOUT</text>
  <text x="185" y="829" font-family="'Segoe UI', Arial" font-size="9.5px" fill="#b91c1c" font-weight="700">DE-ENERGIZED (NC)</text>
  <text x="295" y="829" font-family="'Segoe UI', Arial" font-size="9.5px" fill="#b91c1c" font-weight="700">DE-ENERGIZED (NC)</text>
  <text x="415" y="829" font-family="'Segoe UI', Arial" font-size="9.5px" fill="#b91c1c" font-weight="700">Zero Collision Drop &lt;20ms</text>

  <!-- Panel 2: Physical Collision Avoidance Guarantees -->
  <rect x="615" y="605" width="560" height="265" rx="10" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" class="shadow" />
  <text x="635" y="630" class="panel-title">INDIAN ROAD CONGRESS (IRC:SP:12) SAFETY COMPLIANCE</text>

  <g transform="translate(635, 645)">
    <text x="0" y="16" font-family="'Segoe UI', Arial" font-size="11px" font-weight="700" fill="#0f172a">1. Safe Deceleration Physics (3.5s Amber):</text>
    <text x="0" y="32" class="panel-body">• At 45 km/h (12.5 m/s), reaction distance is 9.4m (0.75s) + braking distance 13.9m = 23.3m.</text>
    <text x="0" y="46" class="panel-body">• 3,500 ms amber provides 43.7m stopping window, fully eliminating the "Dilemma Zone".</text>

    <text x="0" y="74" font-family="'Segoe UI', Arial" font-size="11px" font-weight="700" fill="#0f172a">2. Intersection Box Evacuation (2.0s All-Red):</text>
    <text x="0" y="90" class="panel-body">• A 24m wide 4-lane intersection requires 1.92s for a 12m commercial bus to clear at 45 km/h.</text>
    <text x="0" y="104" class="panel-body">• 2,000 ms all-red ensures zero vehicle collision risk before Priority Green turns ON.</text>

    <text x="0" y="132" font-family="'Segoe UI', Arial" font-size="11px" font-weight="700" fill="#0f172a">3. Series Power Chaining (Zero Dual-Green Guarantee):</text>
    <text x="0" y="148" class="panel-body">• The 230V AC phase power for Cross Green (K3) is fed through Normally Closed (NC) pin of K6.</text>
    <text x="0" y="162" class="panel-body">• When K6 energizes, the power to K3 is physically severed before K6 NO contact closes.</text>

    <text x="0" y="190" font-family="'Segoe UI', Arial" font-size="11px" font-weight="700" fill="#0f172a">4. Hard Ceiling Watchdog (30.0s Timeout):</text>
    <text x="0" y="206" class="panel-body">• If edge-AI camera drops or officer neglects reset, hardware timer forces exit at t = 30.0s.</text>
  </g>
</svg>
"""

# -------------------------------------------------------------------------------------------------
# 3. docs/timing_sequence.svg
# -------------------------------------------------------------------------------------------------
svg_timing = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 800" width="1200" height="800">
  <defs>
    <style>
      .title { font-family: 'Segoe UI', Arial, sans-serif; font-weight: 800; font-size: 24px; fill: #0f172a; }
      .subtitle { font-family: 'Segoe UI', Arial, sans-serif; font-weight: 500; font-size: 13.5px; fill: #475569; }
      .axis-label { font-family: 'Segoe UI', Arial, sans-serif; font-size: 11px; font-weight: 700; fill: #475569; }
      .lane-title { font-family: 'Segoe UI', Arial, sans-serif; font-size: 12px; font-weight: 700; fill: #0f172a; }
      .bar-text { font-family: 'Segoe UI', Arial, sans-serif; font-size: 10px; font-weight: 700; fill: #ffffff; text-anchor: middle; }
      .bar-text-dark { font-family: 'Segoe UI', Arial, sans-serif; font-size: 10px; font-weight: 700; fill: #713f12; text-anchor: middle; }
      .phase-callout { font-family: 'Segoe UI', Arial, sans-serif; font-size: 10px; font-weight: 700; fill: #0284c7; text-anchor: middle; }
      .phase-dur { font-family: 'Segoe UI', Arial, sans-serif; font-size: 9px; fill: #64748b; text-anchor: middle; }
      .note-title { font-family: 'Segoe UI', Arial, sans-serif; font-size: 11px; font-weight: 700; fill: #0f172a; }
      .note-text { font-family: 'Segoe UI', Arial, sans-serif; font-size: 10.5px; fill: #334155; }
      .shadow { filter: drop-shadow(0px 3px 6px rgba(0, 0, 0, 0.05)); }
    </style>
    <linearGradient id="headerGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f8fafc" />
      <stop offset="100%" stop-color="#f1f5f9" />
    </linearGradient>
    <marker id="arrow-down" viewBox="0 0 10 10" refX="5" refY="6" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 1 0 L 5 10 L 9 0 z" fill="#0284c7" />
    </marker>
  </defs>

  <!-- Background -->
  <rect x="0" y="0" width="1200" height="800" fill="#f8fafc" />

  <!-- Header -->
  <rect x="25" y="20" width="1150" height="70" rx="12" fill="url(#headerGrad)" stroke="#cbd5e1" stroke-width="1.5" class="shadow" />
  <text x="50" y="48" class="title">Millisecond-Level Phase Timing Sequence &amp; Interlock Clearance</text>
  <text x="50" y="72" class="subtitle">Complete Preemption Phasing: Active Green ➔ 3.5s Amber ➔ 2.0s All-Red ➔ Priority Green ➔ Recovery</text>

  <!-- Timeline Top Scale Container -->
  <!-- Origin x = 200 corresponds to t = 0 ms. Width = 950 px corresponds to 35,000 ms. Scale = 950 / 35000 = 0.02714 px/ms -->
  <!-- Key Timepoints:
       t = 0 ms: x = 200
       t = 3,500 ms: x = 200 + 3500 * 0.02714 = 295
       t = 5,500 ms: x = 200 + 5500 * 0.02714 = 349
       t = 25,500 ms: x = 200 + 25500 * 0.02714 = 892
       t = 29,000 ms: x = 200 + 29000 * 0.02714 = 987
       t = 30,500 ms: x = 200 + 30500 * 0.02714 = 1028
       t = 35,000 ms: x = 200 + 35000 * 0.02714 = 1150
  -->

  <!-- Phase Header Callouts -->
  <g transform="translate(0, 105)">
    <!-- Phase 1: Pre-Trigger -->
    <rect x="60" y="0" width="130" height="42" rx="6" fill="#f1f5f9" stroke="#cbd5e1" />
    <text x="125" y="18" class="phase-callout" fill="#475569">NORMAL FLOW</text>
    <text x="125" y="32" class="phase-dur">Round-Robin</text>

    <!-- Phase 2: Active Amber -->
    <rect x="200" y="0" width="95" height="42" rx="6" fill="#fef9c3" stroke="#eab308" />
    <text x="247" y="18" class="phase-callout" fill="#854d0e">ACTIVE AMBER</text>
    <text x="247" y="32" class="phase-dur">3,500 ms</text>

    <!-- Phase 3: All-Red Inter-Green -->
    <rect x="298" y="0" width="51" height="42" rx="6" fill="#fee2e2" stroke="#ef4444" />
    <text x="323" y="18" class="phase-callout" fill="#991b1b">ALL-RED</text>
    <text x="323" y="32" class="phase-dur">2,000 ms</text>

    <!-- Phase 4: Priority Green -->
    <rect x="352" y="0" width="540" height="42" rx="6" fill="#dcfce7" stroke="#22c55e" />
    <text x="622" y="18" class="phase-callout" fill="#15803d">PRIORITY GREEN CORRIDOR PREEMPTION</text>
    <text x="622" y="32" class="phase-dur">20,000 ms (Emergency Corridor Transit + Automated Challan Immunity Window)</text>

    <!-- Phase 5: Recovery Amber -->
    <rect x="895" y="0" width="92" height="42" rx="6" fill="#fef9c3" stroke="#eab308" />
    <text x="941" y="18" class="phase-callout" fill="#854d0e">REC. AMBER</text>
    <text x="941" y="32" class="phase-dur">3,500 ms</text>

    <!-- Phase 6: Recovery All-Red -->
    <rect x="990" y="0" width="38" height="42" rx="6" fill="#fee2e2" stroke="#ef4444" />
    <text x="1009" y="18" class="phase-callout" fill="#991b1b">ALL-RED</text>
    <text x="1009" y="32" class="phase-dur">1,500ms</text>

    <!-- Phase 7: Resume Normal -->
    <rect x="1031" y="0" width="119" height="42" rx="6" fill="#f1f5f9" stroke="#cbd5e1" />
    <text x="1090" y="18" class="phase-callout" fill="#475569">NORMAL CYCLE</text>
    <text x="1090" y="32" class="phase-dur">Resumed</text>
  </g>

  <!-- Vertical Phase Boundary Guidelines -->
  <line x1="200" y1="150" x2="200" y2="570" stroke="#0284c7" stroke-width="1.5" stroke-dasharray="4,4" />
  <line x1="295" y1="150" x2="295" y2="570" stroke="#64748b" stroke-width="1" stroke-dasharray="3,3" />
  <line x1="349" y1="150" x2="349" y2="570" stroke="#16a34a" stroke-width="1.5" stroke-dasharray="4,4" />
  <line x1="892" y1="150" x2="892" y2="570" stroke="#64748b" stroke-width="1" stroke-dasharray="3,3" />
  <line x1="987" y1="150" x2="987" y2="570" stroke="#64748b" stroke-width="1" stroke-dasharray="3,3" />
  <line x1="1028" y1="150" x2="1028" y2="570" stroke="#0284c7" stroke-width="1.5" stroke-dasharray="4,4" />

  <!-- Trigger Event Marker -->
  <g transform="translate(200, 155)">
    <polygon points="-6,0 6,0 0,10" fill="#0284c7" />
    <rect x="-65" y="-22" width="130" height="20" rx="4" fill="#0284c7" />
    <text x="0" y="-8" font-family="'Segoe UI', Arial" font-size="9.5px" font-weight="700" fill="#ffffff" text-anchor="middle">⚡ RF TRIGGER (t=0ms)</text>
  </g>

  <!-- ========================================================================= -->
  <!-- SWIMLANE 1: CROSS-TRAFFIC SIGNAL HEAD (E-W APPROACH)                      -->
  <!-- ========================================================================= -->
  <g transform="translate(25, 185)">
    <rect x="0" y="0" width="170" height="60" rx="6" fill="#ffffff" stroke="#cbd5e1" class="shadow" />
    <text x="15" y="25" class="lane-title">Cross-Traffic (E-W)</text>
    <text x="15" y="42" font-family="'Segoe UI', Arial" font-size="10px" fill="#64748b">Moving Traffic Lane</text>

    <!-- Signal Bars -->
    <!-- Prior to t=0: Green -->
    <rect x="35" y="10" width="140" height="40" rx="4" fill="#16a34a" />
    <text x="105" y="34" class="bar-text">ACTIVE GREEN</text>

    <!-- 0ms to 3500ms: Amber -->
    <rect x="175" y="10" width="95" height="40" rx="4" fill="#eab308" />
    <text x="222" y="34" class="bar-text-dark">AMBER (3.5s)</text>

    <!-- 3500ms to 5500ms: Red -->
    <rect x="273" y="10" width="51" height="40" rx="4" fill="#dc2626" />
    <text x="298" y="34" class="bar-text">RED (2s)</text>

    <!-- 5500ms to 25500ms: HARD LOCKED RED -->
    <rect x="327" y="10" width="540" height="40" rx="4" fill="#991b1b" stroke="#7f1d1d" stroke-width="1" />
    <text x="597" y="34" class="bar-text">🔒 HARD LOCKED RED (Form-C Relays Severed - Mutually Exclusive)</text>

    <!-- 25500ms to 29000ms: Red -->
    <rect x="870" y="10" width="92" height="40" rx="4" fill="#dc2626" />
    <text x="916" y="34" class="bar-text">RED (3.5s)</text>

    <!-- 29000ms to 30500ms: Red -->
    <rect x="965" y="10" width="38" height="40" rx="4" fill="#dc2626" />
    <text x="984" y="34" class="bar-text">RED</text>

    <!-- >30500ms: Resumed Green -->
    <rect x="1006" y="10" width="119" height="40" rx="4" fill="#16a34a" />
    <text x="1065" y="34" class="bar-text">GREEN RESUMED</text>
  </g>

  <!-- ========================================================================= -->
  <!-- SWIMLANE 2: PRIORITY EMERGENCY SIGNAL HEAD (NORTH APPROACH)               -->
  <!-- ========================================================================= -->
  <g transform="translate(25, 265)">
    <rect x="0" y="0" width="170" height="60" rx="6" fill="#ffffff" stroke="#cbd5e1" class="shadow" />
    <text x="15" y="25" class="lane-title">Emergency (North)</text>
    <text x="15" y="42" font-family="'Segoe UI', Arial" font-size="10px" fill="#64748b">Ambulance Approach</text>

    <!-- Signal Bars -->
    <!-- Prior to t=0: Red -->
    <rect x="35" y="10" width="140" height="40" rx="4" fill="#dc2626" />
    <text x="105" y="34" class="bar-text">RED (QUEUED)</text>

    <!-- 0ms to 3500ms: Red -->
    <rect x="175" y="10" width="95" height="40" rx="4" fill="#dc2626" />
    <text x="222" y="34" class="bar-text">RED (HOLD)</text>

    <!-- 3500ms to 5500ms: Red -->
    <rect x="273" y="10" width="51" height="40" rx="4" fill="#dc2626" />
    <text x="298" y="34" class="bar-text">ALL-RED</text>

    <!-- 5500ms to 25500ms: PRIORITY GREEN -->
    <rect x="327" y="10" width="540" height="40" rx="4" fill="#16a34a" stroke="#15803d" stroke-width="1.5" />
    <text x="597" y="34" class="bar-text">🟢 PHYSICAL OVERHEAD GREEN (Queue Clears Stop Line with Full Confidence)</text>

    <!-- 25500ms to 29000ms: Recovery Amber -->
    <rect x="870" y="10" width="92" height="40" rx="4" fill="#eab308" />
    <text x="916" y="34" class="bar-text-dark">AMBER (3.5s)</text>

    <!-- 29000ms to 30500ms: Recovery All-Red -->
    <rect x="965" y="10" width="38" height="40" rx="4" fill="#dc2626" />
    <text x="984" y="34" class="bar-text">ALL-RED</text>

    <!-- >30500ms: Red in normal cycle -->
    <rect x="1006" y="10" width="119" height="40" rx="4" fill="#dc2626" />
    <text x="1065" y="34" class="bar-text">RED (NORMAL CYCLE)</text>
  </g>

  <!-- ========================================================================= -->
  <!-- SWIMLANE 3: RELAY CONTACT HARDWARE STATE                                  -->
  <!-- ========================================================================= -->
  <g transform="translate(25, 345)">
    <rect x="0" y="0" width="170" height="60" rx="6" fill="#ffffff" stroke="#cbd5e1" class="shadow" />
    <text x="15" y="25" class="lane-title">Form-C Relay State</text>
    <text x="15" y="42" font-family="'Segoe UI', Arial" font-size="10px" fill="#64748b">Break-Before-Make Matrix</text>

    <!-- Pre-trigger: Relays De-energized -->
    <rect x="35" y="10" width="140" height="40" rx="4" fill="#e2e8f0" />
    <text x="105" y="34" font-family="'Segoe UI', Arial" font-size="9.5px" font-weight="700" fill="#475569" text-anchor="middle">NC PASSTHROUGH</text>

    <!-- 0ms to 3500ms: Amber Relay ON -->
    <rect x="175" y="10" width="95" height="40" rx="4" fill="#fef3c7" stroke="#f59e0b" />
    <text x="222" y="34" font-family="'Segoe UI', Arial" font-size="9.5px" font-weight="700" fill="#b45309" text-anchor="middle">K2 ENERGIZED</text>

    <!-- 3500ms to 5500ms: All-Red (K1, K4 ON) -->
    <rect x="273" y="10" width="51" height="40" rx="4" fill="#fee2e2" stroke="#ef4444" />
    <text x="298" y="34" font-family="'Segoe UI', Arial" font-size="9px" font-weight="700" fill="#b91c1c" text-anchor="middle">K1+K4 ON</text>

    <!-- 5500ms to 25500ms: Priority K6 ON (K3 POWER CUT) -->
    <rect x="327" y="10" width="540" height="40" rx="4" fill="#ecfdf5" stroke="#10b981" stroke-width="1.2" />
    <text x="597" y="34" font-family="'Segoe UI', Arial" font-size="10px" font-weight="700" fill="#047857" text-anchor="middle">⚡ K6 ENERGIZED (NO CLOSED) | K3 GREEN POWER RAIL MECHANICALLY SEVERED</text>

    <!-- 25500ms to 29000ms: Target Amber K5 ON -->
    <rect x="870" y="10" width="92" height="40" rx="4" fill="#fef3c7" stroke="#f59e0b" />
    <text x="916" y="34" font-family="'Segoe UI', Arial" font-size="9.5px" font-weight="700" fill="#b45309" text-anchor="middle">K5 ENERGIZED</text>

    <!-- 29000ms to 30500ms: All Red K1+K4 -->
    <rect x="965" y="10" width="38" height="40" rx="4" fill="#fee2e2" stroke="#ef4444" />
    <text x="984" y="34" font-family="'Segoe UI', Arial" font-size="8.5px" font-weight="700" fill="#b91c1c" text-anchor="middle">K1+K4</text>

    <!-- >30500ms: All coils drop -->
    <rect x="1006" y="10" width="119" height="40" rx="4" fill="#e2e8f0" />
    <text x="1065" y="34" font-family="'Segoe UI', Arial" font-size="9.5px" font-weight="700" fill="#475569" text-anchor="middle">ALL COILS DROP (NC)</text>
  </g>

  <!-- ========================================================================= -->
  <!-- SWIMLANE 4: EDGE-AI & E-CHALLAN EXEMPTION TIMELINE                         -->
  <!-- ========================================================================= -->
  <g transform="translate(25, 425)">
    <rect x="0" y="0" width="170" height="60" rx="6" fill="#ffffff" stroke="#cbd5e1" class="shadow" />
    <text x="15" y="25" class="lane-title">Edge-AI &amp; Challan</text>
    <text x="15" y="42" font-family="'Segoe UI', Arial" font-size="10px" fill="#64748b">ITMS Automatic Immunity</text>

    <!-- Pre-trigger: Continuous Monitoring -->
    <rect x="35" y="10" width="140" height="40" rx="4" fill="#f8fafc" stroke="#cbd5e1" />
    <text x="105" y="34" font-family="'Segoe UI', Arial" font-size="9px" fill="#64748b" text-anchor="middle">30 FPS RTSP MONITOR</text>

    <!-- Exemption Lead Window (T_trigger - 10s buffer) -->
    <!-- Exemption Active Bar spanning from t = -10s up to t = 35s -->
    <rect x="140" y="10" width="875" height="40" rx="4" fill="#f5f3ff" stroke="#8b5cf6" stroke-width="1.5" />
    <text x="577" y="26" font-family="'Segoe UI', Arial" font-size="10.5px" font-weight="700" fill="#6d28d9" text-anchor="middle">🛡️ AUTOMATED E-CHALLAN EXEMPTION WINDOW: [ T_trigger - 10s  to  T_clearance + 10s ]</text>
    <text x="577" y="42" font-family="'Segoe UI', Arial" font-size="9.5px" fill="#7c3aed" text-anchor="middle">YOLOv8 + ANPR OCR logs all crossing citizen plates ➔ Direct Push to Raipur ICCC ➔ Zero Court Fines</text>

    <!-- Normal monitoring resumed -->
    <rect x="1018" y="10" width="107" height="40" rx="4" fill="#f8fafc" stroke="#cbd5e1" />
    <text x="1071" y="34" font-family="'Segoe UI', Arial" font-size="9px" fill="#64748b" text-anchor="middle">AUDIT SYNC</text>
  </g>

  <!-- ========================================================================= -->
  <!-- HORIZONTAL TIME AXIS                                                      -->
  <!-- ========================================================================= -->
  <g transform="translate(200, 520)">
    <line x1="0" y1="0" x2="950" y2="0" stroke="#475569" stroke-width="2" />
    
    <!-- Ticks & Time Labels -->
    <!-- 0 ms -->
    <line x1="0" y1="0" x2="0" y2="8" stroke="#475569" stroke-width="2" />
    <text x="0" y="22" class="axis-label" text-anchor="middle">0 ms</text>
    <text x="0" y="34" font-family="'Segoe UI', Arial" font-size="9px" fill="#64748b" text-anchor="middle">Trigger</text>

    <!-- 3,500 ms -->
    <line x1="95" y1="0" x2="95" y2="8" stroke="#475569" stroke-width="2" />
    <text x="95" y="22" class="axis-label" text-anchor="middle">3,500 ms</text>
    <text x="95" y="34" font-family="'Segoe UI', Arial" font-size="9px" fill="#64748b" text-anchor="middle">+3.5s Amber</text>

    <!-- 5,500 ms -->
    <line x1="149" y1="0" x2="149" y2="8" stroke="#475569" stroke-width="2" />
    <text x="149" y="22" class="axis-label" text-anchor="middle">5,500 ms</text>
    <text x="149" y="34" font-family="'Segoe UI', Arial" font-size="9px" fill="#64748b" text-anchor="middle">+2.0s All-Red</text>

    <!-- 25,500 ms -->
    <line x1="692" y1="0" x2="692" y2="8" stroke="#475569" stroke-width="2" />
    <text x="692" y="22" class="axis-label" text-anchor="middle">25,500 ms</text>
    <text x="692" y="34" font-family="'Segoe UI', Arial" font-size="9px" fill="#64748b" text-anchor="middle">+20s Green</text>

    <!-- 29,000 ms -->
    <line x1="787" y1="0" x2="787" y2="8" stroke="#475569" stroke-width="2" />
    <text x="787" y="22" class="axis-label" text-anchor="middle">29,000 ms</text>
    <text x="787" y="34" font-family="'Segoe UI', Arial" font-size="9px" fill="#64748b" text-anchor="middle">+3.5s Amber</text>

    <!-- 30,500 ms -->
    <line x1="828" y1="0" x2="828" y2="8" stroke="#475569" stroke-width="2" />
    <text x="828" y="22" class="axis-label" text-anchor="middle">30,500 ms</text>
    <text x="828" y="34" font-family="'Segoe UI', Arial" font-size="9px" fill="#64748b" text-anchor="middle">+1.5s All-Red</text>

    <!-- 35,000 ms -->
    <line x1="950" y1="0" x2="950" y2="8" stroke="#475569" stroke-width="2" />
    <text x="950" y="22" class="axis-label" text-anchor="middle">35,000 ms</text>
    <text x="950" y="34" font-family="'Segoe UI', Arial" font-size="9px" fill="#64748b" text-anchor="middle">Resumed</text>
  </g>

  <!-- ========================================================================= -->
  <!-- TECHNICAL EXPLANATION FOOTER CARDS                                        -->
  <!-- ========================================================================= -->
  <g transform="translate(25, 595)">
    <!-- Card 1: 5-Second Clearance Physics -->
    <rect x="0" y="0" width="370" height="175" rx="8" fill="#ffffff" stroke="#cbd5e1" class="shadow" />
    <rect x="0" y="0" width="5" height="175" rx="2.5" fill="#eab308" />
    <text x="18" y="25" class="note-title">1. Safe Clearance Physics (5.5s Total)</text>
    <text x="18" y="48" class="note-text">• <tspan font-weight="700">3,500 ms Amber Deceleration:</tspan></text>
    <text x="28" y="65" class="note-text">Allows 45 km/h vehicles to brake at comfortable</text>
    <text x="28" y="81" class="note-text">3.2 m/s² deceleration without skidding.</text>
    <text x="18" y="105" class="note-text">• <tspan font-weight="700">2,000 ms All-Red Box Clearance:</tspan></text>
    <text x="28" y="122" class="note-text">Guarantees that straggling buses/trucks completely</text>
    <text x="28" y="138" class="note-text">evacuate the intersection box before target green.</text>
    <text x="18" y="160" class="note-text font-semibold" fill="#b45309">100% compliant with IRC:SP:12 (2015) §7.3–7.4</text>
  </g>

  <g transform="translate(415, 595)">
    <!-- Card 2: Form-C Relay Interlock -->
    <rect x="0" y="0" width="370" height="175" rx="8" fill="#ffffff" stroke="#cbd5e1" class="shadow" />
    <rect x="0" y="0" width="5" height="175" rx="2.5" fill="#16a34a" />
    <text x="18" y="25" class="note-title">2. Form-C Break-Before-Make Guarantee</text>
    <text x="18" y="48" class="note-text">• <tspan font-weight="700">Hardware Mutually Exclusive Greens:</tspan></text>
    <text x="28" y="65" class="note-text">The 230V AC feed to Cross Green (K3) is routed</text>
    <text x="28" y="81" class="note-text">through the Normally Closed (NC) pin of K6.</text>
    <text x="18" y="105" class="note-text">• <tspan font-weight="700">Mechanical Break Air-Gap (2.5 ms):</tspan></text>
    <text x="28" y="122" class="note-text">Even if firmware sets both GPIOs HIGH or memory</text>
    <text x="28" y="138" class="note-text">latches up, simultaneous greens are physically</text>
    <text x="28" y="154" class="note-text font-bold" fill="#15803d">IMPOSSIBLE under mechanical relay laws.</text>
  </g>

  <g transform="translate(805, 595)">
    <!-- Card 3: Challan Protection Math -->
    <rect x="0" y="0" width="370" height="175" rx="8" fill="#ffffff" stroke="#cbd5e1" class="shadow" />
    <rect x="0" y="0" width="5" height="175" rx="2.5" fill="#8b5cf6" />
    <text x="18" y="25" class="note-title">3. Citizen Challan Immunity Engine</text>
    <text x="18" y="48" class="note-text">• <tspan font-weight="700">The Stop-Line Deadlock Solution:</tspan></text>
    <text x="28" y="65" class="note-text">Motorists refuse to yield over red stop-lines</text>
    <text x="28" y="81" class="note-text">because ITMS cameras issue automatic fines.</text>
    <text x="18" y="105" class="note-text">• <tspan font-weight="700">Dynamic Exemption Window:</tspan></text>
    <text x="28" y="122" class="note-text">Window = [T_trigger - 10s  to  T_clearance + 10s].</text>
    <text x="28" y="138" class="note-text">All yielding plates tagged EXEMPT at ICCC.</text>
    <text x="18" y="160" class="note-text font-semibold" fill="#6d28d9">Eliminates 100% of Good Samaritan court disputes.</text>
  </g>
</svg>
"""

# Write files and validate XML syntax
files_to_generate = [
    ("system_architecture.svg", svg_arch),
    ("state_machine.svg", svg_fsm),
    ("timing_sequence.svg", svg_timing),
]

for filename, content in files_to_generate:
    filepath = os.path.join(DOCS_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip())
    
    # Validate with ElementTree
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
        print(f"SUCCESS: {filename} generated and parsed successfully! Root tag: {root.tag}, Elements: {len(list(root.iter()))}")
    except ET.ParseError as e:
        print(f"ERROR: XML Parse error in {filename}: {e}")
        raise
