"use client"

import { useState, useCallback } from "react"
import { FileUpload } from "@/components/file-upload"
import { SettingsInput } from "@/components/settings-input"
import { ProgressDisplay } from "@/components/progress-display"
import { ResultsSection } from "@/components/results-section"
import { Button } from "@/components/ui/button"
import { Spinner } from "@/components/ui/spinner"

type RunState = "PENDING" | "RUNNING" | "COMPLETED" | "FAILED" | "CANCELED"

interface RunStatus {
  run_id: string
  state: RunState
  message: string
  current_script: number
  total_scripts: number
  current_prompt: number
  total_prompts: number
  progress_pct: number
  error: string | null
  output_docx_path: string | null
}

export default function HomePage() {
  const [file, setFile] = useState<File | null>(null)
  const [outputFilename, setOutputFilename] = useState("output.docx")
  const [runId, setRunId] = useState<string | null>(null)
  const [status, setStatus] = useState<RunStatus | null>(null)
  const [isUploading, setIsUploading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const isRunning = status?.state === "RUNNING"
  const isCompleted = status?.state === "COMPLETED"
  const isFailed = status?.state === "FAILED"
  const canGenerate = file && !isRunning && !isUploading

  const pollStatus = useCallback(async (id: string) => {
    try {
      const res = await fetch(`/bulk/${id}/status`)
      if (!res.ok) throw new Error("Failed to fetch status")
      const data: RunStatus = await res.json()
      setStatus(data)

      if (data.state === "RUNNING") {
        setTimeout(() => pollStatus(id), 1000)
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error")
    }
  }, [])

  const handleGenerate = async () => {
    if (!file) return

    setError(null)
    setIsUploading(true)
    setStatus(null)

    try {
      // Step 1: Upload CSV
      const formData = new FormData()
      formData.append("file", file)

      const uploadRes = await fetch("/bulk/upload-csv", {
        method: "POST",
        body: formData,
      })

      if (!uploadRes.ok) {
        const errData = await uploadRes.json()
        throw new Error(errData.detail || "Upload failed")
      }

      const { run_id, total_scripts } = await uploadRes.json()
      setRunId(run_id)
      setStatus({
        run_id,
        state: "PENDING",
        message: "Starting...",
        current_script: 0,
        total_scripts,
        current_prompt: 0,
        total_prompts: 10,
        progress_pct: 0,
        error: null,
        output_docx_path: null,
      })

      // Step 2: Start the run
      const startRes = await fetch(`/bulk/${run_id}/start`, {
        method: "POST",
      })

      if (!startRes.ok) {
        throw new Error("Failed to start generation")
      }

      setIsUploading(false)

      // Step 3: Poll for status
      pollStatus(run_id)
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error")
      setIsUploading(false)
    }
  }

  const handleCancel = async () => {
    if (!runId) return

    try {
      await fetch(`/bulk/${runId}/cancel`, { method: "POST" })
    } catch (err) {
      console.error("Cancel failed:", err)
    }
  }

  const handleReset = () => {
    setFile(null)
    setRunId(null)
    setStatus(null)
    setError(null)
    setOutputFilename("output.docx")
  }

  return (
    <main className="min-h-screen bg-background">
      <div className="mx-auto max-w-xl px-6 py-16">
        <header className="mb-12 text-center">
          <h1 className="text-2xl font-semibold tracking-tight text-foreground">
            AI Script Generator
          </h1>
          <p className="mt-2 text-sm text-muted-foreground">
            Upload a CSV file to generate scripts
          </p>
        </header>

        <div className="space-y-8">
          {/* Upload Section */}
          <FileUpload
            file={file}
            onFileChange={setFile}
            disabled={isRunning || isUploading}
          />

          {/* Settings */}
          <SettingsInput
            value={outputFilename}
            onChange={setOutputFilename}
            disabled={isRunning || isUploading}
          />

          {/* Error Display */}
          {(error || isFailed) && (
            <div className="rounded-lg border border-destructive/50 bg-destructive/10 px-4 py-3 text-sm text-destructive">
              {error || status?.error || "An error occurred"}
            </div>
          )}

          {/* Progress Display */}
          {status && (isRunning || isCompleted) && (
            <ProgressDisplay status={status} />
          )}

          {/* Results */}
          {isCompleted && runId && (
            <ResultsSection
              runId={runId}
              filename={outputFilename}
              onReset={handleReset}
            />
          )}

          {/* Action Buttons */}
          {!isCompleted && (
            <div className="flex gap-3">
              <Button
                onClick={handleGenerate}
                disabled={!canGenerate}
                className="flex-1"
              >
                {isUploading ? (
                  <>
                    <Spinner className="mr-2" />
                    Uploading...
                  </>
                ) : isRunning ? (
                  <>
                    <Spinner className="mr-2" />
                    Generating...
                  </>
                ) : (
                  "Generate"
                )}
              </Button>

              {isRunning && (
                <Button variant="outline" onClick={handleCancel}>
                  Cancel
                </Button>
              )}
            </div>
          )}
        </div>
      </div>
    </main>
  )
}
