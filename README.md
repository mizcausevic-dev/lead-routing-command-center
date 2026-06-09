# Lead Routing Command Center

Lead Routing Command Center is a brokerage routing engine for matching inbound real estate leads to the right agent based on geography, property type, budget, responsiveness, workload, language fit, and luxury readiness.

- Live: `https://mizcausevic-dev.github.io/lead-routing-command-center/`
- Repo: `https://github.com/mizcausevic-dev/lead-routing-command-center`

![Overview](./screenshots/01-overview.png)

## Why this repo is good

- It targets a real brokerage pain point: getting high-intent leads to the right person fast.
- It turns matching into explainable routing instead of opaque round-robin assignment.
- It connects naturally to sales ops, follow-up workflow, and performance accountability.

## What it does

- Scores lead-to-agent fit across zone, property type, budget, language, luxury expectations, response SLA, and load.
- Recommends both a primary route and a backup agent.
- Highlights same-hour follow-up lanes for high-intent demand.
- Exposes a clean API plus operator-friendly proof surfaces.

## What this product does

Lead Routing Command Center turns inbound real estate demand into an explainable routing layer: who should own the lead, why they are the best fit, who is the backup, and whether the follow-up SLA is already at risk.

For a SaaS go-to-market analyst, the product exposes where brokerage growth breaks down: high-intent buyers sitting in generic queues, agents fighting over unclear ownership, and luxury or language-fit leads drifting before anyone can prove who should act. For a SaaS value architect, the value is cleaner conversion motion, lower agent conflict, fewer missed high-value opportunities, and a reusable handoff contract that can connect CRM, ads, concierge, and sales-performance reporting.

Technically, this repo ships a FastAPI service, deterministic ranking logic, JSON endpoints, prerendered public pages, demo fixtures, smoke checks, and screenshot assets. It shares the broader Kinetic Gain pattern: convert operational ambiguity into named lanes, owner-visible evidence, and board-readable next actions.

## Proof

![Matchboard](./screenshots/02-matchboard.png)
![Agent Loads](./screenshots/03-agent-loads.png)
![API Summary](./screenshots/04-api-summary.png)

## Local run

```powershell
cd lead-routing-command-center
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m app.main
```

Open:

- `http://127.0.0.1:4762/`
- `http://127.0.0.1:4762/matchboard`
- `http://127.0.0.1:4762/agent-loads`
- `http://127.0.0.1:4762/api-summary`
- `http://127.0.0.1:4762/docs`

## Validation

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests
.\.venv\Scripts\python.exe scripts\run_demo.py
.\.venv\Scripts\python.exe scripts\smoke_check.py
.\.venv\Scripts\python.exe scripts\prerender_site.py
.\.venv\Scripts\python.exe scripts\render_readme_assets.py
```

## API shape

Endpoints:

- `/api/dashboard/summary`
- `/api/leads`
- `/api/agents`
- `/api/leads/{lead_id}`
- `/api/sample`

## Repo layout

```text
app/
  data/
  services/
docs/
scripts/
screenshots/
tests/
```
