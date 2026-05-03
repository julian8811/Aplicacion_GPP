# File Operations Specification

## Purpose

This specification covers save evaluation to file, load evaluation from file, and Excel export functionality.

## Requirements

### Requirement: Save Evaluation to File

The system SHALL allow users to save an evaluation to a JSON file on their local machine. The file SHALL contain all evaluation data including ratings and metadata.

#### Scenario: Download evaluation as JSON

- GIVEN the user is viewing an evaluation
- WHEN the user clicks "Guardar Evaluación"
- THEN the system SHALL trigger a file download of the evaluation as JSON
- AND the file SHALL be named `evaluacion_{id}_{date}.json`

#### Scenario: JSON contains complete evaluation data

- GIVEN an evaluation is saved to JSON
- WHEN the file is examined
- THEN it SHALL contain `fecha`, `establishment`, `evaluaciones_pa`, `evaluaciones_po`, `general_pct`, `pa_pct`, `po_pct`

### Requirement: Load Evaluation from File

The system SHALL allow users to load an evaluation from a previously saved JSON file. Loading SHALL create a new evaluation record.

#### Scenario: Load evaluation from JSON file

- GIVEN the user is on the history or dashboard page
- WHEN the user clicks "Cargar Evaluación" and selects a JSON file
- THEN the system SHALL parse the file and create a new evaluation
- AND SHALL redirect to the evaluation wizard with the loaded data

#### Scenario: Invalid file shows error

- GIVEN the user selects an invalid JSON file
- WHEN the file is parsed
- THEN the system SHALL display "Archivo no válido"
- AND SHALL NOT create any evaluation record

### Requirement: Export to Excel

The system SHALL allow users to export an evaluation to an Excel (.xlsx) file. The export SHALL include all assessment data in a formatted spreadsheet.

#### Scenario: Export evaluation to Excel

- GIVEN the user is viewing an evaluation
- WHEN the user clicks "Exportar a Excel"
- THEN the system SHALL generate an .xlsx file
- AND SHALL trigger a download with filename `evaluacion_{id}_{date}.xlsx`

#### Scenario: Excel contains structured data

- GIVEN an evaluation is exported to Excel
- WHEN the file is opened
- THEN it SHALL have a "Resumen" sheet with overall scores
- AND SHALL have a "Detalle PA" sheet with per-aspect breakdown for PA
- AND SHALL have a "Detalle PO" sheet with per-aspect breakdown for PO
- AND SHALL have a "Preguntas" sheet with individual question ratings

### Requirement: Save/Load/Export UI

The system SHALL provide intuitive UI controls for save, load, and export operations accessible from the ResultsPage or ActionPlanPage.

#### Scenario: File operations accessible from results

- GIVEN the user is on the ResultsPage
- WHEN the page renders
- THEN the system SHALL show action buttons: "Guardar", "Cargar", "Exportar Excel"

#### Scenario: Buttons disabled during operations

- GIVEN a file operation is in progress
- WHEN the user clicks an action button
- THEN the button SHALL show loading state
- AND other buttons SHALL be disabled until the operation completes