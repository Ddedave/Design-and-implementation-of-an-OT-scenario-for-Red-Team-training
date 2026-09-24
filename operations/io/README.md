# I/O Server

This system represents an I/O Server deployed in the Level 3.

It acts as a protocol gateway between the PLC and the SCADA Server.

# System Information

- Operating system: Debian 13
- CPU: 1 vCPU
- Memory: 1 GB RAM
- Disk: 20 GB
- Host role: OT data collection and protocol gateway
- Network adapter: Level 3 Operations subnet
- VMware network: `subnet-level-3`
- IP address: `10.10.3.20/24`
- Application: Python / Flask
- Protocols: HTTP and Modbus TCP

## Network Configuration

- IP address: `10.10.3.20/24`
- Network: Level 3 Operations Network
- SCADA Server: `10.10.3.10`
- PLC1_MIXER: `10.10.1.101`

The server communicates with the SCADA Server through HTTP and with PLC1_MIXER through Modbus TCP.

## Role

The server represents the protocol gateway between the Operations network and the control layer.

It provides two main functions within the laboratory:

- Collection of process data from PLC1_MIXER through Modbus TCP.
- Exposure of process telemetry to the SCADA Server through an HTTP API.

The intended data flow is:

    PLC1_MIXER
        ↓
    Modbus TCP
        ↓
    I/O Server
        ↓
    HTTP API
        ↓
    SCADA Server

## Services

The system hosts:

- Python 3
- Flask
- PyModbus
- HTTP API on TCP port `8080`
- Modbus TCP client functionality

## PLC Communication

The I/O Server communicates with the following PLC:

    PLC1_MIXER
    IP: 10.10.1.101
    Protocol: Modbus TCP
    Port: 502
    Unit ID: 1

The PLC uses holding registers beginning at address `1024`.

The I/O Server reads the following values:

    mixing_speed_rpm
    target_mixing_speed_rpm
    tank_level_percent
    safe_mixing_limit_rpm

The server also reads three coils beginning at address `0`:

    mixer_running
    mixer_fault_state
    high_level_alarm

The Modbus client is implemented using PyModbus. :contentReference[oaicite:0]{index=0} :contentReference[oaicite:1]{index=1}

## HTTP API

The API implementation is provided in:

    io_api.py

The Flask application listens on:

    0.0.0.0:8080

The main endpoint used by the SCADA Server is:

    http://10.10.3.20:8080/api/process

This endpoint retrieves the current process state from PLC1_MIXER and exposes the resulting telemetry in JSON format. :contentReference[oaicite:2]{index=2} :contentReference[oaicite:3]{index=3}

## API Endpoints

The API provides several endpoints used throughout the laboratory.

### Service Status

    GET /api/status

Returns the current status of the I/O Server and the data quality of the connected PLC.

### PLC Inventory

    GET /api/inventory

Returns information about the PLC assets known by the I/O Server.

### Process Telemetry

    GET /api/process

Returns the process telemetry consumed by the SCADA Server.

Individual assets can also be queried through:

    GET /api/process/<asset>

### Internal Process View

The real process values can be inspected through:

    GET /api/process/real
    GET /api/process/real/<asset>

These endpoints provide the values obtained directly from the PLC before any
telemetry manipulation is applied.

### PLC Register Map

The PLC communication map can be discovered through:

    GET /api/plc/PLC1_MIXER/map

The response identifies:

- PLC IP address.
- Modbus TCP port.
- Unit ID.
- Holding-register base.
- Holding-register mapping.
- Coil base.
- Coil mapping.

Accessing this endpoint also returns the exercise flag:

    flag{plc1_mixer_mapping_discovered}

:contentReference[oaicite:4]{index=4}

## Control Restrictions

The public control endpoint does not allow PLC1_MIXER setpoints to be changed through the normal HTTP API.

Requests to:

    POST /api/control/setpoint

for PLC1_MIXER are rejected.

The API indicates that control and safety parameters must be modified directly through Modbus TCP rather than through the normal SCADA-facing interface. :contentReference[oaicite:5]{index=5}

## Diagnostic Interface

The I/O Server contains internal diagnostic endpoints protected by the `X-Diagnostic-Token` HTTP header.

The configured diagnostic token is:

    diag-ot-internal-only

The diagnostic interface allows internal testing of:

- PLC setpoint changes.
- Safety-limit changes.
- Mixer running state.

These endpoints are intended for laboratory validation and internal testing rather than normal SCADA operation. :contentReference[oaicite:6]{index=6} :contentReference[oaicite:7]{index=7}

## Telemetry Spoofing

The API contains functionality used to simulate false process data injection.

Telemetry spoofing can be enabled through:

    POST /api/debug/spoofing

When enabled, the values presented to the SCADA Server can differ from the actual values retrieved from PLC1_MIXER.

This allows the laboratory to represent a scenario in which the physical process enters an unsafe state while the supervisory interface continues todisplay apparently normal telemetry. :contentReference[oaicite:8]{index=8} :contentReference[oaicite:9]{index=9}

## Exercise Validation

The false-data-injection scenario can be validated through:

    GET /api/validate/false-data-injection/PLC1_MIXER

When the required condition is successfully reproduced, the API returns:

    flag{plc1_mixer_telemetry_spoofed}

If the PLC register map was previously discovered, an additional methodology flag is returned:

    flag{plc1_full_methodology_followed}

These flags are intentionally included as part of the isolated OT Red Team training scenario. :contentReference[oaicite:10]{index=10}

## Application Deployment

The I/O Server application is provided in:

    io_api.py

To deploy the service:

1. Install Python 3.
2. Install the required Python packages:

       pip install flask pymodbus

3. Copy `io_api.py` to the I/O Server.
4. Start the application:

       python3 io_api.py

5. Verify that the service is available at:

       http://10.10.3.20:8080/api/status

6. Verify that process telemetry is available at:

       http://10.10.3.20:8080/api/process

7. Verify that PLC1_MIXER is reachable from the I/O Server through Modbus TCP:

       10.10.1.101:502

The PLC runtime must be running for Modbus TCP communication to succeed.
