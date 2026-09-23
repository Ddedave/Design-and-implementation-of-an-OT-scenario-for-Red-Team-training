# Virtual Machine Specifications

| System | RAM | CPU | Disk | Network Adapters |
|---|---:|---:|---:|---|
| IT Firewall | 512 MB | 1 vCPU | 6 GB | Level 5, Attacker subnet |
| Parrot Attacker | 4 GB | 2 vCPU | 50 GB | Attacker subnet |
| Web Server | 3 GB | 2 vCPU | 20 GB | Level 5 |
| Windows 7 IT Desktop | 3 GB | 2 vCPU | 40 GB | Level 5, Level 4 |
| Database / Grafana | 2 GB | 2 vCPU | 20 GB | Level 4 |
| Backup Server | 1 GB | 1 vCPU | 20 GB | Level 4 |
| IDMZ Firewall | 512 MB | 1 vCPU | 16 GB | Level 4, IDMZ |
| Jump Server | 2 GB | 1 vCPU | 40 GB | IDMZ |
| Historian | 1 GB | 1 vCPU | 20 GB | IDMZ |
| IDMZ-OT Firewall | 512 MB | 1 vCPU | 20 GB | IDMZ, Level 3, Level 2, Level 1 |
| I/O Server | 1 GB | 1 vCPU | 20 GB | Level 3 |
| SCADA | 1 GB | 1 vCPU | 20 GB | Level 3 |
| HMI1 | 2 GB | 2 vCPU | 20 GB | Level 2 |
| PLC1 | 1 GB | 1 vCPU | 20 GB | Level 1 |
