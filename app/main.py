from __future__ import annotations

import json

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse

from app.render import render_agent_loads, render_api_summary, render_docs, render_matchboard, render_overview
from app.services.routing_service import build_service

app = FastAPI(
    title="Lead Routing Command Center",
    version="1.1.0",
    description=(
        "Real estate lead routing engine for brokerages, agent matching, workload balancing, and follow-up prioritization."
    ),
)

service = build_service()


@app.get("/", response_class=HTMLResponse)
def overview() -> str:
    return render_overview()


@app.get("/matchboard", response_class=HTMLResponse)
def matchboard() -> str:
    return render_matchboard()


@app.get("/agent-loads", response_class=HTMLResponse)
def agent_loads() -> str:
    return render_agent_loads()


@app.get("/api-summary", response_class=HTMLResponse)
def api_summary_page() -> str:
    return render_api_summary()


@app.get("/docs", response_class=HTMLResponse)
def docs_page() -> str:
    return render_docs()


@app.get("/api/dashboard/summary")
def dashboard_summary() -> dict:
    return service.summary()


@app.get("/api/leads")
def leads() -> list[dict]:
    return service.ranked_leads()


@app.get("/api/agents")
def agents() -> list[dict]:
    return service.agent_loads()


@app.get("/api/leads/{lead_id}")
def lead(lead_id: str) -> dict:
    value = service.lead(lead_id)
    if value is None:
      raise HTTPException(status_code=404, detail="Lead not found")
    return value


@app.get("/api/sample")
def sample() -> dict:
    return service.sample_payload()


@app.get("/openapi.json")
def openapi_spec() -> JSONResponse:
    return JSONResponse(json.loads(json.dumps(app.openapi())))


if __name__ == "__main__":
    import os
    import uvicorn

    port = int(os.environ.get("PORT", "4762"))
    uvicorn.run("app.main:app", host="127.0.0.1", port=port, reload=False)
