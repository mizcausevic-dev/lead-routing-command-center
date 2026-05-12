from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from statistics import mean
from typing import Any


def _clamp(value: float, low: int = 0, high: int = 100) -> int:
    return max(low, min(high, round(value)))


@dataclass(slots=True)
class LeadRoutingService:
    source_path: Path

    def load(self) -> dict[str, Any]:
        return json.loads(self.source_path.read_text(encoding="utf-8"))

    def agents(self) -> list[dict[str, Any]]:
        return self.load()["agents"]

    def leads(self) -> list[dict[str, Any]]:
        return self.load()["leads"]

    def match_score(self, lead: dict[str, Any], agent: dict[str, Any]) -> dict[str, Any]:
        zone_bonus = 20 if lead["zone"] in agent["zones"] else -16
        property_bonus = 15 if lead["property_type"] in agent["property_types"] else -12
        budget_fit = 0
        if agent["min_price"] <= lead["budget"] <= agent["max_price"]:
            budget_fit = 12
        elif abs(lead["budget"] - agent["max_price"]) <= 200000 or abs(lead["budget"] - agent["min_price"]) <= 200000:
            budget_fit = 6
        else:
            budget_fit = -10
        language_bonus = 10 if lead["preferred_language"] in agent["languages"] else 0
        luxury_bonus = 8 if lead["luxury_expectation"] and agent["luxury_certified"] else 0
        workload_penalty = agent["active_leads"] * 1.6
        responsiveness_bonus = max(0, 14 - agent["response_sla_minutes"])
        conversion_bonus = agent["conversion_rate"] * 30
        urgency_bonus = max(0, 18 - min(lead["timeline_days"], 18)) * 0.6

        score = _clamp(
            22
            + zone_bonus
            + property_bonus
            + budget_fit
            + language_bonus
            + luxury_bonus
            + responsiveness_bonus
            + conversion_bonus
            + urgency_bonus
            - workload_penalty
        )

        reason = (
            "Assign immediately and queue same-hour follow-up."
            if score >= 82
            else "Route as primary agent and keep a backup on deck."
            if score >= 65
            else "Hold as backup match only."
        )
        return {
            "agentId": agent["agent_id"],
            "agentName": agent["name"],
            "score": score,
            "zoneFit": lead["zone"] in agent["zones"],
            "propertyFit": lead["property_type"] in agent["property_types"],
            "languageFit": lead["preferred_language"] in agent["languages"],
            "luxuryFit": lead["luxury_expectation"] and agent["luxury_certified"],
            "activeLeads": agent["active_leads"],
            "responseSlaMinutes": agent["response_sla_minutes"],
            "reason": reason,
        }

    def ranked_leads(self) -> list[dict[str, Any]]:
        ranked: list[dict[str, Any]] = []
        for lead in self.leads():
            matches = sorted(
                [self.match_score(lead, agent) for agent in self.agents()],
                key=lambda item: item["score"],
                reverse=True,
            )
            primary = matches[0]
            backup = matches[1]
            urgency_score = _clamp(lead["intent_score"] * 0.62 + max(0, 31 - lead["timeline_days"]) * 1.25)
            ranked.append(
                {
                    "leadId": lead["lead_id"],
                    "name": lead["name"],
                    "zone": lead["zone"],
                    "propertyType": lead["property_type"],
                    "budget": lead["budget"],
                    "timelineDays": lead["timeline_days"],
                    "channel": lead["channel"],
                    "intentScore": lead["intent_score"],
                    "urgencyScore": urgency_score,
                    "primaryAgent": primary["agentName"],
                    "primaryScore": primary["score"],
                    "backupAgent": backup["agentName"],
                    "backupScore": backup["score"],
                    "routeRecommendation": primary["reason"],
                    "matches": matches,
                }
            )
        return sorted(ranked, key=lambda item: (-item["urgencyScore"], -item["primaryScore"], item["name"]))

    def lead(self, lead_id: str) -> dict[str, Any] | None:
        for lead in self.ranked_leads():
            if lead["leadId"] == lead_id:
                return lead
        return None

    def summary(self) -> dict[str, Any]:
        data = self.load()
        leads = self.ranked_leads()
        avg_urgency = mean(lead["urgencyScore"] for lead in leads)
        avg_primary = mean(lead["primaryScore"] for lead in leads)
        luxury = [lead for lead in leads if lead["budget"] >= 1800000]
        same_hour = [lead for lead in leads if lead["primaryScore"] >= 82]
        return {
            "brokerage": data["brokerage"],
            "market": data["market"],
            "leadCount": len(leads),
            "averageUrgencyScore": round(avg_urgency, 1),
            "averagePrimaryMatchScore": round(avg_primary, 1),
            "sameHourFollowupCount": len(same_hour),
            "luxuryLeadCount": len(luxury),
            "leadRecommendation": (
                "Protect the fast-response luxury lanes, then keep Quincy and Cambridge leads on dedicated agents so high-intent buyers do not drift while the team load shifts."
            ),
        }

    def agent_loads(self) -> list[dict[str, Any]]:
        return sorted(
            [
                {
                    "agentName": agent["name"],
                    "activeLeads": agent["active_leads"],
                    "responseSlaMinutes": agent["response_sla_minutes"],
                    "conversionRate": round(agent["conversion_rate"] * 100, 1),
                }
                for agent in self.agents()
            ],
            key=lambda item: (item["activeLeads"], -item["conversionRate"]),
        )

    def sample_payload(self) -> dict[str, Any]:
        leads = self.ranked_leads()
        return {
            "dashboard": self.summary(),
            "routes": [
                {
                    "leadId": lead["leadId"],
                    "name": lead["name"],
                    "primaryAgent": lead["primaryAgent"],
                    "primaryScore": lead["primaryScore"],
                    "backupAgent": lead["backupAgent"],
                    "urgencyScore": lead["urgencyScore"],
                    "routeRecommendation": lead["routeRecommendation"],
                }
                for lead in leads[:3]
            ],
        }


def build_service(root: Path | None = None) -> LeadRoutingService:
    base = root or Path(__file__).resolve().parents[2]
    return LeadRoutingService(base / "app" / "data" / "sample_routing.json")
