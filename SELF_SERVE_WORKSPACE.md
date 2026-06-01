# Self-Serve Research Workspace

This is the interactive product workspace for the full research audit chain:

```text
topic / PDFs / URLs
  -> Search / source intake
  -> Read and build claim trees
  -> Verify data nodes and causal edges
  -> Distill source registry
  -> Merge thesis
  -> Visualize
  -> Generate dashboard / tracking model
```

## Start

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the server:

```bash
python main.py demo --port 8000
```

Open:

```text
http://localhost:8000/docs/app.html
```

## Recommended First Experience

Use `mock` provider first. It exercises the full pipeline without API keys.

1. Open `Research Workspace`.
2. Keep provider as `mock - offline demo`.
3. Enter a research question.
4. Optionally paste URLs or upload PDFs.
5. Click `Start Investigation`.
6. Watch the pipeline timeline:
   - Search
   - Read
   - Verify
   - Distill
   - Merge
   - Visualize
   - Track
7. Inspect:
   - Outputs
   - Artifacts
   - Registry
   - Dashboard

## Live Providers

For live runs, set API keys before starting the server:

```bash
set MIROMIND_API_KEY=...
set TAVILY_API_KEY=...
python main.py demo --port 8000
```

Then select `miromind` in the provider dropdown.

## Current Product Boundary

Implemented:

- PDF upload input.
- URL source input.
- Topic-only search mode.
- Run config controls.
- Full pipeline trigger.
- WebSocket progress.
- Run list.
- Cancel.
- Outputs.
- Artifacts.
- Source registry view.
- Dashboard model view.
- Mock provider for offline full-chain experience.

Not implemented as production SaaS infrastructure yet:

- User accounts.
- Team workspaces.
- Durable queue.
- Postgres run store.
- Object storage.
- Billing.
- Multi-worker orchestration.

The page is a complete local product workspace for the research chain, not a multi-tenant hosted SaaS shell.
