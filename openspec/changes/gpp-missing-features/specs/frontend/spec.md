# Delta for Frontend Domain

## MODIFIED Requirements

### Requirement: Evaluation Results Display

The ResultsPage component SHALL display evaluation results using the correct data structure. The component SHALL handle `pa_breakdown`, `po_breakdown`, and `questions` arrays from the API response.
(Previously: Component expected `pa_breakdown`/`po_breakdown` but API returned flat percentages)

#### Scenario: ResultsPage renders breakdowns correctly

- GIVEN the user navigates to the results page after completing an evaluation
- WHEN the evaluation data is fetched
- THEN the system SHALL render each PA aspect from `pa_breakdown` with its percentage
- AND SHALL render each PO aspect from `po_breakdown` with its percentage

#### Scenario: ResultsPage handles missing breakdown data

- GIVEN the API response lacks breakdown data (backwards compatibility)
- WHEN the ResultsPage renders
- THEN the system SHALL display "Datos no disponibles" for missing breakdowns
- AND SHALL NOT crash or show NaN values

### Requirement: Submit Button Styling

The evaluation wizard submit button SHALL have distinct visual styling to indicate its action type. The button SHALL show loading state during submission.
(Previously: Standard button with no visual distinction or loading feedback)

#### Scenario: Submit button has distinct styling

- GIVEN the user reaches the review step of the evaluation wizard
- WHEN the review step renders
- THEN the submit button SHALL have visually distinct styling (e.g., primary color, larger size)
- AND SHALL display "Enviar Evaluación" as the label
- AND SHALL NOT look like a regular "Siguiente" button

#### Scenario: Submit button shows loading state

- GIVEN the user clicks the submit button
- WHEN the submission request is in progress
- THEN the button SHALL show a loading spinner or "Enviando..." text
- AND SHALL be disabled to prevent double submission

#### Scenario: Submit button re-enables on error

- GIVEN the submit button was clicked and showed loading state
- WHEN the submission fails
- THEN the button SHALL return to its normal state
- AND SHALL display an error message to the user
- AND SHALL allow the user to retry

## ADDED Requirements

### Requirement: Action Plan Auto-population

The ActionPlanPage SHALL support auto-populating action items from recommendations with low scores. The system SHALL pre-fill action plan fields when triggered.
(Previously: Action plans were manual entry only)

#### Scenario: Auto-populate from recommendations

- GIVEN the user is on the ActionPlanPage with an evaluation loaded
- WHEN the user clicks "Auto-popular desde recomendaciones"
- THEN the system SHALL fetch recommendations for that evaluation with ratings 0-2
- AND SHALL pre-fill action items with the recommendation text and priority

#### Scenario: User can edit auto-populated items

- GIVEN action items have been auto-populated
- WHEN the user views them
- THEN the items SHALL be editable
- AND changes SHALL persist when saved