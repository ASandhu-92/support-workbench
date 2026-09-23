"""Load data/tickets.json as {id: ticket}."""
import json
from pathlib import Path

DATA = Path(__file__).resolve().parent / "data"


def load_tickets() -> dict:
    return {t["id"]: t for t in json.loads((DATA / "tickets.json").read_text())}
