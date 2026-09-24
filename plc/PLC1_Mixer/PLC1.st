PROGRAM PLC1_MIXER
VAR
    
    mixing_speed_rpm        AT %MW0 : INT := 750;
    target_mixing_speed_rpm AT %MW1 : INT := 750;
    tank_level_percent      AT %MW2 : INT := 65;
    safe_mixing_limit_rpm   AT %MW3 : INT := 1500;

    mixer_running       AT %QX0.0 : BOOL := TRUE;
    mixer_fault_state   AT %QX0.1 : BOOL := FALSE;
    high_level_alarm    AT %QX0.2 : BOOL := FALSE;
    tank_limit_enabled  AT %QX0.3 : BOOL := TRUE;
END_VAR

VAR
    draining     : BOOL := FALSE;
    scan_counter : INT  := 0;

    SCANS_PER_STEP : INT := 20;

    RAMP_STEP_RPM : INT := 15;

    fill_ceiling : INT := 70;
END_VAR

IF target_mixing_speed_rpm < 0 THEN
    target_mixing_speed_rpm := 0;
END_IF;
IF target_mixing_speed_rpm > 2500 THEN
    target_mixing_speed_rpm := 2500;
END_IF;

IF safe_mixing_limit_rpm < 0 THEN
    safe_mixing_limit_rpm := 0;
END_IF;
IF safe_mixing_limit_rpm > 3000 THEN
    safe_mixing_limit_rpm := 3000;
END_IF;

IF NOT mixer_running THEN
    IF mixing_speed_rpm > 0 THEN
        mixing_speed_rpm := mixing_speed_rpm - RAMP_STEP_RPM;
        IF mixing_speed_rpm < 0 THEN
            mixing_speed_rpm := 0;
        END_IF;
    END_IF;
ELSE
    IF mixing_speed_rpm < target_mixing_speed_rpm THEN
        mixing_speed_rpm := mixing_speed_rpm + RAMP_STEP_RPM;
        IF mixing_speed_rpm > target_mixing_speed_rpm THEN
            mixing_speed_rpm := target_mixing_speed_rpm;
        END_IF;
    ELSIF mixing_speed_rpm > target_mixing_speed_rpm THEN
        mixing_speed_rpm := mixing_speed_rpm - RAMP_STEP_RPM;
        IF mixing_speed_rpm < target_mixing_speed_rpm THEN
            mixing_speed_rpm := target_mixing_speed_rpm;
        END_IF;
    END_IF;
END_IF;

scan_counter := scan_counter + 1;

IF scan_counter >= SCANS_PER_STEP THEN
    scan_counter := 0;

    IF NOT draining THEN
        IF mixer_running THEN
            tank_level_percent := tank_level_percent + 1;
        END_IF;

        IF tank_limit_enabled THEN
            fill_ceiling := 70;
        ELSE
            fill_ceiling := 100;
        END_IF;

        IF tank_level_percent >= fill_ceiling THEN
            tank_level_percent := fill_ceiling;
            draining := TRUE;
        END_IF;
    ELSE
        tank_level_percent := tank_level_percent - 2;

        IF tank_level_percent <= 10 THEN
            tank_level_percent := 10;
            draining := FALSE;
        END_IF;
    END_IF;
END_IF;

(* Saturacion de seguridad adicional, por si el nivel llega a
   escribirse externamente fuera de este ciclo. *)
IF tank_level_percent < 0 THEN
    tank_level_percent := 0;
END_IF;
IF tank_level_percent > 100 THEN
    tank_level_percent := 100;
END_IF;

mixer_fault_state := (mixing_speed_rpm > safe_mixing_limit_rpm);
high_level_alarm  := (tank_level_percent >= 90);

END_PROGRAM

CONFIGURATION Config0

    RESOURCE Res0 ON PLC
        TASK task0(INTERVAL := T#100ms, PRIORITY := 0);
        PROGRAM instance0 WITH task0 : PLC1_MIXER;
    END_RESOURCE

END_CONFIGURATION