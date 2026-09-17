## Firewall 1 — Attacker / Internet-facing DMZ

This pfSense firewall separates the external attacker network from the Level 5 Internet-facing DMZ.

### Interfaces

| Interface | IP Address | Network |
|---|---|---|
| WAN | `10.10.99.1/24` | Attacker Network |
| LAN | `10.10.5.1/24` | Level 5 DMZ |

### Port Forwarding

| WAN Port | Protocol | Forward Target | Purpose |
|---|---|---|---|
| `80` | TCP | `10.10.5.110:80` | Access to the vulnerable web server |
| `4444` | TCP | `10.10.99.5:4444` | Reverse connection channel |
| `8000` | TCP | `10.10.99.5:8000` | Auxiliary attack channel |
| `2222` | TCP | `10.10.99.5:2222` | Auxiliary attack channel |
| `9001` | TCP | `10.10.99.5:9001` | Auxiliary attack channel |

### WAN Firewall Rules

The WAN rules permit only the traffic required by the training scenario before the final deny rule.

| Action | Source | Destination | Protocol / Port | Purpose |
|---|---|---|---|---|
| Pass | `10.10.99.0/24` | This firewall | ICMP | Connectivity testing |
| Pass | Any | Web Server (`10.10.5.110`) | TCP/80 | Access to the vulnerable web application |
| Pass | `10.10.5.0/24` | `10.10.99.5` | TCP/4444 | Reverse connection |
| Pass | `10.10.5.0/24` | `10.10.99.5` | TCP/8000 | Auxiliary channel |
| Pass | `10.10.5.0/24` | `10.10.99.5` | TCP/2222 | Auxiliary channel |
| Pass | `10.10.5.0/24` | `10.10.99.5` | TCP/9001 | Auxiliary channel |
| Block | Any | Any | Any | Default deny |

### LAN Configuration

The Level 5 network uses `10.10.5.1` as its default gateway.

The vulnerable web server is configured as:

- IP address: `10.10.5.110/24`
- Default gateway: `10.10.5.1`

pfSense is configured with automatic outbound NAT.

The current laboratory configuration also retains the default IPv4 `LAN net → any` allow rule. More restrictive rules may be applied in a hardened deployment, but this configuration is retained for the training scenario.

### Notes

The additional ports are intentionally permitted to support controlled Red Team activities such as reverse connections and tunnelling.

These rules are specific to the isolated training environment and are not intended to represent a production perimeter security policy.
