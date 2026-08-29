#!/usr/bin/env python3
"""Public release gate for the distributable BusinessOS source tree."""
from pathlib import Path
import os, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
env=dict(os.environ)
env['PYTHONDONTWRITEBYTECODE']='1'
env['PYTHONUTF8']='1'
TESTS=[
    'tests/run_distribution.py',
    'tests/run_routing_acceptance.py',
    'tests/run_ecosystem_intelligence.py',
    'tests/run_intelligence_maturation.py',
    'tests/run_capability_continuity.py',
    'tests/run_playbook_evolution_exchange.py',
    'tests/run_workspace_human_knowledge.py',
    'tests/run_workspace_migration_path_guard.py',
    'tests/run_agent_hardening.py',
    'tests/run_bootstrap_reference_ids.py',
    'tests/run_preferences_multioperator.py',
    'tests/run_preference_authorization_separation.py',
    'tests/run_preference_profile_migration.py',
    'tests/run_onboarding_context_hardening.py',
    'tests/run_brand_onboarding.py',
    'tests/run_run_provenance.py',
    'tests/run_platform_python_compat.py',
    'tests/run_platform_semantic_reverification.py',
    'tests/run_local_evidence.py',
    'tests/run_decision_grounding.py',
    'tests/run_customer_facing_mutations.py',
    'tests/run_customer_facing_draft_provenance.py',
    'tests/run_customer_facing_completion_gate.py',
    'tests/run_customer_facing_qa_invariant.py',
    'tests/run_claim_manifest_operational_promises.py',
    'tests/run_completion_evidence_integrity.py',
    'tests/run_content_native_execution.py',
    'tests/run_qualification_framework.py',
    'tests/run_qualification_resume.py',
    'tests/run_qualification_integrity.py',
    'tests/run_qualification_product_integrity.py',
    'tests/run_qualification_qa_resolution.py',
    'tests/run_qualification_supplied_media.py',
]
for rel in TESTS:
    print(f'== {rel} ==')
    subprocess.run([sys.executable,str(ROOT/rel)],check=True,cwd=ROOT,env=env)
print(f'all public release tests passed: {len(TESTS)} suites')
