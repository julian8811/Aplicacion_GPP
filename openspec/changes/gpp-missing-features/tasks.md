# Tasks: gpp-missing-features

## Phase 1: Fix Results Display

- [x] 1.1 Update `backend/app/api/evaluations.py`: compute `pa_breakdown` and `po_breakdown` from `evaluaciones_pa`/`evaluaciones_po` using aspect averages
- [x] 1.2 Update `backend/app/api/evaluations.py`: compute `questions` array with aspect, question, context, rating, percentage per question
- [x] 1.3 Update `backend/app/api/evaluations.py`: compute `priority` (PA/PO/BALANCED) based on which scoring is lower
- [x] 1.4 Update `frontend/src/pages/ResultsPage.tsx`: remove fallback empty objects since API now provides breakdowns
- [x] 1.5 Test: verify ResultsPage renders gauges, bar charts, and detail table with real evaluation data

## Phase 2: Fix PDF Generation

- [x] 2.1 Rewrite `backend/app/pdf_generator.py`: implement full report with establishment name, date, general/PA/PO percentages, aspect breakdown tables, and recommendations section
- [x] 2.2 Add `/pdf/{evaluation_id}` endpoint to `backend/app/api/` that calls `crear_pdf_auditoria()` and returns PDF blob
- [x] 2.3 Test: download PDF from ResultsPage and verify all sections render correctly

## Phase 3: Fix Recommendations

- [x] 3.1 Fix `backend/app/api/recommendations.py`: correct `aspect_to_category` mapping to match keys in `evaluaciones_pa`/`evaluaciones_po`
- [x] 3.2 Fix `backend/app/api/recommendations.py`: iterate over `evals_pa`/`evals_po` question IDs (e.g., "PA_PLANEACIÓN_...") not category names
- [x] 3.3 Test: call `/recommendations?evaluation_id=xxx` and verify ALTA priority for low-scored aspects, MEDIA for others

## Phase 4: Fix Submit Button Styling

- [x] 4.1 Update `frontend/src/pages/EvaluationWizardPage.tsx`: add `variant="default"` with `className="bg-primary text-primary-foreground hover:bg-primary/90"` to submit button
- [x] 4.2 Add spinner/loader icon in submit button when `isSubmitting` is true
- [x] 4.3 Test: verify submit button has distinct visual weight and loading feedback

## Phase 5: Implement Benchmarking

- [x] 5.1 Verify `BenchmarkingPage.tsx` correctly fetches from `/evaluations` and `/action-plans` endpoints (already connected)
- [x] 5.2 Add "benchmarking enabled" indicator or badge on dashboard if multiple evaluations exist
- [x] 5.3 Test: run with 2+ evaluations and verify chart renders with trend lines and milestones

## Phase 6: Implement Save/Load Drafts

- [x] 6.1 Create `backend/app/api/drafts.py` with `POST /drafts` (save evaluation draft as JSON file) and `GET /drafts/{filename}` (load)
- [x] 6.2 Add "Guardar Borrador" and "Cargar Borrador" buttons to `EvaluationWizardPage.tsx` review step
- [x] 6.3 Use File API in browser to trigger download/upload for JSON files
- [x] 6.4 Test: save a draft, reload the page, upload the file, verify evaluation data restores

## Phase 7: Implement Excel Export

- [x] 7.1 Add `openpyxl` to `backend/requirements.txt` or `pyproject.toml`
- [x] 7.2 Create `backend/app/api/exports.py` with `GET /export/excel/{evaluation_id}`: generate xlsx with sheets for general results, PA breakdown, PO breakdown, questions detail
- [x] 7.3 Add "Exportar Excel" button to `ResultsPage.tsx` next to PDF download
- [x] 7.4 Test: download xlsx and open in Excel/Google Sheets with correct data

## Phase 8: Implement Auto-populate Action Plans

- [x] 8.1 Update `frontend/src/pages/ActionPlanPage.tsx`: add "Auto-popular desde Recomendaciones" button that fetches `/recommendations?evaluation_id=xxx`
- [x] 8.2 Create pre-filled action items from recommendations with ALTA priority, map element to action plan structure
- [x] 8.3 Show confirmation dialog before creating multiple action plans
- [x] 8.4 Test: click auto-populate, verify action plans are pre-filled with recommendation text

## Phase 9: Testing/Verification

- [x] 9.1 Write unit tests for `evaluations.py` breakdown computation (happy path + edge cases: empty ratings, all perfect scores)
- [x] 9.2 Integration test: create evaluation → fetch results → verify structure matches ResultsPage expectations
- [x] 9.3 Manual verification: complete a full evaluation flow, view results, download PDF, view recommendations, create action plan, verify all features work
