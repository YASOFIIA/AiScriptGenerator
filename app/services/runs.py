from __future__ import annotations

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, Optional
import time
import uuid


class RunState(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELED = "CANCELED"

@dataclass
class RunStatus:
    run_id: str
    state: RunState = RunState.PENDING
    message: str = "Waiting"
    current_script: int=0
    total_scripts: int=0
    current_prompt: int=0
    total_prompts: int=10
    progress_pct: int=0
    error: Optional[str]=None
    created_at: float=field(default_factory=time.time)
    output_docx_path: Optional[str] = None
    cancel_requested: bool = False

class RunStore:
    def __init__(self) -> None:
        self._runs: Dict[str, RunStatus] = {}
    def create_run(self, total_scripts:int) -> RunStatus:
        run_id = uuid.uuid4().hex
        run = RunStatus(run_id=run_id, total_scripts=total_scripts)
        self._runs[run_id] = run
        return run
    def get(self,run_id: str) -> RunStatus:
        if run_id not in self._runs:
            raise KeyError(f"Run {run_id} not found")
        return self._runs[run_id]
    def request_cancel(self, run_id: str) -> None:
        run = self.get(run_id)
        run.cancel_requested = True
        run.message = "Cancel requested"
    def update_progress(self, run_id: str, *, script_i: int, prompt_j: int, message: str) -> None:
        run = self.get(run_id)
        run.current_script = script_i
        run.current_prompt = prompt_j
        run.message = message
        #roughly progress in %
        if run.total_scripts > 0:
            done_units = (script_i - 1) * run.total_prompts + prompt_j
            total_units = run.total_scripts * run.total_prompts
            run.progress_pct = int((done_units / total_units) * 100)
    def set_state(self, run_id: str, state: RunState, message: str="" ) -> None:
        run = self.get(run_id)
        run.state= state
        if message:
            run.message = message
        if state == RunState.COMPLETED:
            run.progress_pct = 100
    def set_failed(self, run_id: str, error: str) -> None:
        run = self.get(run_id)
        run.state = RunState.FAILED
        run.error = error
        run.message = "Failed"