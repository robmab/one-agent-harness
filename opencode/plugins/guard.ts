// Harness guard for OpenCode 2: before every command, write, subagent or question it runs guard.py (what the
// PreToolUse hook does in Claude), with the session id so it reads the user's messages from OpenCode's database.
// If it blocks it:
// - a command: swapped for one that only prints the notice and exits with an error;
// - the reviewer before the close: the subagent only answers with the notice;
// - the retro question before the close: the question becomes the notice;
// - a write (a credential in the content): it throws an error with the notice.
// The paths in guard.py's FORBIDDEN_PATHS also go in opencode.jsonc as "edit" → "deny".
import { spawn } from "node:child_process"

const GUARD = "<HARNESS>/personal/scripts/guard.py"
const COMMANDS = new Set(["shell", "bash"])
const WRITES = new Set(["write", "edit", "multiedit", "patch", "apply_patch"])
const CLOSE = new Set(["subagent", "question"])

function guard(event: any): Promise<string> {
  return new Promise((ok) => {
    const proc = spawn("py", ["-3", GUARD, "--hook"], { windowsHide: true })
    let errors = ""
    proc.stderr.on("data", (d) => (errors += d))
    proc.on("error", () => ok(""))   // no Python, no guard: it lets it through, like the hook
    proc.on("close", (code) => ok(code === 2 && errors.startsWith("guard:") ? errors.trim() : ""))
    proc.stdin.end(JSON.stringify({ tool_name: event.tool, tool_input: event.input, opencode_session: event.sessionID }))
  })
}

// a single-quoted string: PowerShell doubles the quote, POSIX shells close and reopen it
function quoted(text: string): string {
  return process.platform === "win32" ? `'${text.replace(/'/g, "''")}'` : `'${text.replace(/'/g, "'\\''")}'`
}

export default {
  id: "harness-guard",
  async setup(ctx: any) {
    await ctx.tool.hook("execute.before", async (event: any) => {
      const t = event.tool
      if (!COMMANDS.has(t) && !WRITES.has(t) && !CLOSE.has(t)) return
      const notice = await guard(event)
      if (!notice) return
      if (COMMANDS.has(t)) event.input = { ...event.input, command: `echo ${quoted(notice)}; exit 1` }
      else if (t === "subagent") event.input = { ...event.input, prompt: `Do nothing: answer only with this text, as is.\n\n${notice}` }
      else if (t === "question") event.input = { ...event.input, questions: [{ question: notice, header: "guard", options: [{ label: "OK", description: "Not launched" }] }] }
      else throw new Error(notice)
    })
  },
}
