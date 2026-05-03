# Delta for Evaluations Domain

## ADDED Requirements

### Requirement: Results Breakdown Computation

The system SHALL compute `pa_breakdown`, `po_breakdown`, and `questions` arrays in the evaluation API response. The breakdown SHALL contain per-aspect and per-element percentage scores calculated from the ratings in `evaluaciones_pa` and `evaluaciones_po`.

#### Scenario: API returns complete results structure

- GIVEN an evaluation with ID exists with ratings in `evaluaciones_pa` and `evaluaciones_po`
- WHEN the GET `/api/evaluations/{id}` endpoint is called
- THEN the response SHALL include `pa_breakdown` as `Record<string, number>` with aspect percentages
- AND SHALL include `po_breakdown` as `Record<string, number>` with aspect percentages
- AND SHALL include `questions` array with `{aspect, element, question, context, rating, percentage}` objects

#### Scenario: ResultsPage receives correct data structure

- GIVEN the ResultsPage component loads after evaluation completion
- WHEN the evaluation data is fetched
- THEN the component SHALL receive `pa_breakdown` matching the expected `{ "Planificación": 65, ... }` format
- AND SHALL receive `po_breakdown` matching the expected `{ "Logística de Compras": 55, ... }` format

## MODIFIED Requirements

### Requirement: Evaluation Results Display

The system SHALL display evaluation results including overall percentage, PA and PO breakdowns by aspect, and individual question ratings with percentages.
(Previously: Data structure mismatch — API returned flat `general_pct`, `pa_pct`, `po_pct` but page expected `pa_breakdown`/`po_breakdown`)

#### Scenario: Display overall and aspect breakdowns

- GIVEN an evaluation has been completed
- WHEN the ResultsPage renders
- THEN the system SHALL display `general_pct` prominently
- AND SHALL display each PA aspect with its percentage from `pa_breakdown`
- AND SHALL display each PO aspect with its percentage from `po_breakdown`

#### Scenario: Display per-question details

- GIVEN the `questions` array is populated
- WHEN the user expands the detailed view
- THEN the system SHALL show each question with its aspect, element, rating (0-5), and calculated percentage
- AND SHALL highlight questions with ratings 0-2 in a distinct color

## REMOVED Requirements

### Requirement: Simple Flat Percentage Response

(Reason: Replaced by structured breakdown response with `pa_breakdown`, `po_breakdown`, and `questions`)