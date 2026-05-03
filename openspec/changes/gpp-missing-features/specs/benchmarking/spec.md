# Benchmarking Specification

## Purpose

This specification covers the benchmarking/multi-site comparison feature that allows users to compare evaluation results across multiple establishments.

## Requirements

### Requirement: Benchmarking Data Collection

The system SHALL store evaluation data in a structure suitable for benchmarking comparisons. Each evaluation SHALL include establishment metadata for comparison purposes.

#### Scenario: Evaluation includes establishment name

- GIVEN a new evaluation is created
- WHEN the user enters establishment information
- THEN the evaluation SHALL store the establishment name
- AND SHALL include it in benchmarking queries

### Requirement: Benchmarking Comparison API

The system SHALL provide an API endpoint that returns benchmarking data for a given evaluation compared against other evaluations in the system.

#### Scenario: Fetch benchmarking data

- GIVEN an evaluation with ID exists
- WHEN GET `/api/benchmarking/{evaluation_id}` is called
- THEN the system SHALL return that evaluation's results
- AND SHALL return aggregate statistics from other evaluations (average, highest, lowest)
- AND SHALL include comparisons by aspect

#### Scenario: Benchmarking shows percentile ranking

- GIVEN benchmarking data is retrieved
- WHEN the data is displayed
- THEN the system SHALL show the evaluation's percentile rank
- AND SHALL show how it compares to the average

### Requirement: Benchmarking Page Connected

The BenchmarkingPage component SHALL be connected to the benchmarking API and display comparison data.

#### Scenario: BenchmarkingPage displays comparison

- GIVEN the user navigates to `/benchmarking/:evaluationId`
- WHEN the page loads
- THEN the system SHALL fetch and display comparison charts
- AND SHALL show bar charts comparing the evaluation to averages

### Requirement: Multi-site Comparison View

The system SHALL support comparing results across multiple specific evaluations, not just aggregate statistics.

#### Scenario: Compare multiple evaluations

- GIVEN the user selects multiple evaluations for comparison
- WHEN the comparison view loads
- THEN the system SHALL display a side-by-side comparison
- AND SHALL highlight the highest and lowest performers per aspect