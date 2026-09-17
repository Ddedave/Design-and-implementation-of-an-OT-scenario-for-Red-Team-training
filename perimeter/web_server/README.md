# Vulnerable Web Server

This system represents the initial entry point of the Red Team exercise.

It is deployed in the Level 5 Internet-facing DMZ and exposes an intentionally vulnerable web application used during the initial-access stage of the scenario.

## System Information

- Operating system: Debian 13
- CPU: 2 vCPU
- Memory: 3 GB RAM
- Disk: 20 GB
- Web server: Apache2

## Network Configuration

- IP address: `10.10.5.110/24`
- Default gateway: `10.10.5.1`
- Network: Level 5 Internet-facing DMZ

## Role

The server exposes the vulnerable web application used as the initial compromise point of the exercise.

Firewall 1 forwards TCP port 80 from the attacker-facing network to this server.

## Intended Vulnerability

The web application contains an intentionally insecure file-upload mechanism used during the Red Team exercise.

This vulnerability is included exclusively for use within the isolated training environment.

## Attack Path

The intended progression begins with compromise of this server, followed by post-exploitation and pivoting towards the internal Enterprise environment.
