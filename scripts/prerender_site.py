from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.render import render_agent_loads, render_api_summary, render_docs, render_matchboard, render_overview
from app.services.routing_service import build_service

SITE = ROOT / "site"
BASE_URL = "https://mizcausevic-dev.github.io/lead-routing-command-center"


def write(relative_path: str, contents: str) -> None:
    target = SITE / relative_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(contents, encoding="utf-8")


def main() -> None:
    if SITE.exists():
        shutil.rmtree(SITE)

    service = build_service(ROOT)
    pages = {
        "index.html": render_overview(),
        "matchboard/index.html": render_matchboard(),
        "agent-loads/index.html": render_agent_loads(),
        "api-summary/index.html": render_api_summary(),
        "docs/index.html": render_docs(),
    }
    for route, html in pages.items():
        write(route, html)

    payloads = {
        "api/dashboard/summary/index.json": service.summary(),
        "api/leads/index.json": service.ranked_leads(),
        "api/agents/index.json": service.agent_loads(),
        "api/sample/index.json": service.sample_payload(),
    }
    for route, payload in payloads.items():
        write(route, f"{json.dumps(payload, indent=2)}\n")

    routes = ["", "matchboard/", "agent-loads/", "api-summary/", "docs/"]
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}/sitemap.xml\n")
    write(
        "sitemap.xml",
        "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
        "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n"
        + "\n".join(f"  <url><loc>{BASE_URL}/{route}</loc></url>" for route in routes)
        + "\n</urlset>\n",
    )

    print(f"Prerendered {len(pages)} pages and {len(payloads)} JSON endpoints to {SITE}")


if __name__ == "__main__":
    main()
