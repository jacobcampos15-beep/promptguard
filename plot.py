#!/usr/bin/env python3
"""
plot.py — render results/summary.csv into a grouped bar chart.

Produces results/matrix.png: injection-success rate per attack, grouped by
defense, so you can see at a glance which defenses actually help.
"""

import csv
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).parent


def main():
    data = defaultdict(dict)  # data[attack][defense] = rate
    defenses_seen, attacks_seen = [], []
    with open(ROOT / "results" / "summary.csv") as f:
        for r in csv.DictReader(f):
            if r["attack"] == "none":
                continue
            data[r["attack"]][r["defense"]] = float(r["injection_success_rate"])
            if r["defense"] not in defenses_seen:
                defenses_seen.append(r["defense"])
            if r["attack"] not in attacks_seen:
                attacks_seen.append(r["attack"])

    x = range(len(attacks_seen))
    n = len(defenses_seen)
    width = 0.8 / n

    fig, ax = plt.subplots(figsize=(9, 5))
    for i, defense in enumerate(defenses_seen):
        vals = [data[a].get(defense, 0) for a in attacks_seen]
        ax.bar([p + i * width for p in x], vals, width, label=defense)

    ax.set_xticks([p + width * (n - 1) / 2 for p in x])
    ax.set_xticklabels(attacks_seen, rotation=15)
    ax.set_ylabel("Injection success rate (lower is better)")
    ax.set_title("PromptGuard: prompt-injection success by attack and defense")
    ax.set_ylim(0, 1)
    ax.legend(title="defense")
    fig.tight_layout()
    out = ROOT / "results" / "matrix.png"
    fig.savefig(out, dpi=150)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
