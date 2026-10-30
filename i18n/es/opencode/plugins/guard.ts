// Guard del harness para OpenCode 2: antes de cada orden, escritura, subagente o pregunta pasa guard.py (lo que
// hace el hook PreToolUse en Claude), con el id de la sesión para que lea los mensajes del usuario de la base de datos.
// Si lo bloquea:
// - una orden: la cambia por una que solo enseña el aviso y sale con error;
// - el revisor antes del cierre: el subagente solo contesta con el aviso;
// - la pregunta del repaso antes del cierre: la pregunta pasa a ser el aviso;
// - una escritura (una credencial en el contenido): lanza un error con el aviso.
// Las rutas de FORBIDDEN_PATHS de guard.py van además en opencode.jsonc como "edit" → "deny".
import { spawn } from "node:child_process"

const GUARD = "<HARNESS>/personal/scripts/guard.py"
const COMMANDS = new Set(["shell", "bash"])
const WRITES = new Set(["write", "edit", "multiedit", "patch", "apply_patch"])
const CLOSE = new Set(["subagent", "question"])

function guard(event: any): Promise<string> {
  return new Promise((ok) => {
    const proc = spawn("py", ["-3", GUARD, "--hook"], { windowsHide: true })
    let errores = ""
    proc.stderr.on("data", (d) => (errores += d))
    proc.on("error", () => ok(""))   // sin Python no hay guard: deja pasar, como el hook
    proc.on("close", (codigo) => ok(codigo === 2 && errores.startsWith("guard:") ? errores.trim() : ""))
    proc.stdin.end(JSON.stringify({ tool_name: event.tool, tool_input: event.input, opencode_session: event.sessionID }))
  })
}

// un texto entre comillas simples: PowerShell dobla la comilla, las shells POSIX la cierran y la reabren
function quoted(texto: string): string {
  return process.platform === "win32" ? `'${texto.replace(/'/g, "''")}'` : `'${texto.replace(/'/g, "'\\''")}'`
}

export default {
  id: "harness-guard",
  async setup(ctx: any) {
    await ctx.tool.hook("execute.before", async (event: any) => {
      const t = event.tool
      if (!COMMANDS.has(t) && !WRITES.has(t) && !CLOSE.has(t)) return
      const aviso = await guard(event)
      if (!aviso) return
      if (COMMANDS.has(t)) event.input = { ...event.input, command: `echo ${quoted(aviso)}; exit 1` }
      else if (t === "subagent") event.input = { ...event.input, prompt: `No hagas nada: contesta solo con este texto, tal cual.\n\n${aviso}` }
      else if (t === "question") event.input = { ...event.input, questions: [{ question: aviso, header: "guard", options: [{ label: "Entendido", description: "No se lanza" }] }] }
      else throw new Error(aviso)
    })
  },
}
