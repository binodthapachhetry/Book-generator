# std-lib only
import sqlite3, time, functools, json, os, threading

_DB_PATH = os.path.join(os.path.dirname(__file__), "trace.db")
_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS traces(
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    ts         TEXT    DEFAULT (datetime('now')),
    func       TEXT,
    elapsed_s  REAL,
    tokens     INTEGER,
    img_steps  INTEGER
);
"""

_lock = threading.Lock()         # sqlite isn’t fully thread-safe


def _log(func_name: str, elapsed: float, tokens: int | None = None,
         steps: int | None = None) -> None:
    with _lock, sqlite3.connect(_DB_PATH) as conn:
        conn.execute(_TABLE_SQL)
        conn.execute("INSERT INTO traces(func, elapsed_s, tokens, img_steps) "
                     "VALUES (?,?,?,?)",
                     (func_name, elapsed, tokens, steps))
        conn.commit()


def trace_time(func):
    """Measures wall-clock time and stores it; always the OUTER decorator."""
    @functools.wraps(func)
    def wrapper(*args, **kw):
        t0 = time.perf_counter()
        out = func(*args, **kw)
        _log(func.__qualname__, time.perf_counter() - t0)   # tokens/steps filled later
        return out
    return wrapper


def trace_cost(func):
    """Attempts to infer ‘tokens’ (LLM) or ‘steps’ (image) from return value / kwargs."""
    @functools.wraps(func)
    def wrapper(*args, **kw):
        out = func(*args, **kw)

        # Very light heuristics – adjust as needed later
        tokens = None
        if isinstance(out, str):
            tokens = len(out.split())
        elif hasattr(out, "usage"):          # e.g. OpenAI responses
            tokens = out.usage.get("total_tokens")

        steps = kw.get("num_inference_steps") or kw.get("steps")
        _log(func.__qualname__, 0.0, tokens, steps)         # elapsed updated by @trace_time
        return out
    return wrapper
