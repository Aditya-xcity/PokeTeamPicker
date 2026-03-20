# Pokemon Team Optimizer

A Flask-based web game where you select the best 6 Pokemon from a random pool of 10 and compare your result against an optimizer.

## Features

- Randomly loads 10 Pokemon per round from a local SQLite database.
- Lets you select exactly 6 Pokemon.
- Supports a difficulty mode that hides profit values.
- Includes a one-click "Generate Best Team" helper in the game UI.
- Shows result comparison:
  - Your total team profit
  - Optimized team profit
  - Profit gap

## Tech Stack

- Python 3.9+
- Flask
- SQLite (local file: `pokemon.db`)
- HTML, CSS, JavaScript

## Project Structure

```text
BestTeam/
|- app.py
|- pokemonData.json
|- pokemonDataGenerator.py
|- requirements.txt
|- templates/
|  |- index.html
|  |- game.html
|  |- result.html
|- static/
   |- css/style.css
   |- js/script.js
   |- Images/
   |- sound/
```

## How It Works

1. On startup, `app.py` initializes `pokemon.db`.
2. If the `pokemon` table is empty, data is imported from `pokemonData.json`.
3. Visiting `/game` generates a random pool of 10 Pokemon and stores pool IDs in session.
4. You submit exactly 6 selections.
5. The backend computes:
   - Your team profit (sum of selected Pokemon profit)
   - Optimal profit (top 6 profits from the same pool)
6. Results are shown on `/submit` (POST) in `result.html`.

## Setup

### 1. Clone or open the project

Make sure you are inside the project root where `app.py` exists.

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Run the App

```bash
python app.py
```

Open your browser at:

- http://127.0.0.1:5000

## Game Routes

- `GET /` - Home page
- `GET /game` - New game screen with 10 random Pokemon
- `GET /game?hide_profit=1` - Difficulty mode (profits hidden in cards)
- `GET /api/random-pokemon` - Returns a random pool as JSON
- `POST /submit` - Evaluates selected team and renders result

## Data Notes

- Source data is read from `pokemonData.json`.
- During DB seed, image and cry URLs are generated as:
  - `/static/Images/<id>.png`
  - `/static/sound/<id>.wav`
- Ensure matching files exist in those folders if you update Pokemon entries.

## Optional: Regenerate Pokemon Data

`pokemonDataGenerator.py` can fetch and compute Pokemon stats/profit for the first 151 Pokemon using `pokebase`.

If you want to run it, install `pokebase` first:

```bash
pip install pokebase
```

Then run:

```bash
python pokemonDataGenerator.py
```

This rewrites `pokemonData.json`.

## Security and Production Notes

- The app currently uses:
  - Flask debug mode (`app.run(debug=True)`)
  - A development fallback secret key (`dev-secret-key-change-me`)
- For production:
  - Set `FLASK_SECRET_KEY` in environment
  - Disable debug mode
  - Run behind a production WSGI server

## Common Issues

- `ModuleNotFoundError: No module named 'flask'`
  - Activate your virtual environment and reinstall requirements.
- Missing images or sounds in cards
  - Verify files under `static/Images/` and `static/sound/` match Pokemon IDs.
- Game session expired message
  - Reload home page and start a fresh game.

## License

Add your preferred license in this repository (for example, MIT).
