# Direct stdio calls to a configured MCP server

Use when a tool exists on a configured stdio MCP server (per `config.yaml`) but is not exposed in the live Hermes toolset. Spawning the configured server and speaking JSON-RPC over stdio reaches the same tool with the same auth.

1. **Read the server block.** `~/.hermes/config.yaml` (or `$HERMES_HOME/config.yaml`) under `mcp_servers.<name>`: `command`, `args`, `env`, and any `--enabled-tools` regex in args. Extend a copy of the regex if it excludes the tool you need, and pass the config `env` into the child environment.
2. **Spawn.** `subprocess.Popen(command + args, stdin=PIPE, stdout=PIPE, stderr=DEVNULL, text=True)`.
3. **Handshake, one JSON object per line, flush after each write:**
   - initialize: `{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"...","version":"1.0"}}}` (known-good protocol version)
   - then the notification: `{"jsonrpc":"2.0","method":"notifications/initialized"}` (no `id`)
   - then the call: `{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"<tool-name>","arguments":{...}}}`
4. **Read responses by `id`.** Read stdout line by line, keep only the object whose `id` matches the request, skip parseable-but-unrelated lines. Fail on a response carrying `error`, on EOF or process exit, or on a deadline (90s suits Graph-backed calls). The tool payload arrives as `result.content[].text` (often JSON encoded as text); check `result.isError` too.
5. **Clean up in `finally`.** Terminate the process; kill if terminate times out.
6. **Still verify through the normal connector read tools.** Transport-level success is not state success.

The `--enabled-tools` regex in the server's config already covers the common mail tools; when spawning standalone, reuse the config's args rather than inventing a fresh set, so scope and auth match the configured server.
