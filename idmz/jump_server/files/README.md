## OT Access Files

The Jump Server contains an `OT_access` directory located at:

    C:\OT_access

This directory contains internal documentation intentionally left on the system as part of the scenario.

The files provide information about the OT network architecture.

### `readme.txt`

Describes the Jump Server as the controlled access point between the Enterprise network and the OT environment.

The documented access path is:

    Enterprise Workstation
        ↓
    Jump Server
        ↓
    Operations Network
        ↓
    SCADA / HMI
        ↓
    PLC Network

The Jump Server is identified as:

    Hostname: jump-idmz01
    IP Address: 10.10.35.120

### `network_segments.txt`

Documents the OT network segmentation:

    IDMZ:                10.10.35.0/24
    Operations / SCADA: 10.10.3.0/24
    Supervisory / HMI:  10.10.2.0/24
    Control / PLC:      10.10.1.0/24

It also identifies the main systems located in the lower Purdue levels.

### `scada_access_notes.txt`

Contains operational access information for the systems located behind the
IDMZ-OT firewall.

The document identifies:

    SCADA Operations: 10.10.3.10
    I/O Server:       10.10.3.20

It also reinforces that direct Enterprise access to SCADA and PLC systems must
remain blocked.

### `flag8.txt`

Contains the Jump Server exercise flag:

    flag{jump_server_idmz_access}
