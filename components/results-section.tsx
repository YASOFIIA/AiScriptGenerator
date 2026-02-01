"use client"

import { CheckCircle2, Download, RotateCcw } from "lucide-react"
import { Button } from "@/components/ui/button"

interface ResultsSectionProps {
  runId: string
  filename: string
  onReset: () => void
}

export function ResultsSection({ runId, filename, onReset }: ResultsSectionProps) {
  const handleDownload = () => {
    // Create a download link
    const downloadUrl = `/bulk/${runId}/download`
    const link = document.createElement("a")
    link.href = downloadUrl
    link.download = filename.endsWith(".docx") ? filename : `${filename}.docx`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }

  return (
    <div className="space-y-4 rounded-lg border border-border bg-muted/20 px-4 py-6 text-center">
      <div className="flex flex-col items-center gap-2">
        <CheckCircle2 className="h-10 w-10 text-green-600" />
        <p className="text-lg font-semibold text-foreground">Done</p>
        <p className="text-sm text-muted-foreground">
          Your document is ready to download
        </p>
      </div>

      <div className="flex flex-col gap-2 pt-2 sm:flex-row sm:justify-center">
        <Button onClick={handleDownload} className="gap-2">
          <Download className="h-4 w-4" />
          Download {filename}
        </Button>
        <Button variant="outline" onClick={onReset} className="gap-2">
          <RotateCcw className="h-4 w-4" />
          Start over
        </Button>
      </div>
    </div>
  )
}
