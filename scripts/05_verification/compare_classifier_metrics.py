"""Compare regenerated classifier accuracies with the committed ones, within a tolerance.

The self-preference results are checked for exact equality in CI. Classifier
accuracies can shift slightly with library versions (NLTK's part-of-speech tagger,
scikit-learn, XGBoost), because the requirements allow version ranges. This check
allows differences up to TOLERANCE (absolute, as a fraction: 0.01 = 1 percentage point).

Usage: python compare_classifier_metrics.py COMMITTED.json REGENERATED.json
"""

import json
import sys

TOLERANCE = 0.01


def flatten(data, prefix=""):
    if isinstance(data, dict):
        for key, value in data.items():
            yield from flatten(value, f"{prefix}{key}.")
    elif isinstance(data, (int, float)):
        yield prefix.rstrip("."), float(data)


def main(committed_path, regenerated_path):
    with open(committed_path) as f:
        committed = dict(flatten(json.load(f)))
    with open(regenerated_path) as f:
        regenerated = dict(flatten(json.load(f)))
    if committed.keys() != regenerated.keys():
        print("Different metrics:", sorted(committed.keys() ^ regenerated.keys()))
        return 1
    worst = 0.0
    failed = False
    for key in sorted(committed):
        diff = abs(committed[key] - regenerated[key])
        worst = max(worst, diff)
        if diff > TOLERANCE:
            failed = True
            print(f"FAIL {key}: committed {committed[key]:.4f}, regenerated {regenerated[key]:.4f}")
    print(f"Largest difference: {worst * 100:.2f} percentage points (tolerance {TOLERANCE * 100:.0f})")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
