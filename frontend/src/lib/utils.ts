import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatDate(date: string | Date): string {
  return new Intl.DateTimeFormat('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  }).format(new Date(date))
}

export function getScoreColor(pct: number): string {
  if (pct >= 75) return 'text-success'
  if (pct >= 60) return 'text-warning'
  return 'text-error'
}

export function getScoreBgColor(pct: number): string {
  if (pct >= 75) return 'bg-green-100 text-green-800'
  if (pct >= 60) return 'bg-yellow-100 text-yellow-800'
  return 'bg-red-100 text-red-800'
}