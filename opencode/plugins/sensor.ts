// Sensor del harness para OpenCode 2: tras cada edición pasa comprobar.py y le añade el resultado
// a la salida de la herramienta, para que el modelo lo vea en el mismo turno (lo que hace el hook PostToolUse en Claude).
// Reutiliza el modo --hook del sensor: fuera del repo (MARCADOR) o con ficheros que no tocan, no dice nada.
import { spawn } from "node:child_process"
import { appendFileSync, existsSync } from "node:fs"
import { dirname, isAbsolute, join, resolve } from "node:path"
import { fileURLToPath } from "node:url"

const SENSOR = "<HARNESS>/personal/scripts/comprobar.py"
const AQUI = dirname(fileURLToPath(import.meta.url))
// Crea plugins/sensor.debug para registrar qué herramientas y campos llegan (en plugins/sensor.log)
const DEBUG = existsSync(join(AQUI, "sensor.debug"))

const RE_PARCHE = /^\*\*\* (?:Add|Update) File: (.+)$/gm
// Solo las que escriben: `read` lleva el mismo campo `path` y no hay que comprobar nada al leer
const ESCRIBEN = new Set(["write", "edit", "multiedit", "patch", "apply_patch"])

function rutas(input: any, base: string): string[] {
  if (!input || typeof input !== "object") return []
  const directa = input.filePath ?? input.file_path ?? input.path
  const sueltas = typeof directa === "string" ? [directa] : []
  // Los parches traen varios ficheros dentro del texto
  const texto = input.patchText ?? input.patch ?? input.input
  const delParche = typeof texto === "string" ? [...texto.matchAll(RE_PARCHE)].map((m) => m[1].trim()) : []
  return [...sueltas, ...delParche].map((r) => (isAbsolute(r) ? r : resolve(base, r)))
}

function sensor(ruta: string): Promise<{ codigo: number; salida: string; errores: string }> {
  return new Promise((ok) => {
    const proc = spawn("py", ["-3", SENSOR, "--hook"], { windowsHide: true })
    let salida = ""
    let errores = ""
    proc.stdout.on("data", (d) => (salida += d))
    proc.stderr.on("data", (d) => (errores += d))
    proc.on("error", (e) => ok({ codigo: 0, salida: "", errores: String(e) }))
    proc.on("close", (codigo) => ok({ codigo: codigo ?? 0, salida, errores }))
    proc.stdin.end(JSON.stringify({ tool_input: { file_path: ruta } }))
  })
}

function avisos(salida: string): string {
  try {
    return JSON.parse(salida)?.hookSpecificOutput?.additionalContext ?? ""
  } catch {
    return ""
  }
}

export default {
  id: "sensor-<PROYECTO>",
  async setup(ctx: any) {
    await ctx.tool.hook("execute.after", async (event: any) => {
      if (DEBUG) appendFileSync(join(AQUI, "sensor.log"), JSON.stringify({ tool: event.tool, status: event.status, input: event.input }).slice(0, 600) + "\n")
      if (event.status !== "completed" || !ESCRIBEN.has(event.tool)) return
      const ficheros = rutas(event.input, ctx.location?.directory ?? process.cwd())
      if (!ficheros.length) return

      const notas: string[] = []
      for (const ruta of ficheros) {
        const r = await sensor(ruta)
        if (r.codigo === 2) notas.push(r.errores.trim() + "\nCorrígelo antes de seguir.")
        else if (avisos(r.salida)) notas.push(avisos(r.salida))
      }
      if (!notas.length) return

      const previo = event.result?.content
      const nota = notas.join("\n\n")
      const content = Array.isArray(previo) ? [...previo, { type: "text", text: nota }] : [previo, nota].filter(Boolean).join("\n\n")
      event.result = { ...event.result, content }
    })
  },
}
