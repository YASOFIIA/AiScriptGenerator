"use client"

import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

interface SettingsInputProps {
  value: string
  onChange: (value: string) => void
  disabled?: boolean
}

export function SettingsInput({ value, onChange, disabled }: SettingsInputProps) {
  return (
    <div className="space-y-2">
      <Label htmlFor="output-filename" className="text-sm font-medium text-foreground">
        Output filename
      </Label>
      <Input
        id="output-filename"
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        disabled={disabled}
        placeholder="output.docx"
        className="bg-background"
      />
    </div>
  )
}
