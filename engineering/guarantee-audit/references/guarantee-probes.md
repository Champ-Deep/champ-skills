# Copy-pasteable probes for the common guarantee classes

Pairs with the SKILL.md: each probe is the smallest thing that would prove the
claim false. Run it against the real dependency, not a test double.

## Claims made in prose about a payload contract

| The claim | The probe |
|---|---|
| "the provider accepts our contact block" | Send the payload once against the live endpoint with a test key and read the provider's error text: an unknown field name comes back as *missing*, not as a validation error naming your field |
| "identity fields are optional" | Send the block omitted entirely. If the provider rejects with a missing-field error naming it, the block is mandatory and must carry real data or be configured at the account level |
| "the account default covers what we omit" | Read the provider's account settings page (or an unauthenticated profile probe) before concluding the block must ship in every request |

Never satisfy the probe by filling the block with a placeholder: the provider
accepts it and the false data lands where it cannot be recalled. A placeholder
that would become a real-world fact is a finding, not a fixture.

## Claims about verification

| The claim | The probe |
|---|---|
| "the suite passes" | Run the unfiltered suite once and state the command next to the count. A path-filtered green run is a report about the filter |
| "the fix did not break anything else" | Run the same unfiltered command on the unchanged baseline and compare totals; a lower post-fix count from a narrower filter is not a regression and not a pass |
| "the new build is live" | Read the platform's own version or commit identity field back after the rollout line, and read the log tail: a deploy script can print a failed post-deploy smoke *after* reporting the container live |

## Claims about per-call limits and metering

| The claim | The probe |
|---|---|
| "every call is rate limited, capped and logged" | Find where the limit is counted: per HTTP request or per operation. On any JSON-RPC endpoint (MCP, LSP-style), POST an array of N `tools/call` messages in one request with the daily cap at 2 and count the results that ran and the log rows written. SDK transports often still accept batches, so a per-request guard lets one request run N calls |
| "one log row per call" | Same batch probe: the log must show N rows or the array must be refused before the transport sees it |

## The double that hides the failure

A `fakeredis`, in-memory dict, or mocked transport executes commands one at a
time, so the interleaving that breaks the code cannot occur. When the guarantee
is about concurrency, ordering, or an external field contract, re-run the probe
against the real service and say in the report which double the suite uses.