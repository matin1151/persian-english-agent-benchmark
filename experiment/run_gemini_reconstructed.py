#!/usr/bin/env python3
"""Reconstructed Gemini tool-calling probe runner, NOT the exact original script.

Requires: pip install google-genai
Set GEMINI_API_KEY securely in your environment.
Run in an EMPTY output directory to avoid mixing reruns with original data.
"""
import argparse
import csv
import json
import os
import time
from pathlib import Path
from google import genai
from google.genai import types

TOOLS = [
    {"name": "lookup_order", "description": "Look up an order by its identifier.", "parameters": {"type": "OBJECT", "properties": {"order_id": {"type": "STRING"}}, "required": ["order_id"]}},
    {"name": "update_shipping_address", "description": "Update an order's shipping address.", "parameters": {"type": "OBJECT", "properties": {"order_id": {"type": "STRING"}, "city": {"type": "STRING"}, "street": {"type": "STRING"}}, "required": ["order_id", "city", "street"]}},
    {"name": "cancel_order", "description": "Cancel an order.", "parameters": {"type": "OBJECT", "properties": {"order_id": {"type": "STRING"}}, "required": ["order_id"]}},
    {"name": "create_support_ticket", "description": "Create a support ticket for an order.", "parameters": {"type": "OBJECT", "properties": {"order_id": {"type": "STRING"}, "reason": {"type": "STRING"}}, "required": ["order_id", "reason"]}},
]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="gemini-3.1-flash-lite")
    parser.add_argument("--manifest", default="experiment/trial_manifest_reconstructed.csv")
    parser.add_argument("--output", default="new_observations.jsonl")
    parser.add_argument("--limit", type=int, default=30)
    args = parser.parse_args()
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key:
        raise SystemExit("Set GEMINI_API_KEY first (never commit it).")
    client = genai.Client(api_key=key)
    with open(args.manifest, newline="", encoding="utf-8") as f:
        manifest = list(csv.DictReader(f))
    tasks = [(row, repetition) for row in manifest for repetition in (1,2,3)]
    out = Path(args.output)
    if out.name == "gemini_observations_raw.jsonl":
        raise SystemExit("Do not overwrite the original research data.")
    for row, repetition in tasks[:args.limit]:
        start = time.monotonic()
        try:
            response = client.models.generate_content(
                model=args.model,
                contents=row["prompt"],
                config=types.GenerateContentConfig(
                    temperature=0,
                    tools=[types.Tool(function_declarations=TOOLS)],
                    tool_config=types.ToolConfig(function_calling_config=types.FunctionCallingConfig(mode="ANY")),
                ),
            )
            calls = [{"name": c.name, "arguments": dict(c.args or {})} for c in (response.function_calls or [])]
            status = "completed"
            error = None
        except Exception as exc:
            calls = []
            status = "error"
            error = str(exc)
        expected = {"name": row["expected_function"], "arguments": json.loads(row["expected_arguments_json"])}
        result = {
            "trial_key": f'{row["task_id"]}:{row["language"]}:{repetition}',
            "task_id": row["task_id"], "language": row["language"],
            "prompt": row["prompt"], "model_requested": args.model,
            "expected": expected, "actual_calls": calls,
            "status": status, "error": error,
            "latency_seconds": round(time.monotonic() - start, 3),
        }
        with out.open("a", encoding="utf-8") as f:
            f.write(json.dumps(result, ensure_ascii=False) + "\n")
        print(result["trial_key"], status, flush=True)

if __name__ == "__main__":
    main()
