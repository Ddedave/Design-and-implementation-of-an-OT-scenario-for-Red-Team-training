# IT Desktop

This system is a legacy workstation used in the Enterprise stage of the Red Team.

The workstation is intentionally deployed with an obsolete Windows operating system and vulnerable network services to reproduce a realistic legacy asset that still exist inside industrial environments.

## System Information

- Operating system: Windows 7 Ultimate SP1 x64
- Build: 7601
- CPU: 2 vCPU
- Memory: 4 GB RAM
- Disk: 40 GB
- Host role: Corporate IT workstation
- Network role: Pivot between the Level 5 DMZ and the Level 4 Enterprise network

## Network Configuration

The workstation is dual-homed and connects to both the Level 5 DMZ and the Enterprise network.

| Interface | IP Address | Network |
|---|---|---|
| NIC 1 | `10.10.5.102/24` | Level 5 Internet-facing DMZ |
| NIC 2 | `10.10.4.102/24` | Level 4 Enterprise Network |

This dual-homed configuration allows the workstation to act as the next pivot point after compromise of the vulnerable Web Server.

The Enterprise-side address `10.10.4.102` is also authorised by Firewall 2 to communicate with the Jump Server located in the Industrial DMZ.

## Role

The IT Desktop represents an outdated corporate workstation connected to both the Internet-facing DMZ and the internal Enterprise network.

The intended exercise progression is:

    Vulnerable Web Server
            ↓
    Pivot into Level 5
            ↓
    IT Desktop
            ↓
    Enterprise Network
            ↓
    Industrial DMZ

After compromising the Web Server, the student discovers the Windows workstation and reaches its exposed SMB service through the existing pivot.

Successful compromise of the workstation provides access to the Level 4 Enterprise network.

## Default Laboratory Credentials

The following credentials are intentionally configured for the training environment:

- Username: `IT_desktop`
- Password: `desktop`

## Exposed Services

The workstation exposes services required by the training scenario.

| Service | Port | Purpose |
|---|---:|---|
| SMB | TCP/445 | Vulnerable SMB service used during exploitation |
| RDP | TCP/3389 | Interactive access after compromise |

## Intended Vulnerability

The workstation runs an intentionally outdated Windows 7 SP1 installation vulnerable to MS17-010.

The SMB service is deliberately left exposed and the system is maintained in a vulnerable state for training purposes.

Windows Firewall is disabled in the laboratory configuration to ensure that the intended SMB-based exploitation path remains accessible.

This configuration must never be reproduced on a production or Internet-connected system.

## Initial Setup

Create a Windows 7 Ultimate SP1 x64 virtual machine with approximately:

- 2 vCPU
- 4 GB RAM
- 40 GB virtual disk
- Two virtual network adapters

Configure the two network interfaces with:

    10.10.5.102/24
    10.10.4.102/24

The virtual network adapters must be connected to their corresponding isolated VMware networks.

## User Configuration

Create the laboratory user:

    Username: IT_desktop
    Password: desktop

The account is used during the post-exploitation stage of the exercise and for subsequent RDP access.

## SMB Configuration

SMB must be enabled and reachable on:

    TCP/445

The Windows installation is intentionally maintained without the security updates that remediate MS17-010.

The vulnerable SMB service provides the exploitation path used during this stage of the exercise.

## Remote Desktop

Remote Desktop is enabled to provide interactive access to the workstation after compromise.

RDP listens on:

    TCP/3389

The `IT_desktop` account must be permitted to log in through Remote Desktop.

## Windows Firewall

Windows Firewall is intentionally disabled for the laboratory scenario.

This ensures that the SMB and RDP services required by the exercise remain reachable through the isolated network.

This configuration is intentionally insecure and should only be used inside the training environment.

## Exercise Progression

The intended progression through this machine is:

    Discovery of IT Desktop
            ↓
    SMB enumeration
            ↓
    Exploitation of vulnerable SMB service
            ↓
    SYSTEM-level access
            ↓
    Credential recovery
            ↓
    RDP access
            ↓
    Pivot into the Enterprise network

The workstation therefore serves both as a privilege-compromise target and as the bridge into the internal corporate environment.

## Relationship with Firewall 2

Firewall 2 separates the Enterprise network from the Industrial DMZ.

The Enterprise-side interface of this workstation uses:

    10.10.4.102

Firewall 2 specifically permits this system to communicate with the Jump Server at:

    10.10.35.120

The permitted communication includes:

- ICMP for connectivity validation.
- TCP/3389 for RDP access to the Jump Server.

This restriction ensures that progression toward the Industrial DMZ occurs through the intended compromised workstation rather than through arbitrary Enterprise hosts.

## Security Notice

This virtual machine is intentionally vulnerable.

It contains:

- An obsolete operating system.
- A deliberately vulnerable SMB service.
- Weak laboratory credentials.
- Disabled host firewall protections.
- Exposed remote-access services.

The system must only be deployed inside an isolated cybersecurity training environment.
