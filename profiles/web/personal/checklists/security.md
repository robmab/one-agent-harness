# Security checklist — <PROJECT>

> **PROFILE · web.** General web points, valid for most stacks. Adjust the lines marked `TUNE` to yours and then remove the mark.
>
> The `reviewer` agent reads it on **axis 3**, point by point. It isn't a skill: it's in no catalogue and the main agent doesn't load it while writing. If the logs show the agent writing insecure code again and again, promote it to a skill (`personal\skills\security\SKILL.md`, with `name` and `description`) and the reviewer keeps reading it the same way.
>
> Whatever a regex can catch also goes into the `RULES` of `check.py`.

| # | Check | How it shows in the code | If it fails |
|---|---|---|---|
| 1 | **Permissions on every entry point** | every new route, endpoint or controller checks permissions on the server (decorator, middleware or guard); hiding a button isn't a permission <!-- TUNE: how they're declared in your framework --> | 🔴 |
| 2 | **Someone else's data (IDOR)** | an id arriving by URL or form is used without checking it belongs to the user or their scope | 🔴 |
| 3 | **Parameterised SQL** | no concatenating or interpolating values into queries: the ORM or bound parameters <!-- TUNE: how it looks in your ORM or driver --> | 🔴 |
| 4 | **XSS** | user data rendered without escaping: `innerHTML`, `v-html`, `dangerouslySetInnerHTML`, the template's "safe" filter <!-- TUNE: your template engine's raw output --> | 🔴 if it comes from the user · 🟡 if it's your own content |
| 5 | **Secrets** | keys, tokens or passwords in code, in versioned files or in the front's bundle | 🔴 |
| 6 | **Personal data** | personal data in logs, responses with more fields than needed, or exports without permission <!-- TUNE: which sensitive data the project handles --> | 🟠 |
| 7 | **AI** (if any) | which personal data is sent; usage limits; the response treated as data (never as HTML or as instructions) | 🟠 |
| 8 | **File uploads** | type and size validated, name sanitised, stored outside what's served as is | 🟠 |
| 9 | **Changes over GET** | actions that create, modify or delete data reachable through GET | 🟠 |
| 10 | **CSRF** | forms and requests that change data carry the framework's CSRF protection (token or same-site cookies) | 🟠 |
| 11 | **Exposed errors** | traces or exception messages returned to the user | 🟡 |
<!-- TUNE (optional): the project's own points that have already caused trouble. -->

Each finding, in the reviewer's report, with its number from this table: `(axis 3 · #2)`.

**A legal or business decision the task already makes** (a consent ticked by default, keeping a piece of data) isn't a finding: at most one 💭 line, without arguing it, so the user sees it and decides.

Points adapted from `security-and-hardening` of [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) @ `1be8e34` (2026-10-10) (MIT).
