# Design: gpp-missing-features

## Technical Approach

Fix broken data flows and implement missing features by enriching API responses and adding frontend capabilities. The frontend is already well-structured — the issues are backend computation and missing feature hooks.

## Architecture Decisions

### Decision: Results Page Data Enrichment

**Choice**: Compute `pa_breakdown`, `po_breakdown`, and `questions` in the `/results/calculate` endpoint and store in `evaluations` table via enriched POST payload.
**Alternatives considered**: Compute on-the-fly in ResultsPage (duplicates logic), create new `/results/{id}` endpoint (more endpoints).
**Rationale**: Centralizes calculation logic, results are stored pre-computed for PDF and benchmarking.

### Decision: PDF Generator Scope

**Choice**: Full rewrite of `pdf_generator.py` using FPDF to include establishment branding, gauges, aspect breakdown tables, and question-level details.
**Alternatives considered**: Use ReportLab (licensing), html2pdf (external dependency), keep stub and document limitation.
**Rationale**: Legacy had professional PDF; users expect this quality. FPDF is already in dependencies.

### Decision: Recommendations Filtering Fix

**Choice**: Replace `aspect_to_category` mapping with direct element-to-recommendation lookup using the question IDs from `evaluaciones_pa`/`evaluaciones_po`.
**Alternatives considered**: Fix mapping keys (fragile), use separate lookup table (adds indirection).
**Rationale**: The current mapping is backwards — `evaluaciones_pa` keys ARE the question IDs which map to elements via matrices.

### Decision: Save/Load Implementation

**Choice**: Use `draftStore.ts` as persistence layer, add file export/import using browser File API with JSON serialization.
**Alternatives considered**: Backend file storage (complex), IndexedDB (overkill for JSON).
**Rationale**: Draft store already has correct schema; adding file export complements auto-save.

### Decision: Excel Export Approach

**Choice**: Backend endpoint `/export/excel/{evaluation_id}` using `openpyxl`, triggered from ResultsPage.
**Alternatives considered**: Frontend-only with SheetJS (legacy approach), CSV (insufficient for charts).
**Rationale**: openpyxl available in backend dependencies, produces native xlsx with formatting.

### Decision: Action Plans Auto-populate

**Choice**: Add "Generar desde Recomendaciones" button in `ActionPlanPage` that POSTs low-scoring elements as pre-filled action plan drafts.
**Alternatives considered**: Auto-create on evaluation save (too aggressive), separate wizard (adds complexity).
**Rationale**: User control, matches legacy behavior, simple implementation.

## Data Flow

```
EvaluationWizardPage
    │
    ├─► useDraftStore (Zustand + localStorage auto-save)
    │         │
    │         └─► "Guardar Archivo" → downloads JSON
    │         └─► "Cargar Archivo" → File API → setPADraft/setPODraft
    │
    └─► handleSubmit → /results/calculate
              │
              ▼
         /evaluations POST (enriched with breakdowns)
              │
              ▼
         ResultsPage reads + displays breakdown data
              │
              ├─► handleDownloadPDF → /pdf/{id} → pdf_generator.py
              │
              └─► ActionPlanPage (if no existing plans)
                        │
                        └─► "Generar desde Recomendaciones" → pre-fills from low scores
```

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `backend/app/api/results.py` | Modify | Compute `pa_breakdown`, `po_breakdown`, `questions` array with per-aspect percentages |
| `backend/app/api/evaluations.py` | Modify | Accept and store enriched evaluation data including breakdowns |
| `backend/app/api/pdf.py` | Modify | Pass full evaluation data to pdf_generator |
| `backend/app/pdf_generator.py` | Modify | Complete rewrite with establishment branding, gauges, breakdown tables, question details |
| `backend/app/api/recommendations.py` | Modify | Fix filtering: use question ID → element mapping from matrices, not aspect_to_category |
| `backend/app/api/export.py` | Create | New endpoint for Excel export using openpyxl |
| `frontend/src/pages/ResultsPage.tsx` | Modify | Add Excel export button, improve loading states |
| `frontend/src/pages/ActionPlanPage.tsx` | Modify | Add "Generar desde Recomendaciones" button and pre-fill logic |
| `frontend/src/pages/EvaluationWizardPage.tsx` | Modify | Add file save/load buttons, enhance submit button styling |
| `frontend/src/store/draftStore.ts` | Modify | Add `exportToJSON()` and `importFromJSON()` helpers |
| `frontend/src/hooks/useApi.ts` | Modify | Add `useExportExcel` hook |

## Interfaces / Contracts

### Enriched Evaluation Data (POST /evaluations)

```python
{
    "general_pct": 65.5,
    "pa_pct": 70.0,
    "po_pct": 61.2,
    "priority": "PA",
    "evaluaciones_pa": { "PLANEACIÓN": { "PA_PLANEACIÓN_...": 3 } },
    "evaluaciones_po": { "LOGÍSTICA DE COMPRAS": { "PO_...": 2 } },
    # NEW: computed breakdowns
    "pa_breakdown": { "Planificacion": 72.0, "Organizacion": 68.5, ... },
    "po_breakdown": { "Logistica de Compras": 55.0, "Gestion de Produccion": 65.0, ... },
    "questions": [
        { "aspect": "PLANEACIÓN", "question": "...", "context": "...", "rating": 3, "percentage": 60.0 },
        ...
    ]
}
```

### Excel Export Response

```
GET /export/excel/{evaluation_id}
→ Response: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
→ Contains: "Resumen" sheet with scores, "Detalle" sheet with per-question breakdown
```

### Recommendations API Fix

```python
# Before (broken): aspect_to_category["Análisis del contexto"] → "PLANEACIÓN"
# After (fixed): Direct lookup via MATRIZ_PREGUNTAS to find element for each low-scored question ID
```

## Testing Strategy

| Layer | What to Test | Approach |
|-------|-------------|----------|
| Unit | `results.py` breakdown computation | pytest with sample evals_pa/po data |
| Unit | `pdf_generator.py` output | Verify PDF bytes, open in browser |
| Unit | `recommendations.py` filtering | Mock low-scoring evaluation, verify only matching recommendations return ALTA |
| Integration | Excel export | Download and verify opens in Excel/LibreOffice |
| E2E | Save/load workflow | Playwright: wizard → save JSON → clear → load JSON → verify values |

## Migration / Rollout

No migration required. All changes are additive:
- Existing evaluations remain intact (backwards compatible)
- New computed fields (`pa_breakdown`, etc.) optional — ResultsPage has fallbacks
- Feature flags not needed — all features can ship together

## Open Questions

- [ ] Should `evaluations` table schema change to store breakdowns, or keep as computed field in API response?
- [ ] BenchmarkingPage appears functional — confirm if any fixes needed (exploration suggested it was "unconnected" but code shows it fetches all evaluations)
