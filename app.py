import json
import os
import random
import sqlite3
from pathlib import Path

from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "pokemon.db"
JSON_PATH = BASE_DIR / "pokemonData.json"

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key-change-me")


def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = get_db_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS pokemon (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            image_url TEXT NOT NULL,
            cry_url TEXT NOT NULL,
            attack INTEGER NOT NULL,
            defense INTEGER NOT NULL,
            speed INTEGER NOT NULL,
            profit INTEGER NOT NULL
        )
        """
    )

    existing = conn.execute("SELECT COUNT(*) AS count FROM pokemon").fetchone()["count"]
    if existing == 0:
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            source_data = json.load(f)

        rows = []
        for p in source_data:
            poke_id = int(p["id"])
            rows.append(
                (
                    poke_id,
                    p["name"],
                    f"/static/Images/{poke_id}.png",
                    f"/static/sound/{poke_id}.wav",
                    int(p["attack"]),
                    int(p["defense"]),
                    int(p["speed"]),
                    int(p["profit"]),
                )
            )

        conn.executemany(
            """
            INSERT INTO pokemon (id, name, image_url, cry_url, attack, defense, speed, profit)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            rows,
        )

    conn.commit()
    conn.close()


def fetch_random_pokemon(limit: int = 10) -> list[dict]:
    conn = get_db_connection()
    rows = conn.execute(
        "SELECT id, name, image_url, cry_url, attack, defense, speed, profit FROM pokemon ORDER BY RANDOM() LIMIT ?",
        (limit,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def fetch_pokemon_by_ids(ids: list[int]) -> list[dict]:
    if not ids:
        return []

    placeholders = ",".join("?" for _ in ids)
    conn = get_db_connection()
    rows = conn.execute(
        f"SELECT id, name, image_url, cry_url, attack, defense, speed, profit FROM pokemon WHERE id IN ({placeholders})",
        ids,
    ).fetchall()
    conn.close()

    by_id = {int(r["id"]): dict(r) for r in rows}
    return [by_id[i] for i in ids if i in by_id]


def calculate_team_profit(team: list[dict]) -> int:
    return sum(int(p["profit"]) for p in team)


def calculate_best_team(pool: list[dict], team_size: int = 6) -> list[dict]:
    return sorted(pool, key=lambda p: int(p["profit"]), reverse=True)[:team_size]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/game")
def game():
    hide_profit = request.args.get("hide_profit", "0") == "1"
    pool = fetch_random_pokemon(10)
    session["current_pool_ids"] = [int(p["id"]) for p in pool]
    session["hide_profit"] = hide_profit
    return render_template("game.html", pokemon_pool=pool, hide_profit=hide_profit)


@app.route("/api/random-pokemon")
def random_pokemon_api():
    return jsonify(fetch_random_pokemon(10))


@app.route("/submit", methods=["POST"])
def submit_team():
    selected_ids_raw = request.form.getlist("selected_pokemon")
    pool_ids = session.get("current_pool_ids", [])
    hide_profit = bool(session.get("hide_profit", False))

    if not pool_ids:
        flash("Game session expired. Please load a new game.")
        return redirect(url_for("index"))

    try:
        selected_ids = [int(i) for i in selected_ids_raw]
    except ValueError:
        flash("Invalid selection. Please try again.")
        return redirect(url_for("game", hide_profit=int(hide_profit)))

    if len(selected_ids) != 6:
        flash("You must select exactly 6 Pokemon.")
        return redirect(url_for("game", hide_profit=int(hide_profit)))

    if not set(selected_ids).issubset(set(pool_ids)):
        flash("Selection must come from the current 10 Pokemon.")
        return redirect(url_for("game", hide_profit=int(hide_profit)))

    user_team = fetch_pokemon_by_ids(selected_ids)
    pool = fetch_pokemon_by_ids(pool_ids)

    user_profit = calculate_team_profit(user_team)
    optimal_team = calculate_best_team(pool, 6)
    optimal_profit = calculate_team_profit(optimal_team)

    return render_template(
        "result.html",
        user_team=user_team,
        user_profit=user_profit,
        optimal_team=optimal_team,
        optimal_profit=optimal_profit,
        difference=optimal_profit - user_profit,
        perfect=(user_profit == optimal_profit),
        hide_profit=hide_profit,
    )


init_db()

if __name__ == "__main__":
    app.run(debug=True)
