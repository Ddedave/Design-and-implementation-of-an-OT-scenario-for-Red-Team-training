# Attacker Workstation

This system represents the external attacker workstation used to perform the Red Team exercise.

It is deployed outside the internal laboratory networks and is used as the starting point for the complete attack path.

# System Information

- Operating system: Parrot OS
- CPU: 2 vCPU
- Memory: 4 GB RAM
- Disk: 50 GB
- Host role: External attacker / student workstation
- Network adapter: Attacker subnet
- IP address: `10.10.99.5/24`
- Application: Local Flag Submission Portal
- Web framework: Flask
- Local database: SQLite

## Network Configuration

- IP address: `10.10.99.5/24`
- Network: Attacker Network
- Gateway: `10.10.99.1`

The attacker workstation is connected to the external attacker network used by the laboratory.

The intended communication flow begins from this system:

    Attacker Workstation
            ↓
    Internet-facing DMZ
            ↓
    Enterprise Network
            ↓
    Industrial DMZ
            ↓
    OT Networks

## Role

The system represents the student's initial position before any compromise of the laboratory infrastructure.

It provides two main functions within the laboratory:

- Execution of the Red Team exercise against the simulated environment.
- Local submission and tracking of flags obtained during the exercise.

The workstation is used to perform reconnaissance, exploitation, pivoting, remote access, and OT interaction throughout the scenario.

## Services

The system hosts:

- Parrot OS offensive security tooling.
- Python 3.
- Flask.
- SQLite.
- Remina
- Local Flag Submission Portal.

## Flag Submission Portal

The attacker workstation includes a lightweight local web application used to validate the flags obtained during the exercise.

The portal is available at:

    http://127.0.0.1:5000

The application provides:

- Twelve exercise stages.
- Flag validation.
- Stage completion tracking.
- Progress bar.
- Per-stage hints.
- Persistent progress using SQLite.

The portal is intended to run only on the attacker workstation.

## Portal Structure

The complete portal configuration is provided in:

    flag-portal/

The directory contains:

    flag-portal/
    ├── app.py
    ├── templates/
    │   └── index.html
    └── static/
        └── style.css

The progress database is generated automatically during execution:

    progress.db

This database should not be included in the repository.

## Flask Installation

Flask is required to run the portal.

To create a Python virtual environment:

1. Navigate to the portal directory:

       cd flag-portal

2. Create the virtual environment:

       python3 -m venv venv

3. Activate it:

       source venv/bin/activate

4. Install Flask:

       python -m pip install Flask

If the attacker workstation does not have Internet access, Flask and its dependencies can be downloaded on another system and transferred to the virtual machine.

Example offline installation:

    python -m pip install --no-index --find-links=/path/to/packages Flask

## Running the Portal

To start the flag submission portal:

1. Navigate to the portal directory:

       cd flag-portal

2. Activate the virtual environment:

       source venv/bin/activate

3. Start the Flask application:

       python app.py

4. Open the local browser and navigate to:

       http://127.0.0.1:5000

5. Verify that the OT Red Team Assessment portal is displayed.

## Progress Persistence

The application uses SQLite to preserve the student's progress.

The following file is created automatically:

    progress.db

Completed stages remain marked after:

- Refreshing the browser.
- Restarting the Flask application.

To reset the exercise progress:

1. Stop the Flask application.
2. Delete the database:

       rm progress.db

3. Start the application again.

A new empty database will be generated automatically.
