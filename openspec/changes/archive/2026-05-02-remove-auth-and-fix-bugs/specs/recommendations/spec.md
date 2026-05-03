# Delta for Recommendations Domain

## MODIFIED Requirements

### Requirement: Recommendation Generation

The system SHALL generate recommendations from evaluation answers where the rating is 0 (no-cumple) or 1-2 (cumple-parcial). Each recommendation MUST include: element reference, description, priority (high/medium/low), and suggested action. The system SHALL NOT require authentication to access recommendations.
(Previously: Required auth and ignored evaluation_id parameter)

#### Scenario: Generate recommendations from evaluation

- GIVEN an evaluation with ID is completed
- WHEN the results page loads
- THEN the system SHALL fetch recommendations filtered by that evaluation_id
- AND SHALL generate recommendations for ratings 0-2
- AND SHALL sort by priority (high first)

#### Scenario: Recommendations without auth

- GIVEN the app operates without authentication
- WHEN `/api/recommendations?evaluation_id=X` is called
- THEN the endpoint SHALL return recommendations for evaluation X
- AND SHALL NOT require Bearer token

### Requirement: Priority Calculation

Priority SHALL be calculated based on the rating value: rating 0 = high priority, rating 1-2 = medium priority, rating 3-5 = low priority. Recommendations SHALL be sorted by priority descending, then by aspect.
(Previously: Always returned "ALTA" priority regardless of actual scores)

#### Scenario: Priority based on rating

- GIVEN an evaluation has questions with ratings 0, 1, 3, and 5
- WHEN recommendations are generated
- THEN the rating 0 recommendation SHALL have priority "ALTA"
- AND ratings 1-2 SHALL have priority "MEDIA"
- AND ratings 3-5 SHALL have priority "BAJA"

#### Scenario: Recommendations sorted correctly

- GIVEN a set of recommendations with mixed priorities
- WHEN the recommendations list is displayed
- THEN all "ALTA" recommendations SHALL appear before "MEDIA"
- AND all "MEDIA" recommendations SHALL appear before "BAJA"

## ADDED Requirements

### Requirement: Recommendations API Parameter Handling

The recommendations endpoint MUST accept and use the `evaluation_id` query parameter to filter recommendations. The system SHALL fetch the evaluation data and only return recommendations for aspects with low scores (ratings 0-2).
(Previously: Ignored evaluation_id, returned all recommendations with hardcoded "ALTA")

#### Scenario: Evaluation ID passed correctly

- GIVEN a request to `/api/recommendations?evaluation_id=abc123`
- WHEN the endpoint receives the request
- THEN it SHALL fetch the evaluation with ID `abc123`
- AND extract the aspect ratings from `evaluaciones_pa` and `evaluaciones_po`
- AND filter recommendations to only aspects with low scores

#### Scenario: Missing evaluation ID handled

- GIVEN a request to `/api/recommendations` without evaluation_id
- WHEN the endpoint receives the request
- THEN the system SHALL return an empty list of recommendations
- AND SHALL NOT return all recommendations by default
