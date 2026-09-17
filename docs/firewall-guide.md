# Firewall guide

This document describes the firewall segmentation used in the OT/ Red Team training laboratory.

The environment uses three pfSense firewalls to control communication between the different Purdue-inspired network zones.

## Firewall Overview

| Firewall | Boundary | Purpose |
|---|---|---|
| Firewall 1 | Attacker Network ↔ Internet-facing DMZ | Controls access to the externally reachable services |
| Firewall 2 | Enterprise Network ↔ Industrial DMZ | Restricts movement from corporate IT into the IDMZ |
| Firewall 3 | Industrial DMZ ↔ OT Networks | Controls access from the IDMZ into the Operations, Supervision, and Controller networks |

## Firewall 1 — Perimeter

This firewall separates the external attacker network from the Internet-facing DMZ.

### Interfaces

| Interface | Network |
|---|---|
| External | `10.10.99.0/24` |
| Internal | `10.10.5.0/24` |

### Purpose

The firewall allows the traffic required to reach the vulnerable web server and to complete the initial stages of the training scenario.

---

## Firewall 2 — Enterprise / IDMZ

This firewall separates the Enterprise network from the Industrial DMZ.

### Interfaces

| Interface | Network |
|---|---|
| Enterprise | `10.10.4.0/24` |
| IDMZ | `10.10.35.0/24` |

### Purpose

The firewall restricts communication between the corporate environment and the Industrial DMZ.

---

## Firewall 3 — IDMZ / OT

This firewall separates the Industrial DMZ from the OT networks.

### Interfaces

| Interface | Network |
|---|---|
| IDMZ | `10.10.35.0/24` |
| Operations | `10.10.3.0/24` |
| Supervision | `10.10.2.0/24` |
| Controller | `10.10.1.0/24` |

### Purpose

The firewall controls access from the Industrial DMZ into the OT environment and enforces segmentation between the different operational levels.
