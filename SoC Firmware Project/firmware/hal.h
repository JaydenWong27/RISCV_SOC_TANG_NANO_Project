#pragma once

#include <stdint.h>

// UART
#define UART_TX_DATA  (*(volatile uint32_t *)0x10000000)
#define UART_TX_BUSY  (*(volatile uint32_t *)0x10000004)

// GPIO
#define GPIO_OUT (*(volatile uint32_t *)0x10001000)
#define GPIO_DIR (*(volatile uint32_t *)0x10001004)
#define GPIO_IN (*(volatile uint32_t *)0x10001008)

// PWM
#define PWM_PERIOD (*(volatile uint32_t *)0x10002000)
#define PWM_COMPARE (*(volatile uint32_t *)0x10002004)
#define PWM_ENABLE (*(volatile uint32_t *)0x10002008)

// TIMER
#define TIMER_CONTROL (*(volatile uint32_t *)0x10003000)
#define TIMER_LIMIT (*(volatile uint32_t *)0x10003004)
#define TIMER_VALUE (*(volatile uint32_t *)0x10003008)
#define TIMER_STATUS (*(volatile uint32_t *)0x1000300C) 