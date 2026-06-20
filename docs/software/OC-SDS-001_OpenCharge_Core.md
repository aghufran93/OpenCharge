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


````markdown
# 17. Smart Charging Architecture

## Overview

The Smart Charging Engine is responsible for determining the optimal charging current and power delivered to the connected electric vehicle.

The Smart Charging Engine shall operate independently of the communication protocol.

Whether charging commands originate from:

- Local Configuration
- RFID
- QR Code
- OCPP
- Mobile Application
- REST API

all charging decisions shall be evaluated by the Smart Charging Engine.

---

## Responsibilities

The Smart Charging Engine shall:

- Calculate charging current
- Calculate charging power
- Apply charging profiles
- Apply user limits
- Apply site limits
- Apply utility restrictions
- Apply Dynamic Load Balancing results
- Apply Time-of-Use schedules
- Apply Configuration Manager settings

---

## Inputs

The Smart Charging Engine receives:

- Vehicle Requested Current
- Charger Maximum Current
- Connector Rating
- Site Power Limit
- Load Manager Allocation
- Power Manager Limit
- OCPP Charging Profile
- Local Charging Profile
- Configuration Parameters

---

## Outputs

The Smart Charging Engine produces:

- Target Current (A)
- Target Power (kW)
- IEC61851 PWM Duty Cycle

---

## Smart Charging Flow

Vehicle Connected

↓

Authorization Successful

↓

Charging Session Created

↓

Smart Charging Engine

↓

Load Manager

↓

Power Manager

↓

IEC61851 Controller

↓

PWM Generated

↓

Charging Starts

---

# 18. Dynamic Load Balancing

## Overview

Dynamic Load Balancing (DLB) ensures that multiple chargers operate within the electrical capacity of a site.

The objective is to maximize charging performance while preventing overload of electrical infrastructure.

---

## Responsibilities

The Load Manager shall:

- Monitor site capacity
- Monitor charger demand
- Allocate available current
- Prevent overload
- Support multiple chargers
- Support priority charging

---

## Site Architecture

```text
                  Utility Grid

                       │

                Main Breaker

                       │

                Main Energy Meter

                       │

                Load Manager

      ┌──────────┬──────────┬──────────┐

      ▼          ▼          ▼

 Charger 1   Charger 2   Charger 3
```

---

## Example

Site Capacity

160 A

Current Building Load

90 A

Available for EV Charging

70 A

Requested

32 A

32 A

32 A

Allocated

24 A

23 A

23 A

No breaker trips.

---

## Future Features

- Phase Balancing
- Building Energy Management
- External Modbus Meter
- OCPP Site Controller
- Cluster Charging

---

# 19. Power Management

## Overview

The Power Manager ensures that charging power never exceeds configured or calculated limits.

Unlike the Smart Charging Engine, which calculates the desired charging current, the Power Manager enforces operational limits.

---

## Responsibilities

- Maximum Current
- Maximum Power
- Phase Current
- Grid Limit
- Thermal Derating
- Utility Restrictions
- Emergency Power Reduction

---

## Example

Vehicle Requests

32 A

↓

Building Limit

20 A

↓

Power Manager

↓

Output

20 A

---

## Thermal Protection

When charger temperature exceeds configured thresholds, the Power Manager shall reduce charging current.

Example

65°C

↓

Current Reduced

32 A → 24 A

↓

Temperature Stabilized

---

# 20. Configuration Management

## Overview

The Configuration Manager is the single source of truth for all configurable parameters.

No component shall maintain independent configuration.

---

## Responsibilities

- Load Configuration
- Save Configuration
- Validate Configuration
- Apply Defaults
- Version Configuration
- Import
- Export
- Factory Reset

---

## Configuration Categories

### Charger

- Charger ID
- Name
- Manufacturer
- Firmware
- Serial Number

### Connector

- Connector Count
- Connector Type
- Lock Enabled
- Maximum Current

### Electrical

- Rated Voltage
- Rated Current
- Maximum Power
- RCD Settings

### Smart Charging

- Default Current
- Maximum Current
- Charging Profile

### Dynamic Load Balancing

- Enabled
- Site Capacity
- Priority

### OCPP

- Server URL
- Charge Point ID
- Heartbeat
- Meter Interval

### Network

- Ethernet
- Wi-Fi
- DHCP
- Static IP
- DNS
- NTP

### Security

- Certificates
- API Keys
- Local Users
- Passwords

### User Interface

- Language
- Brightness
- Theme
- QR Display

### Logging

- Log Level
- Debug
- Remote Logging

---

## Storage

Initially

JSON Configuration

Future

SQLite

Encrypted Secure Storage

---

# 21. Charging Profiles

The Smart Charging Engine shall support Charging Profiles.

Charging Profiles define how charging current changes over time.

---

## Supported Sources

- Local Configuration
- OCPP Smart Charging
- Mobile Application
- Utility

---

## Example

18:00

16 A

↓

22:00

32 A

↓

06:00

Stop

---

# 22. Future Energy Management

OpenCharge shall support future energy management capabilities.

Examples

- Solar Charging
- Battery Storage
- Home Energy Management
- Building Energy Management
- Utility Demand Response

---

## Solar Charging Example

Solar Production

8 kW

↓

House Load

2 kW

↓

Available

6 kW

↓

EV Charging

6 kW

---

# 23. Multi-Charger Coordination

Future versions of OpenCharge shall support charger clustering.

Capabilities

- Master Charger
- Satellite Chargers
- Shared Site Capacity
- Central Load Balancing
- OCPP Site Controller

---

## Design Goal

One software architecture shall support:

- Home Charger
- Office Charger
- Apartment Charger
- Public Charger
- Fleet Charger
- Charging Hub

without architectural redesign.
````


# 24. Role-Based Access Control (RBAC)

## Overview

The OpenCharge platform shall implement Role-Based Access Control (RBAC) to ensure that users can only access features and configuration appropriate to their assigned role.

RBAC shall be enforced consistently across:

- Desktop Simulator
- Raspberry Pi HMI
- Local Web Interface
- REST API
- OCPP Remote Operations
- Future Mobile Applications

All privileged operations shall require authentication and authorization.

---

## Supported Roles

### 1. Guest

Purpose

- View charger status only

Permissions

- View charger availability
- View charging status
- View connector status

Restrictions

- No configuration
- No charging control
- No diagnostics

---

### 2. Driver (End User)

Purpose

Charge an electric vehicle.

Permissions

- Start Charging
- Stop Charging
- RFID Authentication
- QR Charging
- View Session Information

Restrictions

- No charger configuration
- No diagnostics
- No firmware update

---

### 3. Installer

Purpose

Commission a newly installed charger.

Permissions

- Configure network
- Configure charger ID
- Configure connector ratings
- Configure electrical parameters
- Configure OCPP server

Restrictions

- No firmware development
- No service diagnostics
- No security management

---

### 4. Service Engineer

Purpose

Maintain and troubleshoot chargers.

Permissions

- Diagnostics
- View Logs
- Fault Reset
- Test Contactor
- Test Lock
- Test LEDs
- Test IEC61851
- Calibration

Restrictions

- Cannot modify billing
- Cannot modify user accounts

---

### 5. Operator (CPO)

Purpose

Operate charging infrastructure.

Permissions

- Remote Start
- Remote Stop
- Enable Charger
- Disable Charger
- Manage Charging Profiles
- Configure Smart Charging
- Configure Dynamic Load Balancing

Restrictions

- No firmware modification

---

### 6. Administrator

Purpose

Manage complete charger configuration.

Permissions

- Full Configuration
- User Management
- Security Configuration
- Network Configuration
- Firmware Upgrade
- Certificate Management
- Factory Reset

Restrictions

None

---

### 7. Developer

Purpose

Development and testing.

Permissions

- Debug Mode
- Simulation
- Internal Logs
- Test Commands
- Engineering Features

Restrictions

Disabled in production firmware.

---

# Permission Matrix

| Feature | Guest | Driver | Installer | Service | Operator | Admin | Developer |
|----------|:-----:|:------:|:----------:|:--------:|:--------:|:-----:|:---------:|
| View Status | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Start Charging | ✗ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Stop Charging | ✗ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Configure Network | ✗ | ✗ | ✓ | ✗ | ✗ | ✓ | ✓ |
| Configure OCPP | ✗ | ✗ | ✓ | ✗ | ✓ | ✓ | ✓ |
| Diagnostics | ✗ | ✗ | ✗ | ✓ | ✓ | ✓ | ✓ |
| Firmware Update | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ | ✓ |
| Factory Reset | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ | ✓ |
| Debug Mode | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ |

---

## Audit Logging

All privileged operations shall be recorded.

Each audit record shall include:

- Timestamp
- User ID
- User Role
- Action
- Target Component
- Previous Value
- New Value
- Result
- IP Address (where applicable)

Example

2026-07-01 14:20:10

Administrator

Changed

Maximum Current

32 A → 25 A

Result

Success

---

## Security Principles

The OpenCharge platform shall follow these principles:

- Least Privilege
- Separation of Duties
- Secure by Default
- Auditability
- Traceability

Unauthorized access shall never modify charger configuration or safety-related parameters.



# 26. Future Enhancements

The following capabilities are outside the scope of Version 1.0 but have been considered during the architectural design.

Future enhancements shall be implemented without requiring significant redesign of the OpenCharge Core.

## Enterprise Services

- User Management
- Audit Logging
- Diagnostics Manager
- Health Monitoring
- Licensing Manager
- Certificate Manager
- OTA Update Manager

## Energy Management

- Solar Charging
- Battery Storage Integration
- Home Energy Management System (HEMS)
- Building Energy Management System (BEMS)
- Utility Demand Response
- Vehicle-to-Grid (V2G)
- Vehicle-to-Home (V2H)

## Connectivity

- MQTT
- OCPI
- ISO 15118 Plug & Charge
- REST API
- GraphQL API

## Deployment

- Multi-Charger Clustering
- Central Site Controller
- Cloud Synchronization
- Edge Computing

## Product Editions

- Community
- Home
- Business
- Enterprise
- Industrial






```markdown
# 24. External Interfaces

## Overview

The OpenCharge Core communicates with external systems exclusively through well-defined interfaces.

External systems shall not directly manipulate internal Core objects.

The Core remains independent of communication protocols, hardware implementations, and user interface technologies.

---

## Supported Interfaces

### Desktop Simulator

Purpose

Development, testing, debugging and simulation.

Capabilities

- Charger Simulation
- Vehicle Simulation
- Event Monitoring
- Fault Injection
- Meter Simulation
- Configuration

---

### Raspberry Pi HMI

Purpose

Local charger operation.

Capabilities

- Status Display
- User Authentication
- Session Monitoring
- Configuration
- Diagnostics

---

### STM32 Firmware

Purpose

Real-time hardware control.

Responsibilities

- GPIO
- PWM
- ADC
- UART
- Lock Control
- Contactor Control
- CP Measurement
- PP Detection

---

### IEC 61851 Controller

Purpose

Charging protocol implementation.

Responsibilities

- CP State Detection
- PWM Generation
- Duty Cycle Control
- Safety Monitoring

---

### OCPP Client

Purpose

Communication with Central Management System.

Supported Versions

- OCPP 1.6J
- OCPP 2.0.1

Responsibilities

- Boot Notification
- Authorization
- Status Notification
- Transactions
- Meter Values
- Smart Charging

---

### REST API (Future)

Purpose

External integrations.

Future Applications

- Mobile Applications
- Fleet Management
- Building Management
- Energy Management

---

# 25. Design Constraints

The following constraints shall be observed throughout the OpenCharge project.

---

## Hardware Independence

Business logic shall never directly communicate with hardware.

---

## Protocol Independence

The Core shall not depend on:

- OCPP
- IEC 61851
- Modbus
- CAN
- MQTT

Protocols depend on the Core.

---

## Platform Independence

The Core shall execute without modification on:

- Windows
- Linux
- macOS
- Raspberry Pi

---

## Configuration First

Operational parameters shall never be hardcoded.

All configurable values shall be managed by the Configuration Manager.

---

## Security by Design

Authentication and authorization shall be considered in every subsystem.

---

## Safety First

Whenever uncertainty exists,

the charger shall enter a safe state.

Safety always takes precedence over availability.

---

## Testability

Every component shall support unit testing.

Simulation shall be possible without physical hardware.

---

## Scalability

The architecture shall support:

- Single Connector Chargers
- Dual Connector Chargers
- Multi-Connector Chargers
- Charging Hubs

without redesign.

---

# 26. Non-Functional Requirements

## Performance

- Startup Time < 10 seconds
- State Transition < 100 ms
- Authorization Response < 2 seconds
- Charging Start < 5 seconds after authorization

---

## Reliability

- Automatic recovery where possible
- Fault isolation
- Graceful shutdown
- Watchdog compatibility

---

## Maintainability

- Modular architecture
- Clear interfaces
- Comprehensive documentation
- High code readability

---

## Security

- RBAC
- Secure configuration
- TLS support
- Certificate management
- Audit readiness

---

## Portability

The Core shall remain independent of:

- Operating System
- GUI Framework
- Hardware Platform

---

# 27. Product Editions

The OpenCharge architecture shall support multiple product editions from a common codebase.

---

## Community Edition

Target

Open-source development and education.

Features

- Single Connector
- IEC 61851
- OCPP
- RFID
- Desktop Simulator

---

## Home Edition

Target

Residential charging.

Additional Features

- Smart Charging
- Charging Scheduler
- Solar Ready

---

## Business Edition

Target

Commercial buildings, offices and hotels.

Additional Features

- Dynamic Load Balancing
- Multiple Users
- Reporting
- Smart Charging Profiles

---

## Enterprise Edition

Target

Charging Point Operators (CPOs), apartment complexes and fleet operators.

Additional Features

- RBAC
- Advanced Configuration
- Diagnostics
- Multi-Charger Coordination
- Central Management

---

## Industrial Edition

Target

Utility companies, depots and large charging infrastructure.

Additional Features

- SCADA Integration
- MQTT
- Advanced Energy Management
- Utility Demand Response
- High Availability

---

# 28. Future Enhancements

The following capabilities are outside the scope of Version 1.0 but have been considered during architectural design.

Future enhancements shall be implemented without significant redesign.

---

## Enterprise Services

- User Management
- Audit Logging
- Diagnostics Manager
- Health Monitor
- OTA Updates
- Certificate Manager
- Licensing Manager

---

## Smart Energy

- Solar Charging
- Battery Storage
- Home Energy Management System (HEMS)
- Building Energy Management System (BEMS)
- Vehicle-to-Grid (V2G)
- Vehicle-to-Home (V2H)

---

## Connectivity

- MQTT
- OCPI
- REST API
- GraphQL API
- ISO 15118 Plug & Charge

---

## Deployment

- Multi-Charger Clustering
- Edge Computing
- Cloud Synchronization
- Central Site Controller

---

# 29. Implementation Roadmap

The OpenCharge implementation shall follow the sequence below.

## Phase 1

Foundation

- Documentation
- Architecture
- Standards

---

## Phase 2

Core Domain

- Enums
- State Machine
- Charger
- Connector
- Charging Session
- Vehicle
- Meter
- Event Bus
- Fault Manager
- Configuration Manager

---

## Phase 3

Desktop Simulator

- GUI
- Simulator
- Event Monitor
- Virtual Vehicle
- Virtual Meter

---

## Phase 4

Communication

- IEC 61851
- OCPP 1.6J
- OCPP 2.0.1

---

## Phase 5

Energy Management

- Smart Charging
- Dynamic Load Balancing
- Power Management

---

## Phase 6

Firmware

- STM32
- HAL
- Drivers

---

## Phase 7

Hardware

- KiCad
- Schematics
- PCB
- BOM

---

## Phase 8

System Integration

- Desktop
- Firmware
- Hardware
- OCPP
- Validation

---

# 30. Traceability Matrix

| Requirement | Design | Implementation |
|-------------|--------|----------------|
| Charger Management | Charger | charger.py |
| Connector Management | Connector | connector.py |
| State Management | State Machine | state_machine.py |
| Charging Transactions | Charging Session | charging_session.py |
| Vehicle Model | Vehicle | vehicle.py |
| Meter Model | Meter | meter.py |
| Fault Handling | Fault Manager | fault_manager.py |
| Event Handling | Event Bus | event_bus.py |
| Authorization | Authorization | authorization.py |
| Smart Charging | Smart Charging Engine | smart_charging.py |
| Load Balancing | Load Manager | load_manager.py |
| Power Limitation | Power Manager | power_manager.py |
| Configuration | Configuration Manager | configuration_manager.py |

---

# 31. Conclusion

The OpenCharge Core provides a modular, scalable and hardware-independent software foundation for the OpenCharge platform.

The architecture has been designed to support:

- Commercial AC EV Chargers
- Residential Chargers
- Fleet Chargers
- Apartment Installations
- Public Charging Infrastructure
- Future Smart Energy Systems

without requiring architectural redesign.

The principles defined in this document shall guide all future implementation activities to ensure that OpenCharge remains maintainable, extensible and suitable for commercial deployment.

---

**End of Document**
```

