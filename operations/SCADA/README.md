# SCADA Server

This system represents a SCADA Server deployed in the Level 3.

It hosts Node-RED and provides process supervision by consuming data from the I/O Server.

# System Information

- Operating system: Debian 13
- CPU: 1 vCPU
- Memory: 1 GB RAM
- Disk: 20 GB
- Host role: SCADA process supervision server
- Network adapter: Level 3 Operations subnet
- VMware network: `subnet-level-3`
- IP address: `10.10.3.10/24`
- Application: Node-RED
- Dashboard framework: FlowFuse Node-RED Dashboard

## Network Configuration

- IP address: `10.10.3.10/24`
- Network: Level 3 Operations Network
- I/O Server: `10.10.3.20`

The primary network adapter is connected to the Level 3 Operations network.


## Role

The server represents the process supervision system within the Operations network.

It provides a main function within the laboratory:

- Visualisation and interpretation of process data received from the I/O Server.

The intended data flow is:

    PLC1_MIXER
        ↓
    I/O Server
        ↓
    SCADA Server
        ↓
    Node-RED Dashboard

## Services

The system hosts:

- Node-RED
- FlowFuse Node-RED Dashboard
- HTTP-based process monitoring

## Data Source

The SCADA Server retrieves process information from the I/O Server located at:

    10.10.3.20

The Node-RED flow performs HTTP requests to:

    http://10.10.3.20:8080/api/process

The request is executed periodically and the returned data is used to update the SCADA dashboard. :contentReference[oaicite:0]{index=0}

The flow monitors the following values from `PLC1_MIXER`:

    mixing_speed_rpm
    tank_level_percent
    mixer_running

:contentReference[oaicite:1]{index=1} :contentReference[oaicite:2]{index=2} :contentReference[oaicite:3]{index=3}

## Node-RED Dashboard

The exported Node-RED configuration is provided in:

    flows.json

The dashboard is configured under:

    /dashboard

and provides visualisation of:

- Mixer speed.
- Tank level.
- Mixer running state.
- Process alarm conditions. :contentReference[oaicite:4]{index=4}

## Exercise Flags

The dashboard contains flags associated with specific process conditions.

### Mixer Overspeed

Displayed when the mixer speed exceeds 1300 RPM:

    flag{mixer_speed_threshold_exceeded}

### High Tank Level

Displayed when the tank level reaches or exceeds 90%:

    flag{mixer_tank_high_level}

### Mixer Stopped

Displayed when the mixer process is no longer running:

    flag{mixer_process_stopped}

These flags are intentionally included as part of the OT training scenario. :contentReference[oaicite:5]{index=5} :contentReference[oaicite:6]{index=6} :contentReference[oaicite:7]{index=7}

## Node-RED Flow Import

To restore the SCADA configuration:

1. Install Node-RED.
2. Install the required dashboard module:

       @flowfuse/node-red-dashboard@1.30.2

3. Start Node-RED.
4. Open the Node-RED editor.
5. Navigate to **Menu → Import**.
6. Import `flows.json`.
7. Deploy the flow.
8. Verify that the I/O Server is reachable at:

       http://10.10.3.20:8080/api/process

9. Open the Node-RED dashboard.

The exported flow uses:

    @flowfuse/node-red-dashboard 1.30.2

:contentReference[oaicite:8]{index=8}
