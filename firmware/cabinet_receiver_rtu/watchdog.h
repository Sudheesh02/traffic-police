/**
 * @file watchdog.h
 * @brief Multi-Tier Watchdog & Supervisory System Interface for STM32F4 Cabinet RTU
 * @target STM32F401RCT6 / STM32F411CEU6 Industrial MCU (-40°C to +85°C)
 * @supervisor Texas Instruments TPS3823-33DBVT (1.6s Hardware Supervisor)
 */

#ifndef WATCHDOG_H
#define WATCHDOG_H

#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef enum {
    RESET_REASON_UNKNOWN        = 0,
    RESET_REASON_POWER_ON       = 1,  /**< Cold power-on reset (POR/PDR) */
    RESET_REASON_PIN_RESET      = 2,  /**< External NRST pin pulled (TPS3823 or manual) */
    RESET_REASON_IWDG_TIMEOUT   = 3,  /**< Internal Independent Watchdog starvation */
    RESET_REASON_WWDG_TIMEOUT   = 4,  /**< Internal Window Watchdog violation */
    RESET_REASON_SOFTWARE       = 5,  /**< Software requested reset (NVIC_SystemReset) */
    RESET_REASON_BROWNOUT       = 6   /**< Brownout detection (BOR) */
} reset_reason_t;

/**
 * @brief Initialize all three tiers of watchdog supervision.
 * Tier 1: STM32 IWDG (~500 ms timeout, 32 kHz LSI clock)
 * Tier 2: STM32 WWDG (~50 ms window, APB1 clock)
 * Tier 3: External TI TPS3823-33 Hardware Supervisor (1.6s WDI strobe)
 */
void watchdog_init(void);

/**
 * @brief Service Tier 1 (IWDG), Tier 2 (WWDG), and Tier 3 (TPS3823) watchdogs.
 * Must be invoked from main supervisory thread within the allowable window.
 */
void watchdog_refresh_all(void);

/**
 * @brief Strobe the external TPS3823 supervisor WDI pin (PB12).
 */
void watchdog_strobe_external(void);

/**
 * @brief Read and clear the hardware reset reason flags from RCC->CSR.
 */
reset_reason_t watchdog_get_last_reset_reason(void);

/**
 * @brief Force immediate hardware shutdown and fail-safe relay drop.
 */
void watchdog_trigger_failsafe_lockout(const char *reason);

#ifdef __cplusplus
}
#endif

#endif /* WATCHDOG_H */
