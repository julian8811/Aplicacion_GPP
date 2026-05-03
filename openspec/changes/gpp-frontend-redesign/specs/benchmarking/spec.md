# Benchmarking Specification

## Purpose

Cross-establishment comparison view showing the current user's establishment compared to anonymized aggregate benchmarks. Helps users understand their relative performance.

## Requirements

### Requirement: Benchmark Comparison Chart

The system SHALL display a bar chart comparing the user's establishment scores against the benchmark average. Metrics compared: general_pct, pa_pct, po_pct, and per-section scores.

#### Scenario: View benchmark comparison

- GIVEN the user navigates to `/benchmarking`
- WHEN the page loads
- THEN the system SHALL display a grouped bar chart with user vs benchmark scores

### Requirement: Benchmark Data Source

The system SHALL fetch anonymized aggregate statistics from `/api/benchmarking`. Statistics SHALL exclude the requesting user's own data. The benchmark SHALL include: mean, median, and percentile distribution.

#### Scenario: Benchmark data returned

- GIVEN benchmark data exists for 50 establishments
- WHEN the user loads benchmarking page
- THEN the system SHALL display: user score, benchmark mean, benchmark median

### Requirement: Section-Level Breakdown

The system SHALL allow drilling down into PA and PO sections to compare specific dimension scores against benchmarks.

#### Scenario: Drill down to PA sections

- GIVEN the user is on the benchmarking page
- WHEN the user clicks "PA Breakdown"
- THEN the system SHALL display comparison for all 5 PA sections

### Requirement: Trend Over Time

The system SHALL display a line chart showing the user's score evolution across multiple evaluations alongside the benchmark trend line.

#### Scenario: View trend chart

- GIVEN the user has 4 historical evaluations
- WHEN the trend chart renders
- THEN it SHALL display 4 user data points and a benchmark trend line

### Requirement: Benchmark Privacy

The system SHALL NOT expose individual establishment names or identifying information in benchmark data. Only aggregate anonymized statistics SHALL be transmitted.

#### Scenario: No individual data exposure

- GIVEN the user inspects the benchmarking API response
- THEN the response SHALL NOT contain any establishment_name other than the user's own