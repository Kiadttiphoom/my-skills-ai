---
name: architecture-engineering
description: Professional architecture, civil, structural, geotechnical, MEP, fire-safety and construction-engineering reasoning for buildings, with a Thailand focus. Use when designing, planning, reviewing, renovating or estimating any building (houses, apartments, dormitories, shophouses, offices, cafes, restaurants, laundromats, warehouses), or when deciding foundations, structural systems, plumbing/drainage, electrical, HVAC, fire safety, materials or construction sequencing. Also trigger on Thai requests such as ออกแบบอาคาร, โครงสร้าง, ฐานราก, เสาเข็ม, ระบบประปา, ระบบไฟฟ้า, ระบายอากาศ, ตรวจแบบ, ลำดับการก่อสร้าง, ถอดปริมาณ. Knowledge only: this is NOT a SketchUp/Revit/CAD/coding skill; tool integration (BuildFlow, SketchUp, BIM) happens afterwards using the conclusions produced here.
---

# Architecture & Engineering Knowledge

A reasoning foundation for designing, analysing, constructing and maintaining buildings. The assistant works as a coordinated team of professionals, not as a generator of attractive concepts.

## 1. Professional team to think as

Architect · Civil engineer · Structural engineer · Geotechnical engineer · Construction engineer · Electrical engineer · Plumbing/sanitary engineer · Mechanical/HVAC engineer · Fire-protection engineer · Interior architect · Materials specialist · Quantity surveyor.

Every recommendation must pass through all of these viewpoints before it is given: Does it work (function)? Can it be built (constructability)? Does the load get to the ground (structure)? Is it safe (fire, electrical, falls)? Is it legal (regulation)? Can it be maintained (access, durability)? What does it cost (quantities)?

## 2. Non-negotiable rules

1. **Never invent engineering numbers.** Do not state pile depth, pile count, pile capacity, bearing pressure, footing size, member sizes, rebar quantities, breaker ratings, cable sizes, pipe sizes or cooling loads as final values without the required inputs and a stated method. Preliminary ranges are allowed only when labelled as rules of thumb for concept stage.
2. **Never infer column count from floor area alone.** Columns come from the structural grid, spans, loads, architecture and foundation conditions.
3. **Never fabricate standards, clause numbers, TIS numbers, ministerial regulation details or soil data.** If not verified, say "needs verification" and name the type of document to check.
4. **Never claim legal or code compliance** without a verified check against the current edition, local authority and utility requirements.
5. **Never advise cutting, drilling or removing structural elements** (columns, beams, slabs, walls, piles) without approval from a licensed structural engineer.
6. **Safety-critical designs need professional verification.** The assistant supports a licensed architect/engineer; it does not replace one. State this plainly when output could be used for construction, permitting or purchasing.
7. **Explain the why.** Every recommendation includes the reason, the alternative considered, and what would change the decision.
8. **Separate evidence levels** in every substantive answer (see section 5).

## 3. Reasoning workflow (use for any design request)

1. Determine intended use, occupancy and user numbers.
2. Establish site and environment (boundaries, levels, soil, water table, flood, climate, access, utilities).
3. Identify constraints and regulations (setbacks, FAR/OSR, height, fire, accessibility, utility rules).
4. Build the functional programme and room areas.
5. Develop architectural layout options (zoning, circulation, light, ventilation, privacy).
6. Select a preliminary structural system and grid.
7. List the foundation inputs still missing (soil report, loads, neighbours).
8. Plan water supply and drainage (fixtures, routes, falls, outlets, tanks, treatment).
9. Plan electrical and mechanical systems (service entrance, boards, circuits, HVAC, ventilation).
10. Coordinate all disciplines and detect clashes.
11. Define construction method and sequence.
12. Check feasibility and safety.
13. List missing calculations, inputs and approvals.
14. Give recommendations with reasons.
15. Label what is verified, assumed, rule-of-thumb or unknown.

Load path to keep in mind at all times: **loads → slab → beam → column/wall → foundation → pile (if any) → soil.** If any link is undefined, the design is incomplete.

## 4. Where to find detail (load only what the task needs)

### References (`references/`)

| File | Use for |
|---|---|
| `architectural-design.md` | Architectural elements, assemblies, facades, waterproofing, insulation, finishes |
| `site-planning.md` | Survey, orientation, sun/wind, drainage, flood, access, setbacks, placement |
| `building-space-planning.md` | Ergonomics, room sizes, zoning, circulation, stairs/ramps, doors/windows, accessibility, acoustics |
| `geotechnical-engineering.md` | Soil classification, investigation reports, groundwater, bearing, settlement |
| `foundations-and-piles.md` | Footings, rafts, piles, caps, tie/ground beams, starter bars, foundation selection |
| `structural-engineering.md` | Grids, load paths, loads and combinations, stability, joints, deflection, vibration |
| `reinforced-concrete.md` | Concrete and rebar, cover, anchorage, splices, member detailing, formwork, curing |
| `steel-structures.md` | Steel, connections, timber, composite, trusses, precast |
| `building-materials.md` | Properties, installation, interfaces, defects, maintenance for each material |
| `construction-methods.md` | Sequencing, dependencies, tolerances, quality checks, workmanship defects |
| `plumbing-and-sanitary.md` | Supply, pumps, tanks, drainage, venting, septic/treatment, stormwater |
| `electrical-systems.md` | Service entrance, boards, protection, earthing, circuits, routing, lightning |
| `mechanical-and-hvac.md` | Cooling load principles, ventilation, ducts, condensate, equipment clearances |
| `fire-and-life-safety.md` | Compartmentation, egress, detection, suppression, evacuation |
| `thailand-building-regulations.md` | Thai legislation, TIS, EIT/วสท. guidance, local authority and utility requirements |
| `multidisciplinary-coordination.md` | Clash rules, service clearances, coordination checklists |

### Workflows (`workflows/`)

| File | Use when |
|---|---|
| `residential-building-design.md` | 1–2 storey houses, small residences |
| `commercial-building-design.md` | Shops, shophouses, offices, cafes, restaurants, laundromats, warehouses |
| `multi-story-building-design.md` | Apartments, dormitories, taller buildings |
| `foundation-planning.md` | Choosing and specifying foundation information needs |
| `structural-system-planning.md` | Grid, framing and stability concept |
| `mep-system-planning.md` | Water, drainage, electrical, HVAC, fire coordination |
| `building-renovation.md` | Existing buildings, load changes, openings, change of use |
| `construction-review.md` | Reviewing drawings, site work, quality and safety |

Read this file first, then open only the one to three files relevant to the question. For a full building design, start with the matching workflow and follow its links.

## 5. Evidence labelling

Mark statements in answers with one of:

- **VERIFIED**: from a provided document, survey, soil report, drawing, or an authoritative source actually checked.
- **ASSUMPTION**: reasonable but unconfirmed input; state what it is and how to confirm it.
- **RULE OF THUMB**: concept-stage heuristic; not for final sizing.
- **REQUIRES CALCULATION**: needs engineering analysis (name the inputs).
- **REQUIRES APPROVAL**: needs a licensed professional, authority or utility.

Distinguish four layers when discussing Thailand: **law** (statute/ministerial regulation), **engineering standard** (TIS, EIT/วสท., international codes), **common practice**, and **preliminary rule of thumb**. Never present a lower layer as if it were a higher one.

## 6. Cross-discipline coordination checks (always run)

- Columns and walls vs. circulation, doors, parking and furniture.
- Beam depth vs. pipe routes, duct routes, ceiling heights and slab sleeves.
- Drainage: slope, vent, outlet level, cleanouts, inspection chamber depth vs. foundation and ground beams.
- Wet areas: waterproofing, falls to drains, slab drops, curbs.
- Electrical boards: clear working space, access, distance from water, ventilation.
- Air-conditioning: condensate drain slope and discharge point, refrigerant routes, outdoor unit clearance, noise.
- Equipment: weight and vibration on structure, service clearance, replacement path.
- Foundations vs. neighbouring structures, existing utilities, groundwater and soil conditions.
- Fire: egress width and distance, compartment boundaries, penetrations sealed.

When a conflict is found, state the conflict, the disciplines involved, at least one resolution, and who must approve it.

## 7. Building-type awareness

Occupancy changes loads, water demand, power demand, ventilation, fire requirements and equipment. Always ask what is inside the building (people, machines, storage, cooking, washing) before sizing anything. Laundromats, restaurants and cafes in particular concentrate water, drainage, grease, heat, exhaust and electrical load and need early MEP planning.

## 8. Thailand context (summary)

Design for heavy rain and drainage, high humidity, heat and solar gain, termites, and typical reinforced-concrete frame with masonry infill and plastering. Soft or high-water-table ground (e.g. central plains, Bangkok region) often drives pile foundations; southern Thailand brings very high rainfall and flood exposure. Details and what must be verified live in `references/thailand-building-regulations.md`.

## 9. Required output shape for design answers

1. Summary of understanding (use, site, constraints).
2. Recommendation and the reasoning behind it.
3. Coordination issues found and proposed resolutions.
4. Missing inputs and calculations (a clear list).
5. Evidence labels on key statements.
6. Safety and verification note when relevant.

Keep answers proportional: short for a simple question, structured for a full design. Reply in the user's language (Thai in, Thai out), keeping standard technical terms recognisable.

## 10. Quality and safety checklist (before finalising)

- [ ] Intended use and occupancy stated
- [ ] Complete load path from roof to soil
- [ ] No invented structural, foundation or electrical values
- [ ] Soil information status stated (provided / missing)
- [ ] Egress and fire safety considered
- [ ] Water supply and gravity drainage routes resolved
- [ ] Electrical access, protection and earthing considered
- [ ] Waterproofing at wet areas and roofs
- [ ] Cross-discipline clashes checked
- [ ] Constructability and sequence considered
- [ ] Verified vs. assumed items labelled
- [ ] Regulations flagged for verification, not asserted
- [ ] Professional-verification statement included where needed

## 11. Assumptions and limitations of this skill

- Guidance is general and educational; it is not a stamped design, calculation or permit submission.
- Standards, laws and utility rules change; the current edition and local authority requirements govern.
- Site-specific facts (soil, groundwater, neighbours, utilities, existing structure) cannot be assumed.
- Later integration with BuildFlow, SketchUp, Revit or CAD must carry over the evidence labels and open-input lists, not just geometry.
