"""
Investment Research Logic Engine — CLI Entry Point.

Usage:
    python main.py --topic "白银"
    python main.py --topic "白银" --reports report1.pdf report2.pdf report3.pdf
    python main.py --topic "白银" --provider miromind
    python main.py --demo  (serve pre-computed demo)
"""
import argparse
import asyncio
import logging
import sys

from config import Config, LLMConfig
from runtime.harness import PipelineHarness
from runtime.orchestrator import Orchestrator


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("main")


def progress_callback(step: str, status: str, detail: str = ""):
    icons = {
        "started": "⏳",
        "completed": "✅",
        "skipped": "⏭️",
    }
    icon = icons.get(status, "📌")
    print(f"  {icon} [{step}] {status} {detail}")


async def run_pipeline(args):
    config = Config(
        llm=LLMConfig.from_env(args.provider),
        output_dir=args.output or "output",
    )

    print(f"\n{'='*60}")
    print(f"  Investment Research Logic Engine")
    print(f"  Topic: {args.topic}")
    print(f"  Provider: {config.llm.provider} ({config.llm.model})")
    print(f"{'='*60}\n")

    orchestrator = Orchestrator(config)
    result = await orchestrator.run(
        topic=args.topic,
        report_paths=args.reports,
        on_progress=progress_callback,
    )

    print(f"\n{'='*60}")
    print(f"  Pipeline complete!")
    print(f"  Outputs: {result['run_dir']}")
    print(f"{'='*60}\n")


def serve_demo(args):
    """Serve pre-computed demo via FastAPI."""
    try:
        from server import create_app
        import uvicorn

        app = create_app()
        print(f"\n  Serving demo at http://localhost:{args.port}")
        print(f"  Demo directory: {args.demo_dir or 'demo'}\n")
        uvicorn.run(app, host="0.0.0.0", port=args.port)
    except ImportError as e:
        print(f"Error: {e}")
        print("Install server dependencies: pip install fastapi uvicorn")
        sys.exit(1)


def run_harness(args):
    """Run artifact harness commands."""
    harness = PipelineHarness(args.run_dir)
    if args.harness_command == "validate":
        report = harness.validate()
        for row in report.steps:
            status = "OK" if row["ok"] else "FAIL"
            print(f"{status} {row['step']}")
            for err in row["errors"]:
                print(f"  - {err}")
        print(f"\nHarness report: {harness.write_report()}")
    elif args.harness_command == "parse-raw":
        result = harness.parse_raw_step(args.step)
        print(f"Parsed {result['step']}: valid={result['valid']}")
        for err in result["errors"]:
            print(f"  - {err}")


def main():
    parser = argparse.ArgumentParser(
        description="Investment Research Logic Engine — Deep Research Agent"
    )
    sub = parser.add_subparsers(dest="command")

    # Run pipeline
    run_parser = sub.add_parser("run", help="Run the research pipeline")
    run_parser.add_argument("--topic", required=True, help="Investment topic")
    run_parser.add_argument("--reports", nargs="*", help="PDF report file paths")
    run_parser.add_argument(
        "--provider",
        choices=["anthropic", "openai", "miromind", "mock"],
        default=None,
        help="LLM provider (default: from env LLM_PROVIDER)",
    )
    run_parser.add_argument("--output", default="output", help="Output directory")

    # Serve demo
    demo_parser = sub.add_parser("demo", help="Serve pre-computed demo")
    demo_parser.add_argument("--port", type=int, default=8000)
    demo_parser.add_argument("--demo-dir", default="demo")

    # Harness utilities
    harness_parser = sub.add_parser("harness", help="Validate and replay saved artifacts")
    harness_sub = harness_parser.add_subparsers(dest="harness_command", required=True)

    validate_parser = harness_sub.add_parser("validate", help="Validate parsed artifacts in a run directory")
    validate_parser.add_argument("--run-dir", required=True)

    parse_parser = harness_sub.add_parser("parse-raw", help="Parse a raw artifact into parsed JSON")
    parse_parser.add_argument("--run-dir", required=True)
    parse_parser.add_argument("--step", required=True)

    args = parser.parse_args()

    if args.command == "run":
        asyncio.run(run_pipeline(args))
    elif args.command == "demo":
        serve_demo(args)
    elif args.command == "harness":
        run_harness(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
