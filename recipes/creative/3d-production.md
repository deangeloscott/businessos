# 3D Assets & Scenes

> Optional craft reference for a usable 3D model, product representation, character, or environment. Apply the concerns that affect the intended use; a background prop does not need every check required by an animated character or an interactive product model. The active model and tools choose the production method.

## Start with the intended use

A still composition, animated scene, interactive model, and fabricated object have different requirements. Establish the needed views, motion or interaction, fidelity, editability, and delivery context from the request. Reuse suitable models, drawings, scans, photographs, or procedural construction when they serve the result; generation is another possible starting point.

For a real subject, choose references that establish its important proportions, dimensions, parts, and surfaces. A single view may establish appearance without establishing depth or hidden geometry. Keep unresolved dimensions or unseen details distinct from measured information. For stylized work, preserve the recognizable or functional features the user needs while changing the permitted shapes and materials. [Shopify's model-review guidance](https://help.shopify.com/en/manual/products/product-media/expert-3d-model) illustrates reference photography, measurements, proportion, and scale checks for real products; its platform limits are not universal requirements.

## Give geometry and surfaces a job

Build enough shape to support the silhouette, useful viewpoints, contact, and movement. Inspect gaps, intersections, surface direction, and shading where they affect the result. More geometry does not automatically improve a model; concentrate detail where the audience or intended use needs it. For real-time use, balance visible quality with loading and playback constraints. [Khronos's asset-creation guidance](https://github.com/KhronosGroup/3DC-Asset-Creation/blob/main/asset-creation-guidelines/RealtimeAssetCreationGuidelines.md) supplies detailed geometry, texture, and delivery considerations; use the destination's current requirements for actual limits.

Distinguish a shape problem from a material, lighting, or surface-shading problem before repairing it. A polished surface's reflections can reveal form, but do not establish its dimensions. Match texture scale and direction, important labels, and transitions between materials. Where relevant, compare under more than one useful view or light so a flattering render does not conceal a mismatch. The [physically based rendering reference on roughness](https://www.pbr-book.org/4ed/Reflection_Models/Roughness_Using_Microfacet_Theory) explains one reason surface response changes appearance; its implementation is not a required production method.

## Test what must move or remain connected

When articulation or deformation matters, test representative poses and contacts before spending heavily on fine detail. Look for collapsed joints, sliding feet, stretched surfaces, separated parts, and an action the geometry cannot support. A character that looks right in one pose is not necessarily ready to animate. For scenes, keep scale, support surfaces, camera relationships, and important landmarks coherent; the [identity and continuity note](video/notes/identity-and-continuity.md) helps distinguish stable anchors from intentional variation.

## Inspect the delivered model

Open the export in the intended viewer or application when available. Check relevant units, orientation, textures, transparency, materials, animation, and loading behavior there. A successful render from the authoring scene does not establish the exported result. A format validator such as the [glTF Validator](https://github.com/KhronosGroup/glTF-Validator) checks supported structural requirements, not likeness or artistic quality.

For example, an editable product turntable needs faithful visible form and a reusable source model; an interactive version also needs inspection from user-controlled angles. Fabrication requires its own dimensional, material, and manufacturing checks: a convincing visual is not proof of printability or engineering suitability.

Preserve useful editable source, required textures or other dependencies, selected references, and the delivered version through existing Assets when future work benefits. [Render and package guidance](../../systems/content-synthesis/workflows/rendering/package-asset/CONTEXT.md) covers shared inspection, correction, and handoff. Consult current tool documentation for execution specifics; these are portable craft decisions.
