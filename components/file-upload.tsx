"use client"

import { useCallback } from "react"
import { Upload, FileText, X } from "lucide-react"
import { Button } from "@/components/ui/button"

interface FileUploadProps {
  file: File | null
  onFileChange: (file: File | null) => void
  disabled?: boolean
}

export function FileUpload({ file, onFileChange, disabled }: FileUploadProps) {
  const handleDrop = useCallback(
    (e: React.DragEvent<HTMLDivElement>) => {
      e.preventDefault()
      if (disabled) return

      const droppedFile = e.dataTransfer.files[0]
      if (droppedFile?.name.toLowerCase().endsWith(".csv")) {
        onFileChange(droppedFile)
      }
    },
    [onFileChange, disabled]
  )

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0]
    if (selectedFile) {
      onFileChange(selectedFile)
    }
  }

  const handleRemove = () => {
    onFileChange(null)
  }

  if (file) {
    return (
      <div className="flex items-center justify-between rounded-lg border border-border bg-muted/30 px-4 py-3">
        <div className="flex items-center gap-3">
          <FileText className="h-5 w-5 text-muted-foreground" />
          <span className="text-sm font-medium text-foreground">{file.name}</span>
          <span className="text-xs text-muted-foreground">
            ({(file.size / 1024).toFixed(1)} KB)
          </span>
        </div>
        {!disabled && (
          <Button
            variant="ghost"
            size="icon"
            className="h-8 w-8"
            onClick={handleRemove}
          >
            <X className="h-4 w-4" />
            <span className="sr-only">Remove file</span>
          </Button>
        )}
      </div>
    )
  }

  return (
    <div
      onDrop={handleDrop}
      onDragOver={(e) => e.preventDefault()}
      className={`relative flex flex-col items-center justify-center rounded-lg border-2 border-dashed border-border bg-muted/20 px-6 py-10 transition-colors ${
        disabled
          ? "cursor-not-allowed opacity-50"
          : "cursor-pointer hover:border-muted-foreground/50 hover:bg-muted/40"
      }`}
    >
      <input
        type="file"
        accept=".csv"
        onChange={handleChange}
        disabled={disabled}
        className="absolute inset-0 cursor-pointer opacity-0 disabled:cursor-not-allowed"
      />
      <Upload className="mb-3 h-8 w-8 text-muted-foreground" />
      <p className="text-sm font-medium text-foreground">
        Drop your CSV file here
      </p>
      <p className="mt-1 text-xs text-muted-foreground">or click to browse</p>
    </div>
  )
}
