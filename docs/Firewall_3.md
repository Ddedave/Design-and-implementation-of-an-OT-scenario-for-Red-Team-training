## Firewall 3 — IDMZ / OT

This pfSense firewall separates the IDMZ from the operational technology networks and provides the routing and filtering boundaries for Purdue Levels 3, 2 and 1.

### Interfaces

| Interface | IP Address | Network |
|---|---|---|
| WAN | `10.10.35.254/24` | Industrial DMZ |
| LAN | `10.10.3.1/24` | Level 3 — Operations |
| OPT1 | `10.10.2.1/24` | Level 2 — Supervision |
| OPT2 | `10.10.1.1/24` | Level 1 — Control |

### NAT

Automatic outbound NAT is enabled.

### IDMZ-side rules

Access from the Industrial DMZ into the OT environment is restricted to the Jump Server at `10.10.35.120`.

| Action | Source | Destination | Protocol / Port | Purpose |
|---|---|---|---|---|
| Pass | `10.10.35.120` | `10.10.3.10` | TCP/1880 | Access to the SCADA Node-RED interface |
| Pass | `10.10.35.120` | `10.10.3.20` | TCP/8080 | Access to the I/O Server API |
| Pass | `10.10.35.120` | `10.10.3.20` | TCP/22 | SSH access to the I/O Server |
| Pass | `10.10.35.120` | `10.10.3.20` | ICMP | Connectivity testing |
| Pass | `10.10.35.120` | `10.10.3.10` | ICMP | Connectivity testing |
| Pass | `10.10.35.120` | `10.10.1.101` | TCP | Access to the OpenPLC web interface |
| Pass | `10.10.35.120` | Level 1 / OPT2 | ICMP | Connectivity testing to the Control network |
| Pass | `10.10.35.120` | This firewall | TCP/80 | pfSense WebConfigurator access |
| Pass | `10.10.35.120` | Any | ICMP | Firewall / routing validation |

### Operations Network Rules

The Level 3 Operations network uses `10.10.3.1` as its gateway.

The current configuration includes:

- ICMP from the I/O Server (`10.10.3.20`) to the firewall.
- The default IPv4 `LAN net → any` rule.

### Supervision Network Rules

The Level 2 Supervision network uses `10.10.2.1` as its gateway.

The HMI at `10.10.2.20` is permitted to communicate with the PLC at `10.10.1.101` over Modbus/TCP:

| Action | Source | Destination | Protocol / Port | Purpose |
|---|---|---|---|---|
| Pass | `10.10.2.20` | `10.10.1.101` | TCP/502 | HMI to PLC Modbus/TCP |
| Pass | `10.10.2.20` | Any | ICMP | Connectivity testing |

### Control Network Rules

The Level 1 Control network uses `10.10.1.1` as its gateway.

The PLC at `10.10.1.101` is permitted to send ICMP traffic for connectivity testing.

### Notes

This firewall is the primary segmentation boundary protecting the OT environment. The intended path into the OT networks originates from the Jump Server in the Industrial DMZ.

The configuration intentionally permits only the services required by the training scenario, including SCADA access, the I/O Server API, SSH, Modbus/TCP and limited ICMP diagnostics.
