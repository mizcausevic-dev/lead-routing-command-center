from __future__ import annotations

import html
from pathlib import Path

from app.services.routing_service import build_service

service = build_service()


def page_shell(title: str, eyebrow: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
    :root {{
      --bg: #09111d;
      --panel: #101d2f;
      --panel-2: #17263c;
      --line: #29486f;
      --ink: #f3ecde;
      --muted: #b5c2d7;
      --blue: #6db2ff;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background:
        radial-gradient(circle at top left, rgba(54, 103, 164, 0.18), transparent 30%),
        linear-gradient(180deg, #08111c 0%, #0b1522 100%);
      color: var(--ink);
      font-family: Georgia, "Times New Roman", serif;
    }}
    .frame {{
      width: 1440px;
      min-height: 920px;
      margin: 0 auto;
      padding: 48px;
    }}
    .shell {{
      background: rgba(13, 24, 39, 0.94);
      border: 1px solid var(--line);
      border-radius: 36px;
      padding: 34px 36px 36px;
    }}
    .eyebrow {{
      margin: 0 0 22px;
      font: 700 13px/1.2 "Segoe UI", sans-serif;
      letter-spacing: 0.35em;
      text-transform: uppercase;
      color: var(--blue);
    }}
    h1 {{
      margin: 0;
      font-size: 70px;
      line-height: 1.02;
      max-width: 1180px;
      letter-spacing: -0.05em;
    }}
    p.lead {{
      margin: 24px 0 0;
      max-width: 1060px;
      color: var(--muted);
      font: 400 19px/1.55 "Segoe UI", sans-serif;
    }}
    .pills {{
      display: flex;
      gap: 14px;
      flex-wrap: wrap;
      margin: 22px 0 26px;
    }}
    .pill {{
      background: #1d2d45;
      border: 1px solid #335a8d;
      color: #f5f7fb;
      padding: 10px 16px;
      border-radius: 999px;
      font: 700 15px/1 "Segoe UI", sans-serif;
    }}
    .stats {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 18px;
      margin: 8px 0 34px;
    }}
    .card {{
      background: var(--panel-2);
      border: 1px solid #335885;
      border-radius: 24px;
      padding: 22px 22px 18px;
      min-height: 170px;
    }}
    .card h2 {{
      margin: 0 0 12px;
      color: #a8cbff;
      font: 700 12px/1.2 "Segoe UI", sans-serif;
      letter-spacing: 0.24em;
      text-transform: uppercase;
    }}
    .metric {{
      font-size: 58px;
      line-height: 1;
      margin: 0 0 10px;
    }}
    .card p, .card li, .table, .lane {{
      color: var(--muted);
      font: 400 18px/1.45 "Segoe UI", sans-serif;
    }}
    .grid-2 {{
      display: grid;
      grid-template-columns: 1.25fr 0.85fr;
      gap: 18px;
    }}
    .table {{
      display: grid;
      gap: 12px;
    }}
    .row {{
      display: grid;
      grid-template-columns: 1.15fr 0.9fr 0.8fr 0.9fr;
      gap: 14px;
      align-items: center;
      padding: 16px 18px;
      background: #0c1728;
      border: 1px solid #223c5d;
      border-radius: 18px;
    }}
    .row strong {{
      color: var(--ink);
      display: block;
      font: 700 24px/1.1 Georgia, serif;
    }}
    .small {{
      font-size: 15px;
      color: #87a2c7;
    }}
    .lane {{
      padding: 16px 18px;
      background: #0c1728;
      border: 1px solid #223c5d;
      border-radius: 18px;
      margin-bottom: 12px;
    }}
    .lane strong {{
      display: block;
      color: var(--ink);
      font: 700 24px/1.15 Georgia, serif;
      margin-bottom: 6px;
    }}
    pre {{
      margin: 0;
      color: #d7e8ff;
      font: 16px/1.5 Consolas, monospace;
      white-space: pre-wrap;
    }}
  </style>
</head>
<body>
  <div class="frame">
    <div class="shell">
      <p class="eyebrow">{html.escape(eyebrow)}</p>
      {body}
    </div>
  </div>
</body>
</html>"""


def render_overview() -> str:
    summary = service.summary()
    leads = service.ranked_leads()[:3]
    rows = "".join(
        f"""
        <div class="row">
          <div>
            <strong>{html.escape(lead['name'])}</strong>
            <div class="small">{html.escape(lead['zone'])} · {html.escape(lead['propertyType'])}</div>
          </div>
          <div>{html.escape(lead['primaryAgent'])}</div>
          <div>{lead['primaryScore']}</div>
          <div>{lead['urgencyScore']}</div>
        </div>
        """
        for lead in leads
    )
    body = f"""
      <h1>Route every lead to the right agent before high intent drifts into silence or overlap.</h1>
      <p class="lead">
        Lead Routing Command Center scores geography, property fit, budget alignment, language, responsiveness, and agent load
        so brokerages can assign inbound demand with much more precision than a round-robin queue.
      </p>
      <div class="pills">
        <div class="pill">geo + budget routing</div>
        <div class="pill">agent workload balancing</div>
        <div class="pill">luxury and language matching</div>
        <div class="pill">same-hour follow-up priority</div>
      </div>
      <div class="stats">
        <div class="card"><h2>leads queued</h2><div class="metric">{summary['leadCount']}</div><p>Inbound opportunities ranked for immediate routing.</p></div>
        <div class="card"><h2>avg. urgency</h2><div class="metric">{summary['averageUrgencyScore']}</div><p>Composite of intent and timeline pressure.</p></div>
        <div class="card"><h2>same-hour follow-up</h2><div class="metric">{summary['sameHourFollowupCount']}</div><p>Assignments strong enough to trigger immediate action.</p></div>
        <div class="card"><h2>luxury leads</h2><div class="metric">{summary['luxuryLeadCount']}</div><p>{html.escape(summary['leadRecommendation'])}</p></div>
      </div>
      <div class="grid-2">
        <div class="card"><h2>route queue</h2><div class="table">{rows}</div></div>
        <div class="card"><h2>lead recommendation</h2><p>{html.escape(summary['leadRecommendation'])}</p></div>
      </div>
    """
    return page_shell("Lead Routing Command Center", "Lead Routing Command Center", body)


def render_matchboard() -> str:
    lead = service.lead("lead-9002") or service.ranked_leads()[0]
    matches = "".join(
        f"""
        <div class="lane">
          <strong>{html.escape(match['agentName'])}</strong>
          <div>Score {match['score']} · SLA {match['responseSlaMinutes']} min · Active leads {match['activeLeads']}</div>
          <div class="small">{html.escape(match['reason'])}</div>
        </div>
        """
        for match in lead["matches"]
    )
    body = f"""
      <h1>Every lead keeps a visible primary route and backup path instead of disappearing into a black box assignment.</h1>
      <p class="lead">
        The matchboard makes it easy for brokerage ops to explain why one agent got the lead, which backup exists,
        and whether the route should prioritize language, luxury, or response speed.
      </p>
      <div class="card">
        <h2>{html.escape(lead['name'])} · {html.escape(lead['zone'])}</h2>
        {matches}
      </div>
    """
    return page_shell("Matchboard", "Agent Matchboard", body)


def render_agent_loads() -> str:
    agents = service.agent_loads()
    cards = "".join(
        f"""
        <div class="lane">
          <strong>{html.escape(agent['agentName'])}</strong>
          <div>Active leads {agent['activeLeads']} · SLA {agent['responseSlaMinutes']} min · Conversion {agent['conversionRate']}%</div>
        </div>
        """
        for agent in agents
    )
    body = f"""
      <h1>The ops team can see whether agent capacity and conversion quality still support the routing strategy.</h1>
      <p class="lead">
        Load visibility keeps the command center from overfeeding a top closer while other qualified agents sit underused.
      </p>
      <div class="card">
        <h2>agent load board</h2>
        {cards}
      </div>
    """
    return page_shell("Agent Loads", "Agent Load Board", body)


def render_api_summary() -> str:
    payload = service.sample_payload()
    body = f"""
      <h1>The API exposes route recommendations in a shape that CRMs, ops dashboards, and brokerage workflows can use.</h1>
      <p class="lead">
        Lead urgency, primary and backup assignment, and route rationale stay together so downstream systems can act without guesswork.
      </p>
      <div class="card">
        <h2>sample payload</h2>
        <pre>{html.escape(str(payload))}</pre>
      </div>
    """
    return page_shell("API Summary", "API Summary", body)


def write_static_proof_pages(output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    pages = {
        "01-overview.html": render_overview(),
        "02-matchboard.html": render_matchboard(),
        "03-agent-loads.html": render_agent_loads(),
        "04-api-summary.html": render_api_summary(),
    }
    written: list[Path] = []
    for name, contents in pages.items():
        path = output_dir / name
        path.write_text(contents, encoding="utf-8")
        written.append(path)
    return written
