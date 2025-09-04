# FastestMCP — Quick Agent Prompt (Readable + Actionable)

TL;DR
FastestMCP is a tiny, high-level Python toolkit to generate and run MCP (Model Context Protocol) servers and clients quickly. Start with `fastestmcp --help` for live examples; use `--level` to pick how much structure you want.

Installation
```bash
# Install with uv (recommended)
uv pip install fastestmcp

# Or with pip
pip install fastestmcp
```

Core commands
- `fastestmcp --help` — show CLI help and examples
- `fastestmcp server --help` — server generation options
- `fastestmcp client --help` — client generation options

Quick flow
1. Pick a generation `--level` (1–5). 2. Run `fastestmcp server --level N --name my-server`. 3. Inspect or run the generated server (single file or module). 4. Connect a client with `fastestmcp client` or an MCP-aware host.

MCP in one sentence
Servers expose Tools (functions), Resources (data), and Prompts (templates); clients discover capabilities, call tools/read resources, and receive notifications.

What each generation level gives you defaults you can add to
- Level 1 — Zero-config: single-file server, 1–2 example tools, stdio transport. Fastest to get started.
- Level 2 — Minimal: mono-file with small component imports, a few tools/resources, simple examples.
- Level 3 — Standard: modular code, multiple tools/resources, basic error handling and component marketplace wiring.
- Level 4 — Advanced: auth examples, multiple transports (stdio/http), middleware, logging, and more complex workflows.
- Level 5 — Enterprise: production-ready layout (microservices, monitoring, tests), full MCP primitives implemented.

Best-practice checklist (short)
- Start small: prototype at Level 1 or 2.
- Use stdio locally, HTTP for multi-client/remote servers.
- Design tools with clear input schemas and single responsibility.
- Validate inputs and return structured error content (not raw exceptions).
- Document tool signatures and sample responses.
- Add unit tests for tool logic; integration tests for server lifecycle.

When to use FastestMCP vs FastMCP vs Vanilla MCP
- FastestMCP: fastest path — CLI generation, demos, prototypes.
- FastMCP: production-ready Pythonic framework with decorators and cleaner APIs.
- Vanilla MCP: raw JSON-RPC / custom transports for advanced users.


Final TL;DR: FastestMCP is the quickest way to generate, run, and experiment with MCP servers and clients. Start with `fastestmcp --help`, pick a level, and build up as needed. For anything else, just ask for an example or a file.
