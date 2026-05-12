# Architecture

Lead Routing Command Center treats inbound lead assignment as a matching and workload-balancing problem.

## Inputs

- Lead geography
- Property type
- Budget
- Timeline
- Intent score
- Preferred language
- Luxury expectations
- Agent zones
- Agent specialties
- Active lead load
- Response SLA
- Conversion rate

## Core idea

Many brokerages still rely on simple rotation. This repo improves that by keeping routing explainable:

- why one agent is the primary route
- which backup agent exists
- whether the match is strong enough for same-hour follow-up
- whether the team load is drifting toward imbalance

## Outputs

- Dashboard summary
- Lead route queue
- Matchboard for individual leads
- Agent load board
- API payloads for CRMs and ops tools
