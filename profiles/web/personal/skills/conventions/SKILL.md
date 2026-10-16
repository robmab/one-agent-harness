---
name: conventions
description: "<PROJECT> code conventions: where logic lives, endpoints and permissions, database, frontend, tests and anti-patterns. Use when: before writing or reviewing ANY <PROJECT> code."
---

# Code conventions — <PROJECT>

**CONCEPT:** the rules that always apply to the project's code, loaded before writing or reviewing any of it. Without them the agent writes "good code" in general, not code that fits here.

> **PROFILE · web.** General web rules, valid for most stacks. Adjust the lines marked `TUNE` to yours and then remove the mark.

If you're not in the <PROJECT> repo, ignore this skill.

## Tech stack
<!-- TUNE: main languages and frameworks. Exact versions and their traps go in `stack`. -->

## Naming
- One language for identifiers across the project, and one case per kind of file.
<!-- TUNE: camelCase or snake_case per language; file and folder names. -->

## Architecture: where things go
- **Business logic in the model or a service,** not in the controller or the template: a calculation about an entity is a method of that entity.
- **Thin controllers:** read the request, call the logic, return the response.
- **Shared pieces** (used on 2+ screens) in a shared place; one screen's pieces next to that screen.
<!-- TUNE: the project's folders for models, services, controllers, templates and components. -->

## Endpoints and permissions
- **A permission on every entry point,** checked on the server; the endpoint behind a screen uses the same permission as the screen.
- **Validate the input on the server,** early, and return early. Never trust what the front sends (hidden fields, disabled buttons).
- **Changes only through POST, PUT or DELETE,** never through GET.

## Database
- **Schema changes through migrations,** never by hand in a shared database.
- **Queries with parameters,** never by concatenating or interpolating values.
- **Writes to a shared database or environment:** ask first.
<!-- TUNE: the migration tool and where migrations live. -->

## Frontend
- **Visible text translatable** with the project's i18n function, never hard-coded in one language.
- **No inline styles or loose values:** colours, radii and spacing come from the design variables (`ui`).
- **Versioned assets:** when a CSS or JS changes, its cache-busting (`?v=`, a hash) changes too.
- **Accessibility minimum:** every input with its label, images with `alt`, visible focus, enough contrast.
- **No debugging leftovers** (`console.log`, `debugger`) and no keys or secrets in the front.
<!-- TUNE: the framework and its component pattern; how assets are loaded. -->

## Tests
- **If the project has tests:** business logic, calculations, permissions and every fixed bug get one; layout and glue code don't.
- **The user decides the cases;** the agent writes them, and a review looks at the assertions, not the setup.
<!-- TUNE: framework, where tests live and how to run a single one. -->

## Anti-patterns — DO NOT
- Rewriting what works to "tidy it up", or changing an API without asking.
- Adding a library for something the stack already does.
- Copying a component that already exists instead of reusing it.
<!-- TUNE: what has already caused damage in this project. The reviewer treats this section as critical. -->

## Formatting and comments
- **Lines of about 100 characters:** split long conditions, calls and objects instead of leaving them long.
- **Short comments** that say what or why; a fix doesn't get a comment (it goes in the commit).
<!-- TUNE: the project's formatter or linter. -->
