"""The one place that talks to a model.

Every call shells out to the Claude Code CLI in headless mode (`claude -p`) with no tools, no
settings, no MCP servers and no session file, and asks for JSON that matches a schema. That runs on
the logged-in Claude subscription, or on ANTHROPIC_API_KEY if it is set.

Responses are cached under .cache/ by a hash of (system prompt, prompt, schema, model), so a rerun
of the same tickets costs nothing. Pass use_cache=False (or --no-cache on the scripts) to force a
fresh call.
"""
import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
CACHE_DIR = HERE / ".cache"
MODEL = "sonnet"
TIMEOUT_S = 300

# House style: plain punctuation. The prompts ask for it; this catches the rest.
_PUNCT = {chr(0x2014): " - ", chr(0x2013): "-"}  # em dash, en dash


class LLMError(RuntimeError):
    pass


def _plain(value):
    if isinstance(value, str):
        for bad, good in _PUNCT.items():
            value = value.replace(bad, good)
        return value
    if isinstance(value, list):
        return [_plain(v) for v in value]
    if isinstance(value, dict):
        return {k: _plain(v) for k, v in value.items()}
    return value


def cache_key(system: str, prompt: str, schema: dict, model: str = MODEL) -> str:
    blob = json.dumps([system, prompt, schema, model], sort_keys=True).encode()
    return hashlib.sha256(blob).hexdigest()


def command(system: str, prompt: str, schema: dict, model: str = MODEL) -> list[str]:
    return [
        "claude", "-p", prompt,
        "--output-format", "json",
        "--json-schema", json.dumps(schema),
        "--tools", "",
        "--model", model,
        "--no-session-persistence",
        "--setting-sources", "",
        "--strict-mcp-config",
        "--disable-slash-commands",
        "--system-prompt", system,
    ]


def ask(system: str, prompt: str, schema: dict, *, use_cache: bool = True, model: str = MODEL) -> dict:
    """Return {"output": <structured output>, "cost_usd", "duration_ms", "models", "cached"}."""
    key = cache_key(system, prompt, schema, model)
    path = CACHE_DIR / f"{key}.json"
    if use_cache and path.exists():
        hit = json.loads(path.read_text())
        return {**hit, "cached": True}

    try:
        proc = subprocess.run(command(system, prompt, schema, model), capture_output=True,
                              text=True, timeout=TIMEOUT_S, cwd="/tmp")
    except subprocess.TimeoutExpired as exc:
        raise LLMError(f"claude -p timed out after {TIMEOUT_S}s") from exc
    except FileNotFoundError as exc:
        raise LLMError("the `claude` CLI is not on PATH") from exc

    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError:
        tail = (proc.stderr or proc.stdout).strip()[-400:]
        raise LLMError(f"claude -p exit {proc.returncode}, output was not JSON: {tail}")
    if proc.returncode != 0 or data.get("is_error"):
        raise LLMError(f"claude -p exit {proc.returncode}, subtype={data.get('subtype')}, "
                       f"api_error_status={data.get('api_error_status')}: {str(data.get('result'))[:300]}")
    if data.get("structured_output") is None:
        raise LLMError(f"claude -p returned no structured_output (subtype={data.get('subtype')})")

    result = {
        "output": _plain(data["structured_output"]),
        "cost_usd": data.get("total_cost_usd") or 0.0,
        "duration_ms": data.get("duration_ms") or 0,
        "models": sorted((data.get("modelUsage") or {}).keys()),
    }
    CACHE_DIR.mkdir(exist_ok=True)
    path.write_text(json.dumps(result, indent=1))
    return {**result, "cached": False}
