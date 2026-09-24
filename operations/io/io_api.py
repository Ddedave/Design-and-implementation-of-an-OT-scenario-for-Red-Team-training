from flask import Flask, jsonify, request
from datetime import datetime, timezone
from functools import wraps

try:
    from pymodbus.client import ModbusTcpClient
except ImportError:
    ModbusTcpClient = None
app = Flask(__name__)

DIAG_TOKEN = "diag-ot-internal-only"

def diagnostic_protected(func):
    """
    Protege endpoints de uso interno/testing (no para el estudiante).
    Requiere cabecera X-Diagnostic-Token.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get("X-Diagnostic-Token")
        if token != DIAG_TOKEN:
            return jsonify({
                "status": "error",
                "message": "Forbidden: diagnostic token missing or invalid"
            }), 403
        return func(*args, **kwargs)
    return wrapper
plc_inventory = {
    "PLC1_MIXER": {
        "ip": "10.10.1.101",
        "protocol": "modbus_tcp",
        "port": 502,
        "role": "Mixing process controller",
        "unit_id": 1,
        "holding_register_base": 1024,
        "holding_registers": {
            "mixing_speed_rpm": 0,
            "target_mixing_speed_rpm": 1,
            "tank_level_percent": 2,
            "safe_mixing_limit_rpm": 3
        },
        "coil_base": 0,
        "coils": {
            "mixer_running": 0,
            "mixer_fault_state": 1,
            "high_level_alarm": 2
        },
        "mode": "modbus_live"
    }
}

real_process_state = {
    "PLC1_MIXER": {
        "asset": "PLC1_MIXER",
        "mode": "modbus_live",
        "mixing_speed_rpm": 0,
        "target_mixing_speed_rpm": 0,
        "tank_level_percent": 0,
        "safe_mixing_limit_rpm": 0,
        "mixer_running": False,
        "mixer_fault_state": False,
        "high_level_alarm": False,
        "data_quality": "UNKNOWN",
        "last_update": None
    }
}

spoofing_state = {
    "PLC1_MIXER": {
        "enabled": False,
        "reported_mixing_speed_rpm": 750,
        "reported_target_mixing_speed_rpm": 750,
        "reported_tank_level_percent": 65,
        "reported_mixer_fault_state": False,
        "reported_high_level_alarm": False
    }
}

discovery_state = {
    "PLC1_MIXER": {"map_discovered": False, "discovered_at": None}
}


setpoint_audit_log = []
control_audit_log = [] 


def _now():
    return datetime.now(timezone.utc).isoformat()

def asset_exists(asset):
    return asset in real_process_state

def parse_bool(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in ("true", "1", "yes", "on"):
            return True
        if normalized in ("false", "0", "no", "off", ""):
            return False
        raise ValueError(f"Cannot parse boolean from string: {value!r}")
    raise ValueError(f"Cannot parse boolean from type: {type(value)}")

def _modbus_call(method, *, address, unit_id, **kwargs):
    last_error = None
    for unit_keyword in ("device_id", "slave", "unit"):
        try:
            return method(address=address, **kwargs, **{unit_keyword: unit_id})
        except TypeError as exc:
            last_error = exc
    if last_error:
        raise last_error
    raise RuntimeError("Unable to execute Modbus request")

def _new_modbus_client(plc):
    if ModbusTcpClient is None:
        raise RuntimeError("pymodbus no esta instalado en el I/O Server.")
    return ModbusTcpClient(host=plc["ip"], port=plc["port"], timeout=2)

def read_plc1_modbus():
    plc = plc_inventory["PLC1_MIXER"]
    client = _new_modbus_client(plc)
    try:
        if not client.connect():
            raise ConnectionError(f"No se pudo conectar a PLC1_MIXER ({plc['ip']}:{plc['port']})")
        holding_result = _modbus_call(
            client.read_holding_registers,
            address=plc["holding_register_base"],
            count=4,
            unit_id=plc["unit_id"]
        )
        if holding_result.isError():
            raise RuntimeError(f"Error leyendo holding registers: {holding_result}")
        coil_result = _modbus_call(
            client.read_coils,
            address=plc["coil_base"],
            count=3,
            unit_id=plc["unit_id"]
        )
        if coil_result.isError():
            raise RuntimeError(f"Error leyendo coils: {coil_result}")

        regs = holding_result.registers
        bits = coil_result.bits
        state = real_process_state["PLC1_MIXER"]

        state.update({
            "asset": "PLC1_MIXER",
            "mode": "modbus_live",
            "mixing_speed_rpm": int(regs[0]),
            "target_mixing_speed_rpm": int(regs[1]),
            "tank_level_percent": int(regs[2]),
            "safe_mixing_limit_rpm": int(regs[3]),
            "mixer_running": bool(bits[0]),
            "mixer_fault_state": bool(bits[1]),
            "high_level_alarm": bool(bits[2]),
            "data_quality": "GOOD",
            "last_update": _now()
        })
        return state.copy()

    except Exception:
        real_process_state["PLC1_MIXER"]["data_quality"] = "BAD"
        real_process_state["PLC1_MIXER"]["last_update"] = _now()
        raise
    finally:
        client.close()

def write_plc1_holding(tag, value):
    plc = plc_inventory["PLC1_MIXER"]
    if tag not in plc["holding_registers"]:
        raise ValueError(f"Unknown PLC1 holding-register tag: {tag}")
    address = plc["holding_register_base"] + plc["holding_registers"][tag]
    client = _new_modbus_client(plc)
    try:
        if not client.connect():
            raise ConnectionError(f"No se pudo conectar a PLC1_MIXER ({plc['ip']}:{plc['port']})")
        result = _modbus_call(client.write_register, address=address, value=int(value), unit_id=plc["unit_id"])
        if result.isError():
            raise RuntimeError(f"Error escribiendo registro Modbus: {result}")
    finally:
        client.close()

def write_plc1_coil(tag, value):
    plc = plc_inventory["PLC1_MIXER"]
    if tag not in plc["coils"]:
        raise ValueError(f"Unknown PLC1 coil tag: {tag}")
    address = plc["coil_base"] + plc["coils"][tag]
    client = _new_modbus_client(plc)
    try:
        if not client.connect():
            raise ConnectionError(f"No se pudo conectar a PLC1_MIXER ({plc['ip']}:{plc['port']})")
        result = _modbus_call(client.write_coil, address=address, value=bool(value), unit_id=plc["unit_id"])
        if result.isError():
            raise RuntimeError(f"Error escribiendo coil Modbus: {result}")
    finally:
        client.close()

def update_process_safety(asset):
    if asset == "PLC1_MIXER":
        return read_plc1_modbus()
    raise ValueError(f"Unknown asset: {asset}")


def update_all_process_safety():
    errors = {}
    for asset in real_process_state:
        try:
            update_process_safety(asset)
        except Exception as exc:
            errors[asset] = str(exc)
    return errors

def get_scada_view(asset):
    state = real_process_state[asset]
    spoof = spoofing_state[asset]
    if not spoof["enabled"]:
        return {**state, "telemetry_source": "modbus_live", "spoofing_enabled": False}

    return {
        "asset": "PLC1_MIXER",
        "mode": state["mode"],
        "mixing_speed_rpm": spoof["reported_mixing_speed_rpm"],
        "target_mixing_speed_rpm": spoof["reported_target_mixing_speed_rpm"],
        "tank_level_percent": spoof["reported_tank_level_percent"],
        "safe_mixing_limit_rpm": state["safe_mixing_limit_rpm"],
        "mixer_running": state["mixer_running"],
        "mixer_fault_state": spoof["reported_mixer_fault_state"],
        "high_level_alarm": spoof["reported_high_level_alarm"],
        "data_quality": "GOOD",
        "last_update": state["last_update"],
        "telemetry_source": "spoofed",
        "spoofing_enabled": True
    }

@app.route("/api/status", methods=["GET"])

def status():
    errors = update_all_process_safety()
    return jsonify({
        "service": "io-server",
        "status": "degraded" if errors else "running",
        "role": "plc-to-http gateway",
        "mode": "modbus_live",
        "assets": {
            asset: {"mode": real_process_state[asset]["mode"], "data_quality": real_process_state[asset]["data_quality"]}
            for asset in real_process_state
        },
        "errors": errors
    })

@app.route("/api/inventory", methods=["GET"])

def inventory():
    return jsonify({
        "plcs": {
            asset: {"role": data["role"], "protocol": data["protocol"], "mode": data["mode"]}
            for asset, data in plc_inventory.items()
        },
        "hint": "IPs y puertos no se publican aqui. Escanea el segmento de control desde una zona autorizada."
    })

@app.route("/api/process", methods=["GET"])

def process_all():
    errors = update_all_process_safety()
    return jsonify({
        "mode": "modbus_live",
        "assets": {asset: get_scada_view(asset) for asset in real_process_state},
        "errors": errors
    })

@app.route("/api/process/<asset>", methods=["GET"])

def process_asset(asset):
    if not asset_exists(asset):
        return jsonify({"status": "error", "message": "Unknown asset", "valid_assets": list(real_process_state.keys())}), 404
    try:
        update_process_safety(asset)
    except Exception as exc:
        return jsonify({"status": "error", "asset": asset, "message": "Unable to refresh process state", "detail": str(exc)}), 503
    return jsonify(get_scada_view(asset))

@app.route("/api/process/real", methods=["GET"])

def real_process_all():
    errors = update_all_process_safety()
    return jsonify({"mode": "modbus_live", "telemetry_source": "real_internal_view", "assets": real_process_state, "errors": errors})

@app.route("/api/process/real/<asset>", methods=["GET"])

def real_process_asset(asset):
    if not asset_exists(asset):
        return jsonify({"status": "error", "message": "Unknown asset", "valid_assets": list(real_process_state.keys())}), 404
    try:
        update_process_safety(asset)
    except Exception as exc:
        return jsonify({"status": "error", "asset": asset, "message": "Unable to refresh real process state", "detail": str(exc)}), 503
    return jsonify({**real_process_state[asset], "telemetry_source": "real_internal_view"})
@app.route("/api/plc/<asset>/map", methods=["GET"])
def plc_map(asset):
    if asset not in plc_inventory:
        return jsonify({"status": "error", "message": "Unknown PLC asset", "valid_assets": list(plc_inventory.keys())}), 404
    discovery_state[asset]["map_discovered"] = True
    discovery_state[asset]["discovered_at"] = _now()
    plc = plc_inventory[asset]

    response = {
        "asset": asset,
        "plc": {
            "ip": plc["ip"], "protocol": plc["protocol"], "port": plc["port"],
            "role": plc["role"], "unit_id": plc["unit_id"], "mode": plc["mode"]
        },
        "register_map": {
            "holding_register_base": plc["holding_register_base"],
            "holding_registers": plc["holding_registers"],
            "coil_base": plc["coil_base"],
            "coils": plc["coils"]
        }
    }

    if asset == "PLC1_MIXER":
        response["flag"] = "flag{plc1_mixer_mapping_discovered}"
    return jsonify(response)

@app.route("/api/control/setpoint", methods=["POST"])

def setpoint():
    data = request.get_json(silent=True) or {}
    required_fields = ["asset", "tag", "value"]
    missing = [f for f in required_fields if f not in data]
    if missing:
        return jsonify({"status": "error", "message": "Missing required fields", "missing": missing}), 400
    asset = data["asset"]
    if not asset_exists(asset):
        return jsonify({"status": "error", "message": "Unknown asset", "valid_assets": list(real_process_state.keys())}), 404
    try:
        int(data["value"])
    except (ValueError, TypeError):
        return jsonify({"status": "error", "message": "value must be an integer"}), 400
    if asset == "PLC1_MIXER":
        return jsonify({
            "status": "error",
            "message": (
                "PLC1_MIXER control is not available through this API. "
                "This gateway only relays telemetry to SCADA for this asset. "
                "Setpoints and safety parameters must be written directly via Modbus TCP to the PLC."
            )
        }), 403
    return jsonify({"status": "error", "message": "Unsupported asset"}), 400
@app.route("/api/diagnostic/control/setpoint", methods=["POST"])
@diagnostic_protected
def diagnostic_setpoint():
    data = request.get_json(silent=True) or {}
    required_fields = ["tag", "value"]
    missing = [f for f in required_fields if f not in data]
    if missing:
        return jsonify({"status": "error", "message": "Missing required fields", "missing": missing}), 400
    tag = data["tag"]
    try:
        value = int(data["value"])
    except (ValueError, TypeError):
        return jsonify({"status": "error", "message": "value must be an integer"}), 400
    valid_tags = ["target_mixing_speed_rpm", "safe_mixing_limit_rpm"]
    if tag not in valid_tags:
        return jsonify({"status": "error", "message": "Invalid writable tag for PLC1_MIXER", "valid_tags": valid_tags}), 400
    try:
        write_plc1_holding(tag, value)
        new_state = read_plc1_modbus()
    except Exception as exc:
        return jsonify({"status": "error", "message": "Modbus write failed", "detail": str(exc)}), 503
    return jsonify({
        "status": "ok", "message": "diagnostic write ok (internal use only)",
        "tag": tag, "value": value, "real_process_state": new_state
    })

@app.route("/api/diagnostic/control/mixer", methods=["POST"])
@diagnostic_protected
def diagnostic_mixer_control():
    data = request.get_json(silent=True) or {}
    if "running" not in data:
        return jsonify({"status": "error", "message": "Missing required field: running"}), 400
    try:
        running = parse_bool(data["running"])
    except ValueError as exc:
        return jsonify({"status": "error", "message": str(exc)}), 400
    try:
        write_plc1_coil("mixer_running", running)
        new_state = read_plc1_modbus()
    except Exception as exc:
        return jsonify({"status": "error", "message": "Modbus coil write failed", "detail": str(exc)}), 503
    return jsonify({
        "status": "ok", "message": "diagnostic coil write ok (internal use only)",
        "mixer_running": running, "real_process_state": new_state
    })
@app.route("/api/debug/spoofing", methods=["POST"])

def spoofing():
    data = request.get_json(silent=True) or {}
    if "asset" not in data or "enabled" not in data:
        return jsonify({"status": "error", "message": "Missing required fields: asset, enabled"}), 400
    asset = data["asset"]
    if not asset_exists(asset):
        return jsonify({"status": "error", "message": "Unknown asset", "valid_assets": list(real_process_state.keys())}), 404
    try:
        enabled_value = parse_bool(data["enabled"])
    except ValueError as exc:
        return jsonify({"status": "error", "message": str(exc)}), 400
    spoofing_state[asset]["enabled"] = enabled_value
    return jsonify({
        "status": "ok", "asset": asset,
        "spoofing_enabled": spoofing_state[asset]["enabled"],
        "message": "SCADA telemetry spoofing updated"
    })


@app.route("/api/audit/setpoints", methods=["GET"])

def audit_setpoints():
    return jsonify({"total_events": len(setpoint_audit_log), "events": setpoint_audit_log})

@app.route("/api/audit/control", methods=["GET"])
def audit_control():
    return jsonify({"total_events": len(control_audit_log), "events": control_audit_log})

@app.route("/api/validate/false-data-injection/<asset>", methods=["GET"])

def validate_false_data_injection(asset):
    if not asset_exists(asset):
        return jsonify({"status": "error", "message": "Unknown asset", "valid_assets": list(real_process_state.keys())}), 404
    try:
        update_process_safety(asset)
    except Exception as exc:
        return jsonify({"status": "error", "asset": asset, "message": "Unable to refresh real process state", "detail": str(exc)}), 503
    scada_view = get_scada_view(asset)
    state = real_process_state[asset]
    methodology_complete = discovery_state[asset]["map_discovered"]

    if asset == "PLC1_MIXER":
        real_dangerous = state["mixer_fault_state"] is True
        scada_looks_safe = (
            scada_view["mixer_fault_state"] is False
            and scada_view["data_quality"] == "GOOD"
        )
        if real_dangerous and spoofing_state[asset]["enabled"] and scada_looks_safe:
            result = {
                "status": "success", "asset": asset,
                "message": "False process data injection condition validated",
                "flag": "flag{plc1_mixer_telemetry_spoofed}",
                "methodology_complete": methodology_complete
            }
            if methodology_complete:
                result["bonus_flag"] = "flag{plc1_full_methodology_followed}"
            return jsonify(result)

    return jsonify({
        "status": "not_validated", "asset": asset,
        "spoofing_enabled": spoofing_state[asset]["enabled"],
        "methodology_complete": methodology_complete,
        "real_process_state": state, "scada_view": scada_view
    })



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
