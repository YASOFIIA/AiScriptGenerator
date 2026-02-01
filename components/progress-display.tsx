"use client"

import { Progress } from "@/components/ui/progress"

interface RunStatus {
  state: string
  message: string
  current_script: number
  total_scripts: number
  current_prompt: number
  total_prompts: number
  progress_pct: number
}

interface ProgressDisplayProps {
  status: RunStatus
}

export function ProgressDisplay({ status }: ProgressDisplayProps) {
  const isCompleted = status.state === "COMPLETED"

  return (
    <div className="space-y-4 rounded-lg border border-border bg-muted/20 px-4 py-4">
      {/* Progress Bar */}
      <div className="space-y-2">
        <div className="flex items-center justify-between text-sm">
          <span className="font-medium text-foreground">
            {isCompleted ? "Complete" : "Processing"}
          </span>
          <span className="text-muted-foreground">{status.progress_pct}%</span>
        </div>
        <Progress value={status.progress_pct} className="h-2" />
      </div>

      {/* Status Text */}
      {!isCompleted && (
        <div className="space-y-1 text-sm text-muted-foreground">
          <p>
            Processing item {status.current_script} of {status.total_scripts}
          </p>
          <p>
            Prompt {status.current_prompt}/{status.total_prompts}
          </p>
        </div>
      )}
    </div>
  )
}
