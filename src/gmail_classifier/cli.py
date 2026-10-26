"""Local-only command line interface."""

import argparse
import json
from pathlib import Path

from .baseline import evaluate, load_model, save_model, train
from .dataset import load_dataset
from .policy import Policy


def main(argv=None):
    parser = argparse.ArgumentParser(description="Offline synthetic email baseline (no Gmail access)")
    commands = parser.add_subparsers(dest="command", required=True)
    training = commands.add_parser("train")
    training.add_argument("--dataset", type=Path, required=True)
    training.add_argument("--model", type=Path, default=Path("models/baseline.joblib"))
    training.add_argument("--report", type=Path, default=Path("reports/baseline.json"))
    training.add_argument("--spam-threshold", type=float, default=0.90)
    training.add_argument("--legitimate-threshold", type=float, default=0.20)
    training.add_argument("--category-threshold", type=float, default=0.60)
    prediction = commands.add_parser("predict", help="Load only models you trained and trust")
    prediction.add_argument("--model", type=Path, required=True)
    prediction.add_argument("--subject", default="")
    prediction.add_argument("--body", default="")
    args = parser.parse_args(argv)
    try:
        if args.command == "train":
            if args.model.resolve() == args.report.resolve():
                raise ValueError("Model and report must use different paths")
            if args.dataset.resolve() in (args.model.resolve(), args.report.resolve()):
                raise ValueError("Outputs cannot overwrite dataset")
            rows = load_dataset(args.dataset)
            policy = Policy(args.spam_threshold, args.legitimate_threshold, args.category_threshold)
            model = train(rows, policy)
            report = evaluate(model, rows)
            save_model(model, args.model)
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
            print(json.dumps({"model": str(args.model), "report": str(args.report),
                              "warning": report["warning"]}, ensure_ascii=False))
        else:
            print(json.dumps(load_model(args.model).predict(args.subject, args.body), ensure_ascii=False))
    except (ValueError, OSError):
        parser.exit(2, "Invalid input or unavailable artifact; verify schema, paths and model version.\n")


if __name__ == "__main__":
    main()
