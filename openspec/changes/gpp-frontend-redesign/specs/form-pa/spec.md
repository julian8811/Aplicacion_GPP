# Form-PA Specification

## Purpose

Proceso Administrativo (PA) evaluation form wizard. Covers 5 sections (Evaluación Preliminar, Planeación, Dirección, Control, Información y Comunicación) with multiple-choice questions. Implements field-level validation, progress tracking, and auto-save.

## Requirements

### Requirement: PA Form Structure

The PA form SHALL contain exactly 5 sections: Evaluación Preliminar, Planeación, Dirección, Control, and Información y Comunicación. Each section MUST contain its designated questions loaded from a static config.

#### Scenario: Load PA form

- GIVEN the user starts or resumes a PA evaluation
- WHEN the form initializes
- THEN the system SHALL render 5 sections with correct question sets
- AND SHALL restore any previously saved answers from `evaluaciones_pa`

### Requirement: Section Navigation

The system SHALL allow navigation between sections via sidebar click and Next/Previous buttons. The user SHALL NOT skip required questions before proceeding to the next section.

#### Scenario: Navigate to next section with missing required fields

- GIVEN the user is on section 1 with unanswered required questions
- WHEN the user clicks "Next"
- THEN the system SHALL display inline errors on required fields
- AND SHALL NOT navigate away

#### Scenario: Navigate to previous section

- GIVEN the user is on section 2 of the PA form
- WHEN the user clicks "Previous"
- THEN the system SHALL navigate to section 1
- AND SHALL preserve all entered answers

### Requirement: Answer Persistence

The system SHALL save each answer to `evaluaciones_pa` immediately on selection. Answers SHALL be one of: "cumple" (100%), "cumple-parcial" (50%), "no-cumple" (0%). Unanswered optional questions SHALL default to `null`.

#### Scenario: Select answer

- GIVEN the user is on a PA question
- WHEN the user selects an answer option
- THEN the system SHALL immediately save the answer to `evaluaciones_pa`
- AND SHALL show a subtle "Saved" indicator

### Requirement: Progress Indicator

The system SHALL display a progress bar showing percentage of answered required questions across all PA sections. The progress SHALL update in real-time as answers are selected.

#### Scenario: View progress during form completion

- GIVEN the user has answered 15 of 30 required PA questions
- WHEN the progress bar renders
- THEN the system SHALL display 50% progress

### Requirement: Form Validation

The form SHALL validate that all required questions are answered before allowing the user to proceed to the PO form. Questions with answers "cumple-parcial" or "no-cumple" SHALL display a comment input requiring explanation.

#### Scenario: Proceed to PO without all required answers

- GIVEN the user has 3 unanswered required questions in PA
- WHEN the user clicks "Proceed to PO"
- THEN the system SHALL block navigation
- AND SHALL scroll to first unanswered required question

#### Scenario: Answer requires comment

- GIVEN the user answers "cumple-parcial" on a required question
- WHEN the answer is saved
- THEN the system SHALL display a required comment textarea
- AND SHALL NOT allow proceeding without comment text