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
