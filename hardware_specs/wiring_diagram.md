# SynchroClear-ITS: Cabinet Terminal Block & Relay Interlock Wiring Diagram
## Standard Industrial UTC / NEMA TS-2 Cabinet Retrofit Specification

- **Project**: SynchroClear-ITS (Raipur Police Commissionerate Traffic Automation Pilot)
- **Document ID**: `HW-SPEC-WIRE-M3-V1.0`
- **Controller Interface**: Standard 24V DC Preemption Terminals / Conflict Monitor Unit (CMU)
- **Terminal Standard**: DIN-Rail Push-in Cage Clamp (WAGO 221-415 / Phoenix UK3N)
- **Wire Specification**: 0.75 mm² to 1.5 mm² stranded copper with crimped insulated bootlace ferrules

---

## 1. Schematic Architecture & Relay Interlock Topology

The Cabinet RTU utilizes **Omron G2R-1-SND-DC24(S)** industrial Form-C relays with mechanical Break-Before-Make contacts and optocoupled auxiliary sensing.

```
                                  24V DC Preemption Power Bus
                                              │
               ┌──────────────────────────────┼──────────────────────────────┐
               │                              │                              │
        Relay 1 (North)                Relay 2 (East)                 Relay 3 (South)
        [Coil: PA0 Sink]               [Coil: PA1 Sink]               [Coil: PA2 Sink]
               │                              │                              │
    ┌──────────┴──────────┐        ┌──────────┴──────────┐        ┌──────────┴──────────┐
    │ NC: Series Lockout  │        │ NC: Series Lockout  │        │ NC: Series Lockout  │
    │ to East/South/West  │        │ to North/South/West │        │ to North/East/West  │
    │ NO: North Green     │        │ NO: East Green      │        │ NO: South Green     │
    └──────────┬──────────┘        └──────────┬──────────┘        └──────────┬──────────┘
               │                              │                              │
               ▼                              ▼                              ▼
      [Traffic Controller:          [Traffic Controller:          [Traffic Controller:
       Preempt Input 1]              Preempt Input 2]              Preempt Input 3]
```

### Fail-Safe Coil Drop Guarantee
Each relay gate driver (ULN2803A Darlington sink) is pulled down to GND via an external **4.7 kΩ 1% metal-film resistor**.
If the STM32 microcontroller experiences a hardware reset, loss of VDD, brownout, or high-impedance pin float:
- All relay coils de-energize within **< 10 ms**.
- Spring-return mechanical armatures instantly snap to Normally Closed (NC) contacts.
- Preemption control drops entirely, returning 100% control to the native municipal Traffic Signal Controller (TSC) and Malfunction Management Unit (MMU).

---

## 2. Terminal Block Wiring Mapping Table

| Terminal ID | Signal Name | Source / Destination | Function & Wire Color | Industrial Rating |
| :---: | :--- | :--- | :--- | :--- |
| **TB1-1** | 24V_DC_IN (+) | Cabinet 24V Service Bus | RTU System Power (Red) | 24V DC ± 10%, 15W |
| **TB1-2** | 24V_DC_GND (-) | Cabinet Common Ground | Power Return (Black) | 0V Common |
| **TB1-3** | EARTH_GND | Cabinet PE Ground Stud | Enclosure & Surge Ground (Green/Yellow) | Low Impedance (< 5 Ω) |
| **TB2-1** | RELAY1_NO | TSC Preempt Ch 1 (North) | Approach 1 Active Green Trigger (Blue) | 250V AC / 10A Form-C |
| **TB2-2** | RELAY1_COM | Isolated 24V Excitation | Preemption Bus Feed (Orange) | 24V DC / 1A fused |
| **TB2-3** | RELAY2_NO | TSC Preempt Ch 2 (East) | Approach 2 Active Green Trigger (Blue) | 250V AC / 10A Form-C |
| **TB2-4** | RELAY2_COM | Isolated 24V Excitation | Preemption Bus Feed (Orange) | 24V DC / 1A fused |
| **TB2-5** | RELAY3_NO | TSC Preempt Ch 3 (South) | Approach 3 Active Green Trigger (Blue) | 250V AC / 10A Form-C |
| **TB2-6** | RELAY3_COM | Isolated 24V Excitation | Preemption Bus Feed (Orange) | 24V DC / 1A fused |
| **TB2-7** | RELAY4_NO | TSC Preempt Ch 4 (West) | Approach 4 Active Green Trigger (Blue) | 250V AC / 10A Form-C |
| **TB2-8** | RELAY4_COM | Isolated 24V Excitation | Preemption Bus Feed (Orange) | 24V DC / 1A fused |
| **TB3-1** | SENSE_PC0 | Relay 1 Auxiliary Contact | Optoisolated Contact Closure Verify (Violet) | 5,000 Vrms Isolation |
| **TB3-2** | SENSE_PC1 | Relay 2 Auxiliary Contact | Optoisolated Contact Closure Verify (Violet) | 5,000 Vrms Isolation |
| **TB3-3** | SENSE_PC2 | Relay 3 Auxiliary Contact | Optoisolated Contact Closure Verify (Violet) | 5,000 Vrms Isolation |
| **TB3-4** | SENSE_PC3 | Relay 4 Auxiliary Contact | Optoisolated Contact Closure Verify (Violet) | 5,000 Vrms Isolation |
| **TB4-1** | RS485_A (D+) | RSCL Edge IPC / Camera | Telemetry & Audit Stream (White/Blue) | TIA/EIA-485-A Diff |
| **TB4-2** | RS485_B (D-) | RSCL Edge IPC / Camera | Telemetry & Audit Stream (Blue) | TIA/EIA-485-A Diff |
| **TB4-3** | ISO_GND | Edge Unit Ground | Optoisolated RS-485 Shield (Gray) | Isolated Signal Ground |

---

## 3. Microcontroller Pinout & Watchdog Hardware Connections

```
STM32F401 / STM32F411 MCU (48-Pin LQFP):
├── PA0 ──────► ULN2803A Pin 1 ──► Omron Relay 1 Coil (North Green)
├── PA1 ──────► ULN2803A Pin 2 ──► Omron Relay 2 Coil (East Green)
├── PA2 ──────► ULN2803A Pin 3 ──► Omron Relay 3 Coil (South Green)
├── PA3 ──────► ULN2803A Pin 4 ──► Omron Relay 4 Coil (West Green)
│
├── PC0 ◄────── TLP281-4 Ch 1 ◄── Relay 1 Aux Contact Sense
├── PC1 ◄────── TLP281-4 Ch 2 ◄── Relay 2 Aux Contact Sense
├── PC2 ◄────── TLP281-4 Ch 3 ◄── Relay 3 Aux Contact Sense
├── PC3 ◄────── TLP281-4 Ch 4 ◄── Relay 4 Aux Contact Sense
│
├── PB12 ─────► TI TPS3823 WDI Pin (1.6s Periodic Supervisor Strobe)
├── NRST ◄───── TI TPS3823 RESET Pin (Open-Drain Hardware MCU Reset)
│
├── PA9  ──────► MAX13487 DI (RS-485 TX to Edge AI IPC)
├── PA10 ◄───── MAX13487 RO (RS-485 RX from Edge AI IPC)
│
└── SPI1 (PA5/6/7) ──► Semtech SX1262 Sub-GHz Transceiver (868 MHz)
```

---

## 4. Mechanical Installation & Enclosure Footprint

1. **Mounting Location**: Standard 35 mm symmetrical DIN rail (`EN 50022`), installed horizontally on the cabinet lower equipment shelf adjacent to the detector input rack.
2. **Clearance Requirements**: Maintain minimum 50 mm clearance above and below terminal blocks for wire routing and convection ventilation.
3. **RF Antenna Lead**: RG58 50 Ω coaxial cable routed through cabinet bottom environmental cable gland up to overhead mast-arm or gantry, terminating at 5 dBi fiberglass omnidirectional antenna.
4. **Surge Protection**: Bourns SMBJ24CA transient voltage suppressor installed across TB1-1 and TB1-2; SM712 TVS array installed across TB4-1 and TB4-2.
