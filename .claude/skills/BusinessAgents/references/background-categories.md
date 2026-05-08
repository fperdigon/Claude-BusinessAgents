# Background Categories

## Startup Context Extraction

Read `memory/startup-context.md` and extract:
- **Company name** and any product names mentioned
- **City / region** (e.g., "Montréal", "Austin", "Berlin")
- **Industry** keywords (e.g., "legal", "engineering", "healthcare")
- **Niche / core advantage** (e.g., "private on-premise AI", "document automation")
- **Technology** keywords (e.g., "GPU", "local LLM", "CAD", "Python")

## Augmented Keyword Table

Extend the base categories below with the extracted terms:
- Add the company's city/region name to `local_presence`
- Add the company name to the category matching its primary industry
- Add technology keywords to their closest category (GPU → `hardware`, LLM/AI → `ai_technology`, CAD → `engineering`, etc.)

## Category Matching

Match the carousel topic (the founder's words from Q2) and the company niche against the augmented table:

| Base keywords (extended at runtime with company-specific terms) | Category |
|---|---|
| AI, model, neural, machine learning, automation, algorithm | `ai_technology` |
| server, hardware, infrastructure, deployment, rack | `hardware` |
| legal, contract, compliance, document, firm, clause | `legal_workflow` |
| engineering, blueprint, technical, spec, RFP, CAD | `engineering` |
| privacy, security, data, isolated, on-premise, vault | `privacy_security` |
| network, firewall, topology, local, isolated | `network_isolation` |
| workflow, process, adoption, transformation, before, after | `workflow_change` |
| city, local, community, neighbour, region, advisor | `local_presence` |
| stat, metric, ROI, result, productivity, number, percentage | `data_analysis` |
| circuit, board, PCB, trace, chip | `infrastructure` |
| no match | `default` |

Store the matched category as `<bg-category>`.

## Background SVG Resolution

**If `<has-visual-theme>` = true:**
- Look up `<bg-category>` in `<bg-map>` → get the filename
- Read the SVG file from `<visual-theme-folder>/<filename>` — store as `<bg-svg>`

**If `<has-visual-theme>` = false:**
- Use this inline default SVG (neural network nodes, opacity 0.22):

```svg
<svg viewBox="0 0 700 700" xmlns="http://www.w3.org/2000/svg" opacity="0.22" preserveAspectRatio="xMidYMid slice">
  <circle cx="120" cy="100" r="5" fill="var(--accent)"/>
  <circle cx="300" cy="180" r="7" fill="var(--accent)"/>
  <circle cx="500" cy="90" r="5" fill="var(--accent)"/>
  <circle cx="200" cy="320" r="6" fill="var(--accent)"/>
  <circle cx="420" cy="280" r="8" fill="var(--accent)"/>
  <circle cx="600" cy="350" r="5" fill="var(--accent)"/>
  <circle cx="150" cy="500" r="6" fill="var(--accent)"/>
  <circle cx="360" cy="460" r="7" fill="var(--accent)"/>
  <circle cx="550" cy="530" r="5" fill="var(--accent)"/>
  <circle cx="250" cy="620" r="6" fill="var(--accent)"/>
  <circle cx="480" cy="650" r="5" fill="var(--accent)"/>
  <line x1="120" y1="100" x2="300" y2="180" stroke="var(--accent)" stroke-width="1"/>
  <line x1="300" y1="180" x2="500" y2="90" stroke="var(--accent)" stroke-width="1"/>
  <line x1="300" y1="180" x2="200" y2="320" stroke="var(--accent)" stroke-width="1"/>
  <line x1="300" y1="180" x2="420" y2="280" stroke="var(--accent)" stroke-width="1"/>
  <line x1="420" y1="280" x2="600" y2="350" stroke="var(--accent)" stroke-width="1"/>
  <line x1="200" y1="320" x2="360" y2="460" stroke="var(--accent)" stroke-width="1"/>
  <line x1="420" y1="280" x2="360" y2="460" stroke="var(--accent)" stroke-width="1"/>
  <line x1="360" y1="460" x2="150" y2="500" stroke="var(--accent)" stroke-width="1"/>
  <line x1="360" y1="460" x2="550" y2="530" stroke="var(--accent)" stroke-width="1"/>
  <line x1="550" y1="530" x2="480" y2="650" stroke="var(--accent)" stroke-width="1"/>
  <line x1="150" y1="500" x2="250" y2="620" stroke="var(--accent)" stroke-width="1"/>
</svg>
```

One background per carousel — all cards use the same `<bg-svg>`.
