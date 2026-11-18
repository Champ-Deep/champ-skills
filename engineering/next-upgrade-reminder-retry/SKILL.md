---
name: next-upgrade-reminder-retry
description: Use when Next exits after an upgrade reminder.
---

# Next upgrade reminder retry

Read the installed Next upgrade nudge implementation before treating a repeated reminder as a failed compilation. Some versions store a retry receipt under the build cache with a five-minute lifetime. Retry the identical command immediately after the reminder, not after a long test or screenshot run, because an expired receipt prompts again.

Keep the retry bounded to one immediate retry. Do not edit node_modules, disable security checks or upgrade dependencies outside the task's scope. A successful retry proves the build, not that the advisory is resolved. Preserve both command logs and route the advisory to the main lane separately.
