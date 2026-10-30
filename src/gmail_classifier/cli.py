"""Local training and optional read-only Gmail collection."""

import argparse
import json
from pathlib import Path

from .baseline import evaluate, load_model, save_model, train
from .dataset import load_dataset
from .policy import Policy
from .private_storage import private_home, private_path, write_private_json
from .gmail import GmailError


def main(argv=None):
    parser = argparse.ArgumentParser(description="Email baseline and read-only Gmail sampling")
    commands = parser.add_subparsers(dest="command", required=True)
    training = commands.add_parser("train")
    training.add_argument("--dataset", type=Path, required=True)
    training.add_argument("--model", type=Path, default=Path("models/baseline.joblib"))
    training.add_argument("--report", type=Path, default=Path("reports/baseline.json"))
    training.add_argument("--spam-threshold", type=float, default=0.90)
    training.add_argument("--legitimate-threshold", type=float, default=0.20)
    training.add_argument("--category-threshold", type=float, default=0.60)
    training.add_argument("--allow-private", action="store_true", help="Use a reviewed private dataset outside Git")
    training.add_argument("--allow-ai-labels", action="store_true", help="Explicitly accept exploratory AI labels, not human ground truth")
    training.add_argument("--spam-reference", type=Path, help="Trusted model to preserve spam stage if AI sample has only one spam class")
    spamshield_download = commands.add_parser("download-spamshield", help="Download the gated multilingual corpus from Hugging Face")
    spamshield_download.add_argument("--cache-dir", type=Path)
    spamshield_training = commands.add_parser("train-spamshield", help="Train/evaluate the separate multilingual SMS spam model")
    spamshield_training.add_argument("--dataset", type=Path, help="Local combined.parquet; downloads to HF cache when omitted")
    spamshield_training.add_argument("--model", type=Path, default=Path("models/spamshield-multilingual.joblib"))
    spamshield_training.add_argument("--report", type=Path, default=Path("reports/spamshield-multilingual.json"))
    spamshield_training.add_argument("--seed", type=int, default=42)
    prediction = commands.add_parser("predict", help="Load only models you trained and trust")
    prediction.add_argument("--model", type=Path, required=True)
    prediction.add_argument("--subject", default="")
    prediction.add_argument("--body", default="")
    authentication = commands.add_parser("gmail-auth", help="Open browser consent for gmail.readonly only")
    authentication.add_argument("--credentials", type=Path, default=private_home() / "credentials.json")
    authentication.add_argument("--token", type=Path, default=private_home() / "token.json")
    collection = commands.add_parser("gmail-collect", help="Collect a limited private sample; never changes Gmail")
    collection.add_argument("--credentials", type=Path, default=private_home() / "credentials.json")
    collection.add_argument("--token", type=Path, default=private_home() / "token.json")
    collection.add_argument("--query", required=True, help="Gmail search expression; not stored in the collection")
    collection.add_argument("--limit", type=int, default=50)
    collection.add_argument("--include-spam", action="store_true", help="Include Spam and Trash in search")
    collection.add_argument("--output", type=Path, default=private_home() / "review.json")
    preparation = commands.add_parser("prepare-dataset", help="Validate manual labeling, privacy review and splits")
    preparation.add_argument("--input", type=Path, default=private_home() / "review.json")
    preparation.add_argument("--output", type=Path, default=private_home() / "dataset.json")
    reviewer = commands.add_parser("review", help="Open a local browser form for human labeling and privacy review")
    reviewer.add_argument("--input", type=Path, default=private_home() / "review.json")
    reviewer.add_argument("--port", type=int, default=0)
    reviewer.add_argument("--no-browser", action="store_true")
    simulation = commands.add_parser("predict-batch", help="Offline simulation; writes pseudonyms and predictions only")
    simulation.add_argument("--input", type=Path, default=private_home() / "review.json")
    simulation.add_argument("--model", type=Path, required=True)
    simulation.add_argument("--output", type=Path, default=private_home() / "predictions.json")
    args = parser.parse_args(argv)
    try:
        if args.command == "train":
            if args.allow_private:
                # Reject default in-checkout model/report paths before reading private input.
                private_path(args.dataset)
                private_path(args.model)
                private_path(args.report)
            if args.model.resolve() == args.report.resolve():
                raise ValueError("Model and report must use different paths")
            if args.dataset.resolve() in (args.model.resolve(), args.report.resolve()):
                raise ValueError("Outputs cannot overwrite dataset")
            if args.spam_reference and args.spam_reference.resolve() in (args.model.resolve(), args.report.resolve()):
                raise ValueError("Outputs cannot overwrite the reference model")
            rows = load_dataset(args.dataset, allow_private=args.allow_private, allow_ai=args.allow_ai_labels)
            policy = Policy(args.spam_threshold, args.legitimate_threshold, args.category_threshold)
            reference = load_model(args.spam_reference) if args.spam_reference else None
            model = train(rows, policy, allow_private=args.allow_private,
                          allow_ai=args.allow_ai_labels, spam_reference=reference)
            report = evaluate(model, rows, allow_private=args.allow_private, allow_ai=args.allow_ai_labels)
            save_model(model, args.model)
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
            print(json.dumps({"model": str(args.model), "report": str(args.report),
                              "warning": report["warning"]}, ensure_ascii=False))
        elif args.command == "download-spamshield":
            from .spamshield import download_dataset
            print(json.dumps({"dataset": str(download_dataset(args.cache_dir)),
                              "source": "M-Arjun/SpamShield-Datasets"}, ensure_ascii=False))
        elif args.command == "train-spamshield":
            from .spamshield import download_dataset, train_and_evaluate
            dataset = args.dataset or download_dataset()
            report = train_and_evaluate(dataset, args.model, args.report, seed=args.seed)
            print(json.dumps({"model": str(args.model), "report": str(args.report),
                              "rows": report["total_count"],
                              "languages": len(report["languages"])}, ensure_ascii=False))
        elif args.command == "predict":
            print(json.dumps(load_model(args.model).predict(args.subject, args.body), ensure_ascii=False))
        elif args.command == "gmail-auth":
            from .gmail import authenticate
            authenticate(args.credentials, args.token, interactive=True)
            print(json.dumps({"authenticated": True, "scope": "gmail.readonly"}))
        elif args.command == "gmail-collect":
            from .gmail import collect, connect, MAX_MESSAGES
            output = private_path(args.output)
            if output in {private_path(args.credentials), private_path(args.token)} or output.exists():
                raise ValueError("Choose a new collection output path")
            if not 1 <= args.limit <= MAX_MESSAGES or not args.query.strip():
                raise GmailError("Specify a non-empty query and a limit between 1 and 500")
            sample = collect(connect(args.credentials, args.token), query=args.query,
                             limit=args.limit, include_spam=args.include_spam)
            write_private_json(output, sample)
            print(json.dumps({"collected": len(sample["records"]), "fetched": sample["fetched"],
                              "skipped": sample["skipped"]}))
        elif args.command == "prepare-dataset":
            from .review import prepare_dataset
            rows = prepare_dataset(args.input, args.output)
            print(json.dumps({"prepared": len(rows), "source": "gmail_reviewed"}))
        elif args.command == "review":
            from .review_ui import serve
            serve(args.input, port=args.port, open_browser=not args.no_browser)
        else:
            from .review import simulate
            predictions = simulate(args.input, args.model, args.output)
            print(json.dumps({"predicted": len(predictions), "mailbox_changes": 0}))
    except (GmailError, RuntimeError) as error:
        parser.exit(2, f"{error}\n")
    except (ValueError, OSError, TypeError, KeyError):
        parser.exit(2, "Invalid input or unavailable artifact; verify schema, paths and model version.\n")


if __name__ == "__main__":
    main()
