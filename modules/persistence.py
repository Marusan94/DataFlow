"""Persistencia liviana para EduAnalytics HUB.
SQLite + session_state + query_params. Sin Postgres, sin lentitud.
Copiar a: Eduanalytics/modules/persistence.py
Uso en app.py:
  from modules.persistence import init_db, save_search, get_history
  init_db()
"""
import pathlib
import sqlite3
import time

DB_PATH = pathlib.Path(__file__).resolve().parent.parent / 'resultados' / 'eduanalytics.db'


def _connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = _connect()
    conn.execute(
        """CREATE TABLE IF NOT EXISTS searches(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        query TEXT NOT NULL, top_k INTEGER DEFAULT 5,
        n_results INTEGER DEFAULT 0, created REAL)"""
    )
    conn.execute(
        """CREATE TABLE IF NOT EXISTS results(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        kind TEXT NOT NULL, title TEXT, content TEXT, created REAL)"""
    )
    conn.commit()
    conn.close()


def save_search(query: str, top_k: int = 5, n_results: int = 0):
    try:
        conn = _connect()
        conn.execute(
            'INSERT INTO searches(query, top_k, n_results, created) VALUES(?,?,?,?)',
            (query[:300], top_k, n_results, time.time()),
        )
        conn.commit()
        conn.close()
    except Exception:
        pass


def save_result(kind: str, title: str, content: str):
    """Guarda humanizer / cajal / quick tools. kind: humanizer|cajal|resumen|..."""
    try:
        conn = _connect()
        conn.execute(
            'INSERT INTO results(kind, title, content, created) VALUES(?,?,?,?)',
            (kind, title[:200], content[:20000], time.time()),
        )
        conn.commit()
        conn.close()
    except Exception:
        pass


def get_history(limit: int = 20) -> list:
    try:
        conn = _connect()
        rows = conn.execute(
            'SELECT query, top_k, n_results, created FROM searches ORDER BY id DESC LIMIT ?',
            (limit,),
        ).fetchall()
        conn.close()
        return [dict(r) for r in rows]
    except Exception:
        return []


def get_saved_results(kind: str = None, limit: int = 20) -> list:
    try:
        conn = _connect()
        if kind:
            rows = conn.execute(
                'SELECT kind, title, content, created FROM results WHERE kind=? ORDER BY id DESC LIMIT ?',
                (kind, limit),
            ).fetchall()
        else:
            rows = conn.execute(
                'SELECT kind, title, content, created FROM results ORDER BY id DESC LIMIT ?',
                (limit,),
            ).fetchall()
        conn.close()
        return [dict(r) for r in rows]
    except Exception:
        return []


def streamlit_persistence_boot():
    """Llamar una vez al inicio de app.py para persistencia + reactividad.
    No importa nada pesado. Solo session_state defaults.
    """
    try:
        import streamlit as st
        defaults = {'df_edu': None, 'search_q': '', 'humanizer_result': None, 'cajal_result': None}
        for k, v in defaults.items():
            if k not in st.session_state:
                st.session_state[k] = v
        init_db()
    except Exception:
        init_db()
