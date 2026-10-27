# Direct stdio calls to a configured MCP server

Use when a tool exists on a configured stdio MCP server (per `config.yaml`) but is not exposed in the live Hermes toolset. Spawning the configured server and speaking JSON-RPC over stdio reaches the same tool with the same auth.

1. **Read the server block.** `~/.hermes/config.yaml` (or `$HERMES_HOME/config.yaml`) under `mcp_servers.<name>`: `command`, `args`, `env`, and any `--enabled-tools` regex in args. Extend a copy of the regex if it excludes the tool you need, and pass the config `env` into the child environment. The sandbox has no `yaml` module, so regex the block: cut it at the next two-space-indented key (`\n {2}[a-z_]+:`), never at `\n\S`, because sibling servers under `mcp_servers:` are indented two spaces, so an `\n\S` cut never fires and your args pattern silently swallows the next server's argv (a stray script path lands in the child's command line). Print the raw block before spawning so a parse slip is visible in the same output.
2. **Spawn.** `subprocess.Popen(command + args, stdin=PIPE, stdout=PIPE, stderr=DEVNULL, text=True)`.
3. **Handshake, one JSON object per line, flush after each write:**
   - initialize: `{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"...","version":"1.0"}}}` (known-good protocol version)
   - then the notification: `{"jsonrpc":"2.0","method":"notifications/initialized"}` (no `id`)
   - then `tools/list` (its own id) and take the exact tool name from the result: server-side spelling can differ from the connector's exposed name, and the reply doubles as the server-ready check before you spend the real call.
   - then the call: `{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"<tool-name>","arguments":{...}}}`
4. **Read responses by `id`.** Read stdout line by line, keep only the object whose `id` matches the request, skip parseable-but-unrelated lines. Fail on a response carrying `error`, on EOF or process exit, or on a deadline (90s suits Graph-backed calls). The tool payload arrives as `result.content[].text` (often JSON encoded as text); check `result.isError` too.
5. **Clean up in `finally`.** Terminate the process; kill if terminate times out.
6. **Still verify through the normal connector read tools.** Transport-level success is not state success.

The `--enabled-tools` regex in the server's config already covers the common mail tools; when spawning standalone, reuse the config's args rather than inventing a fresh set, so scope and auth match the configured server.
