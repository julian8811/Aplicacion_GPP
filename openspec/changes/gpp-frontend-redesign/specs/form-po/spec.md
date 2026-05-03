# Form-PO Specification

## Purpose

Proceso Operativo (PO) evaluation form wizard. Covers 3 sections (Abasto, Almacén, Producción) mirroring the PA structure with PO-specific questions. Final step triggers score calculation and evaluation completion.

## Requirements

### Requirement: PO Form Structure

The PO form SHALL contain exactly 3 sections: Abasto, Almacén, and Producción. Each section MUST contain its designated questions loaded from a static config.

#### Scenario: Load PO form

- GIVEN the user completes or resumes a PO evaluation
- WHEN the form initializes
- THEN the system SHALL render 3 sections with correct PO question sets
- AND SHALL restore any previously saved answers from `evaluaciones_po`

### Requirement: Section Navigation

The system SHALL allow navigation between sections via sidebar click and Next/Previous buttons. The user SHALL NOT skip required questions before proceeding to the next section.

#### Scenario: Navigate with unanswered required fields

- GIVEN the user is on PO section 1 with unanswered required questions
- WHEN the user clicks "Next"
- THEN the system SHALL display inline errors on required fields
- AND SHALL NOT navigate away

### Requirement: Answer Persistence

The system SHALL save each answer to `evaluaciones_po` immediately on selection, mirroring the PA auto-save behavior.

#### Scenario: PO answer selection

- GIVEN the user is on a PO question
- WHEN the user selects an answer
- THEN the system SHALL immediately persist to `evaluaciones_po`

### Requirement: Final Submission

The user SHALL click "Complete Evaluation" only on the final PO section. The system SHALL calculate `pa_pct` and `po_pct` from saved answers and store them in the evaluation record.

#### Scenario: Complete PO form

- GIVEN the user has answered all required PO questions
- WHEN the user clicks "Complete Evaluation" on section 3
- THEN the system SHALL calculate `pa_pct` from `evaluaciones_pa` answers
- AND calculate `po_pct` from `evaluaciones_po` answers
- AND calculate `general_pct` as weighted average
- AND set status to `completed`
- AND redirect to the results page

#### Scenario: Complete with missing PO answers

- GIVEN the user has 2 unanswered required PO questions
- WHEN the user clicks "Complete Evaluation"
- THEN the system SHALL display "Please answer all required questions"
- AND SHALL NOT submit

### Requirement: Comment on Non-Cumple Answers

Questions answered "cumple-parcial" or "no-cumple" SHALL display a required comment input field before submission is allowed.

#### Scenario: Answer triggers comment requirement

- GIVEN the user answers "no-cumple" on a PO question
- WHEN the answer is saved
- THEN the system SHALL display a required comment textarea