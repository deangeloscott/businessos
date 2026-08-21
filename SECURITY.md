# Security and Proprietary Boundary

This repository/distribution contains **ViralTrac's BusinessOS**, not the proprietary ViralTrac hosted application.

## Included

- portable BusinessOS workflows, schemas, policies, templates, and helper scripts;
- provider-neutral capability definitions;
- public/client-facing ViralTrac integration metadata needed to discover and use authorized API, MCP, semantic-data, measurement, action, receipt, and event capabilities.

## Not included

- ViralTrac hosted-application source code;
- private application repositories or internal engineering directives/roadmaps;
- database migrations, internal storage schemas, infrastructure definitions, provider credentials, signing material, secrets, or service credentials;
- customer data or production operational state;
- authentication, authorization, tenant-isolation, policy-engine, or server-side implementation code.

Knowing that a public/client API or tool exists does not grant access to it. ViralTrac remains responsible for enforcing authentication, scopes, tenant isolation, policy, consent/suppression, action eligibility, rate limits, and other server-side controls.

## Security reporting

Do not open a public issue containing secrets, credentials, customer data, or exploit details. Report suspected security issues privately through https://viraltrac.com.

## Distribution safety

Before a public package is produced, `scripts/validate_public_distribution.py` checks for prohibited internal paths/terminology, populated operator/business state, common secret material, and required license/provenance files. This is a packaging safeguard, not a claim that any public software is impossible to attack.
