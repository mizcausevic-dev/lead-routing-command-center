# Changelog

All notable changes to this project are documented here.

## [1.1.0] - 2026-06-05

### Released
- Added `/docs` to match the documented route surface.
- Added static GitHub Pages publishing without consuming a new Kinetic Gain subdomain.
- Added `scripts/prerender_site.py` for HTML, JSON, robots, and sitemap output.
- Refreshed README live URL and validation steps.

## [1.0.0] - 2026-05-12

### Released
- Shipped **lead-routing-command-center** as a public artifact for teams dealing with brokerage lead assignment, follow-up latency, and agent-capacity routing.
- Packaged the current implementation, documentation, validation flow, and proof surfaces into a repo that can be reviewed by technical and operating stakeholders.
- Clarified the core problem the project is addressing: high-intent real estate leads lose value when assignment logic is opaque, overloaded, or too slow.

### Why this mattered
- Existing CRM routing rules and round-robin assignments were useful for parts of the workflow.
- They still left out a durable operator workflow for fit scoring, backup ownership, workload pressure, and follow-up priority.
- This release made the repo read like an operational capability rather than a narrow technical demo.

## [0.1.0] - 2026-03-17

### Shipped
- Cut the first coherent internal version of **lead-routing-command-center** with stable domain objects, review surfaces, and decision outputs.
- Established the first reviewable version of the architecture described as: Real estate lead routing engine for brokerages, agent matching, workload balancing, and follow-up prioritization.
- Focused the repo around actionability instead of passive reporting.

## [Prototype] - 2025-07-13

### Built
- Built the first runnable prototype for the repo's main workflow and decision model.
- Validated the concept against pressure points such as overloaded top agents, weak backup routing, and lead urgency decay.
- Used the prototype phase to test whether the project could drive action, not just present information.

## [Design Phase] - 2024-02-11

### Designed
- Defined the system around operator-first and decision-legible outputs.
- Chose interfaces and examples that made sense for brokerage operators, RevOps owners, and agent team leads.
- Avoided reducing the project to a generic dashboard, CRUD app, or fashionable wrapper around the stack.

## [Idea Origin] - 2023-03-11

### Observed
- The original idea surfaced while looking at how teams were handling lead ownership, speed-to-lead pressure, and routing conflicts across high-intent demand.
- The recurring pattern was that teams had data and tools, but still lacked a usable operating layer for the hardest decisions.

## [Background Signals] - 2022-08-09

### Context
- Earlier platform, governance, and operator-tooling work made one pattern hard to ignore: the systems that create the most drag are often the ones with partial controls and weak operational coherence, not the ones with no controls at all.
- That pattern shaped the thinking behind this repo well before the public version existed.
