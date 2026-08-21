# Operational & Token Efficiency

Business OS v1.1 treats context size as an operating constraint. The goal is not terse SOPs; it is to spend tokens on **job-specific reasoning** rather than repeated universal rules.

## Inheritance
Core → system → family → atomic contract. Universal verification, uncertainty, fallback, ownership, and completion rules are stated once and inherited.

## Contract size
The v1.0 contract library was approximately 110,000 words during the refinement audit. v1.1 contains approximately **69,226 contract words** while preserving the ordered Process steps and adding deeper family rules/decision references where they matter.

## Runtime context
The Context Planner resolves actual active-business objects and selective lineage. It does not load whole intelligence directories. Write schemas are loaded automatically; unrelated input schemas are not.

## High-volume data
Raw telemetry remains in source systems or bounded snapshots where appropriate. Canonical state stores decision-relevant objects, provenance, metrics, summaries, and references rather than duplicating every source record.

## Regression guard
`tests/test_contract_efficiency.py` blocks the generic boilerplate patterns removed in v1.1 and enforces a contract-library word budget with safety margin.
