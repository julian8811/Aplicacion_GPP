# Delta for Recommendations Domain

## MODIFIED Requirements

### Requirement: Recommendation Generation

The system SHALL generate recommendations from evaluation answers where the rating is 0 (no-cumple) or 1-2 (cumple-parcial). Each recommendation MUST include: element reference, description, priority (high/medium/low), and suggested action. The system SHALL NOT require authentication to access recommendations.
(Previously: Ignored evaluation_id and returned hardcoded priorities)

#### Scenario: Generate recommendations from specific evaluation

- GIVEN an evaluation with ID exists with ratings 0, 1, 2, 3, 4, 5 across various questions
- WHEN the recommendations are fetched for that evaluation
- THEN the system SHALL return recommendations ONLY for questions with ratings 0-2
- AND SHALL calculate priority based on rating: 0 = ALTA, 1-2 = MEDIA

#### Scenario: Recommendations filtered by evaluation

- GIVEN an evaluation ID is provided in the request
- WHEN `/api/recommendations?evaluation_id=X` is called
- THEN the system SHALL fetch that specific evaluation's `evaluaciones_pa` and `evaluaciones_po`
- AND SHALL return recommendations only for aspects where ratings are 0-2
- AND SHALL NOT return recommendations for aspects with ratings 3-5

### Requirement: Priority Calculation

Priority SHALL be calculated based on the rating value: rating 0 = high priority (ALTA), rating 1-2 = medium priority (MEDIA), rating 3-5 = low priority (BAJA). Recommendations SHALL be sorted by priority descending, then by aspect.
(Previously: Always returned "ALTA" priority regardless of actual scores)

#### Scenario: Priority assignment follows rating

- GIVEN an evaluation has questions with ratings 0, 1, 3, and 5
- WHEN recommendations are generated
- THEN the rating 0 recommendation SHALL have priority "ALTA"
- AND ratings 1-2 SHALL have priority "MEDIA"
- AND ratings 3-5 SHALL have priority "BAJA"

#### Scenario: Recommendations sorted by priority

- GIVEN a set of recommendations with mixed priorities
- WHEN the recommendations list is displayed
- THEN all "ALTA" recommendations SHALL appear before "MEDIA"
- AND all "MEDIA" recommendations SHALL appear before "BAJA"

### Requirement: Recommendations API Parameter Handling

The recommendations endpoint MUST accept and use the `evaluation_id` query parameter to filter recommendations. When evaluation_id is provided, the system SHALL fetch the evaluation data and only return recommendations for aspects with low scores (ratings 0-2).
(Previously: Ignored evaluation_id, returned all or no recommendations)

#### Scenario: Evaluation ID correctly filters recommendations

- GIVEN a request to `/api/recommendations?evaluation_id=abc123`
- WHEN the endpoint receives the request
- THEN it SHALL fetch the evaluation with ID `abc123`
- AND extract ratings from `evaluaciones_pa` and `evaluaciones_po`
- AND filter recommendations to only aspects with ratings 0-2

#### Scenario: Missing evaluation ID returns empty

- GIVEN a request to `/api/recommendations` without evaluation_id
- WHEN the endpoint receives the request
- THEN the system SHALL return an empty list
- AND SHALL NOT return all recommendations by default

#### Scenario: Invalid evaluation ID handled gracefully

- GIVEN a request to `/api/recommendations?evaluation_id=nonexistent`
- WHEN the evaluation does not exist
- THEN the system SHALL return an empty list
- AND SHALL NOT return a 404 error