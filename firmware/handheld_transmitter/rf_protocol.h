/**
 * @file rf_protocol.h
 * @brief SynchroClear-ITS Sub-GHz Over-The-Air RF Wire Protocol Specification
 * @target Nordic nRF52840 / nRF5340 & Semtech SX1262 Transceiver
 * @standard India WPC GSR 564(E) 865-867 / 868 MHz License-Free SRD Band
 * @classification Safety-Critical Industrial Embedded Firmware
 *
 * Designed for Raipur Police Commissionerate Traffic Automation Pilot.
 * Guarantees cryptographic packet authenticity, rolling monotonic anti-replay
 * protection, and strict 37-byte deterministic wire framing.
 */

#ifndef RF_PROTOCOL_H
#define RF_PROTOCOL_H

#include <stdint.h>
#include <stdbool.h>
#include <string.h>

#ifdef __cplusplus
extern "C" {
#endif

/* ========================================================================== */
/*                           PROTOCOL CONSTANTS                               */
/* ========================================================================== */

/** @brief SynchroClear Magic Synchronization Word ('S' 'C' = 0x5343) */
#define RF_SYNC_WORD                    ((uint16_t)0x5343)

/** @brief Protocol Version (v1.0.0) */
#define RF_PROTOCOL_VERSION             ((uint8_t)0x01)

/** @brief Total packet frame length in bytes */
#define RF_PACKET_TOTAL_SIZE            (37)

/** @brief Plaintext header + payload size before cryptographic MAC tag */
#define RF_PAYLOAD_PLAIN_SIZE           (21)

/** @brief Cryptographic Authentication Tag size (AES-128-GCM or HMAC-SHA256) */
#define RF_MAC_TAG_SIZE                 (16)

/** @brief Maximum allowable timestamp drift in seconds (replay protection) */
#define RF_MAX_TIMESTAMP_DRIFT_SEC      (300)

/** @brief Maximum preemption duration allowed in a single burst (seconds) */
#define RF_MAX_PREEMPT_DURATION_SEC     (35)

/** @brief Default preemption duration granted per request (seconds) */
#define RF_DEFAULT_PREEMPT_DURATION_SEC (22)

/* ========================================================================== */
/*                     RF PHYSICAL LAYER PARAMETERS (INDIA)                   */
/* ========================================================================== */
/*
 * Indian Regulatory Compliance:
 * Wireless Planning & Coordination (WPC) Wing, Ministry of Communications,
 * Government of India Gazette Notification GSR 564(E) for Short Range Devices (SRD).
 * Bands: 865.0 - 867.0 MHz and 868.0 MHz.
 */
#define RF_FREQ_PRIMARY_HZ              (865500000UL)  /* 865.500 MHz */
#define RF_FREQ_SECONDARY_HZ            (866500000UL)  /* 866.500 MHz */
#define RF_FREQ_ALTERNATIVE_HZ          (868000000UL)  /* 868.000 MHz */

/* Semtech SX1262 LoRa Modulation Parameters */
#define LORA_SPREADING_FACTOR           (7)            /* SF7: High speed, low ToA */
#define LORA_BANDWIDTH_KHZ              (125)          /* 125 kHz BW */
#define LORA_CODING_RATE                (1)            /* 4/5 Coding Rate */
#define LORA_PREAMBLE_LENGTH            (8)            /* 8 Symbols */
#define LORA_TX_POWER_DEFAULT_DBM       (14)           /* +14 dBm (25 mW) default */
#define LORA_TX_POWER_MAX_DBM           (22)           /* +22 dBm (150 mW) boost */

/* Time-on-Air (ToA) for 37 bytes @ SF7/125kHz/CR 4/5 is approx 56.6 ms */
#define LORA_TIME_ON_AIR_MS             (57)

/* ========================================================================== */
/*                              MESSAGE TYPES                                 */
/* ========================================================================== */

typedef enum {
    /** @brief Preemption override trigger request from traffic officer */
    MSG_TYPE_PREEMPT_REQ                = 0x10,

    /** @brief Instant abort / early cancel request from officer or camera */
    MSG_TYPE_PREEMPT_CANCEL             = 0x11,

    /** @brief Periodic heartbeat and battery state telemetry */
    MSG_TYPE_STATUS_BEACON              = 0x20,

    /** @brief Cabinet RTU Acknowledgement receipt */
    MSG_TYPE_ACK                        = 0x30,

    /** @brief System diagnostic / alarm frame */
    MSG_TYPE_DIAGNOSTIC                 = 0x7F
} rf_message_type_t;

/* ========================================================================== */
/*                          APPROACH DIRECTION CODES                          */
/* ========================================================================== */

typedef enum {
    DIR_NONE                            = 0x00,
    DIR_NORTH                           = 0x01,  /**< Approach 1: Northbound corridor */
    DIR_EAST                            = 0x02,  /**< Approach 2: Eastbound corridor  */
    DIR_SOUTH                           = 0x03,  /**< Approach 3: Southbound corridor */
    DIR_WEST                            = 0x04   /**< Approach 4: Westbound corridor  */
} rf_direction_t;

/* ========================================================================== */
/*                    EMERGENCY VEHICLE CLASSIFICATION                        */
/* ========================================================================== */

typedef enum {
    VEH_CLASS_NONE                      = 0x00,
    VEH_CLASS_AMBULANCE                 = 0x10,  /**< Highest Priority: Medical Emergency */
    VEH_CLASS_FIRE_TRUCK                = 0x20,  /**< High Priority: Fire and Rescue     */
    VEH_CLASS_POLICE                    = 0x30,  /**< Tactical Priority: Law Enforcement */
    VEH_CLASS_VIP_CONVOY                = 0x40   /**< Protocol Preemption                */
} rf_vehicle_class_t;

/* ========================================================================== */
/*                      BATTERY CHEMISTRY CONSTANTS                           */
/* ========================================================================== */
/*
 * Industrial LiFePO4 (Lithium Iron Phosphate) Cell:
 * Standard 18650 format, 1600 mAh nominal capacity.
 * Temperature range: -20°C to +70°C.
 * Inherently thermally stable; will not undergo thermal runaway under +48°C Raipur heat.
 */
#define LIFEPO4_VOLTAGE_FULL_MV         (3650)  /* 3.65V Full Charge Termination */
#define LIFEPO4_VOLTAGE_NOMINAL_MV      (3200)  /* 3.20V Flat Discharge Plateau  */
#define LIFEPO4_VOLTAGE_LOW_WARN_MV     (2800)  /* 2.80V Low Battery Warning LED */
#define LIFEPO4_VOLTAGE_CUTOFF_MV       (2500)  /* 2.50V Hardware Shutdown Cutoff*/
#define LIFEPO4_TEMP_MIN_C              (-20)   /* Minimum operating temperature */
#define LIFEPO4_TEMP_MAX_C              (70)    /* Maximum operating temperature */

/* ========================================================================== */
/*                    37-BYTE WIRE PACKET SPECIFICATION                       */
/* ========================================================================== */
/*
 * Byte-level Framing Structure (Packed, Zero Padding):
 * +--------+--------+--------+--------+--------+--------+--------+--------+
 * | Byte 0 | Byte 1 | Byte 2 | Byte 3 | Byte 4 | Byte 5 | Byte 6 | Byte 7 |
 * +--------+--------+--------+--------+--------+--------+--------+--------+
 * |  0x53  |  0x43  |  0x01  |  TYPE  |         UNIT_ID (32-bit)       |
 * |  ('S') |  ('C') | (VER)  | (0x10) |        (Officer Badge UUID)    |
 * +--------+--------+--------+--------+--------+--------+--------+--------+
 *
 * +--------+--------+--------+--------+--------+--------+--------+--------+
 * | Byte 8 | Byte 9 | Byte 10| Byte 11| Byte 12| Byte 13| Byte 14| Byte 15|
 * +--------+--------+--------+--------+--------+--------+--------+--------+
 * |        JUNCTION_ID (32-bit)       | DIR_ID | VEH_CLS| SEQUENCE_CNTR  |
 * |      (0x00000000 = Broadcast)     | (0x01) | (0x10) |   (MSB..B2)    |
 * +--------+--------+--------+--------+--------+--------+--------+--------+
 *
 * +--------+--------+--------+--------+--------+--------+--------+--------+
 * | Byte 16| Byte 17| Byte 18| Byte 19| Byte 20| Byte 21 ...     Byte 36|
 * +--------+--------+--------+--------+--------+--------+--------+--------+
 * |  SEQUENCE_CNTR  | DURATION (sec)  | BATT % | AES-128-GCM / HMAC-256 |
 * |    (B1..LSB)    |    (uint16_t)   | (0-100)|   Auth Tag (16 Bytes)  |
 * +--------+--------+--------+--------+--------+--------+--------+--------+
 * Total Length: Exactly 37 Bytes.
 */

#pragma pack(push, 1)

typedef struct {
    /* --- Plaintext Header and Payload (21 Bytes) --- */
    uint16_t sync_word;         /**< [Bytes 0..1]  0x5343 ('SC') synchronization word    */
    uint8_t  protocol_ver;      /**< [Byte 2]      0x01 Protocol version                 */
    uint8_t  msg_type;          /**< [Byte 3]      Message type (rf_message_type_t)      */
    uint32_t unit_id;           /**< [Bytes 4..7]  Handheld transmitter badge UUID       */
    uint32_t junction_id;       /**< [Bytes 8..11] Target junction ID (0 = Broadcast)    */
    uint8_t  direction;         /**< [Byte 12]     Approach corridor (rf_direction_t)    */
    uint8_t  vehicle_class;     /**< [Byte 13]     Vehicle type (rf_vehicle_class_t)     */
    uint32_t sequence_counter;  /**< [Bytes 14..17] Monotonic rolling anti-replay counter */
    uint16_t duration_sec;      /**< [Bytes 18..19] Requested green dwell duration (sec)  */
    uint8_t  battery_pct;       /**< [Byte 20]     LiFePO4 State of Charge (0-100%)      */

    /* --- Cryptographic Integrity & Authenticity (16 Bytes) --- */
    uint8_t  mac_tag[RF_MAC_TAG_SIZE]; /**< [Bytes 21..36] AES-128-GCM tag or HMAC-SHA256 (16B) */
} rf_packet_t;

#pragma pack(pop)

/* Compile-time static assert to guarantee 37-byte exact packaging */
typedef char assert_rf_packet_size[(sizeof(rf_packet_t) == RF_PACKET_TOTAL_SIZE) ? 1 : -1];

/* ========================================================================== */
/*                       PROTOCOL HELPER FUNCTIONS                            */
/* ========================================================================== */

/**
 * @brief Initialize a preemption request packet with default parameters.
 * @param[out] pkt Pointer to the packet structure to populate.
 * @param[in] unit_id Unique serial identifier of the handheld transmitter.
 * @param[in] junction_id Target junction identifier (0 for omni/nearest).
 * @param[in] direction Requested green approach corridor (N/E/S/W).
 * @param[in] veh_class Type of emergency vehicle requesting preemption.
 * @param[in] seq Monotonic rolling anti-replay counter value.
 * @param[in] duration_sec Desired priority green duration in seconds.
 * @param[in] batt_pct LiFePO4 battery percentage (0-100).
 */
static inline void rf_packet_init(rf_packet_t *pkt,
                                  uint32_t unit_id,
                                  uint32_t junction_id,
                                  rf_direction_t direction,
                                  rf_vehicle_class_t veh_class,
                                  uint32_t seq,
                                  uint16_t duration_sec,
                                  uint8_t batt_pct)
{
    if (!pkt) return;
    memset(pkt, 0, sizeof(rf_packet_t));

    pkt->sync_word        = RF_SYNC_WORD;
    pkt->protocol_ver     = RF_PROTOCOL_VERSION;
    pkt->msg_type         = (uint8_t)MSG_TYPE_PREEMPT_REQ;
    pkt->unit_id          = unit_id;
    pkt->junction_id      = junction_id;
    pkt->direction        = (uint8_t)direction;
    pkt->vehicle_class    = (uint8_t)veh_class;
    pkt->sequence_counter = seq;
    pkt->duration_sec     = (duration_sec > RF_MAX_PREEMPT_DURATION_SEC) ?
                             RF_MAX_PREEMPT_DURATION_SEC : duration_sec;
    pkt->battery_pct      = (batt_pct > 100) ? 100 : batt_pct;
}

/**
 * @brief Validate incoming packet framing sanity checks (size, magic, version).
 * @param[in] pkt Pointer to received packet buffer.
 * @param[in] len Received buffer length.
 * @return true if framing passes sanity checks, false otherwise.
 */
static inline bool rf_packet_validate_framing(const rf_packet_t *pkt, size_t len)
{
    if (!pkt || len != RF_PACKET_TOTAL_SIZE) {
        return false;
    }
    if (pkt->sync_word != RF_SYNC_WORD) {
        return false;
    }
    if (pkt->protocol_ver != RF_PROTOCOL_VERSION) {
        return false;
    }
    if (pkt->msg_type == MSG_TYPE_PREEMPT_REQ) {
        if (pkt->direction < DIR_NORTH || pkt->direction > DIR_WEST) {
            return false;
        }
    } else {
        if (pkt->direction > DIR_WEST) {
            return false;
        }
    }
    return true;
}

/**
 * @brief Human-readable string for approach direction.
 */
static inline const char* rf_direction_str(rf_direction_t dir)
{
    switch (dir) {
        case DIR_NORTH: return "NORTH";
        case DIR_EAST:  return "EAST";
        case DIR_SOUTH: return "SOUTH";
        case DIR_WEST:  return "WEST";
        default:        return "UNKNOWN";
    }
}

/**
 * @brief Human-readable string for emergency vehicle class.
 */
static inline const char* rf_vehicle_class_str(rf_vehicle_class_t cls)
{
    switch (cls) {
        case VEH_CLASS_AMBULANCE:  return "AMBULANCE";
        case VEH_CLASS_FIRE_TRUCK: return "FIRE_TRUCK";
        case VEH_CLASS_POLICE:     return "POLICE";
        case VEH_CLASS_VIP_CONVOY: return "VIP_CONVOY";
        default:                   return "UNKNOWN";
    }
}

#ifdef __cplusplus
}
#endif

#endif /* RF_PROTOCOL_H */
