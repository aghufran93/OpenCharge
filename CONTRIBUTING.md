# Contributing to OpenCharge

---

## Document Information

| Item             | Details                                  |
| ---------------- | ---------------------------------------- |
| **Project**      | OpenCharge                               |
| **Document**     | Contribution Guidelines                  |
| **Version**      | 1.0                                      |
| **Status**       | Active                                   |
| **Author**       | Ahmed Ghufran                            |
| **Role**         | Founder & Lead System Architect          |
| **License**      | Apache License 2.0                       |
| **Repository**   | https://github.com/aghufran93/OpenCharge |
| **Last Updated** | June 2026                                |

---

## Revision History

| Version | Date      | Author        | Description     |
| ------- | --------- | ------------- | --------------- |
| 1.0     | June 2026 | Ahmed Ghufran | Initial Release |

---

## Table of Contents

1. Welcome
2. Before You Start
3. Development Principles
4. Development Workflow
5. Branch Strategy
6. Commit Message Convention
7. Coding Standards
8. Documentation Standards
9. Testing Requirements
10. Pull Requests
11. Reporting Issues
12. Feature Requests
13. Code Review Checklist
14. Contributor Recognition
15. Development Environment
16. Community Values
17. Questions
18. Thank You

---

---

# Welcome

Thank you for your interest in contributing to **OpenCharge**.

OpenCharge is an open-source initiative to build a commercial-grade AC EV charging platform using professional software engineering practices.

Whether you are fixing bugs, improving documentation, designing hardware, or implementing new features, your contributions are greatly appreciated.

---

# Before You Start

Please read the following documents before contributing:

* README.md
* VISION.md
* ROADMAP.md
* ARCHITECTURE.md
* CODE_OF_CONDUCT.md

Understanding the project architecture before writing code helps maintain consistency and long-term quality.

---

# Development Principles

Every contribution should follow these principles:

* Documentation before implementation
* Clean Architecture
* SOLID Principles
* Small and focused commits
* Testable code
* Modular design
* Platform independence
* Professional documentation

---

# Development Workflow

Every new feature follows the workflow below:

```text
Requirement
      ↓
Architecture
      ↓
Implementation
      ↓
Unit Testing
      ↓
Simulation
      ↓
Code Review
      ↓
Merge
```

Features should always be tested in the desktop simulator before hardware implementation.

---

# Branch Strategy

OpenCharge uses a Git Flow inspired workflow.

```
main
│
├── develop
│
├── feature/*
│
├── release/*
│
└── hotfix/*
```

## Branch Types

### main

Production-ready code.

### develop

Integration branch for ongoing development.

### feature

Used for new functionality.

Example:

```
feature/state-machine
feature/ocpp-client
feature/iec61851
```

### release

Used for preparing new versions.

Example:

```
release/v0.5.0
```

### hotfix

Critical fixes for released versions.

---

# Commit Message Convention

OpenCharge follows Conventional Commits.

Examples:

```
feat(core): implement charger state machine

fix(ocpp): correct heartbeat interval

docs: update architecture document

test(core): add charger unit tests

refactor(core): simplify event manager

chore: update dependencies
```

Common prefixes:

* feat
* fix
* docs
* refactor
* test
* chore
* ci

---

# Coding Standards

## Python

* Python 3.12+
* Type hints required
* Google-style docstrings
* Black formatting
* Ruff linting
* MyPy type checking

---

## Naming Conventions

### Classes

```
Charger
Connector
ChargingSession
Meter
```

### Functions

```
start_charging()

stop_charging()

authorize_user()
```

### Constants

```
MAX_CURRENT

DEFAULT_PWM

LOCK_TIMEOUT
```

---

# Documentation Standards

Every new feature must include documentation.

Documentation should explain:

* Purpose
* Design
* Interfaces
* Limitations
* Testing

Code without documentation may be rejected during review.

---

# Testing Requirements

Every feature should include appropriate tests.

Testing includes:

* Unit Tests
* Simulator Tests
* Integration Tests (when applicable)

No feature should be merged without verification.

---

# Pull Requests

Before opening a Pull Request, ensure:

* Code builds successfully.
* Unit tests pass.
* Documentation is updated.
* Code follows formatting standards.
* Commit history is clean.

Pull Requests should describe:

* What changed
* Why it changed
* Testing performed
* Related issues

---

# Reporting Issues

When reporting bugs, include:

* OpenCharge version
* Operating system
* Python version
* Hardware (if applicable)
* Steps to reproduce
* Expected behaviour
* Actual behaviour
* Screenshots or logs

---

# Feature Requests

Feature requests should include:

* Problem statement
* Proposed solution
* Expected benefits
* Possible implementation ideas

Architectural changes should be discussed before implementation.

---

# Code Review Checklist

Reviewers should verify:

* Correctness
* Readability
* Performance
* Security
* Test coverage
* Documentation
* Coding standards
* Architecture compliance

---

# Contributor Recognition

All contributors who make meaningful improvements to OpenCharge will be acknowledged in project documentation and release notes.

Community collaboration is one of the core values of this project.

---

# Development Environment

Recommended tools:

* Visual Studio Code
* Python 3.12+
* Git
* PySide6
* STM32CubeIDE
* KiCad
* GitHub

---

# Community Values

We encourage:

* Respectful discussions
* Constructive feedback
* Knowledge sharing
* Continuous learning
* Engineering excellence

OpenCharge welcomes contributions from:

* Students
* Engineers
* Researchers
* Hardware Designers
* Software Developers
* Technical Writers

---

# Questions

If you have questions about the project architecture, implementation, or roadmap, please open a GitHub Discussion or Issue.

---

# Thank You

Thank you for helping improve OpenCharge.

Every contribution, no matter how small, helps move the project closer to becoming a complete open-source EV charging platform.

Together, we are building the future of open EV charging.


