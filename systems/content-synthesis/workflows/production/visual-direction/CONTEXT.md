---
id: content.production.visual-direction
type: workflow
owner_system: content-synthesis
reads:
- Insight
- Opportunity
- WorkRequest
- ProofRecord
- Asset
- PlatformProfile
writes:
- Asset
- WorkRequest
context:
- Brand
- AudienceSegment
- Objective
- Offer
---
# Content Visual Direction

## Purpose
Define coherent visual direction for images, video, animation, 3D assets, and scenes, balancing faithful representation, expressive style, audience, and intended use.

## Business Outcome
Make visuals purposeful and consistent instead of a series of unrelated generated images.

## Run When
Use when an asset needs visual direction, including an editable 3D product model, a realistic reference-based scene of a real place, or a stylized world. Reuse suitable existing direction rather than creating another brief unnecessarily.

## Process
1. [DETERMINISTIC] Resolve Brand visual context, message, audience, platform profile, existing reusable Assets, and production constraints.
2. [AI] Define visual concept, information hierarchy, subject treatment, composition, typography role, iconography/diagram style, motion approach, and realism/stylization where appropriate. Interpret style references into useful choices such as shape, palette, texture, framing, or rhythm; distinguish what must remain faithful from what the user wants reinterpreted.
3. [AI] Tie visual choices to the intended understanding, emotion, atmosphere, or experience. For real subjects, use references that establish the important forms, proportions, materials, actions, and spatial relationships; keep unseen or unmeasured details distinct from verified information. Add views, measurements, or source research only where they resolve a consequential ambiguity.
4. [HYBRID] Check brand consistency, accessibility, cultural/context appropriateness, and risk of misleading synthetic representation.
5. [AI] Specify consistency rules across frames/slides/scenes and what may intentionally vary.
6. [AI] Identify assets requiring real screenshots/proof versus generated illustration.
7. [AI] Apply the useful visual direction to production, or preserve it as a brief when handoff or future work benefits. A separate document is not required to begin creating.

## Optional craft references
When a visual identity must persist across images, scenes, or presentations, the optional [creative identity and continuity note](../../../../../recipes/creative/video/notes/identity-and-continuity.md) can help separate recognizable anchors from intentional variation. Use it as a reference, not a required identity dossier.

For a model or environment that needs actual 3D production, the optional [3D assets and scenes reference](../../../../../recipes/creative/3d-production.md) covers geometry, materials, scale, movement, and destination inspection. Visual direction alone is not a completed 3D asset.

When the brief is commerce-oriented, consult the [image menu](../../../../../recipes/creative/ecommerce-image-lookbooks/INDEX.md), optional [image creative principles](../../../../../recipes/creative/ecommerce-image-lookbooks/notes/creative-principles.md), [image dialects](../../../../../recipes/creative/ecommerce-image-lookbooks/DIALECTS.md), and [video concepts and craft menu](../../../../../recipes/creative/video/INDEX.md) with its optional [core motion notes](../../../../../recipes/creative/video/notes/core-motion.md) for adaptable visual choices. Treat a generic ideal-versus-poor contrast as an illustrative communication device unless supplied evidence supports a factual comparison.

When existing footage needs purposeful emphasis, the optional [editorial enhancement notes](../../../../../recipes/creative/video/notes/editorial-enhancement.md) can help choose a crop, overlay, cutaway, caption, sound cue, color treatment, or silence. When a supplied or generated element must belong in filmed footage, use the optional [compositing and matching notes](../../../../../recipes/creative/video/notes/compositing-and-matching.md). These are references for the model or operator, not required brief sections.

For an expressive image, use the optional [conceptual and editorial image reference](../../../../../recipes/creative/conceptual-editorial-image.md). For an explanatory detail or mechanism, use the [annotated detail and mechanism reference](../../../../../recipes/creative/information-design/09-annotated-detail-and-mechanism.md). For a browse-scale cover, use the [thumbnail and cover concepts](../../../../../recipes/creative/thumbnail-cover-concepts.md). Choose or skip them according to the actual visual job.
