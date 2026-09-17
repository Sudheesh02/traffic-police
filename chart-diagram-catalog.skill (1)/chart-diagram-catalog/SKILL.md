---
name: chart-diagram-catalog
description: Reference catalog of 265 named business-presentation diagram, chart, and slide-template types (think-cell / consulting-deck style) across 29 categories — process flows, org charts, pyramids, matrices, funnels, Venn diagrams, timelines, Gantt charts, waterfalls, Mekko charts, SWOT layouts, team-profile slides, bar/line/pie/scatter charts, and more. Each item lists its structure, standard use cases, a unique/creative use case, and why it works. Use this whenever building or reviewing a PowerPoint deck, designing a dashboard or report slide, or whenever the user asks what chart or diagram to use, wants to compare diagram options, is picking a visual for data or a process, or mentions "think-cell", a consulting-style deck, "chart type", "diagram type", or slide layouts — even if they haven't named a specific diagram. Consult this before recommending or building a diagram/chart in a presentation so the terminology and options are exact and complete.
---

# Chart & Diagram Catalog

A complete reference of **265 named presentation diagram, chart, and slide-template
types**, organized into **29 categories**. Sourced from a think-cell-style consulting
slide library, so the names, structures, and standard uses match what a consulting
or corporate-strategy audience will recognize on sight.

## What this is for

Use this skill whenever a task involves **choosing, naming, or building a diagram or
chart for a slide, report, or dashboard** — for example:

- "What's a good way to show declining market share by region?"
- "Build me a PowerPoint slide comparing three product options."
- "I need a diagram for my process, not just a bullet list."
- Any think-cell, consulting-deck, or PowerPoint-diagram request, even generic ones
  like "make this slide more visual."

The goal is precision: recommend or build the *exact, correctly-named* diagram type
for the job, rather than a generic "bar chart" or "flowchart" when a more specific,
purpose-built layout exists in the catalog.

## How this skill is organized

- **`references/00-master-index.md`** — a flat table of all 265 items in ID order
  (name, category, which file it lives in). Use this first if the user names a
  specific diagram (e.g. "a Mekko chart" or "the Iceberg diagram") — grep or scan it
  to find the right category file fast.
- **`references/01-*.md` through `references/29-*.md`** — one file per category
  (see the Category Index below), each with a full table of that category's items.
  Every row has five fields:
  - **Structure** — what it visually looks like
  - **Common Uses** — the standard, expected use case(s)
  - **Unique / Creative Use** — a specific, less-obvious application worth
    suggesting when the standard use doesn't fit
  - **Significance** — why this layout works / what it communicates that a plainer
    chart wouldn't

## Workflow

1. **Identify the underlying need**, not just the literal ask — what relationship,
   comparison, or structure is actually being communicated? ("Show sales by region"
   is geographic + composition; "show how a bug gets fixed" is a process or decision
   tree.)
2. **Check the Decision Guide below** for a fast match, or scan the **Category
   Index** for the right category, then `view` that category's reference file.
3. **If the user names a specific diagram**, check `references/00-master-index.md`
   for its exact category/file rather than guessing.
4. **Recommend 2-4 named options**, not the whole catalog — lead with the best fit,
   mention one alternative, and use the exact catalog name (e.g. "a build-down
   waterfall" not "a waterfall-ish chart").
5. **When actually building the slide/file** (PPTX, HTML, an artifact, etc.), pair
   this skill with the relevant build skill (e.g. `pptx` or `frontend-design`) —
   this catalog tells you *which* diagram and *why*; the build skill tells you *how*
   to construct it in that format.
6. Don't invent diagram names not in this catalog when a real one already fits;
   if nothing fits well, say so rather than forcing a mismatch.

## Decision Guide (common needs → catalog items)

- **Show market share or composition** → Structure, composition: Pie (#227), Structure, composition: Doughnut (#228), Composition: Stacked 100% column (#209), Structure, composition: Mekko (% axis) (#225), Matrix: Four blocks I (#158)
- **Show change or a trend over time** → Time series: Line (#217), Time series: Area (#219), Time series: Combination (Column + Line) (#211), Contribution to change: Build-up waterfall (#236), Contribution to change: Build-down waterfall (#235)
- **Show a linear process or workflow** → Process flow (#58), Process flow with swim lanes (#59), Infographic process I (#61), Numbered process (#72)
- **Show a cyclical / repeating process** → Circular arrows, cycles (#98), Process circle (#77), Circular ongoing sprint (#73), Phases/processes (#97)
- **Show hierarchy or reporting lines** → Simple organigram (#127), Hierarchy tree I (#133), Organigram, clustered I (#128)
- **Show priority tiers or foundational levels** → Pyramid with four layers (#138), 3D pyramid with three layers (#136), Ziggurat diagram (#143)
- **Compare two or more named options** → Aspect matrix (#161), Item comparison: Bar II (#214), Pros and cons I (#43)
- **Show overlap or shared attributes** → Venn diagram (#155), Intersection (#152), Three important values (#154)
- **Prioritize a list of items** → Matrix/prioritization: 2×2 (#197), Matrices with four areas (#164), Matrix: Nine blocks (#160)
- **Show a conversion or drop-off pipeline** → Funnel I (#121), Comparison: Funnel, pipeline (#237)
- **Show geographic or regional data** → World map with text (#12), World map dashboard (#13), Map: Australia (#22)
- **Show a project schedule or plan** → Timeline: Gantt I (#232), Sprint planning (#251), Road map (#250)
- **Show a decision with branching logic** → Decision tree (#132), Problem tree (#135)
- **Diagnose root causes of a problem** → Cause and effect I (#91), Problem tree (#135), Influencing components (#89)
- **Introduce a team or a person** → Team slide with four members (#177), Short personal profile (#185), Detailed personal profile (#186)
- **Run a SWOT or strategic-position analysis** → SWOT analysis I (#165), Matrix: Four blocks I (#158)
- **Headline a single KPI or stat** → Comparison of percentages (#6), Innovative power (#115), 100 people (#4)
- **Annotate an existing chart with a callout** → Annotations: CAGR arrow (#201), Annotations: Value line (#207), Call-out (#254)
- **Show correlation between variables** → Correlation: Scatter (#230), Item comparison: Bubble (#231)
- **Mark a slide's status (draft, confidential, etc.)** → Draft (#255), Confidential (#258), Preliminary (#259)
- **Show a multivariate profile comparison** → Spiderweb (#151)
- **Show nested / hierarchical proportions** → Sunburst diagram, illustrative (#149)
- **Open a deck with an agenda or outline** → Agenda I (#101), Table of contents (#105)

This list is illustrative, not exhaustive — many items serve more than one need.
When in doubt, open the relevant category file and scan the full table.

## Category Index

| # | Category | Items | ID(s) | File |
|---|---|---|---|---|
| 1 | Numbers & Percentages | 11 | 1–11 | `references/01-numbers-and-percentages.md` |
| 2 | Maps | 25 | 12–36 | `references/02-maps.md` |
| 3 | Mental Models & Frameworks | 21 | 37–57 | `references/03-mental-models-and-frameworks.md` |
| 4 | Processes & Flow Charts | 43 | 58–100 | `references/04-processes-and-flow-charts.md` |
| 5 | Agendas & Schedules | 11 | 101–111 | `references/05-agendas-and-schedules.md` |
| 6 | Dashboards & Statistics | 6 | 112–117 | `references/06-dashboards-and-statistics.md` |
| 7 | Cubes & 3D Segmentation | 3 | 118–120 | `references/07-cubes-and-3d-segmentation.md` |
| 8 | Funnels | 6 | 121–126 | `references/08-funnels.md` |
| 9 | Organizational Charts & Decision Trees | 9 | 127–135 | `references/09-org-charts-and-decision-trees.md` |
| 10 | Pyramids & Core Elements | 13 | 136–148 | `references/10-pyramids-and-core-elements.md` |
| 11 | Sunbursts, Spiderwebs & Radars | 3 | 149–151 | `references/11-sunbursts-spiderwebs-radars.md` |
| 12 | Venn Diagrams | 5 | 152–156 | `references/12-venn-diagrams.md` |
| 13 | Matrices & SWOT Analyses | 12 | 157–168 | `references/13-matrices-and-swot.md` |
| 14 | Quotes | 3 | 169–171 | `references/14-quotes.md` |
| 15 | Tables | 7 | 172–176, 263–264 | `references/15-tables.md` |
| 16 | Team Introductions & Profiles | 10 | 177–186 | `references/16-team-intros-and-profiles.md` |
| 17 | Text Boxes & Building Blocks | 14 | 187–200 | `references/17-text-boxes-and-building-blocks.md` |
| 18 | Annotations (think-cell) | 7 | 201–207 | `references/18-annotations-think-cell.md` |
| 19 | Bar & Column Charts | 9 | 208–216 | `references/19-bar-and-column-charts.md` |
| 20 | Line & Area Charts | 8 | 217–224 | `references/20-line-and-area-charts.md` |
| 21 | Mekko (Marimekko) Charts | 2 | 225–226 | `references/21-mekko-charts.md` |
| 22 | Pie & Doughnut Charts | 3 | 227–229 | `references/22-pie-and-doughnut-charts.md` |
| 23 | Scatter & Bubble Charts | 2 | 230–231 | `references/23-scatter-and-bubble-charts.md` |
| 24 | Timeline & Gantt Charts | 3 | 232–234 | `references/24-timeline-and-gantt-charts.md` |
| 25 | Waterfall Charts | 3 | 235–237 | `references/25-waterfall-charts.md` |
| 26 | Timelines, Milestones & Project Planning | 16 | 238–253 | `references/26-timelines-milestones-project-planning.md` |
| 27 | Callouts, Comments & Slide Types | 7 | 254–260 | `references/27-callouts-comments-slide-types.md` |
| 28 | Progress Bars, Gauges & Sections | 2 | 261–262 | `references/28-progress-bars-gauges-sections.md` |
| 29 | Gears, Cogwheels | 1 | 265 | `references/29-gears-and-cogwheels.md` |

**Total: 265 items across 29 categories.**

## Notes

- Some items are intentional style variants of one another (e.g. *Cause and effect
  I-VI*, *Infographic process I-VII*) — same core structure and use, different
  layout. Each still has its own distinct "Unique / Creative Use" entry so you're
  not stuck repeating yourself if you need to suggest more than one variant.
- Two categories have non-sequential ID ranges by design (Tables includes items
  172-176 and 263-264; Gears is item 265 alone) — this mirrors the source
  library's own numbering and is not an error.
- This catalog describes *what a diagram is and when to use it* — it is not itself
  a chart-rendering tool. For live data charts in an artifact, use the Visualizer or
  chart libraries as usual; for slide decks, use the `pptx` skill.
