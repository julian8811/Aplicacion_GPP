# Proposal: gpp-missing-features

## Intent

Fix 4 broken features and implement 6 missing features to make the GPP application functionally equivalent to the legacy Streamlit app. The broken features (results display, PDF download, recommendations filtering, submit button styling) block core user workflows. The missing features (benchmarking, save/load, Excel export, virtual consultant, auto-populate action plans, weighted scoring) represent incomplete migration from legacy.

## Scope

### In Scope
- Fix ResultsPage to display evaluation results properly (API data structure mismatch)
- Rewrite PDF generator to create real professional PDF reports
- Fix Recommendations API to filter by evaluation_id properly
- Fix submit button styling in wizard review step
- Implement benchmarking page with multi-site comparison
- Implement save/load evaluation drafts to/from JSON files
- Implement Excel export for results
- Implement auto-populate action plans from recommendations
- Implement weighted scoring for PA/PO questions

### Out of Scope
- Authentication system changes (already works with default user context)
- Matrices data structure changes (keep current, adapt frontend)
- Virtual consultant AI features (deferred to future iteration)

## Capabilities

### New Capabilities
- `benchmarking`: Compare evaluation results across multiple sites against industry standards
- `evaluation-file-persistence`: Save and load evaluation drafts as JSON files locally
- `excel-export`: Export evaluation results to Excel (.xlsx) format with formatted sheets
- `auto-populate-action-plans`: Generate action plan items from low-scored recommendations automatically
- `weighted-evaluation`: Apply element weights to scoring calculations for accurate percentages

### Modified Capabilities
- `evaluations`: Add weighted scoring calculation and proper breakdown structure for results
- `recommendations`: Fix filtering logic to use evaluation_id correctly
- `results-display`: Fix data structure to match API response (pa_breakdown, po_breakdown, questions)
- `pdf-generation`: Rewrite stub to generate full professional PDF reports

## Approach

1. **Fix API responses first** — `evaluations.py` needs to compute `pa_breakdown`, `po_breakdown`, and `questions` array from raw ratings
2. **Fix Recommendations API** — simplify filtering to match on aspect names from evaluation data
3. **Update ResultsPage** — adapt frontend to consume the API's flat structure and compute breakdowns client-side if needed
4. **Rewrite PDF generator** — use FPDF to create multi-section report with establishment info, scores, breakdown charts, and recommendations
5. **Add weighted scoring** — compute weighted averages using PESOS_PA/PESOS_PO weight maps
6. **Implement file persistence** — use browser File API for save/load; FastAPI endpoint for Excel export
7. **Connect benchmarking page** — create `/api/benchmarking` endpoint and wire up the existing but unconnected BenchmarkingPage
8. **Auto-populate action plans** — RecommendationsPage "Generar Plan de Acción" button pre-fills ActionPlanPage with items from recommendations

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `backend/app/api/evaluations.py` | Modified | Add breakdown computation, weighted scoring |
| `backend/app/pdf_generator.py` | Modified | Complete rewrite for full PDF reports |
| `backend/app/api/recommendations.py` | Modified | Fix evaluation_id filtering logic |
| `backend/app/api/benchmarking.py` | New | Multi-site comparison endpoint |
| `backend/app/api/excel_export.py` | New | Excel generation endpoint |
| `frontend/src/pages/ResultsPage.tsx` | Modified | Fix data structure handling |
| `frontend/src/pages/RecommendationsPage.tsx` | Modified | Add auto-populate action plans |
| `frontend/src/pages/BenchmarkingPage.tsx` | Modified | Connect to API |
| `frontend/src/pages/ActionPlanPage.tsx` | Modified | Accept pre-filled items |
| `frontend/src/pages/EvaluationWizardPage.tsx` | Modified | Fix submit button styling |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Weighted scoring changes results interpretation | High | Document the change; add migration note for existing evaluations |
| PDF generator rewrite complex | Medium | Start with working prototype; add sections incrementally |
| Data structure mismatch persists | Low | Write integration tests for API response shape |

## Rollback Plan

1. **Code changes**: Revert via `git checkout HEAD~1 -- backend/ frontend/` for all affected files
2. **Database**: No schema changes required — all modifications are computation/display logic
3. **State**: Local storage drafts unaffected; server-side evaluations remain intact
4. **Feature flags**: None deployed — full rollback required if issues arise

## Dependencies

- FPDF library (`pip install fpdf`) for PDF generation
- `openpyxl` library for Excel export
- Supabase client already configured for data access
- Existing BenchmarkingPage.tsx to connect

## Success Criteria

- [ ] ResultsPage displays pa_breakdown and po_breakdown with per-aspect percentages
- [ ] PDF download creates a readable multi-section report (not stub)
- [ ] Recommendations filtered correctly by evaluation_id (only low-scored aspects)
- [ ] Submit button on wizard review step has distinct styling
- [ ] Save/Load evaluation drafts works via file system
- [ ] Excel export produces valid .xlsx with formatted sheets
- [ ] Benchmarking page shows comparison across multiple evaluations
- [ ] Action plans can be auto-populated from recommendations
- [ ] Scoring uses weighted averages (PESOS_PA/PESOS_PO)
- [ ] All pytest tests pass
- [ ] No console errors on evaluation flow