# OpenCharge Roadmap
# ⚡ OpenCharge

> Open-source commercial-grade AC EV Charging Platform built from scratch.

---

# Document Information

| Item | Details |
|------|---------|
| **Project** | OpenCharge |
| **Document ID** | OC-DOC-001 |
| **Document Name** | Project Overview (README) |
| **Version** | 1.0 |
| **Status** | Active |
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
| 1.0 | June 2026 | Ahmed Ghufran | Initial Release |

---


# Table of Contents

*Will be updated as the document evolves.*

---

# OpenCharge

# ⚡ OpenCharge

> **An open-source, commercial-grade AC EV Charging Platform built from scratch.**

---

Copyright 2026 Ahmed Ghufran

Licensed under the Apache License, Version 2.0.

## 🚧 Project Status

**Current Version:** `v0.1.0-alpha`

> **OpenCharge is under active development.**

The project is currently focused on building a professional software architecture before hardware implementation.

---

# Overview

OpenCharge is an open-source project to design and build a complete AC EV charging platform using industrial software engineering practices.

Unlike many hobby projects, OpenCharge is designed from the ground up with:

* Clean Architecture
* SOLID Principles
* Hardware Abstraction
* Desktop-first Development
* Testability
* Commercial-grade Documentation
* Industrial Coding Standards

The project will include everything required to build a modern AC EV charger.

---

# Vision

OpenCharge aims to become one of the most complete open-source AC EV charging platforms available.

The long-term vision is to provide a modular platform that supports:

* AC EV Chargers
* Desktop Simulator
* IEC 61851 Implementation
* OCPP 1.6J
* OCPP 2.0.1
* STM32 Firmware
* Raspberry Pi HMI
* Hardware Reference Design
* Professional Documentation

The software architecture is designed so that the same business logic can run on:

* Desktop Simulator
* Raspberry Pi
* Embedded Controller
* Future Products

---

# Project Goals

## Software

* Desktop EV Charger Simulator
* Charger State Machine
* IEC 61851 Control Pilot
* OCPP Client
* Modbus Meter Support
* RFID Support
* QR Code Charging
* Configuration Management
* Logging Framework
* Testing Framework

## Embedded

* STM32 Firmware
* Hardware Drivers
* UART Communication
* PWM Generation
* Contactor Control
* Connector Lock
* Safety Monitoring

## Hardware

* KiCad Schematics
* PCB Design
* Bill of Materials
* Reference Enclosure
* Wiring Diagrams

---

# Architecture

The project follows a layered Clean Architecture.

```
                Desktop GUI
                     │
              Application Layer
                     │
                Service Layer
                     │
               OpenCharge Core
                     │
       ┌─────────────┼─────────────┐
       │             │             │
   IEC 61851      OCPP        Simulator
       │             │             │
       └─────────────┼─────────────┘
                     │
          Hardware Abstraction Layer
                     │
         STM32 / Raspberry Pi Hardware
```

The **OpenCharge Core** contains all business logic and is completely independent of the GUI and hardware.

---

# Repository Structure

```
OpenCharge/

.github/
config/
desktop/
docs/
examples/
firmware/
hardware/
logs/
scripts/
tools/

README.md
VISION.md
ROADMAP.md
ARCHITECTURE.md
CONTRIBUTING.md
CHANGELOG.md

requirements.txt
pyproject.toml
```

---

# Technology Stack

| Component        | Technology        |
| ---------------- | ----------------- |
| Language         | Python            |
| GUI              | PySide6 (Qt)      |
| Embedded         | STM32             |
| HMI              | Raspberry Pi      |
| Communication    | UART              |
| Protocol         | IEC 61851         |
| Backend Protocol | OCPP 1.6J / 2.0.1 |
| PCB              | KiCad             |
| Version Control  | Git               |
| Repository       | GitHub            |

---

# Development Philosophy

OpenCharge follows a simple principle:

> **Design for production. Develop in simulation. Deploy to hardware.**

Every feature will first be implemented inside the desktop simulator before being deployed to embedded hardware.

This approach reduces development time and improves software quality.

---

# Development Roadmap

## Phase 0

* Project Foundation
* Development Environment
* Documentation

## Phase 1

* OpenCharge Core
* Domain Model
* State Machine

## Phase 2

* Desktop Simulator
* Virtual EV
* Virtual Meter
* Virtual Hardware

## Phase 3

* IEC 61851 Implementation

## Phase 4

* OCPP 1.6J Client

## Phase 5

* STM32 Firmware

## Phase 6

* Raspberry Pi HMI

## Phase 7

* Hardware Design

## Phase 8

* Prototype Validation

## Phase 9

* Production Release

---

# Getting Started

## Clone Repository

```bash
git clone git@github.com:aghufran93/OpenCharge.git
```

## Create Virtual Environment

```bash
python3 -m venv .venv
```

## Activate

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows

```powershell
.venv\Scripts\activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Project Structure

```
desktop/
    app/
    core/
    gui/
    models/
    services/
    simulator/
    resources/
    tests/
```

---

# Documentation

Project documentation can be found in:

```
docs/

architecture/
protocol/
hardware/
api/
standards/
```

---

# Development Workflow

Each feature follows the same engineering process:

```
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

Hardware Integration

↓

Release
```

---

# Contributing

Contributions are welcome.

Please read:

* CONTRIBUTING.md

before submitting Pull Requests.

---

# License

This project is licensed under the Apache 2.0 License.

See the LICENSE file for details.

---

# Author

**Ahmed Ghufran**

Founder of the OpenCharge Project.

---

# Acknowledgements

This project is inspired by the global open-source community and aims to accelerate EV charging innovation through transparent engineering and collaborative development.

---

# Disclaimer

OpenCharge is under active development.

The project is intended for educational, research, and commercial development purposes.

Always follow local electrical regulations and applicable safety standards before connecting software to high-voltage equipment.

---

## ⭐ Star the Project

If you find this project useful, consider giving it a ⭐ on GitHub and contributing to its development.

Together, we can build a professional open-source EV charging platform.

Copyright 2026 Ahmed Ghufran

Licensed under the Apache License, Version 2.0.