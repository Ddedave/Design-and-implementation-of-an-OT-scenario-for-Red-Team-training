# Jump Server

This system represents a Jump Server deployed in the Level 3.5 IDMZ.

It provides controlled remote access between the Enterprise network and the OT environment.

# System Information

- Operating system: Windows Server 2019 Standard Evaluation
- CPU: 1 vCPU
- Memory: 2 GB RAM
- Disk: 40 GB
- Host role: IDMZ jump server
- Network adapter: Level 3.5 Industrial DMZ subnet
- VMware network: `subnet-idmz-35`
- IP address: `10.10.35.120/24`

## Network Configuration

- IP address: `10.10.35.120/24`
- Default gateway: `10.10.35.1`
- Network: Level 3.5 Industrial DMZ

Static routes are used to reach the OT networks through the IDMZ-OT firewall:

    10.10.3.0/24 via 10.10.35.254
    10.10.2.0/24 via 10.10.35.254
    10.10.1.0/24 via 10.10.35.254

## Role

The server represents the controlled access point between the Enterprise network and the OT environment.

The intended progression is:

    Enterprise Network
        ↓
    Grafana / Backup discovery
        ↓
    Jump Server identified
        ↓
    RDP access to 10.10.35.120
        ↓
    Industrial DMZ
        ↓
    OT systems

## Services

The system provides:

- RDP access
- Controlled access towards OT systems
- Administrative access to selected OT services
- Network routing towards lower Purdue levels

## Maintenance Account

The Grafana dashboard exposes the following temporary maintenance credentials:

    Host: 10.10.35.120
    Protocol: RDP
    Username: plant_maintenance
    Password: TemporaryPlantMaint2026!

These credentials are intentionally exposed as part of the isolated training scenario.

## Installed Tools

The Jump Server includes utilities required to access and validate selected OT services from the IDMZ.

Installed tools include:

- `modpoll` — Modbus TCP client used to query and interact with Modbus-enabled devices.
- Mozilla Firefox — Used to access internal web interfaces and management services.
- Remote Desktop components.
- Standard Windows administrative and networking tools.

These tools allow the Jump Server to function as the main workstation for
controlled access into the lower Purdue levels.

## OT Access

The Jump Server is allowed to communicate with selected systems in the OT environment.

Examples include:

    SCADA Server: 10.10.3.10
    I/O Server: 10.10.3.20
    PLC1_MIXER: 10.10.1.101
