#!/usr/bin/env python3
"""Графики Git-активности для README (требование МУ п. 3.9)."""

from __future__ import annotations

import subprocess
from collections import Counter
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("Agg")

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent / "images"
OUT.mkdir(parents=True, exist_ok=True)


def git_lines(fmt: str) -> list[str]:
    result = subprocess.run(
        ["git", "log", f"--format={fmt}"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
        encoding="utf-8",
    )
    return [line for line in result.stdout.splitlines() if line.strip()]


def activity_chart() -> None:
    result = subprocess.run(
        ["git", "log", "--format=%ad", "--date=short"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
        encoding="utf-8",
    )
    dates = [line for line in result.stdout.splitlines() if line.strip()]
    by_day = Counter(dates)
    days = sorted(by_day)
    counts = [by_day[d] for d in days]

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(days, counts, color="#4a6741", edgecolor="#2d3f28")
    ax.set_title("Активность коммитов по дням", fontsize=14, fontweight="bold")
    ax.set_xlabel("Дата")
    ax.set_ylabel("Количество коммитов")
    ax.tick_params(axis="x", rotation=45)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT / "git-commit-activity.png", dpi=150)
    plt.close(fig)


def punch_card() -> None:
    result = subprocess.run(
        ["git", "log", "--format=%ad", "--date=format:%Y-%m-%d %H"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
        encoding="utf-8",
    )
    raw = [line for line in result.stdout.splitlines() if line.strip()]
    matrix = [[0] * 24 for _ in range(7)]
    weekday_names = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
    for item in raw:
        dt = datetime.strptime(item, "%Y-%m-%d %H")
        matrix[dt.weekday()][dt.hour] += 1

    fig, ax = plt.subplots(figsize=(12, 3.5))
    im = ax.imshow(matrix, aspect="auto", cmap="YlGn", origin="upper")
    ax.set_title("Распределение коммитов (день недели × час)", fontsize=14, fontweight="bold")
    ax.set_yticks(range(7))
    ax.set_yticklabels(weekday_names)
    ax.set_xticks(range(0, 24, 2))
    ax.set_xticklabels([f"{h:02d}" for h in range(0, 24, 2)])
    ax.set_xlabel("Час суток")
    fig.colorbar(im, ax=ax, label="Коммиты")
    fig.tight_layout()
    fig.savefig(OUT / "git-punch-card.png", dpi=150)
    plt.close(fig)


def main() -> None:
    activity_chart()
    punch_card()
    total = subprocess.run(
        ["git", "rev-list", "--count", "HEAD"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    print(f"Git charts saved to {OUT} ({total} commits)")


if __name__ == "__main__":
    main()
