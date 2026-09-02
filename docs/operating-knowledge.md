# Operating Knowledge: Playbooks, Workflows, and Steps

AURA gives capable AI reusable business operating knowledge without turning that knowledge into a runtime controller.

## Hierarchy

**Playbook → Workflow → Step**

- A **Playbook** represents a meaningful end-to-end business job, such as Competitor Research, Customer Research, Industry Intelligence, SEO/AEO, Content Synthesis, Marketing Synthesis, or Customer Optimization.
- A **Workflow** is a reusable procedure that accomplishes a meaningful part of a Playbook and may also be useful independently.
- A **Step** is the minimum procedural guidance needed inside a Workflow to make the intended result reliably achievable.

The hierarchy describes knowledge, not execution authority. The active model/user determines which Playbook and Workflows fit the request and how to combine them.

## Minimum sufficient guidance

AURA should provide the **fewest instructions necessary for a capable model to repeatedly achieve the intended business outcome at the required truth and quality standard**.

Keep guidance when it materially protects or improves:

- the outcome the user actually wants;
- factual truth and evidence;
- important scope or constraints;
- repeatable quality;
- non-obvious domain expertise;
- continuity or durable organizational value.

Do not prescribe implementation detail merely because it can be written down. If the model can reliably choose a better implementation from the current tools, Skills, context, or environment, let it.

For example, prefer:

> Research current competitor websites, relevant review sites, public social profiles, advertising evidence, news, and other sources that materially answer the competitive question.

rather than an artificial sequence of provider/tool identifiers or pixel-level interaction instructions that are not themselves requirements.

## Execution freedom

A Playbook or Workflow describes **what good work requires**, not every possible way to execute it.

The active model/harness may:

- use any appropriate native tool;
- use external or user-installed Skills;
- use APIs, browsers, local programs, connectors, MCP, subagents, or other host resources;
- discover a better source or method than AURA anticipated;
- run independent research/workflows in parallel when useful;
- sequence dependent work when necessary;
- skip irrelevant workflows;
- adapt a workflow while preserving the requirements that materially define the job;
- use another sound method entirely when it better serves the outcome.

AURA does not maintain an allowlist of tools or a universal capability vocabulary the host must implement.

## Improvement through use

When repeated real work reveals that a Workflow is missing an important requirement, contains unnecessary specificity, or consistently points models toward weaker work, improve the Workflow.

Organization-specific reusable improvements belong in organization-owned ProcessExtensions/local operating knowledge. Broadly useful AURA improvements belong in deliberate product development and validation.

The test is not whether the model followed every sentence literally. The test is whether the method reliably helps capable intelligence produce truthful, excellent, reusable work.
