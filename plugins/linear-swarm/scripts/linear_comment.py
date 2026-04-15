#!/usr/bin/env python3
"""Compatibility wrapper for the shared linear-swarm Linear comment helper."""

from __future__ import annotations

import runpy
from pathlib import Path

SHARED = (
    Path(__file__).resolve().parents[2]
    / "_shared"
    / "linear-swarm"
    / "scripts"
    / "linear_comment.py"
)

runpy.run_path(str(SHARED), run_name="__main__")
