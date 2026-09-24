# HMI

This system represents a Human-Machine Interface deployed in the Level 2.

It hosts Node-RED and provides direct supervision and control of PLC1_MIXER through Modbus TCP.

# System Information

- Operating system: Debian 13
- CPU: 2 vCPU
- Memory: 2 GB RAM
- Disk: 20 GB
- Host role: Human-Machine Interface
- Network adapter: Level 2 Supervision subnet
- VMware network: `subnet-level-2`
- IP address: `10.10.2.20/24`
- Application: Node-RED
- Industrial protocol: Modbus TCP

## Network Configuration

- IP address: `10.10.2.20/24`
- Network: Level 2 Supervision Network
- PLC1_MIXER: `10.10.1.101`

The HMI communicates directly with PLC1_MIXER through Modbus TCP.

## Role

The system represents the operator interface used to supervise and control the mixing process.

It provides two main functions within the laboratory:

- Visualisation of process values obtained directly from PLC1_MIXER.
- Operator control of the mixer and its target speed.

The intended communication flow is:

    HMI
        ↓
    Modbus TCP
        ↓
    PLC1_MIXER

## Services

The system hosts:

- Node-RED
- FlowFuse Node-RED Dashboard
- Modbus TCP client functionality

## PLC Communication

The HMI connects to:

    PLC1_MIXER
    IP: 10.10.1.101
    Protocol: Modbus TCP
    Port: 502
    Unit ID: 1

The HMI reads four holding registers beginning at address `1024`:

    1024 - mixing_speed_rpm
    1025 - target_mixing_speed_rpm
    1026 - tank_level_percent
    1027 - safe_mixing_limit_rpm

The HMI also reads three coils beginning at address `0`:

    0 - mixer_running
    1 - mixer_fault_state
    2 - high_level_alarm

## Process Visualisation

The dashboard provides visualisation of:

- Mixer speed.
- Target mixer speed.
- Tank level.
- Mixer running state.
- Mixer fault state.
- High-level alarm state.

The Node-RED dashboard is available under:

    /dashboard

## Process Control

The HMI provides direct control of selected PLC values.

### Mixer Speed Setpoint

The target mixer speed can be modified through the dashboard.

The HMI writes the new value to:

    Holding Register: 1025

The dashboard limits the operator setpoint to the range:

    0 - 1300

### Mixer Run Control

The dashboard contains Start and Stop controls.

These controls write to:

    Coil: 0

The Start control writes:

    true

The Stop control writes:

    false

## Node-RED Flow

The complete Node-RED configuration is provided in:

    flows.json

To restore the HMI configuration:

1. Install Node-RED.
2. Install the required modules:

       node-red-contrib-modbus@5.60.2
       @flowfuse/node-red-dashboard@1.31.0

3. Start Node-RED.
4. Open the Node-RED editor.
5. Navigate to **Menu → Import**.
6. Import `flows.json`.
7. Deploy the flow.
8. Verify that PLC1_MIXER is reachable at:

       10.10.1.101:502

9. Open the Node-RED dashboard.
