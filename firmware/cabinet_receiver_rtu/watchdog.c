/**
 * @file watchdog.c
 * @brief Multi-Tier Industrial Watchdog & Supervisory Implementation for Cabinet RTU
 * @target STM32F401RCT6 / STM32F411CEU6 Cortex-M4 @ 84-100 MHz
 * @supervisor Texas Instruments TPS3823-33DBVT (External SOT-23-5 Supervisor)
 * @standards IEC 61508 SIL-2 / MISRA C:2012 / NEMA TS-2 Cabinet Safety
 *
 * Safety-Critical Multi-Tier Watchdog Architecture:
 * --------------------------------------------------
 * 1. Tier 1: STM32 Independent Watchdog (IWDG)
 *    - Driven by autonomous 32 kHz Low-Speed Internal (LSI) RC oscillator.
 *    - Fully independent of main PLL and high-speed external crystal (HSE).
 *    - Timeout window: 500 ms. If main scheduler locks or clock fails, resets MCU.
 *
 * 2. Tier 2: STM32 Window Watchdog (WWDG)
 *    - Clocked from APB1 peripheral bus.
 *    - Enforces a precise refresh window (~50 ms).
 *    - Detects runaway execution where code refreshes too fast or skips checks.
 *
 * 3. Tier 3: External Hardware Supervisory IC (TI TPS3823-33DBVT)
 *    - Dedicated external watchdog chip directly monitoring microcontroller health.
 *    - Requires Watchdog Input (WDI) transition on STM32 pin PB12 every 1.6 seconds.
 *    - Directly pulls STM32 NRST line LOW for 200 ms if firmware locks up.
 *
 * 4. Hardware Relay De-Energization (Pull-Down Fail-Safe):
 *    - Each preemption relay driver gate (ULN2803A Darlington) is pulled to GND via 4.7 kΩ.
 *    - If MCU enters reset, loses VDD, or pins float into high-impedance tri-state,
 *      all override relay coils de-energize within 10 ms.
 *    - Contacts snap to Normally Closed (NC), returning full control to the native
 *      municipal Traffic Signal Controller (TSC) and Malfunction Management Unit (MMU).
 */

#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include "watchdog.h"

/* ========================================================================== */
/*                       HARDWARE REGISTER DEFINITIONS                        */
/* ========================================================================== */
/*
 * Register offsets for STM32F4 series (or mock harness when testing on host)
 */
#define IWDG_KEY_RELOAD         ((uint16_t)0xAAAA)
#define IWDG_KEY_ENABLE         ((uint16_t)0xCCCC)
#define IWDG_KEY_WRITE_ACCESS   ((uint16_t)0x5555)

#define IWDG_PRESCALER_64       ((uint8_t)0x04)
#define IWDG_RELOAD_500MS       ((uint16_t)250) /* (250 * 64) / 32000 Hz = 500 ms */

#define WWDG_WINDOW_VALUE       ((uint8_t)0x7F)
#define WWDG_COUNTER_INIT       ((uint8_t)0x7F)

#define PIN_EXTERNAL_WDI        (12)            /* PB12: External TPS3823 WDI strobe */

/* State variables */
static reset_reason_t g_last_reset = RESET_REASON_POWER_ON;
static uint32_t g_last_strobe_tick_ms = 0;
static bool g_wdi_pin_state = false;
static bool g_failsafe_latched = false;

/* ========================================================================== */
/*                       RESET REASON PARSING (RCC->CSR)                      */
/* ========================================================================== */
/**
 * @brief Inspect hardware Control/Status Register to identify reset cause.
 * In production: reads RCC->CSR flags (IWDGRSTF, WWDGRSTF, PINRSTF, PORRSTF).
 */
reset_reason_t watchdog_get_last_reset_reason(void)
{
    return g_last_reset;
}

/* ========================================================================== */
/*                       WATCHDOG INITIALIZATION                              */
/* ========================================================================== */
void watchdog_init(void)
{
    printf("[WATCHDOG] Initializing Multi-Tier Industrial Safety Supervisor...\n");

    /*
     * Tier 1: Configure STM32 IWDG
     * 1. Write 0x5555 to IWDG_KR to enable register access.
     * 2. Write Prescaler 64 to IWDG_PR (Clock = 32 kHz / 64 = 500 Hz).
     * 3. Write 250 to IWDG_RLR (Timeout = 250 / 500 Hz = 500 ms).
     * 4. Write 0xAAAA to reload counter.
     * 5. Write 0xCCCC to start watchdog. Once started, CANNOT be disabled by software.
     */
    printf("[WATCHDOG] Tier 1 (IWDG): 32 kHz LSI, Prescaler 64, Timeout = 500 ms (ACTIVE)\n");

    /*
     * Tier 2: Configure STM32 WWDG
     * 1. Enable WWDG peripheral clock on APB1.
     * 2. Set window value and counter reload.
     */
    printf("[WATCHDOG] Tier 2 (WWDG): APB1 Bus Window Supervisor, Window = ~50 ms (ACTIVE)\n");

    /*
     * Tier 3: Configure External Hardware Supervisor (TI TPS3823)
     * 1. Configure PB12 as Push-Pull High-Speed Output.
     * 2. Initial state: LOW. Requires transition within 1.6s.
     */
    g_wdi_pin_state = false;
    g_last_strobe_tick_ms = 0;
    g_failsafe_latched = false;
    printf("[WATCHDOG] Tier 3 (TPS3823): External HW IC on PB12, Timeout = 1600 ms (ACTIVE)\n");
    printf("[WATCHDOG] Failsafe: 4.7k Pull-downs de-energize relays within 10ms on reset.\n");
}

/* ========================================================================== */
/*                       EXTERNAL SUPERVISOR STROBE                           */
/* ========================================================================== */
/**
 * @brief Toggle external TPS3823 WDI pin (PB12).
 * Must be toggled at least once every 1.6 seconds to satisfy the supervisor.
 */
void watchdog_strobe_external(void)
{
    if (g_failsafe_latched) {
        /* Intentionally do NOT strobe if failsafe is latched; allow hardware reset */
        return;
    }

    g_wdi_pin_state = !g_wdi_pin_state;
    /*
     * In hardware:
     * HAL_GPIO_WritePin(GPIOB, GPIO_PIN_12, g_wdi_pin_state ? GPIO_PIN_SET : GPIO_PIN_RESET);
     */
}

/* ========================================================================== */
/*                       MULTI-TIER WATCHDOG REFRESH                          */
/* ========================================================================== */
/**
 * @brief Service all watchdog tiers during normal deterministic execution.
 */
void watchdog_refresh_all(void)
{
    if (g_failsafe_latched) {
        return; /* Lockout active: suppress refresh to let hardware reset fire */
    }

    /* 1. Refresh Tier 1 Internal IWDG */
    /* In hardware: IWDG->KR = IWDG_KEY_RELOAD; */

    /* 2. Refresh Tier 2 Internal WWDG */
    /* In hardware: WWDG->CR = WWDG_COUNTER_INIT | WWDG_CR_WDGA; */

    /* 3. Strobe Tier 3 External Supervisor */
    watchdog_strobe_external();
}

/* ========================================================================== */
/*                       FAIL-SAFE LOCKOUT TRIGGER                            */
/* ========================================================================== */
/**
 * @brief Trip the fail-safe interlock and cease watchdog refresh.
 * Starves the watchdogs to initiate a cold reboot while immediately
 * releasing all relay coils via hardware 4.7 kΩ pull-down resistors.
 */
void watchdog_trigger_failsafe_lockout(const char *reason)
{
    g_failsafe_latched = true;
    printf("\n[WATCHDOG FAILSAFE] *** TRIPPED *** Reason: %s\n", reason ? reason : "Unknown");
    printf("[WATCHDOG FAILSAFE] Disabling watchdog refresh to force cold supervisor reset.\n");
    printf("[WATCHDOG FAILSAFE] All override relays DROPPED to Normally Closed (NC).\n");
    printf("[WATCHDOG FAILSAFE] Traffic control immediately reverted to native cabinet MMU.\n");

    /*
     * In hardware:
     * 1. Immediately write 0x00 to Relay Output GPIO port (GPIOA / GPIOC).
     * 2. Wait for external TPS3823 (1.6s) or internal IWDG (500ms) to assert NRST.
     */
}
