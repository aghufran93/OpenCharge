# OpenCharge Core Software Design Specification (SDS)

---

# Document Information

| Item              | Details                                       |
| ----------------- | --------------------------------------------- |
| **Project**       | OpenCharge                                    |
| **Document ID**   | OC-SDS-001                                    |
| **Document Name** | OpenCharge Core Software Design Specification |
| **Version**       | 1.0                                           |
| **Status**        | Draft                                         |
| **Author**        | Ahmed Ghufran                                 |
| **Role**          | Founder & Lead System Architect               |
| **License**       | Apache License 2.0                            |
| **Repository**    | https://github.com/aghufran93/OpenCharge      |
| **Created**       | June 2026                                     |
| **Last Updated**  | June 2026                                     |

---

# Revision History

| Version | Date      | Author        | Description   |
| ------- | --------- | ------------- | ------------- |
| 1.0     | June 2026 | Ahmed Ghufran | Initial Draft |

---

# 1. Purpose

This document defines the software design of the OpenCharge Core.

The OpenCharge Core contains all business logic and remains independent of:

* Desktop GUI
* Raspberry Pi HMI
* STM32 Firmware
* OCPP Client
* IEC 61851 Hardware
* Hardware Drivers

The objective is to provide a stable, maintainable, and testable foundation for the OpenCharge platform.

---

# 2. Design Principles

The OpenCharge Core follows:

* Clean Architecture
* SOLID Principles
* Separation of Concerns
* Dependency Injection
* Hardware Abstraction
* Event-Driven Architecture
* Test-Driven Development

---

# 3. Core Responsibilities

The OpenCharge Core is responsible for:

* Charger lifecycle management
* Connector management
* Charging session management
* State transitions
* Fault management
* Event publishing
* Meter data modelling
* Authorization modelling

The Core must never communicate directly with hardware.

---

# 4. Core Domain Model

```text
                           Charger
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
   StateMachine          Connector           ChargingSession
        │                     │                     │
        │                     │                Authorization
        │                     │                     │
        │                     │                 Vehicle
        │                     │                     │
        │                     │                  Meter
        │
        ▼
    EventBus
        │
        ▼
   FaultManager
```

Every object has a single responsibility.

---

# 5. Core Components

## 5.1 Charger

The Charger is the root aggregate of the OpenCharge Core.

### Responsibilities

* Own connectors
* Own state machine
* Manage charging sessions
* Publish events
* Coordinate authorization
* Coordinate meter updates
* Expose charger information

### Relationships

* Owns one or more Connectors
* Owns one StateMachine
* Owns one active ChargingSession per Connector

---

## 5.2 Connector

Represents one physical charging outlet.

### Responsibilities

* Plug detection
* Lock control
* Contactor control
* IEC 61851 state
* Connector availability

---

## 5.3 StateMachine

Controls every charger state transition.

The StateMachine validates transitions and guarantees that invalid charger behaviour cannot occur.

Example:

```text
OFFLINE

↓

BOOTING

↓

INITIALIZING

↓

AVAILABLE

↓

PREPARING

↓

CHARGING

↓

FINISHING

↓

AVAILABLE
```

---

## 5.4 ChargingSession

Represents one complete charging transaction.

This object must support:

* OCPP 1.6J
* OCPP 2.0.1
* RFID
* QR Code
* Plug & Charge (Future)
* Billing
* Reporting

### Proposed Attributes

* Session ID
* Connector ID
* Authorization ID
* User ID
* Vehicle ID
* Transaction ID
* Start Time
* Stop Time
* Duration
* Energy Delivered
* Tariff
* Cost
* Currency
* Stop Reason
* Session Status

---

## 5.5 Vehicle

Represents the connected electric vehicle.

### Proposed Attributes

* VIN
* Plug Status
* IEC 61851 State
* Requested Current
* Maximum Current
* Battery Capacity
* State of Charge (Future)

---

## 5.6 Meter

Represents electrical measurements.

### Proposed Attributes

* Voltage
* Current
* Power
* Energy
* Frequency
* Power Factor
* Temperature
* Timestamp

---

## 5.7 EventBus

Provides communication between software modules.

Example events:

* Vehicle Connected
* Vehicle Disconnected
* Charging Started
* Charging Stopped
* Fault Raised
* Fault Cleared
* RFID Authorized
* Meter Updated
* OCPP Connected

The EventBus removes direct dependencies between modules.

---

## 5.8 FaultManager

Responsible for tracking charger faults.

Each fault contains:

* Fault Code
* Severity
* Source
* Timestamp
* Recovery Status
* Acknowledgement Status

---

# 6. Design Rules

The Core:

* Must not depend on GUI frameworks.
* Must not depend on hardware drivers.
* Must not depend on OCPP libraries.
* Must not depend on STM32 firmware.

External systems depend on the Core—not the other way around.

---

# 7. External Interfaces

The Core exposes interfaces to:

* Desktop Simulator
* IEC 61851 Controller
* OCPP Client
* Raspberry Pi HMI
* STM32 Firmware
* Future REST API

Each interface communicates only through well-defined methods and events.

---

# 8. Future Expansion

The design supports future features without major architectural changes.

Planned capabilities include:

* Multi-connector chargers
* Dynamic Load Balancing
* Smart Charging
* OCPP 2.0.1
* ISO 15118
* Plug & Charge
* Local Authorization
* Remote Diagnostics
* Mobile Applications

---

# 9. Design Goals

The OpenCharge Core is designed to be:

* Modular
* Testable
* Hardware Independent
* Protocol Independent
* Scalable
* Commercial Grade
* Maintainable
* Extensible

---

# 10. Next Implementation Order

The implementation will proceed as follows:

1. Global Enumerations
2. Finite State Machine
3. Connector
4. Charger
5. Charging Session
6. Vehicle
7. Meter
8. Event Bus
9. Fault Manager
10. Unit Tests
11. Desktop Simulator Integration

Each component will be fully documented, implemented, and tested before progressing to the next.
