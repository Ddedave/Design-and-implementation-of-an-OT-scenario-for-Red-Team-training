# Grafana Server

This system represents a Grafana server deployed in the Level 4 Enterprise network.

It hosts Grafana for data visualisation and monitoring.

# System Information

- Operating system: Debian 13
- CPU: 2 vCPU
- Memory: 2 GB RAM
- Disk: 20 GB
- Host role: Enterprise database and monitoring server
- Network adapter: Level 4 Enterprise subnet
- IP address: `10.10.4.108/24`

## Network Configuration

- IP address: `10.10.4.108/24`
- Network: Level 4 Enterprise Network

## Role

The server represents an internal Enterprise asset discovered after compromise of the IT Desktop.

It provides a main function within the laboratory:

- Grafana monitoring and visualisation.

The intended progression is:

    Web Server
        ↓
    IT Desktop
        ↓
    Discovery of 10.10.4.108
        ↓
    Grafana Server

## Services

The system hosts:

- Grafana
- Database services

The exact ports, versions and credentials used by the laboratory should be configured according to the deployment instructions provided in this directory.

## Discovery

The address is obtained from the internal note stored on the IT Desktop:

    Update notes

    Database moved to 10.10.4.108
    Backup server is now at 10.10.4.107

This information provides the next set of targets within the network.

## Dashboard Import

The Grafana dashboard configuration is provided in:

    idmz-ot-access-overview.json

To restore the dashboard:

1. Open Grafana.
2. Navigate to **Dashboards → New → Import**.
3. Upload the JSON file.
4. Confirm the dashboard import.
5. Verify that the dashboard appears as:

       IDMZ Migration / OT Access Overview
