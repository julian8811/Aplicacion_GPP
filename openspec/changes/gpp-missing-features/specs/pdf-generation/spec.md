# Delta for PDF Generation Domain

## Purpose

This spec covers the PDF report generation functionality that was previously a stub implementation.

## ADDED Requirements

### Requirement: Full PDF Report Generation

The system SHALL generate a complete professional PDF audit report containing all evaluation data, breakdowns, charts (as tables), and recommendations.

#### Scenario: PDF contains evaluation summary

- GIVEN an evaluation exists with complete data
- WHEN the PDF is generated
- THEN it SHALL include the establishment name and evaluation date
- AND SHALL include overall percentage, PA percentage, and PO percentage

#### Scenario: PDF contains detailed breakdown

- GIVEN an evaluation exists with complete data
- WHEN the PDF is generated
- THEN it SHALL include per-aspect breakdowns for PA and PO
- AND SHALL include a table of individual question ratings

#### Scenario: PDF contains recommendations

- GIVEN an evaluation has recommendations
- WHEN the PDF is generated
- THEN it SHALL include the priority recommendations
- AND SHALL organize them by priority (ALTA, MEDIA, BAJA)

### Requirement: PDF Download from Frontend

The frontend SHALL trigger PDF download and display appropriate loading state during generation.

#### Scenario: Download PDF button works

- GIVEN the user is on the ResultsPage
- WHEN the user clicks "Descargar PDF"
- THEN the system SHALL fetch the PDF from the backend
- AND SHALL trigger a file download in the browser

#### Scenario: PDF download shows loading state

- GIVEN the user clicks "Descargar PDF"
- WHEN the request is in progress
- THEN the button SHALL show "Generando PDF..."
- AND SHALL be disabled during generation