// Sensor del harness para OpenCode 2: tras cada edición pasa check.py y le añade el resultado
// a la salida de la herramienta, para que el modelo lo vea en el mismo turno (lo que hace el hook PostToolUse en Claude).
// Reutiliza el modo --hook del sensor: fuera del repo (MARKER) o con ficheros que no toca, no dice nada.
import { spawn } from "node:child_process"
import { appendFileSync, existsSync } from "node:fs"
import { dirname, isAbsolute, join, resolve } from "node:path"
import { fileURLToPath } from "node:url"

const SENSOR = "<HARNESS>/personal/scripts/check.py"
const HERE = dirname(fileURLToPath(import.meta.url))
// Crea plugins/sensor.debug para registrar qué herramientas y campos llegan (en plugins/sensor.log)
const DEBUG = existsSync(join(HERE, "sensor.debug"))

const RE_PATCH = /^\*\*\* (?:Add|Update) File: (.+)$/gm
// Solo las que escriben: `read` lleva el mismo campo `path` y no hay que comprobar nada al leer
const WRITERS = new Set(["write", "edit", "multiedit", "patch", "apply_patch"])

function paths(input: any, base: string): string[] {
  if (!input || typeof input !== "object") return []
  const direct = input.filePath ?? input.file_path ?? input.path
  const single = typeof direct === "string" ? [direct] : []
  // Los parches llevan varios ficheros dentro del texto
  const text = input.patchText ?? input.patch ?? input.input
  const fromPatch = typeof text === "string" ? [...text.matchAll(RE_PATCH)].map((m) => m[1].trim()) : []
  return [...single, ...fromPatch].map((r) => (isAbsolute(r) ? r : resolve(base, r)))
}

function sensor(path: string): Promise<{ code: number; stdout: string; stderr: string }> {
  return new Promise((ok) => {
    const proc = spawn("py", ["-3", SENSOR, "--hook"], { windowsHide: true })
    let stdout = ""
    let stderr = ""
    proc.stdout.on("data", (d) => (stdout += d))
    proc.stderr.on("data", (d) => (stderr += d))
    proc.on("error", (e) => ok({ code: 0, stdout: "", stderr: String(e) }))
    proc.on("close", (code) => ok({ code: code ?? 0, stdout, stderr }))
    proc.stdin.end(JSON.stringify({ tool_input: { file_path: path } }))
  })
}

function warnings(stdout: string): string {
  try {
    return JSON.parse(stdout)?.hookSpecificOutput?.additionalContext ?? ""
  } catch {
    return ""
  }
}

export default {
  id: "sensor-<PROJECT>",
  async setup(ctx: any) {
    await ctx.tool.hook("execute.after", async (event: any) => {
      if (DEBUG) appendFileSync(join(HERE, "sensor.log"), JSON.stringify({ tool: event.tool, status: event.status, input: event.input }).slice(0, 600) + "\n")
      if (event.status !== "completed" || !WRITERS.has(event.tool)) return
      const files = paths(event.input, ctx.location?.directory ?? process.cwd())
      if (!files.length) return

      const notes: string[] = []
      for (const path of files) {
        const r = await sensor(path)
        if (r.code === 2) notes.push(r.stderr.trim() + "\nCorrígelo antes de seguir.")
        else if (warnings(r.stdout)) notes.push(warnings(r.stdout))
      }
      if (!notes.length) return

      const previous = event.result?.content
      const note = notes.join("\n\n")
      const content = Array.isArray(previous) ? [...previous, { type: "text", text: note }] : [previous, note].filter(Boolean).join("\n\n")
      event.result = { ...event.result, content }
    })
  },
}
