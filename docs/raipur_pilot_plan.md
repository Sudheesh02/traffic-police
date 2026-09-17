# SynchroClear-ITS: Raipur Municipal Pilot Deployment Plan
## 7-Day Operational Blueprint for Jaistambh Chowk & Ghadi Chowk Corridors

- **Target Agency**: Raipur Police Commissionerate Traffic Branch & Raipur Smart City Limited (RSCL)
- **Document ID**: `DOC-PLN-RPR-PILOT-V1.0`
- **Junction 1**: Jaistambh Chowk (`LOCAL_JUNCTION_ID = 0x00040001` / `RPR_JAISTAMBH_01`)
- **Junction 2**: Ghadi Chowk (`LOCAL_JUNCTION_ID = 0x00040002` / `RPR_GHADI_CHOWK_02`)
- **Primary Corridor**: Great Eastern (GE) Road arterial route to Dr. BR Ambedkar Memorial Hospital (Mekahara)
- **Pilot Hardware Allocation**: 2x Cabinet RTUs + 2x Handheld Remotes = ₹19,960 INR (₹9,980/junction)
- **Deployment Budget**: Strictly under the ₹24,000 INR pilot expenditure ceiling

---

## 1. Executive Summary & Site Profiles

The 7-day pilot validates SynchroClear-ITS along Raipur's critical medical emergency transit spine.

```
[Jaistambh Chowk] ═══════ Great Eastern (GE) Road (1.4 km) ═══════► [Ghadi Chowk] ──► [Mekahara Hospital]
 (Junction #1)                                                       (Junction #2)      (Dr. BR Ambedkar)
  4-Way High Comm.                                                    Admin Hub          Emergency Trauma
  Heavy Commercial                                                    Civil Lines        Regional Center
```

### 1.1 Junction 1: Jaistambh Chowk (`0x00040001`)
- **Type**: 4-Leg Major Commercial Intersection (North: Station Road, South: GE Road / Sharda Chowk, East: Telibandha, West: Kotwali).
- **Existing Infrastructure**: UTC/NEMA-style 24VDC controller cabinet, 4-phase cyclic signal heads, 1080p RSCL ITMS ANPR camera mounted on gantry.
- **Traffic Profile**: 48,000 PCU/day; acute congestion during 09:30-11:30 and 18:00-20:30 peak hours.
- **Emergency Priority**: Northbound ambulances from Pandri / GE Road toward Mekahara Hospital.

### 1.2 Junction 2: Ghadi Chowk (`0x00040002`)
- **Type**: High-visibility administrative junction connecting Raj Bhavan, High Court links, and Civil Lines.
- **Existing Infrastructure**: Inductive loop detector rack, 230VAC signal heads with 24V solid-state relays.
- **Emergency Priority**: Eastbound fire and rescue vehicles from Central Fire Station; Southbound trauma transports.

---

## 2. Day-by-Day Deployment Timeline

```
Day 1: Cabinet RTU Mechanical & Electrical Retrofit (Jaistambh Chowk)
├── 09:00 - 10:30: Cabinet survey, 24VDC auxiliary bus voltage verification, DIN-rail mounting
├── 10:30 - 11:30: Wiring Form-C relay harness into controller preemption pins (Zero downtime)
└── 11:30 - 12:30: Antenna gantry installation (868 MHz fiberglass omni, low-loss RG58 cable)

Day 2: Cabinet RTU Installation (Ghadi Chowk)
├── 09:00 - 11:00: Ghadi Chowk RTU installation and Omron auxiliary contact sense verification
└── 11:00 - 13:00: RF link margin test (+14 dB link budget verified across 850m urban corridor)

Day 3: Camera RTSP Integration & Edge Inference Setup
├── 10:00 - 12:00: Tapping existing Smart City RTSP 1080p stream into edge inference box
├── 12:00 - 14:00: YOLOv8 emergency vehicle candidate detection tuning on live traffic
└── 14:00 - 16:00: 1.0 - 2.5 Hz optical strobe FFT frequency verification against Raipur daylight glare

Day 4: ANPR Plate Extraction & MQTT Gateway Commissioning
├── 09:30 - 12:00: ANPR OCR calibration on CG04 (Raipur RTO) and BH series plates
├── 12:00 - 14:00: MQTT broker setup (`rpr_traffic/corridors/preemption_events`) on ICCC network
└── 14:00 - 17:00: Cryptographic SHA-256 audit log validation (`preemption_audit.jsonl`)

Day 5: Controlled Inter-Green Timing & Safety Audit (Off-Peak Hours: 03:00 - 05:00 AM)
├── 03:00 - 03:45: Off-peak live trial with dedicated 108 Emergency Service ambulance
├── 03:45 - 04:30: Oscilloscope & signal head verification: 3.5s Amber + 2.0s All-Red guaranteed
└── 04:30 - 05:00: Intentional dual-green fault injection: zero dual-green interlock verified

Day 6: Traffic Police Constable Field Training
├── 10:00 - 12:00: Practical orientation for 12 traffic constables across Jaistambh & Ghadi Chowk
├── 12:00 - 14:00: Handheld wand operation: 4-quadrant approach selection, 25ms debounce, cancel toggle
└── 14:00 - 17:00: Supervised live daytime trial with non-emergency police convoy

Day 7: Full System Operational Handover & Evaluation
├── 08:00 - 20:00: Continuous 12-hour operational trial with live telemetry push to Raipur ICCC
├── 20:00 - 21:30: Data review: emergency corridor transit time, e-challan whitelisting accuracy
└── 21:30: Official sign-off and delivery of pilot validation report to Traffic Commissionerate
```

---

## 3. Measurable Key Performance Indicators (KPIs)

| KPI Metric | Target Baseline | SynchroClear Target | Verification Method |
| :--- | :---: | :---: | :--- |
| **Ambulance Transit Delay** | 68s per junction | **< 12s per junction** | GPS time-logger on 108 ambulance |
| **Inter-Green Safety Clearance** | 100% compliant | **Strict 5.5s (3.5s Y + 2.0s AR)** | Logic analyzer on relay driver lines |
| **Dual-Green Conflict Prevention** | 0 occurrences | **0% probability (Form-C lock)** | Auxiliary contact feedback sensor PC0-PC3 |
| **False e-Challans for Yielders** | 100% avoided | **0 false challans issued** | ICCC whitelist window reconciliation |
| **RF Preemption Packet Latency** | < 100 ms | **< 42 ms over-the-air** | SX1262 DIO1 timestamp logging |
| **Emergency Strobe Verification** | > 95% accuracy | **> 96.4% precision (1.0-2.5 Hz)** | FFT peak detector on rooftop ROI |

---

## 4. Emergency Contacts & Stakeholder Matrix

- **Raipur Police Commissionerate (Traffic Division)**: Dy. Commissioner of Police (Traffic), Raipur
- **Smart City ICCC Support**: Senior Systems Engineer, Raipur Smart City Limited (RSCL)
- **Medical Emergency Liaison**: Transport Coordinator, Dr. BR Ambedkar Memorial Hospital (Mekahara)
- **Fire & Rescue Liaison**: Divisional Fire Officer, Raipur Central Fire Station
