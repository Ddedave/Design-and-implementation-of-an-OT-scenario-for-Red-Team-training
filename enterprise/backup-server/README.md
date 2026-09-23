# Backup Server

This system represents a Backup Server deployed in the Level 4 Enterprise network.

It hosts an SMB file share used to store internal backup and operational documentation.

# System Information

- Operating system: Debian 13
- CPU: 2 vCPU
- Memory: 2 GB RAM
- Disk: 20 GB
- Host role: Enterprise backup server
- Network adapter: Level 4 Enterprise subnet
- IP address: `10.10.4.107/24`

## Network Configuration

- IP address: `10.10.4.107/24`
- Network: Level 4 Enterprise Network

## Role

The server represents an internal Enterprise asset discovered after compromise of the IT Desktop.

It provides a main function within the laboratory:

- SMB-based backup storage and internal file sharing.

The intended progression is:

    Web Server
        ↓
    IT Desktop
        ↓
    Discovery of 10.10.4.107
        ↓
    Backup Server
        ↓
    SMB Share
        ↓
    Migration and maintenance information
        ↓
    Grafana Server
        ↓
    Industrial DMZ information

## Services

The system hosts:

- Samba
- SMB file sharing

## Discovery

The address is obtained from the internal note stored on the IT Desktop:

    Update notes

    Database moved to 10.10.4.108
    Backup server is now at 10.10.4.107

This information provides the next set of targets within the network.

## SMB Share

The Backup Server exposes an SMB share used as an internal backup repository.

The share is available at:

    \\10.10.4.107\backups

The contents of this share are used as part of the Enterprise discovery and lateral movement phase of the exercise.

## Backup Files

The SMB share contains the following files:

### `readme.txt`

Provides a short description of the Enterprise backup repository and indicates
that migration activities and temporary maintenance accounts are still being
reviewed.

### `migration_notes.txt`

Contains information about the migration of the DB/Grafana server to:

    10.10.4.108

The note identifies the following services:

    Grafana: http://10.10.4.108:3000
    MariaDB: local access only
    SSH: enabled for Linux maintenance

It also indicates that temporary Grafana and Linux maintenance credentials
have not yet been rotated.

### `linux_maintenance.txt`

Contains temporary Linux maintenance access information for the DB/Grafana
Server:

    Server: 10.10.4.108
    Protocol: SSH
    Port: 22
    User: dbuser
    Temporary password: dbpassworduser123

These credentials are intentionally exposed as part of the laboratory scenario.

### `backup_inventory.txt`

Contains database inventory configuration information:

    DB_HOST=10.10.4.108
    DB_PORT=3306
    DB_NAME=enterprise_db
    DB_USER=backup_reader
    DB_PASS=backup2026

### `IDMZ_notes.txt`

Contains information about the future Industrial DMZ access architecture.

The note identifies the Jump Server:

    10.10.35.120

and the downstream OT systems:

    SCADA Operations: 10.10.3.10
    I/O Server: 10.10.3.20

It also states that direct Enterprise access to OT systems should be blocked and that approved access must pass through the Jump Server.
