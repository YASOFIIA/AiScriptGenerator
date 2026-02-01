from __future__ import annotations

import json
import time
import hashlib
from typing import Any, Dict, List

from app.core.config import settings
from app.docx.generator import ScriptOutput, build_docx
from app.services.runs import RunStore, RunState
from app.utils.csv_parser import CsvRow

from app.services.perplexity_client import PerplexityClient
from app.services.gemini_client import GeminiClient

from prompts.prompts import (
    build_prompt_1,
    build_prompt_2,
    build_prompt_3,
    build_prompt_4,
    build_prompt_5,
    build_prompt_6,
    build_prompt_7,
    build_prompt_8,
    build_prompt_9,
    build_prompt_10,
)

pplx = PerplexityClient()
gemini = GeminiClient()


def _sha12(text: str) -> str:
    return hashlib.sha256((text or "").encode("utf-8", errors="ignore")).hexdigest()[:12]


def _trace_step(
    steps: List[Dict[str, Any]],
    *,
    step: int,
    provider: str,
    prompt: str,
    output: str,
) -> None:
    prompt_hash = _sha12(prompt)
    output_hash = _sha12(output)

    entry: Dict[str, Any] = {
        "step": step,
        "provider": provider,
        "prompt_hash": prompt_hash,
        "prompt_preview": (prompt or "")[:500],
        "output_hash": output_hash,
        "output_preview": (output or "")[:500],
    }

    # Optional: store full texts for debugging
    if getattr(settings, "TRACE_STORE_FULL_TEXT", False):
        max_chars = int(getattr(settings, "TRACE_MAX_CHARS", 20000))
        entry["prompt_text"] = (prompt or "")[:max_chars]
        entry["output_text"] = (output or "")[:max_chars]

    steps.append(entry)


def run_bulk_generation(store: RunStore, run_id: str, rows: List[CsvRow]) -> None:
    try:
        store.set_state(run_id, RunState.RUNNING, "Starting run")

        outputs: List[ScriptOutput] = []
        total_scripts = len(rows)

        trace: Dict[str, Any] = {
            "run_id": run_id,
            "created_at": time.time(),
            "use_mock_perplexity": getattr(settings, "USE_MOCK_PERPLEXITY", True),
            "use_mock_gemini": getattr(settings, "USE_MOCK_GEMINI", True),
            "scripts": [],
        }

        for script_index, row in enumerate(rows, start=1):

            if store.get(run_id).cancel_requested:
                store.set_state(run_id, RunState.CANCELED, "Canceled")
                return

            script_steps: List[Dict[str, Any]] = []
            script_trace: Dict[str, Any] = {
                "script_index": script_index,
                "episode_code": row.episode_code,
                "steps": script_steps,
            }


            # PROMPTS

            prompt_1 = build_prompt_1(row)

            store.update_progress(
                run_id,
                script_i=script_index,
                prompt_j=1,
                message=f"Processing item {script_index} of {total_scripts} — Prompt 1/10 (Perplexity)",
            )

            if getattr(settings, "USE_MOCK_PERPLEXITY", True):
                p1_out = f"[MOCK Perplexity P1 | prompt_hash={_sha12(prompt_1)}]\nEpisode: {row.episode_code}\n"
                provider_1 = "perplexity_mock"
            else:
                p1_out = pplx.sonar_deep_research(prompt_1)
                provider_1 = "perplexity"

            if getattr(settings, "USE_TRACE", True):
                _trace_step(script_steps, step=1, provider=provider_1, prompt=prompt_1, output=p1_out)


            prompt_2 = build_prompt_2(p1_out)
            store.update_progress(run_id, script_i=script_index, prompt_j=2,
                                  message=f"Processing item {script_index} of {total_scripts} — Prompt 2/10 (Gemini)")
            p2_out = gemini.generate(prompt_2)
            if getattr(settings, "USE_TRACE", True):
                _trace_step(script_steps, step=2, provider="gemini", prompt=prompt_2, output=p2_out)

            prompt_3 = build_prompt_3(p2_out, row.episode_code)
            store.update_progress(run_id, script_i=script_index, prompt_j=3,
                                  message=f"Processing item {script_index} of {total_scripts} — Prompt 3/10 (Gemini)")
            p3_out = gemini.generate(prompt_3)
            if getattr(settings, "USE_TRACE", True):
                _trace_step(script_steps, step=3, provider="gemini", prompt=prompt_3, output=p3_out)

            prompt_4 = build_prompt_4(p3_out)
            store.update_progress(run_id, script_i=script_index, prompt_j=4,
                                  message=f"Processing item {script_index} of {total_scripts} — Prompt 4/10 (Gemini)")
            p4_out = gemini.generate(prompt_4)
            if getattr(settings, "USE_TRACE", True):
                _trace_step(script_steps, step=4, provider="gemini", prompt=prompt_4, output=p4_out)

            prompt_5 = build_prompt_5(p4_out)
            store.update_progress(run_id, script_i=script_index, prompt_j=5,
                                  message=f"Processing item {script_index} of {total_scripts} — Prompt 5/10 (Gemini)")
            p5_out = gemini.generate(prompt_5)
            if getattr(settings, "USE_TRACE", True):
                _trace_step(script_steps, step=5, provider="gemini", prompt=prompt_5, output=p5_out)

            prompt_6 = build_prompt_6(p5_out)
            store.update_progress(run_id, script_i=script_index, prompt_j=6,
                                  message=f"Processing item {script_index} of {total_scripts} — Prompt 6/10 (Gemini)")
            p6_out = gemini.generate(prompt_6)
            if getattr(settings, "USE_TRACE", True):
                _trace_step(script_steps, step=6, provider="gemini", prompt=prompt_6, output=p6_out)

            prompt_7 = build_prompt_7(p6_out)
            store.update_progress(run_id, script_i=script_index, prompt_j=7,
                                  message=f"Processing item {script_index} of {total_scripts} — Prompt 7/10 (Gemini)")
            p7_out = gemini.generate(prompt_7)
            if getattr(settings, "USE_TRACE", True):
                _trace_step(script_steps, step=7, provider="gemini", prompt=prompt_7, output=p7_out)

            prompt_8 = build_prompt_8(p7_out, row.episode_code)
            store.update_progress(run_id, script_i=script_index, prompt_j=8,
                                  message=f"Processing item {script_index} of {total_scripts} — Prompt 8/10 (Gemini)")
            p8_out = gemini.generate(prompt_8)
            if getattr(settings, "USE_TRACE", True):
                _trace_step(script_steps, step=8, provider="gemini", prompt=prompt_8, output=p8_out)


            prompt_9 = build_prompt_9(p8_out)
            store.update_progress(
                run_id,
                script_i=script_index,
                prompt_j=9,
                message=f"Processing item {script_index} of {total_scripts} — Prompt 9/10 (Perplexity)",
            )

            if getattr(settings, "USE_MOCK_PERPLEXITY", True):
                p9_out = f"[MOCK Perplexity P9 | prompt_hash={_sha12(prompt_9)}]\nOK: (mock fact-check)\n"
                provider_9 = "perplexity_mock"
            else:
                p9_out = pplx.sonar_deep_research(prompt_9)
                provider_9 = "perplexity"

            if getattr(settings, "USE_TRACE", True):
                _trace_step(script_steps, step=9, provider=provider_9, prompt=prompt_9, output=p9_out)

            prompt_10 = build_prompt_10(p9_out, p8_out)
            store.update_progress(
                run_id,
                script_i=script_index,
                prompt_j=10,
                message=f"Processing item {script_index} of {total_scripts} — Prompt 10/10 (Perplexity)",
            )

            if getattr(settings, "USE_MOCK_PERPLEXITY", True):
                p10_out = f"NO MAJOR ERRORS:\n\n{(p8_out or '').strip()}\n\n[MOCK Perplexity P10 | prompt_hash={_sha12(prompt_10)}]"
                provider_10 = "perplexity_mock"
            else:
                p10_out = pplx.sonar_deep_research(prompt_10)
                provider_10 = "perplexity"

            if getattr(settings, "USE_TRACE", True):
                _trace_step(script_steps, step=10, provider=provider_10, prompt=prompt_10, output=p10_out)

            final_script_text = (p10_out or "").strip()

            # Save trace per script
            if getattr(settings, "USE_TRACE", True):
                trace["scripts"].append(script_trace)

            outputs.append(
                ScriptOutput(
                    episode_code=row.episode_code,
                    title=row.episode_code,
                    script_text=final_script_text,
                )
            )

        out_path = settings.outputs_path / f"{run_id}.docx"
        build_docx(outputs, out_path)

        run = store.get(run_id)
        run.output_docx_path = str(out_path)

        if getattr(settings, "USE_TRACE", True):
            trace_path = settings.outputs_path / f"{run_id}.trace.json"
            trace_path.write_text(json.dumps(trace, ensure_ascii=False, indent=2), encoding="utf-8")

        store.set_state(run_id, RunState.COMPLETED, "Completed")

    except Exception as e:
        store.set_failed(run_id, str(e))
