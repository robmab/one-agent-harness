# <PROJECT> domain

Business rules you can't see by reading a screen: where each piece of data lives, what changes it and what traps it has. If something here doesn't match the code, the code wins: say so and it gets fixed. Use function names, not line numbers, which change.

**Index:** <!-- FILL-IN: one area per section. --> Read only the section that applies.

<!-- FILL-IN: start empty and add an entry only when a session struggled to understand a rule. Example: -->
## Invoices (example: replace it)

- **Two different data:** `Invoice.issued_at` says when it was issued; `Invoice.sent_at`, when it reached the customer. Issuing doesn't send it.
- **Who writes it:** `Invoice.issue()` and the nightly job. For the current list, `grep` the assignment.
- **Trap:** an issued invoice is never edited: it gets a credit note.
