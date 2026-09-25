from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

DB = "progress.db"

FLAGS = {
    1: "flag{initial_access_obtained}",
    2: "flag{root_gained}",
    3: "flag{smbflag}",
    4: "flag{shared_files}",
    5: "flag{enterprise_database_recon_complete}",
    6: "flag{grafana_idmz_find}",
    7: "flag{jump_server_idmz_access}",
    8: "flag{plc1_mixer_mapping_discovered}",
    9: "flag{plc1_mixer_telemetry_spoofed}",
    10: "flag{mixer_speed_threshold_exceeded}",
    11: "flag{mixer_process_stopped}",
    12: "flag{mixer_tank_high_level}"
}


def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS progress (
            stage INTEGER PRIMARY KEY,
            solved INTEGER DEFAULT 0
        )
    """)

    for stage in FLAGS:
        conn.execute(
            "INSERT OR IGNORE INTO progress(stage, solved) VALUES (?, 0)",
            (stage,)
        )

    conn.commit()
    conn.close()


@app.route("/")
def index():
    conn = get_db()

    rows = conn.execute(
        "SELECT stage, solved FROM progress ORDER BY stage"
    ).fetchall()

    conn.close()

    solved_stages = [
        row["stage"]
        for row in rows
        if row["solved"] == 1
    ]

    return render_template(
        "index.html",
        solved_stages=solved_stages
    )


@app.route("/submit", methods=["POST"])
def submit_flag():
    data = request.get_json(silent=True) or {}

    try:
        stage_id = int(data.get("stage"))
    except (TypeError, ValueError):
        return jsonify({
            "status": "error",
            "message": "Invalid stage."
        }), 400

    submitted_flag = str(data.get("flag", "")).strip()

    if stage_id not in FLAGS:
        return jsonify({
            "status": "error",
            "message": "Unknown stage."
        }), 404

    if submitted_flag == FLAGS[stage_id]:

        conn = get_db()

        conn.execute(
            "UPDATE progress SET solved = 1 WHERE stage = ?",
            (stage_id,)
        )

        conn.commit()
        conn.close()

        return jsonify({
            "status": "correct",
            "message": "Flag accepted."
        })

    return jsonify({
        "status": "incorrect",
        "message": "Incorrect flag."
    })


if __name__ == "__main__":
    init_db()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
