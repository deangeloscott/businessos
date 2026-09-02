# Security and Proprietary Boundary

This repository/distribution contains **ViralTrac AURA**, an AI-native BusinessOS, not the proprietary ViralTrac hosted application.

## Included

- portable AURA/BusinessOS Playbooks, Workflows, schemas, policies, templates, attachment adapters, and helper scripts;
- public/client-facing ViralTrac integration metadata needed to discover and use authorized API, MCP, semantic-data, measurement, action, receipt, and event interfaces when the active harness has access to them.

AURA does not ship a provider/tool capability registry. Its operating knowledge describes needed work in natural language and lets the active model/harness choose the best available tools, Skills, providers, and execution methods.

## Not included

- ViralTrac hosted-application source code;
- private application repositories or internal engineering directives/roadmaps;
- database migrations, internal storage schemas, infrastructure definitions, provider credentials, signing material, secrets, or service credentials;
- customer data or production operational state;
- authentication, authorization, tenant-isolation, policy-engine, or server-side implementation code.

Knowing that a public/client API or tool exists does not grant access to it. ViralTrac remains responsible for enforcing authentication, scopes, tenant isolation, policy, consent/suppression, action eligibility, rate limits, and other server-side controls.

## Workspace separation

AURA can optionally keep organization-owned state outside the product source tree. External workspaces may contain canonical business state, optional work receipts/recovery state, human knowledge, and permitted attachments. They are never part of the public product distribution merely because the product points to them. Local `.businessos/workspace.json` pointers can contain host-specific paths and must not be packaged or published.

## Security reporting

Do not open a public issue containing secrets, credentials, customer data, workspace paths that expose sensitive infrastructure, or exploit details. Report suspected security issues privately through https://viraltrac.com.

## Distribution safety

Before a public package is produced, `scripts/validate_public_distribution.py` checks for prohibited internal paths/terminology, populated operator/business state, local workspace pointers/state, common secret material, required license/provenance files, and current ViralTrac AURA branding metadata. This is a packaging safeguard, not a claim that any public software is impossible to attack.
