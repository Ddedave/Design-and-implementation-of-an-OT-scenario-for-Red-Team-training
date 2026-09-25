IDMZ Jump Server - OT Access Notes
----------------------------------

This host is used as the controlled access point between the Enterprise network and the OT environment.

Direct access from Enterprise workstations to OT systems should remain blocked.

Approved access path:

Enterprise Workstation
-> Jump Server
-> Operations Network
-> SCADA / HMI
-> PLC network

Current Jump Server:
Hostname: jump-idmz01
IP Address: 10.10.35.120

Next systems to validate:
- Historian Replica: 10.10.35.130
- SCADA Operations: 10.10.3.10
- I/O Server: 10.10.3.20
- HMI 1: 10.10.2.20
- PLC 1: 10.10.1.10
