# Results Specification

## Purpose

Displays completed evaluation results: gauge charts for overall and dimension scores, bar charts for PA/PO breakdowns, and a detailed questions table with filtering. Rendered via Recharts.

## Requirements

### Requirement: Results Dashboard

The system SHALL display a results dashboard with: a large gauge showing `general_pct`, two secondary gauges for `pa_pct` and `po_pct`, and a bar chart breaking down scores by section.

#### Scenario: View results dashboard

- GIVEN the user completes an evaluation
- WHEN the results page loads
- THEN the system SHALL display 3 gauges (general, PA, PO)
- AND a bar chart showing section-level breakdown

### Requirement: Gauge Visualization

Gauge charts SHALL display 0-100% scale with colored zones: red (0-49%), yellow (50-74%), green (75-100%). The current score SHALL be highlighted with a needle indicator.

#### Scenario: Gauge color zones

- GIVEN a gauge with score 65%
- WHEN the gauge renders
- THEN the needle SHALL point to 65%
- AND the arc SHALL show yellow zone highlighting

### Requirement: Bar Chart Breakdown

The system SHALL render a grouped bar chart showing PA sections (5 bars) and PO sections (3 bars) side by side. Hovering a bar SHALL display a tooltip with exact percentage and question count.

#### Scenario: Hover bar chart

- GIVEN the results bar chart is displayed
- WHEN the user hovers over "Planeación" bar
- THEN the system SHALL show tooltip: "Planeación: 85% (20 questions)"

### Requirement: Questions Detail Table

The system SHALL display a searchable, filterable table of all questions with columns: Dimension, Section, Question, Answer, Score. Filters SHALL include: dimension (PA/PO), section, answer value.

#### Scenario: Filter questions by answer

- GIVEN the user is on the questions table
- WHEN the user selects filter "Answer = no-cumple"
- THEN the system SHALL display only questions with "no-cumple" answer

### Requirement: Score Summary Card

The system SHALL display a summary card showing: total questions, answered questions, average score, and date completed.

#### Scenario: View score summary

- GIVEN the results page loads
- WHEN the summary card renders
- THEN it SHALL show: 72 total questions, 72 answered, 78% average, "May 1, 2026"

### Requirement: Export to PDF

The system SHALL provide a "Download PDF" button that triggers the `/api/evaluations/:id/pdf` endpoint. The PDF SHALL contain all result data, charts, and recommendations.

#### Scenario: Download PDF

- GIVEN the user is on the results page
- WHEN the user clicks "Download PDF"
- THEN the system SHALL initiate a file download from `/api/evaluations/:id/pdf`