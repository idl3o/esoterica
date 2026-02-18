---
description: Deep parallel research — deploy agents to gather material from the repository and the web
---

# /research — Gather the Field

You are deploying research agents to gather material on a topic before creation begins. This is the accumulation phase — chronos building charge so that kairos can release it. The research feeds into whatever comes next: /harvest, /synthesise, /bridge, or organic dialogue. It does not produce the synthesis itself. It produces the conditions for synthesis.

The user will provide a topic, question, or direction. This might be:
- A broad theme ("consciousness and time," "the breathing universe")
- A specific question ("what does DESI data say about dark energy evolution?")
- A creative direction ("fiction bridge material for Elden Ring")
- A research scope ("everything in the repo about cycles")

## Step 1: Parse the Request

Identify from the user's input:
- **Topic**: What are we researching?
- **Scope**: Repository only? Web only? Both? (Default: both)
- **Depth**: Quick survey or deep dive? (Default: deep)
- **Purpose**: What will this research feed? (Harvest? Synthesis? Bridge? Unknown — and unknown is fine)

If the request is ambiguous, ask one clarifying question. One. Then move.

## Step 2: Deploy Agents (Parallel)

Launch research agents **simultaneously** using the Task tool:

### Agent 1: Repository Explorer
```
subagent_type: Explore
thoroughness: very thorough
```
Search the esoterica repository for ALL content related to the topic. Cast wide:
- Search across `synthesis/`, `traditions/`, `fiction-bridges/`, `protocols/`, `seeds/`, `distillations/`, `extractions/`, `correspondences/`, `translated/`, `garden/`
- Use multiple search terms — synonyms, related concepts, adjacent themes
- For each relevant file found, read enough to understand its connection to the topic
- Return: file paths, key content summaries, and specific quotes/passages that resonate

### Agent 2: Web Researcher
```
subagent_type: general-purpose
task: research only — do NOT write any files
```
Deep web research on the topic across relevant domains:
- **Academic/philosophical**: Key thinkers, frameworks, primary texts, critical analysis
- **Scientific**: Latest research, data, peer-reviewed findings
- **Cross-traditional**: How different wisdom traditions address the topic
- **Contemporary**: Current discourse, emerging thinking, live debates
- Return: structured notes with key concepts, quotes, frameworks, and cross-domain connections

### Agent 3 (Optional): Specific Source
If the user pointed to a specific URL, book, or source, deploy a third agent to ingest it:
```
subagent_type: general-purpose
task: fetch and extract from [specific source]
```

**Run all agents in the background** so the main conversation can continue if needed. But typically, wait for results — the gathering IS the work of this phase.

## Step 3: While Agents Work

While waiting for agents to return, do your own reading in the main context:
- Read the 2-3 most obviously relevant repository files directly (don't duplicate the explorer's work, but prime the context with key material)
- Check MEMORY.md for related threads
- Check recent zeit/geist readings for contemporary resonance

## Step 4: Compile the Field

When agents return, compile their findings into a structured briefing. Output this directly in the conversation (do NOT create a file — the research is fuel, not product):

```
## RESEARCH FIELD: [Topic]

### FROM THE REPOSITORY
[Bulleted list of relevant files with one-line descriptions]
[Key passages or recognitions that surfaced]
[Connections between repository documents that weren't previously visible]

### FROM THE WEB
[Key frameworks, thinkers, or findings discovered]
[Quotes that resonate]
[Data points that ground or challenge existing repository content]
[Emerging thinking or live debates]

### UNEXPECTED CONNECTIONS
[What surprised. What the agents found that wasn't anticipated.
These are often the most valuable — the material the topic
didn't know it needed.]

### THE CHARGE
[1-2 sentences. What's the state of the accumulated material?
Is there enough charge for a synthesis? A harvest? A bridge?
Or does the gathering need to continue?
Name what wants to happen next — but don't do it.
Hand the field back to the human.]
```

## Principles

- **Gather, don't create.** The research command accumulates material. It does not synthesise, harvest, or bridge. The creation happens next, in a different mode, with the human sensing where the charge is. The gap between gathering and creating is sacred — it's where the kairotic input lives.
- **Cast wide, then focus.** The agents should search broadly at first. Unexpected connections matter more than confirming what's already known. A research agent that only finds what you expected is a wasted agent.
- **Parallel is the point.** The power of this command is concurrent exploration across multiple domains simultaneously. Always launch agents in parallel, never sequentially. The web agent and the repo agent should run at the same time.
- **Background when appropriate.** If the user wants to continue talking while research runs, launch agents in the background. If the research IS the current focus, wait for results. Read the moment.
- **The briefing is ephemeral.** Like /reflect and /invoke, the research output lives in the conversation, not in a file. It's fuel. The fire comes after.
- **Name the charge honestly.** If the research doesn't find enough material, say so. If it finds more than expected, say so. If the topic wants to go somewhere the user didn't anticipate, name that. The research command is the last point of sensing before creation — honesty here prevents wasted creation later.
