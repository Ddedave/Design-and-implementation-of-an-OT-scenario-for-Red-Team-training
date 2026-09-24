# PLC1_MIXER

This system represents a Programmable Logic Controller deployed in the Level 1.

It runs the control logic for the simulated industrial mixing process using OpenPLC.

# System Information

- Operating system: Debian 13
- CPU: 1 vCPU
- Memory: 1 GB RAM
- Disk: 20 GB
- Host role: Mixing process controller
- IP address: `10.10.1.101/24`
- PLC runtime: OpenPLC
- Industrial protocol: Modbus TCP

## Network Configuration

- IP address: `10.10.1.101/24`
- Network: Level 1 Controller Network
- Modbus TCP port: `502`
- Modbus Unit ID: `1`

The PLC communicates with systems located in the upper OT layers through Modbus TCP.

The main systems interacting with PLC1_MIXER are:

    HMI:        10.10.2.20
    I/O Server: 10.10.3.20

## Role

The PLC represents the controller responsible for the simulated mixing process.

It provides the main control logic for:

- Mixer speed.
- Mixer speed setpoint.
- Tank level.
- Safety speed limit.
- Mixer running state.
- Mixer fault state.
- High-level alarm.
- Tank-level safety interlock.

The intended communication flow is:

    HMI
      ↓
    Modbus TCP
      ↓
    PLC1_MIXER
      ↑
    Modbus TCP
      ↑
    I/O Server

## Services

The system hosts:

- OpenPLC Runtime.
- OpenPLC Web Interface.
- Modbus TCP server.

The PLC runtime must be running for Modbus TCP communication on TCP port `502` to be available.

The OpenPLC web interface may still be reachable even when the PLC runtime is stopped.

## PLC Program

The Structured Text program used by the controller is provided in:

    PLC1.st

The program implements the simulated mixing process and the process conditions used throughout the OT training scenario.

To restore the PLC logic:

1. Install OpenPLC.
2. Open the OpenPLC web interface.
3. Upload:

       PLC1_MIXER.st

4. Compile the program.
5. Start the PLC runtime.
6. Verify that Modbus TCP is listening on:

       10.10.1.101:502

## Initial Process State

The PLC program starts with the following values:

    Mixer speed:       750 RPM
    Target speed:      750 RPM
    Tank level:        65 %
    Safe speed limit:  1500 RPM
    Mixer running:     TRUE
    Tank limit:        TRUE

## Modbus Register Map

PLC1_MIXER exposes the simulated process through Modbus TCP.

### Holding Registers

| Modbus Address | OpenPLC Variable | Purpose |
|---|---|---|
| `40001` / address `1024` | `%MW0` | Current mixer speed |
| `40002` / address `1025` | `%MW1` | Target mixer speed |
| `40003` / address `1026` | `%MW2` | Tank level |
| `40004` / address `1027` | `%MW3` | Safe mixer speed limit |

The holding registers represent:

    mixing_speed_rpm
    target_mixing_speed_rpm
    tank_level_percent
    safe_mixing_limit_rpm

### Coils

| Coil | OpenPLC Variable | Purpose |
|---|---|---|
| `00001` / address `0` | `%QX0.0` | Mixer running state |
| `00002` / address `1` | `%QX0.1` | Mixer fault state |
| `00003` / address `2` | `%QX0.2` | High-level alarm |
| `00004` / address `3` | `%QX0.3` | Tank safety-limit interlock |

The coils represent:

    mixer_running
    mixer_fault_state
    high_level_alarm
    tank_limit_enabled

The HMI and I/O Server currently consume the first three coils.

## Mixer Speed Logic

The mixer speed moves gradually towards the configured target speed.

The program uses a ramp step of:

    15 RPM

If the mixer is running, the current speed increases or decreases until it
reaches the configured target.

If the mixer is stopped, the speed gradually decreases until it reaches:

    0 RPM

The target mixer speed is restricted to:

    0 - 2500 RPM

## Safety Speed Limit

The safety threshold is stored in:

    Modbus address 1027

The configured value is limited to:

    0 - 3000 RPM

A mixer fault is generated when:

    mixing_speed_rpm > safe_mixing_limit_rpm

This results in:

    mixer_fault_state = TRUE


## Tank Process Simulation

The PLC simulates a filling and draining cycle.

The process begins with:

    tank_level_percent = 65

The tank level changes every configured number of PLC scans.

While the mixer is running, the tank fills gradually.

Under normal conditions, the tank safety interlock is enabled:

    tank_limit_enabled = TRUE

and the tank level is limited to:

    70 %

When the upper limit is reached, the simulated process begins draining.

The tank then decreases until it reaches:

    10 %

after which the filling cycle begins again.

## Tank Safety Interlock

The tank safety interlock is represented by:

    Modbus coil 3

When enabled:

    tank_limit_enabled = TRUE

the normal filling ceiling is:

    70 %

When disabled:

    tank_limit_enabled = FALSE

the filling ceiling changes to:

    100 %

This allows the simulated process to enter the high-level alarm range.

The interlock is intentionally writable through Modbus as part of the OT
training scenario.

## High-Level Alarm

The high-level alarm is calculated from the simulated tank level.

The alarm is activated when:

    tank_level_percent >= 90

This results in:

    high_level_alarm = TRUE

The process level is additionally restricted to the range:

    0 - 100 %

## I/O Server Interaction

The I/O Server located at:

    10.10.3.20

reads process telemetry from PLC1_MIXER through Modbus TCP.

It reads the holding-register map and the first three coils and exposes the resulting telemetry to the SCADA Server through its HTTP API.

The intended monitoring flow is:

    PLC1_MIXER
        ↓
    Modbus TCP
        ↓
    I/O Server
        ↓
    HTTP API
        ↓
    SCADA Server

## PLC Execution Cycle

The OpenPLC program is executed using:

    TASK task0(INTERVAL := T#100ms, PRIORITY := 0)

The process simulation uses an internal scan counter before updating the tank level.

The configured value is:

    SCANS_PER_STEP = 20


## Repository Files

This directory contains:

    README.md
    PLC1_MIXER.st

`PLC1_MIXER.st` contains the Structured Text implementation required to recreate the simulated mixer controller.
