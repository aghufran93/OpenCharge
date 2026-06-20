# OpenCharge Architecture

**Project:** OpenCharge
**Document:** System Architecture
**Version:** 1.0
**Status:** Active
**Author:** Ahmed Ghufran
**Role:** Founder & Lead System Architect
**License:** Apache License 2.0
**Repository:** https://github.com/aghufran93/OpenCharge
**Last Updated:** June 2026

---

# Purpose

This document defines the high-level architecture of the OpenCharge platform.

It serves as the primary technical reference for developers, contributors, and future maintainers by describing the system structure, module responsibilities, communication paths, and design principles.

The objective is to ensure that every component of OpenCharge is modular, testable, scalable, and independent.

---

# Design Principles

OpenCharge follows these engineering principles:

* Clean Architecture
* SOLID Principles
* Separation of Concerns
* Hardware Abstraction
* Modular Design
* Testability
* Documentation First
* Simulation Before Hardware

---

# System Overview

OpenCharge is composed of independent layers that communicate through well-defined interfaces.

```text
                 Desktop GUI
                      │
               Application Layer
                      │
                 Service Layer
                      │
                OpenCharge Core
                      │
      ┌───────────────┼────────────────┐
      │               │                │
 IEC 61851       OCPP Client      Simulator
      │               │                │
      └───────────────┼────────────────┘
                      │
        Hardware Abstraction Layer
                      │
       STM32 / Raspberry Pi Hardware
```

The **OpenCharge Core** contains all business logic and remains independent of hardware and user interface technologies.

---

# Software Layers

## Presentation Layer

Responsible for user interaction.

Components:

* PySide6 Desktop GUI
* Raspberry Pi Touchscreen HMI
* Future Web Interface

Responsibilities:

* Display charger status
* Display QR codes
* Configuration
* Event visualization
* User interaction

---

## Application Layer

Coordinates application workflows.

Responsibilities:

* Charging session management
* User commands
* Configuration
* Event routing

---

## Service Layer

Provides integrations.

Services include:

* OCPP Client
* UART Communication
* Meter Communication
* Configuration
* Logging
* Database

---

## Core Layer

The heart of OpenCharge.

Contains:

* Charger
* Connector
* Session
* Vehicle
* Meter
* State Machine
* Fault Manager
* Event Manager

The Core must not depend on:

* PySide6
* STM32
* Raspberry Pi
* Linux
* Windows

---

## Hardware Layer

Responsible for physical devices.

Examples:

* STM32 Firmware
* GPIO
* PWM
* UART
* Contactor
* Connector Lock
* LEDs
* Sensors

---

# Desktop Simulator

The simulator allows complete charger testing without hardware.

Virtual components:

* EV
* Connector
* Meter
* Contactor
* Lock
* Control Pilot
* Fault Injection

Purpose:

* Software development
* Debugging
* Unit testing
* Demonstrations

---

# Embedded Architecture

The STM32 firmware is responsible for real-time hardware control.

Responsibilities:

* IEC 61851 PWM generation
* ADC sampling
* GPIO control
* Contactor control
* Lock mechanism
* Temperature monitoring
* Safety monitoring

---

# Raspberry Pi Architecture

The Raspberry Pi acts as the Human Machine Interface (HMI).

Responsibilities:

* Touchscreen GUI
* QR Code generation
* RFID interaction
* Local configuration
* OCPP communication
* Firmware updates

---

# Communication

Supported interfaces include:

* UART
* USB
* Ethernet
* Wi-Fi
* MQTT (Future)

Supported protocols:

* IEC 61851
* OCPP 1.6J
* OCPP 2.0.1
* Modbus RTU
* CAN (Future)

---

# State Machine

The charger follows the lifecycle below:

```text
Boot
   │
Initializing
   │
Available
   │
Vehicle Connected
   │
Authorized
   │
Preparing
   │
Charging
   │
Suspended
   │
Finishing
   │
Available
```

All charging logic is implemented inside the Core.

---

# Repository Architecture

```text
desktop/
    app/
    core/
    gui/
    models/
    services/
    simulator/

firmware/
hardware/
docs/
examples/
```

---

# Future Expansion

The architecture is designed to support:

* Multiple connectors
* Dynamic Load Balancing
* Smart Charging
* ISO 15118
* Plug & Charge
* Cloud Services
* Mobile Applications
* Remote Diagnostics

without changing the Core architecture.

---

# Development Workflow

Every feature follows:

Requirement

↓

Architecture

↓

Implementation

↓

Unit Test

↓

Simulation

↓

Hardware Validation

↓

Release

---

# Architecture Goals

The OpenCharge architecture aims to achieve:

* High maintainability
* Low coupling
* High cohesion
* Platform independence
* Hardware independence
* Production readiness
* Long-term scalability

---

# Conclusion

OpenCharge is designed as a modular engineering platform rather than a single software application.

By separating business logic from hardware and user interfaces, the platform can evolve over many years while remaining maintainable, testable, and suitable for both educational and commercial applications.
