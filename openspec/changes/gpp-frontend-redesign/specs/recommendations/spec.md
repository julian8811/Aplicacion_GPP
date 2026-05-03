# Recommendations Specification

## Purpose

Generates prioritized recommendation cards based on evaluation answers. Recommendations prioritize "no-cumple" and "cumple-parcial" answers, rank by impact, and provide actionable guidance.

## Requirements

### Requirement: Recommendation Generation

The system SHALL generate recommendations from evaluation answers where the answer is "no-cumple" or "cumple-parcial". Each recommendation MUST include: element reference, description, priority (high/medium/low), and suggested action.

#### Scenario: Generate recommendations

- GIVEN an evaluation is marked as completed
- WHEN the results page loads
- THEN the system SHALL generate recommendations for all "no-cumple" and "cumple-parcial" answers
- AND SHALL sort by priority (high first)

### Requirement: Priority Calculation

Priority SHALL be calculated as: "no-cumple" = high, "cumple-parcial" = medium. Ties within the same priority SHALL be broken by the question's weight in the overall score.

#### Scenario: Priority ordering

- GIVEN an evaluation has 3 "no-cumple" and 5 "cumple-parcial" answers
- WHEN recommendations are generated
- THEN all 3 "no-cumple" recommendations SHALL appear before "cumple-parcial" ones

### Requirement: Recommendation Cards

Each recommendation SHALL be displayed as a card with: priority badge, element name, issue description, and action text. Cards SHALL be visually distinct by priority (red border for high, yellow for medium).

#### Scenario: View recommendation cards

- GIVEN recommendations are generated
- WHEN the recommendations section renders
- THEN each card SHALL display: red/yellow priority badge, element name, issue, and recommended action

### Requirement: Link to Action Plan

Each recommendation card SHALL have a "Create Action" button that pre-fills the action plan form with the recommendation's element and description.

#### Scenario: Create action from recommendation

- GIVEN a recommendation card is displayed
- WHEN the user clicks "Create Action"
- THEN the system SHALL navigate to `/action-plans/new` pre-filled with element and suggested action