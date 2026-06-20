# OpenCharge Roadmap
# OpenCharge Roadmap

---

# Document Information

| Item | Details |
|------|---------|
| **Project** | OpenCharge |
| **Document ID** | OC-DOC-003 |
| **Document Name** | Development Roadmap |
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

# Overview

This roadmap defines the planned development milestones for the OpenCharge platform.

The roadmap is organized into progressive phases that gradually transform OpenCharge from a desktop simulator into a complete commercial-grade AC EV charging platform.

Each phase builds upon the previous one while maintaining a stable and modular software architecture.

---

# Development Philosophy

OpenCharge follows the principle:

> **Design → Document → Implement → Test → Simulate → Deploy**

Every milestone must satisfy the following criteria before moving to the next phase:

* Architecture Approved
* Documentation Updated
* Code Reviewed
* Unit Tests Passing
* Simulator Validated
* GitHub Updated

---

# Version Roadmap

## v0.1.0-alpha — Project Foundation

### Objectives

* Project repository
* Development environment
* Folder structure
* Documentation
* Development workflow
* GitHub configuration

### Deliverables

* README
* Vision
* Roadmap
* Architecture
* Contributing Guide
* Changelog

**Status:** ✅ Completed

---

## v0.2.0-alpha — OpenCharge Core

### Objectives

Develop the platform-independent business logic.

### Deliverables

* Charger
* Connector
* Vehicle
* Session
* Meter
* Fault Manager
* Event System
* State Machine

---

## v0.3.0-alpha — Desktop Simulator

### Objectives

Create a complete virtual EV charging environment.

### Deliverables

* Desktop GUI
* Virtual EV
* Virtual Meter
* Virtual Contactor
* Virtual Connector Lock
* Event Log
* Dashboard

---

## v0.4.0-alpha — IEC 61851

### Objectives

Implement the AC charging communication standard.

### Deliverables

* Control Pilot
* Proximity Pilot
* PWM Generation
* State Detection
* Safety Logic
* Cable Detection

---

## v0.5.0-beta — OCPP 1.6J

### Objectives

Enable communication with Charge Point Management Systems.

### Deliverables

* Boot Notification
* Heartbeat
* Authorization
* Start Transaction
* Stop Transaction
* Meter Values
* Status Notifications
* Remote Commands

---

## v0.6.0-beta — STM32 Firmware

### Objectives

Develop embedded firmware for charger control.

### Deliverables

* GPIO Drivers
* UART
* PWM
* Contactor Control
* Lock Control
* Safety Monitoring
* Firmware Logging

---

## v0.7.0-beta — Raspberry Pi HMI

### Objectives

Create the charger user interface.

### Deliverables

* Touchscreen Interface
* Configuration Manager
* QR Code Display
* RFID Management
* Charging Dashboard
* Local Database

---

## v0.8.0-beta — Hardware Design

### Objectives

Design production-ready reference hardware.

### Deliverables

* KiCad Schematics
* PCB Layout
* Bill of Materials
* Wiring Diagrams
* Enclosure Design

---

## v0.9.0-rc — System Integration

### Objectives

Integrate all software and hardware components.

### Deliverables

* Full System Testing
* Hardware Validation
* Integration Testing
* Performance Testing
* Reliability Testing

---

## v1.0.0 — Production Prototype

### Objectives

Deliver the first fully functional OpenCharge prototype.

### Deliverables

* Desktop Simulator
* STM32 Firmware
* Raspberry Pi HMI
* IEC 61851
* OCPP 1.6J
* Hardware Prototype
* Technical Documentation

---

# Future Releases

## Version 1.x

* Multi-Connector Support
* Dynamic Load Balancing
* Local Web Configuration
* MQTT Integration
* REST API
* OTA Firmware Updates

---

## Version 2.x

* OCPP 2.0.1
* ISO 15118 Preparation
* Smart Charging
* Plug & Charge
* Mobile Application
* Cloud Platform
* Analytics Dashboard
* Fleet Management
* Remote Diagnostics

---

# Long-Term Vision

The OpenCharge ecosystem will eventually include:

* OpenCharge Core
* OpenCharge Desktop
* OpenCharge Firmware
* OpenCharge HMI
* OpenCharge Hardware
* OpenCharge SDK
* OpenCharge Cloud
* OpenCharge Mobile
* OpenCharge Documentation Portal

---

# Success Metrics

The roadmap will be considered successful when OpenCharge achieves:

* Production-ready software architecture.
* Complete IEC 61851 implementation.
* OCPP compliance.
* Hardware reference design.
* Automated testing framework.
* Comprehensive documentation.
* Active open-source community.
* Commercial deployment readiness.

---

# Maintainer

**Ahmed Ghufran**
Founder & Lead System Architect
OpenCharge Project

Contributions and suggestions from the open-source community are welcome and encouraged.
