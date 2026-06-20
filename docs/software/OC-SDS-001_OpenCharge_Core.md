# OpenCharge Core Software Design Specification (SDS)

---

# Document Information

| Item | Details |
|------|---------|
| **Project** | OpenCharge |
| **Document ID** | OC-SDS-001 |
| **Document Name** | OpenCharge Core Software Design Specification |
| **Version** | 1.0 |
| **Status** | Draft |
| **Author** | Ahmed Ghufran |
| **Role** | Founder & Lead System Architect |
| **License** | Apache License 2.0 |
| **Repository** | https://github.com/aghufran93/OpenCharge |
| **Created** | June 2026 |
| **Last Updated** | June 2026 |

---

# Revision History

| Version | Date | Author | Description |
|----------|------|--------|-------------|
| 1.0 | June 2026 | Ahmed Ghufran | Initial Design Specification |

---

# Table of Contents

1. Purpose
2. Scope
3. References
4. Definitions & Acronyms
5. Design Principles
6. System Context
7. Architectural Layers
8. Core Responsibilities
9. Core Domain Model
10. Component Relationships
11. State Model
12. Event Architecture
13. Fault Architecture
14. Smart Charging Architecture
15. Dynamic Load Balancing
16. Power Management
17. External Interfaces
18. Design Constraints
19. Non-Functional Requirements
20. Future Expansion
21. Implementation Roadmap
22. Traceability Matrix

---

# 1. Purpose

This Software Design Specification (SDS) defines the architecture, responsibilities, interfaces, and behaviour of the OpenCharge Core.

The OpenCharge Core is the central software component responsible for managing all business logic of an AC EV Charger while remaining independent from hardware, communication protocols, and user interfaces.

This document serves as the master design reference for all software implementation activities within the OpenCharge project.

---

# 2. Scope

The OpenCharge Core includes:

- Charger Management
- Connector Management
- Charging Sessions
- State Machine
- Event Management
- Fault Management
- Vehicle Model
- Meter Model
- Authorization Model
- Smart Charging
- Dynamic Load Balancing
- Power Management

The Core intentionally excludes:

- Desktop GUI
- Raspberry Pi HMI
- STM32 Firmware
- IEC 61851 Hardware Control
- OCPP Protocol
- Modbus Drivers
- GPIO Drivers
- UART Drivers
- CAN Drivers

These systems interact with the Core through well-defined interfaces.

---

# 3. References

The OpenCharge Core is designed in accordance with the following standards and specifications.

## International Standards

- IEC 61851 Electric Vehicle Conductive Charging System
- IEC 62196 Type 2 Connectors
- ISO 15118 (Future Support)

## Communication Standards

- OCPP 1.6J
- OCPP 2.0.1
- Modbus RTU
- Modbus TCP
- CAN Bus

## Software Standards

- Python 3.12+
- PEP8
- SOLID Principles
- Clean Architecture
- Semantic Versioning

---

# 4. Definitions & Acronyms

| Term | Description |
|------|-------------|
| EV | Electric Vehicle |
| EVSE | Electric Vehicle Supply Equipment |
| CP | Control Pilot |
| PP | Proximity Pilot |
| OCPP | Open Charge Point Protocol |
| DLB | Dynamic Load Balancing |
| HMI | Human Machine Interface |
| HAL | Hardware Abstraction Layer |
| RFID | Radio Frequency Identification |
| GUI | Graphical User Interface |
| PWM | Pulse Width Modulation |
| AC | Alternating Current |
| DC | Direct Current |

---

# 5. Design Principles

The OpenCharge Core follows the following engineering principles.

## Configuration First

All configurable values shall be managed by the Configuration Manager.

Business logic shall never contain hardcoded operational values such as:

- Maximum charging current
- OCPP server address
- Site power limits
- Charging schedules
- Connector settings
- Smart charging parameters

Configuration values shall be loaded through the Configuration Manager.

## Clean Architecture

Business logic shall remain independent from frameworks and hardware.

---

## SOLID Principles

The software shall follow all SOLID principles.

- Single Responsibility Principle
- Open Closed Principle
- Liskov Substitution Principle
- Interface Segregation Principle
- Dependency Inversion Principle

---

## Hardware Independence

The Core shall never directly access hardware peripherals.

Hardware access shall be performed exclusively through the Hardware Abstraction Layer (HAL).

---

## Protocol Independence

The Core shall not depend on:

- OCPP
- IEC61851
- Modbus
- CAN

These protocols depend on the Core.

---

## Event Driven Architecture

Software components communicate through events instead of direct dependencies whenever practical.

---

## Testability

Every component shall be independently unit testable.

---

## Extensibility

New charging standards and features shall be added without redesigning the Core.

---

# 6. System Context

The OpenCharge Core is positioned between hardware and external software systems.

                    External Systems

        Mobile App
        OCPP Backend
        Desktop Simulator
        Raspberry Pi HMI

                    │

            OpenCharge Core

                    │

      IEC61851 Controller

      Hardware Abstraction Layer

                    │

           STM32 Hardware

                    │

     Contactor
     Lock
     Meter
     LEDs
     Sensors

The OpenCharge Core serves as the single source of business logic for the complete charging platform.

---

# 7. Architectural Layers

OpenCharge follows a layered architecture.

+-----------------------------------------------------------+
| Presentation Layer                                        |
| Desktop GUI • Raspberry Pi HMI • REST API                 |
+-----------------------------------------------------------+

+-----------------------------------------------------------+
| Application Layer                                         |
| Authorization • Sessions • Configuration                  |
+-----------------------------------------------------------+

+-----------------------------------------------------------+
| Core Domain                                               |
| Charger • Connector • Session • Vehicle • Meter           |
+-----------------------------------------------------------+

+-----------------------------------------------------------+
| Smart Charging Layer                                      |
| Smart Charging • Load Manager • Power Manager             |
+-----------------------------------------------------------+

+-----------------------------------------------------------+
| Hardware Abstraction Layer                                |
| IEC61851 • Meter Drivers • GPIO • UART                    |
+-----------------------------------------------------------+

+-----------------------------------------------------------+
| Hardware                                                  |
| STM32 • Raspberry Pi • Contactor • Type 2 Socket          |
+-----------------------------------------------------------+

---

# 8. Core Responsibilities

The OpenCharge Core shall be responsible for:

- Managing charger lifecycle
- Managing connector state
- Managing charging sessions
- Maintaining state machine
- Publishing events
- Recording faults
- Meter abstraction
- Vehicle abstraction
- Authorization abstraction
- Smart Charging
- Dynamic Load Balancing
- Power Limitation
- Configuration Management

The Core shall never directly manipulate hardware resources.


```markdown
# 9. Core Domain Model

The OpenCharge Core follows Domain-Driven Design (DDD).

The **Charger** is the root aggregate responsible for coordinating all charging operations.

No external component shall directly manipulate the internal state of domain objects without passing through the Charger.

## Core Domain Model
                                     Charger
                                        │
       ┌────────────────────────────────┼────────────────────────────────┐
       │                                │                                │
       ▼                                ▼                                ▼
 StateMachine                     Connector(s)                 ChargingSession
       │                                │                                │
       │                                │                                ▼
       │                                │                       Authorization
       │                                │                                │
       │                                │                                ▼
       │                                │                            Vehicle
       │                                │                                │
       │                                │                                ▼
       │                                │                             Meter
       │
       ├──────────────────────────────────────────────────────────────┐
       │                                                              │
       ▼                                                              ▼
  Event Bus                                                    Fault Manager
       │                                                              │
       └──────────────────────────────┬───────────────────────────────┘
                                      ▼
                             Configuration Manager
                                      │
          ┌───────────────────────────┼───────────────────────────┐
          ▼                           ▼                           ▼
 Smart Charging Engine         Load Manager               Power Manager
                                      │
                                      ▼
                            Hardware Abstraction Layer


The Charger is the only object that coordinates the overall charging process.

---

# 10. Component Relationships

## Relationship Diagram

| Component | Owns | Depends On |
|------------|------|------------|
| Charger | Connector, StateMachine | Session, EventBus, FaultManager |
| Connector | Lock, Contactor | IEC61851 |
| ChargingSession | Vehicle, Authorization | Meter |
| SmartChargingEngine | Charging Profiles | LoadManager |
| LoadManager | Building Capacity | PowerManager |
| PowerManager | Current Limits | IEC61851 |

---

## Dependency Rules

Dependencies shall always flow downward.

Example:

Desktop GUI

↓

Application Layer

↓

Core Domain

↓

Hardware Abstraction

↓

Hardware

Reverse dependencies are not permitted.

---

# 11. Core Components

## 11.1 Charger

### Description

The Charger represents one complete EV Charging Station (EVSE).

It is responsible for coordinating every subsystem.

### Responsibilities

- Own connectors
- Manage charger lifecycle
- Manage charging sessions
- Coordinate authorization
- Publish events
- Monitor faults
- Coordinate Smart Charging
- Coordinate Dynamic Load Balancing
- Coordinate Power Management
- Maintain configuration

### Owned Objects

- StateMachine
- Connector(s)
- ChargingSession(s)
- EventBus
- FaultManager

### Future Services

- AuthorizationService
- SessionService
- ConfigurationService

---

## 11.2 Connector

### Description

Represents one physical charging outlet.

One charger may contain multiple connectors.

### Responsibilities

- Cable detection
- Lock management
- Contactor management
- IEC61851 state
- Connector availability
- Maximum current capability
- Connector diagnostics

### Hardware

- Type 2 Socket
- Lock Actuator
- Contactor
- PP Detection
- CP Interface

---

## 11.3 State Machine

### Description

Controls all charger state transitions.

The State Machine guarantees that invalid charger behaviour cannot occur.

### Responsibilities

- Validate transitions
- Reject invalid transitions
- Publish transition events
- Notify dependent components

---

## 11.4 Charging Session

### Description

Represents one complete charging transaction.

This object becomes the source of truth for billing,
meter values,
authorization,
and transaction history.

### Responsibilities

- Session lifecycle
- Meter aggregation
- Billing information
- Energy accounting
- Transaction status
- OCPP mapping

### Future Compatibility

- OCPP 1.6J
- OCPP 2.0.1
- ISO15118
- Plug & Charge

---

## 11.5 Vehicle

### Description

Represents the connected EV.

### Responsibilities

- Vehicle status
- Current request
- Battery information
- Charging capability

---

## 11.6 Meter

### Description

Represents all electrical measurements.

### Responsibilities

- Voltage
- Current
- Power
- Frequency
- Energy
- Temperature
- Power Factor

The Meter object is independent from the physical meter hardware.

---

## 11.7 Event Bus

### Description

Provides loose coupling between software components.

### Responsibilities

- Event publication
- Event subscription
- Event dispatching

Example Events

- Vehicle Connected
- Vehicle Disconnected
- RFID Accepted
- Charging Started
- Charging Stopped
- Meter Updated
- Fault Raised
- Fault Cleared

---

## 11.8 Fault Manager

### Description

Maintains all charger faults.

### Responsibilities

- Fault recording
- Fault clearing
- Severity classification
- Diagnostics

Faults are persistent until cleared.

---

## 11.9 Authorization

### Description

Represents user authorization.

### Supported Methods

- RFID
- QR Code
- Local Whitelist
- OCPP Remote Authorize

### Future

- ISO15118 Plug & Charge

---

## 11.10 Smart Charging Engine

### Description

Calculates the optimal charging current.

### Inputs

- Vehicle request
- Charger capability
- Site limits
- Charging profile
- OCPP profile

### Outputs

- Current limit
- Power limit

---

## 11.11 Load Manager

### Description

Responsible for Dynamic Load Balancing.

### Responsibilities

- Site load calculation
- Current distribution
- Phase balancing
- Multi-charger coordination

---

## 11.12 Power Manager

### Description

Responsible for enforcing power limits.

### Responsibilities

- Maximum current
- Maximum power
- Grid limitations
- Utility restrictions
- Demand management

---

## 11.13 Configuration Manager

### Description

The Configuration Manager is responsible for storing, validating,
loading, and providing all charger configuration parameters.

The Configuration Manager acts as the single source of truth for all
runtime and persistent configuration within the OpenCharge platform.

No software component shall access configuration directly from files,
hardware, or databases.

All configuration requests shall pass through the Configuration Manager.

### Responsibilities

- Load configuration
- Save configuration
- Validate configuration
- Version configuration
- Apply default values
- Import configuration
- Export configuration
- Notify components when configuration changes

### Configuration Categories

#### Charger

- Charger Name
- Charger ID
- Serial Number
- Firmware Version
- Manufacturer
- Model

#### Connector

- Connector Count
- Connector Type
- Maximum Current
- Rated Voltage
- Lock Enabled
- Socket Type

#### Electrical

- Maximum Current
- Maximum Power
- Grid Frequency
- Voltage Limits
- RCD Configuration
- Contactor Delay

#### Smart Charging

- Enabled
- Default Current
- Maximum Current
- Minimum Current
- Charging Profiles
- Schedule

#### Dynamic Load Balancing

- Enabled
- Site Maximum Current
- Site Maximum Power
- External Meter
- Priority
- Phase Balancing

#### OCPP

- Server URL
- Charge Point ID
- Heartbeat Interval
- Meter Value Interval
- Authorization Cache
- Offline Authorization

#### Network

- Ethernet
- Wi-Fi
- Static IP
- DHCP
- DNS
- NTP

#### Security

- TLS Certificates
- Local Users
- Administrator Password
- API Keys
- SSH Access

#### User Interface

- Language
- Theme
- Brightness
- Screen Timeout
- QR Display
- LED Behaviour

#### Logging

- Log Level
- Log Retention
- Remote Logging
- Debug Mode

### Future Extensions

The Configuration Manager shall support:

- Web Configuration
- Mobile Application Configuration
- OCPP Configuration Updates
- Backup and Restore
- Factory Reset
- Configuration Versioning

# 12. Component Interaction

A typical charging sequence is shown below.

Vehicle Plugged

↓

Connector detects cable

↓

State Machine changes to OCCUPIED

↓

Authorization

↓

Charging Session Created

↓

Smart Charging calculates available current

↓

Power Manager validates limits

↓

IEC61851 receives PWM value

↓

Contactor closes

↓

Charging Starts

↓

Meter updates Session

↓

Event Bus publishes Charging Started

↓

OCPP sends Status Notification

↓

Charging Stops

↓

Charging Session closes

↓

State Machine returns AVAILABLE

This interaction sequence shall remain valid regardless of hardware platform.
```

````markdown

# 13. Charger State Model

## Overview

The OpenCharge Core uses a Finite State Machine (FSM) to control charger behaviour.

Every charger state transition shall be validated before execution.

No component may directly modify the charger state.

All state changes shall be requested through the State Machine.

---

## Charger Lifecycle

```text
                        Power Applied
                              │
                              ▼
                         OFFLINE
                              │
                              ▼
                          BOOTING
                              │
                              ▼
                      INITIALIZING
                              │
                              ▼
                         AVAILABLE
                              │
               Vehicle Connected (CP State B)
                              │
                              ▼
                          OCCUPIED
                              │
                              ▼
                       AUTHORIZING
                              │
                    Authorization Accepted
                              │
                              ▼
                         AUTHORIZED
                              │
                              ▼
                         PREPARING
                              │
                     Contactor Closed
                              │
                              ▼
                         CHARGING
                       ┌─────────────┐
                       ▼             ▼
               SUSPENDED_EV   SUSPENDED_EVSE
                       │             │
                       └──────┬──────┘
                              ▼
                         FINISHING
                              │
                              ▼
                         AVAILABLE

Any State
    │
    ▼
FAULTED
````

---

## State Definitions

| State          | Description                          |
| -------------- | ------------------------------------ |
| OFFLINE        | Charger not operational              |
| BOOTING        | System startup                       |
| INITIALIZING   | Hardware and software initialization |
| AVAILABLE      | Ready to accept a vehicle            |
| OCCUPIED       | Vehicle connected                    |
| AUTHORIZING    | Waiting for authorization            |
| AUTHORIZED     | User successfully authorized         |
| PREPARING      | Preparing to energize connector      |
| CHARGING       | Energy transfer active               |
| SUSPENDED_EV   | Vehicle paused charging              |
| SUSPENDED_EVSE | Charger paused charging              |
| FINISHING      | Charging ending                      |
| FAULTED        | Charger fault                        |
| UNAVAILABLE    | Disabled for maintenance             |

---

## State Transition Rules

Only valid transitions are permitted.

Example:

OFFLINE

↓

BOOTING

↓

INITIALIZING

↓

AVAILABLE

Invalid Example:

OFFLINE

↓

CHARGING

Result:

Transition Rejected

Fault Logged

Event Published

---

# 14. Charging Session Lifecycle

The Charging Session lifecycle is independent of the Charger lifecycle.

A charger may remain AVAILABLE while no session exists.

---

## Session Lifecycle

```text
IDLE
 │
 ▼
CREATED
 │
 ▼
AUTHORIZED
 │
 ▼
PREPARING
 │
 ▼
ACTIVE
 │
 ▼
SUSPENDED
 │
 ▼
STOPPING
 │
 ▼
COMPLETED

or

FAILED

or

CANCELLED
```

---

## Session Responsibilities

The Charging Session records:

* Authorization
* Meter Values
* Start Time
* Stop Time
* Energy
* Tariff
* Cost
* OCPP Transaction
* Stop Reason

---

## Session Ownership

One Connector

↓

One Active Charging Session

↓

One Vehicle

A Connector shall never own more than one active session.

---

# 15. Event Architecture

OpenCharge follows an Event-Driven Architecture.

Components communicate by publishing and subscribing to events.

---

## Event Flow

Vehicle Plugged

↓

Connector

↓

Event Bus

↓

State Machine

↓

Charging Session

↓

GUI

↓

OCPP

↓

Logger

Each subsystem reacts independently.

---

## Typical Events

System

* Startup
* Shutdown
* Configuration Changed

Vehicle

* Connected
* Disconnected

Authorization

* RFID Accepted
* RFID Rejected
* QR Accepted
* Remote Authorized

Charging

* Started
* Stopped
* Suspended
* Resumed

Meter

* Meter Updated

Fault

* Raised
* Cleared

OCPP

* Connected
* Disconnected
* Boot Notification
* Heartbeat

---

## Event Principles

Events shall be immutable.

Events shall include:

* Event ID
* Timestamp
* Source
* Severity
* Payload

---

# 16. Fault Management Architecture

Fault handling is centralized.

Components report faults to the Fault Manager.

---

## Fault Sources

* IEC61851
* Connector
* Meter
* Contactor
* Lock
* Temperature
* OCPP
* Configuration
* Internal Software

---

## Fault Lifecycle

```text
Detected

↓

Active

↓

Reported

↓

Acknowledged

↓

Recovered

↓

Cleared
```

---

## Fault Severity

| Severity | Description                      |
| -------- | -------------------------------- |
| INFO     | Informational                    |
| WARNING  | Non-critical                     |
| ERROR    | Charger cannot continue normally |
| CRITICAL | Immediate shutdown required      |

---

## Fault Recovery

The Fault Manager determines whether:

* Automatic recovery is allowed
* Manual intervention is required
* Charger restart is required

---

## Safety Principle

Whenever uncertainty exists,

Safety takes priority over availability.

The charger shall always move to a safe state before attempting recovery.

```
```
