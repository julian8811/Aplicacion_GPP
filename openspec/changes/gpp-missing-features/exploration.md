# Exploration: GPP Application Missing/Broken Features

**Status**: completed  
**Date**: 2026-05-02  
**Mode**: openspec

---

## 1. Current State Summary

The GPP application has been migrated from a monolithic Streamlit app to a React/FastAPI architecture. During this migration, several features were either lost, broken, or incompletely implemented.

---

## 2. What's Broken vs Missing

### BROKEN (Partially Implemented but Not Working)

| Issue | Location | Root Cause |
|-------|----------|------------|
| **Results don't show properly** | `ResultsPage.tsx` | API returns flat `general_pct`, `pa_pct`, `po_pct` but page expects `pa_breakdown` and `po_breakdown` with per-aspect percentages |
| **PDF download broken** | `pdf.py` + `pdf_generator.py` | PDF generator is a stub that outputs only 3 lines of text. Missing full report generation |
| **Recommendations not filtering** | `recommendations.py` | When `evaluation_id` provided, it tries to filter by low scores but the data structure doesn't match |

### MISSING (Never Implemented)

| Feature | Location in Legacy | Status |
|---------|-------------------|--------|
| Save Evaluation to File | `guardar_evaluacion()` | Not implemented |
| Load Evaluation from File | `cargar_evaluacion()` | Not implemented |
| Excel Export | `mostrar_guardar_cargar()` | Not implemented |
| Benchmarking/Multi-site comparison | `mostrar_benchmarking()` | Page exists but not connected to data |
| Auto-populate Action Plans from Recommendations | `mostrar_plan_accion()` | Manual only |
| Virtual Consultant (Consultor Virtual GPP) | `mostrar_prioridades()` | Not implemented |

---

## 3. Detailed Issues

### 3.1 Button to Submit Evaluation

**Current**: Uses standard `Button` component with `type="submit"`  
**Issue**: No visual distinction or styling for the "submit" action. The wizard's review step has a button but no loading state or visual feedback.

**Files affected**:
- `frontend/src/pages/EvaluationWizardPage.tsx` (lines 291-302)

### 3.2 Evaluation Results Don't Show

**Root Cause Analysis**:

The `ResultsPage.tsx` expects this structure:
```typescript
interface ResultsData {
  pa_breakdown: Record<string, number>  // { "Planificacion": 65, "Organizacion": 70, ... }
  po_breakdown: Record<string, number>   // { "Logistica de Compras": 55, ... }
  questions: Array<{ aspect, question, context, rating, percentage }>
}
```

But the `evaluations.py` API returns:
```json
{
  "id": "...",
  "fecha": "...",
  "general_pct": 65.5,
  "pa_pct": 70.0,
  "po_pct": 61.2,
  "evaluaciones_pa": { "PLANEACIÓN": { "PA_PLANEACIÓN_...": 3 } },
  "evaluaciones_po": { "LOGÍSTICA DE COMPRAS": { "PO_...": 2 } }
}
```

**Missing**: `pa_breakdown`, `po_breakdown`, `questions` array

**Files affected**:
- `backend/app/api/evaluations.py` - needs to compute breakdowns
- `frontend/src/pages/ResultsPage.tsx` - uses wrong data structure

### 3.3 PDF Report Download

**Current State**: The `crear_pdf_auditoria()` function in `backend/app/pdf_generator.py` is a STUB:

```python
def crear_pdf_auditoria(...):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, f"Auditoria GPP - {nombre_est}", ln=True, align="C")
    # Only outputs: title, date, and 3 lines of percentages
    return bytes(pdf.output())
```

**Legacy had**: Full professional PDF with charts, detailed question breakdown, recommendations, and establishment branding.

**Files affected**:
- `backend/app/pdf_generator.py` - needs complete rewrite
- `frontend/src/pages/ResultsPage.tsx` - `handleDownloadPDF()` function (lines 219-228)

### 3.4 "Factores a Mejorar" (Recommendations)

**Current**: `RecommendationsPage.tsx` fetches from `/recommendations?evaluation_id=xxx`

**Issues**:
1. The API returns ALL recommendations with "MEDIA" priority when no `evaluation_id` provided
2. When `evaluation_id` IS provided, it tries to match `aspect_to_category` mapping but the data structure is wrong
3. The legacy app had a proper `MATRIZ_RECOMENDACIONES` that mapped each element to a specific recommendation
4. Legacy app auto-populated action plans from low-scored elements

**Files affected**:
- `backend/app/api/recommendations.py`
- `frontend/src/pages/RecommendationsPage.tsx`

### 3.5 Missing Features from Legacy App

| Legacy Feature | Legacy Location | Current Status |
|----------------|-----------------|---------------|
| Guardar Auditoría (Save to JSON) | `guardar_evaluacion()` | Not implemented |
| Historial (Load from JSON) | `cargar_evaluacion()`, `mostrar_historial()` | Not implemented |
| Exportar a Excel | Lines 1547-1564 | Not implemented |
| Benchmarking | `mostrar_benchmarking()` | `BenchmarkingPage.tsx` exists but unconnected |
| Consultor Virtual GPP | `obtener_recomendaciones_criticas()` | Not implemented |
| Auto-populate Action Plans | Lines 1298-1308 | Manual only |
| Weighted scoring (PESOS_PA/PESOS_PO) | Lines 486-526 | Not implemented |
| Priority levels with thresholds | `calcular_prioridad()` | Simplified |

---

## 4. Data Structure Mismatch

### Legacy Matrix Structure
```
MATRIZ_PA[aspecto][elemento] = [ {pregunta, contexto}, ... ]
PESOS_PA[aspecto][elemento] = weight_percentage
```

### Current Matrix Structure
```
MATRIZ_PA[aspecto][categoria] = [ {id, pregunta, contexto}, ... ]
```

**Problem**: "Elemento" and "Categoria" are conflated. In legacy:
- PLANEACIÓN → Análisis del contexto (elemento)
- ORGANIZACIÓN → Existencia de una estructura organizativa (elemento)

In current:
- PLANEACIÓN has both "Análisis del contexto" AND "Estructura organizativa" as categories
- This doesn't match legacy categorization

---

## 5. Files That Need Fixing

### High Priority

| File | Issue | Effort |
|------|-------|--------|
| `backend/app/api/evaluations.py` | Doesn't compute `pa_breakdown`, `po_breakdown`, or `questions` | Medium |
| `backend/app/pdf_generator.py` | Stub implementation | High |
| `frontend/src/pages/ResultsPage.tsx` | Data structure mismatch with API | Medium |
| `backend/app/api/recommendations.py` | Broken filtering logic | Medium |

### Medium Priority

| File | Issue | Effort |
|------|-------|--------|
| `frontend/src/pages/EvaluationWizardPage.tsx` | Submit button styling/UX | Low |
| `frontend/src/pages/RecommendationsPage.tsx` | Display logic fine, needs better API | Low |
| `frontend/src/pages/ActionPlanPage.tsx` | Works but could auto-populate | Medium |

### Lower Priority (Features)

| File | Feature | Effort |
|------|---------|--------|
| `backend/app/api/benchmarking.py` (new) | Multi-site comparison | High |
| Excel export | Export to xlsx | Medium |
| Save/Load JSON | File persistence | Medium |

---

## 6. Comparison: Legacy vs Current Results Calculation

### Legacy (Weighted)
```python
# Uses PESOS_PA for weighted averages per elemento
for elemento, items in elementos.items():
    calificaciones = [st.session_state.evaluaciones_pa[key] for key in keys]
    promedio = np.mean(calificaciones)
    porcentaje = (promedio / 5) * 100
    peso = PESOS_PA.get(aspecto, {}).get(elemento, 0)
    resultados['pa'][aspecto][elemento] = {
        'promedio': promedio,
        'porcentaje': porcentaje,
        'peso': peso,
        ...
    }
```

### Current (Simple Average)
```python
# Just averages all ratings for PA and PO
all_pa_ratings = [rating for aspect in data.evals_pa for q in aspect for rating in q]
pa_pct = (sum(all_pa_ratings) / len(all_pa_ratings) / 5 * 100)
```

**Impact**: Results are less accurate and don't reflect the importance of different elements.

---

## 7. Recommendations

1. **Immediate**: Fix `evaluations.py` to return proper breakdown structure
2. **High**: Rewrite `pdf_generator.py` to match legacy functionality
3. **Medium**: Fix recommendations API filtering or simplify RecommendationsPage
4. **Low**: Add benchmarking endpoint and page connection

---

## 8. Risks

- Matrix structure changes may require data migration
- PDF generator rewrite is complex and time-consuming
- Weighted scoring change will affect all existing results interpretation