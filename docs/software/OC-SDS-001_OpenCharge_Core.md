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