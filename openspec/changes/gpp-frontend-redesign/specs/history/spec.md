# History Specification

## Purpose

Audit-style history view of all past evaluations with search, date range filtering, and trend indicators. Provides longitudinal insight into evaluation performance.

## Requirements

### Requirement: Evaluation History List

The system SHALL display all evaluations for the current user in reverse chronological order. Each row SHALL show: date, establishment name, general_pct, trend indicator (up/down/stable vs previous), and action buttons.

#### Scenario: View evaluation history

- GIVEN the user navigates to `/history`
- WHEN the page loads
- THEN the system SHALL fetch and display all user evaluations ordered by date desc

#### Scenario: Empty history

- GIVEN the user has no evaluations
- WHEN the user navigates to `/history`
- THEN the system SHALL display "No evaluation history yet."

### Requirement: Search

The system SHALL provide a text search input that filters evaluations by establishment name. Search SHALL be debounced at 300ms.

#### Scenario: Search evaluations

- GIVEN the user has evaluations for "Sucursal Norte" and "Sucursal Sur"
- WHEN the user types "Norte" in search
- THEN the system SHALL display only "Sucursal Norte"

### Requirement: Date Range Filter

The system SHALL allow filtering by date range with start and end date pickers. Selecting a range SHALL filter the displayed evaluations.

#### Scenario: Filter by date range

- GIVEN evaluations exist from January, March, and May 2026
- WHEN the user selects date range Jan 1 to Mar 31, 2026
- THEN the system SHALL display only the January and March evaluations

### Requirement: Trend Indicator

The system SHALL calculate trend by comparing each evaluation's `general_pct` to the previous evaluation. Trend SHALL be: "up" (higher by >2%), "down" (lower by >2%), "stable" (within 2%).

#### Scenario: Trend calculation

- GIVEN Evaluation A has 75% and Evaluation B (later) has 80%
- WHEN the history renders
- THEN Evaluation B SHALL show an "up" trend indicator

### Requirement: View Evaluation Detail

Clicking an evaluation row SHALL navigate to the full results page for that evaluation.

#### Scenario: Navigate to detail

- GIVEN the user is on the history page
- WHEN the user clicks on an evaluation row
- THEN the system SHALL navigate to `/evaluations/:id/results`