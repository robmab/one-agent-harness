// Harness sensor for OpenCode 2: after every edit it runs check.py and appends the result
// to the tool output, so the model sees it in the same turn (what the PostToolUse hook does in Claude).
// It reuses the sensor's --hook mode: outside the repo (MARKER) or with files it doesn't cover, it says nothing.
import { spawn } from "node:child_process"
import { appendFileSync, existsSync } from "node:fs"
import { dirname, isAbsolute, join, resolve } from "node:path"
import { fileURLToPath } from "node:url"

const SENSOR = "<HARNESS>/personal/scripts/check.py"
const HERE = dirname(fileURLToPath(import.meta.url))
// Create plugins/sensor.debug to log which tools and fields arrive (in plugins/sensor.log)
const DEBUG = existsSync(join(HERE, "sensor.debug"))

const RE_PATCH = /^\*\*\* (?:Add|Update) File: (.+)$/gm
// Only the ones that write: `read` carries the same `path` field and there's nothing to check on a read
const WRITERS = new Set(["write", "edit", "multiedit", "patch", "apply_patch"])

function paths(input: any, base: string): string[] {
  if (!input || typeof input !== "object") return []
  const direct = input.filePath ?? input.file_path ?? input.path
  const single = typeof direct === "string" ? [direct] : []
  // Patches carry several files inside the text
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
        if (r.code === 2) notes.push(r.stderr.trim() + "\nFix it before going on.")
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
