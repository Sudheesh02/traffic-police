/**
 * @file state_machine.h
 * @brief SynchroClear-ITS Deterministic Inter-Green Safety State Machine
 * @target STM32F401 / STM32F411 Industrial Microcontroller (-40°C to +85°C)
 * @standard IRC SP:72 & MoRTH Traffic Signal Codes / NEMA TS-2 Collision Standards
 * @classification Safety-Critical Municipal Traffic Preemption Logic
 *
 * Enforces strictly deterministic, collision-free inter-green transitions:
 *  Normal Cycle -> Preempt Trigger -> 3.5s Amber -> 2.0s All-Red Clearance
 *  -> 22.0s Priority Green -> 3.5s Recovery Amber -> 1.5s All-Red -> Normal Cycle.
 *
 * Implements 5 Hard Safety Invariants:
 *  1. No Instantaneous Red (Minimum 3.5s deceleration amber)
 *  2. Mandatory Inter-Green Clearance (2.0s all-red box evacuation)
 *  3. Absolute Phase Exclusivity (Physical & logical zero dual-green guarantee)
 *  4. Non-Resettable Preemption Guard Ceiling (Strict 35.0s maximum hold)
 *  5. Cabinet Fault Fallback (Instant coil drop to autonomous TSC / CMU control)
 */

#ifndef STATE_MACHINE_H
#define STATE_MACHINE_H

#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/* ========================================================================== */
/*                       DETERMINISTIC TIMING CONSTANTS                       */
/* ========================================================================== */
/*
 * Indian Road Congress (IRC SP:72) & Ministry of Road Transport and Highways:
 * Recommended minimum clearance times for urban intersection approach speeds (40-50 km/h).
 */

/** @brief Active green deceleration interval (3.5 seconds) */
#define TIMING_AMBER_CLEARANCE_MS           (3500U)

/** @brief Mandatory all-red intersection evacuation buffer (2.0 seconds) */
#define TIMING_ALL_RED_CLEARANCE_MS         (2000U)

/** @brief Default emergency vehicle priority green hold duration (22.0 seconds) */
#define TIMING_PRIORITY_GREEN_DEFAULT_MS    (22000U)

/** @brief Maximum priority green hold ceiling (35.0 seconds hard ceiling) */
#define TIMING_GUARD_MAX_PREEMPT_MS         (35000U)

/** @brief Priority green termination amber interval (3.5 seconds) */
#define TIMING_RECOVERY_AMBER_MS            (3500U)

/** @brief Final all-red buffer before restoring normal traffic flow (1.5 seconds) */
#define TIMING_RECOVERY_ALL_RED_MS          (1500U)

/** @brief Minimum green dwell before an active phase can be preempted (5.0 seconds) */
#define TIMING_MIN_GREEN_DWELL_MS           (5000U)

/* ========================================================================== */
/*                         STATE MACHINE STATE ENUM                           */
/* ========================================================================== */

typedef enum {
    /**
     * @brief Normal Round-Robin Cycle.
     * RTU override relays remain DE-ENERGIZED (Normally Closed).
     * Municipal Traffic Signal Controller (TSC) cycles phases autonomously.
     */
    STATE_NORMAL_CYCLE = 0,

    /**
     * @brief Amber Deceleration Clearance Phase.
     * Target preemption received. Active phase green is dropped to Amber.
     * Enforces safe stopping distance for motorists (3.5 seconds).
     * Prevents rear-end pileups and sudden red shockwaves.
     */
    STATE_AMBER_CLEARANCE = 1,

    /**
     * @brief Inter-Green All-Red Intersection Evacuation.
     * All signal aspects across ALL approaches are illuminated RED (2.0 seconds).
     * Intersection box is completely evacuated of straggler vehicles.
     * Zero-collision interlock window prior to emergency green illumination.
     */
    STATE_ALL_RED_CLEARANCE = 2,

    /**
     * @brief Priority Emergency Green Phase.
     * Selected approach (e.g. North) is illuminated GREEN for 22.0 seconds.
     * All conflicting approaches (East, South, West) are mechanically locked RED.
     */
    STATE_PRIORITY_GREEN = 3,

    /**
     * @brief Recovery Amber Phase.
     * Emergency vehicle has cleared intersection (or timer / abort triggered).
     * Priority corridor transitions to Amber for 3.5 seconds.
     */
    STATE_RECOVERY_AMBER = 4,

    /**
     * @brief Recovery All-Red Phase.
     * All approaches held RED for 1.5 seconds to settle intersection flow.
     */
    STATE_RECOVERY_ALL_RED = 5,

    /**
     * @brief Failsafe Alarm / Fallback Mode.
     * All override relays de-energized via hardware pull-downs.
     * Cabinet MMU / TSC takes total control; flashing amber warning enabled.
     */
    STATE_FAILSAFE_FALLBACK = 6
} traffic_state_t;

/* ========================================================================== */
/*                             EVENT DEFINITIONS                              */
/* ========================================================================== */

typedef enum {
    EVT_NONE = 0,

    /** @brief Validated, cryptographically signed preemption packet received */
    EVT_PREEMPT_TRIGGER = 1,

    /** @brief Early cancel request from officer button or AI queue dissipation */
    EVT_EARLY_CANCEL = 2,

    /** @brief Phase dwell duration timer has elapsed */
    EVT_TIMER_EXPIRED = 3,

    /** @brief Preemption guard ceiling (35.0s) has elapsed */
    EVT_GUARD_TIMER_EXPIRED = 4,

    /** @brief Hardware fault, relay feedback mismatch, or watchdog warning */
    EVT_HARDWARE_FAULT = 5
} traffic_event_t;

/* ========================================================================== */
/*                     APPROACH DIRECTION BITMASK MASKS                       */
/* ========================================================================== */

#define APPROACH_MASK_NONE      (0x00U)
#define APPROACH_MASK_NORTH     (0x01U)  /* Bit 0: North Approach Green */
#define APPROACH_MASK_EAST      (0x02U)  /* Bit 1: East Approach Green  */
#define APPROACH_MASK_SOUTH     (0x04U)  /* Bit 2: South Approach Green */
#define APPROACH_MASK_WEST      (0x08U)  /* Bit 3: West Approach Green  */

/* ========================================================================== */
/*                     STATE MACHINE CONTEXT STRUCTURE                        */
/* ========================================================================== */

typedef struct {
    traffic_state_t current_state;          /**< Active operating state       */
    traffic_state_t previous_state;         /**< State prior to last transition */
    uint32_t        state_entry_time_ms;    /**< Millisecond tick at state entry*/
    uint32_t        state_dwell_target_ms;  /**< Required dwell time in ms    */
    uint32_t        guard_timer_start_ms;   /**< Preemption ceiling start tick*/
    uint8_t         target_approach;        /**< 1=North, 2=East, 3=South, 4=West */
    uint8_t         interrupted_phase;      /**< Native phase active before preempt */
    uint8_t         active_relay_mask;      /**< Bitmask of currently active coils */
    uint32_t        last_sequence_counter;  /**< Highest verified replay counter */
    bool            preemption_active;      /**< Flag indicating override mode */
    uint32_t        total_preemptions;      /**< Lifetime preemptions serviced */
    uint32_t        fault_count;            /**< Anomalies or contact faults   */
} traffic_state_machine_t;

/* ========================================================================== */
/*                       FUNCTION DECLARATIONS                                */
/* ========================================================================== */

/**
 * @brief Initialize the traffic signal state machine into autonomous normal cycle.
 * @param[out] sm Pointer to state machine context structure.
 */
void state_machine_init(traffic_state_machine_t *sm);

/**
 * @brief Periodic millisecond tick handler. Evaluates state timers and guards.
 * @param[in,out] sm State machine context.
 * @param[in] current_tick_ms System millisecond counter (e.g. HAL_GetTick()).
 */
void state_machine_update_tick(traffic_state_machine_t *sm, uint32_t current_tick_ms);

/**
 * @brief Inject an event (preemption trigger, cancel, timer expiry, or fault).
 * @param[in,out] sm State machine context.
 * @param[in] evt Event to process.
 * @param[in] approach Target approach corridor (for preemption triggers).
 * @param[in] current_tick_ms Current timestamp in milliseconds.
 * @return true if state transition occurred, false if rejected or deferred.
 */
bool state_machine_process_event(traffic_state_machine_t *sm,
                                 traffic_event_t evt,
                                 uint8_t approach,
                                 uint32_t current_tick_ms);

/**
 * @brief Verify that safety invariants are intact (NO simultaneous greens).
 * @param[in] sm State machine context.
 * @return true if all safety invariants are strictly satisfied, false on violation.
 */
bool state_machine_verify_invariants(const traffic_state_machine_t *sm);

/**
 * @brief Return string representation of a state for logging and telemetry.
 */
const char* state_machine_state_str(traffic_state_t state);

#ifdef __cplusplus
}
#endif

#endif /* STATE_MACHINE_H */
