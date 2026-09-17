# Network Addressing

This document defines the network segmentation and IP addressing scheme used throughout the OT Red Team training laboratory.

The environment follows a Purdue architecture in which each network level is deployed on an independent subnet.

## Network Segments

| Zone | Purdue Level | Subnet | Purpose |
|---|---:|---|---|
| Attacker Network | External | `10.10.99.0/24` | Student / attacker workstation |
| Internet-facing DMZ | Level 5 | `10.10.5.0/24` | Public-facing services |
| Enterprise Network | Level 4 | `10.10.4.0/24` | Corporate IT systems |
| Industrial DMZ | Level 3.5 | `10.10.35.0/24` | Boundary between IT and OT |
| Operations Network | Level 3 | `10.10.3.0/24` | SCADA and data acquisition |
| Supervision Network | Level 2 | `10.10.2.0/24` | Human-Machine Interface |
| Controller Network | Level 1 | `10.10.1.0/24` | PLC and process control |

## Host Addressing

| System | IP Address | Network |
|---|---|---|
| Attacker Workstation | `10.10.99.5` | Attacker Network |
| Web Server | `10.10.5.110` | Level 5 |
| IT Desktop | `10.10.5.102` | Level 5 |
| IT Desktop | `10.10.4.102` | Level 4 |
| Backup Server | `10.10.4.107` | Level 4 |
| Database / Grafana Server | `10.10.4.108` | Level 4 |
| Jump Server | `10.10.35.120` | Level 3.5 |
| Historian | `10.10.35.130` | Level 3.5 |
| SCADA Server | `10.10.3.10` | Level 3 |
| I/O Server | `10.10.3.20` | Level 3 |
| HMI | `10.10.2.20` | Level 2 |
| PLC1_MIXER | `10.10.1.101` | Level 1 |
