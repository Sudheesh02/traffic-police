---
name: ppt-pitch-crafter
description: Generates clean, conversational, judge-friendly slide deck content and talking points from your codebase and docs without stiff academic jargon or endless hyphens.
---

# Pitch & Presentation Content Crafter (`/ppt-pitch-crafter`)

Transform any codebase, architecture diagram, benchmark, or markdown specification into compelling, human-friendly presentation content designed to win over hackathon judges, technical evaluators, and project stakeholders.

---

## The 3 Golden Rules for Slide Content

### 1. The 5-Second Judge Test
Judges review dozens of projects and have short attention spans. If a slide cannot be understood in 5 seconds of scanning, it failed. Every slide must feature a single clear takeaway headline, not a generic label like "System Architecture" or "Background".

### 2. Conversational, Grounded English (No High-Level Fluff)
* **Never use buzzword soup**: Avoid empty filler like "leveraging synergistic paradigms to maximize decarbonization efficiencies".
* **Speak like an engineer explaining to a smart friend**: "We stopped the furnace from cracking steel by calculating tramp copper limits in under 4 milliseconds."
* **Keep sentences punchy and active**: Subject -> Action -> Impact.

### 3. Ban Endless Hyphens and Nested Dashes
Do not dump walls of bullet lists separated by dashes and hyphens. Instead, structure content using:
* **Metric Callout Cards**: `[ Metric: 4.17 -> 1.83 tCO2/t | -56% ]`
* **Bold Concept Anchors**: Direct statements with 1 supporting sentence.
* **Problem vs. Breakthrough pairs**: Visual side-by-side contrasts.
* **Numbered Flows**: Step 1, Step 2, Step 3.

---

## Standard Slide Output Structure

When generating slides from a codebase or docs, output each slide in this consistent blueprint:

```markdown
### Slide [Number]: [Action-Driven Title]
> **Key Takeaway**: One clear sentence explaining the core message of this slide.

#### 1. What Judges Need to Know
* [Bold Concept]: Direct explanation in plain English.
* [The Hard Problem]: Why the traditional way breaks or costs too much.
* [Our Fix]: How our code solves this cleanly.

#### 2. Hard Proof & Metrics (Grounded in Code)
* **Metric 1**: Baseline vs. Result (e.g., Latency, Accuracy, Abatement, Cost)
* **Metric 2**: Exact validation proof (e.g., 100% mathematical closure, test suite status)

#### 3. Recommended Visual Layout
[Describe the visual: e.g., Left: Architecture diagram with 3 pipeline boxes; Right: Live cockpit screenshot with glowing slider badge]

#### 4. 30-Second Spoken Pitch (What you say out loud)
"Here's what you say naturally to the judge while they look at this slide..."
```

---

## Workflow Instructions

When the user asks to generate slides or pitch content:

1. **Scan the Project**:
   - Inspect key files: `README.md`, data models, core algorithms, API endpoints, UI components, and test suites.
   - Extract real numbers: benchmarks, response times, supported grades/configurations, mathematical guarantees.

2. **Determine the Deck Arc**:
   - **Slide 1**: Hook & The Pain Point (The costly real-world problem).
   - **Slide 2**: Why Existing Approaches Fail (The technical bottleneck).
   - **Slide 3**: The Core Innovation (Your secret sauce / algorithmic breakthrough).
   - **Slide 4**: System Architecture & Tech Stack (How the pieces talk to each other).
   - **Slide 5**: Grounded Proof & Live Benchmarks (Real metrics from tests/code).
   - **Slide 6**: Operational Impact & Next Horizon (Value delivered today + future roadmap).

3. **Filter the Voice**:
   - Strip out academic stiffness.
   - Strip out double hyphens, em-dashes as bullet replacements, and robotic phrasing.
   - Verify every technical claim matches real code in the repository.
