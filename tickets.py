"""Load a ticket set as {id: ticket}: data/tickets.json (the main 30) or data/heldout.json."""
import json
from pathlib import Path

DATA = Path(__file__).resolve().parent / "data"


FILES = {"main": "tickets.json", "heldout": "heldout.json"}


def load_tickets(ticket_set: str = "main") -> dict:
    return {t["id"]: t for t in json.loads((DATA / FILES[ticket_set]).read_text())}
