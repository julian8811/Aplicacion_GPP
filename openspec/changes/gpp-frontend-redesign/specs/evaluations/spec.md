# Evaluations Specification

## Purpose

Manages the evaluation lifecycle: create, edit, delete, and list PA + PO evaluations. Each evaluation stores scores, percentages, and nested JSONB blobs for detailed answers.

## Requirements

### Requirement: List Evaluations

Authenticated users SHALL see a paginated list of their evaluations sorted by `fecha` descending. Each row SHALL display date, establishment name, general percentage, and status badge.

#### Scenario: View evaluation list

- GIVEN the user is authenticated and on `/evaluations`
- WHEN the page loads
- THEN the system SHALL fetch and display evaluations ordered by date descending
- AND SHALL show date, establishment name, general_pct, and a status badge

#### Scenario: Empty evaluations list

- GIVEN the user has no evaluations
- WHEN the user navigates to `/evaluations`
- THEN the system SHALL display "No evaluations yet. Create your first evaluation."
- AND SHALL show a CTA button to start an evaluation

### Requirement: Create Evaluation

The system SHALL create a new evaluation record with a generated UUID, `user_id` from the session, and `fecha` set to today. The `evaluaciones_pa` and `evaluaciones_po` fields SHALL initialize as empty JSONB objects.

#### Scenario: Create new evaluation

- GIVEN the user is on the evaluations list
- WHEN the user clicks "New Evaluation"
- THEN the system SHALL create an evaluation record with today's date
- AND redirect to the PA form at step 1

### Requirement: Edit Evaluation

The system SHALL allow the owner who created an evaluation to edit it. Viewers SHALL see a read-only view. An evaluation with completed status SHALL be locked from further edits unless explicitly reopened.

#### Scenario: Owner edits draft evaluation

- GIVEN an owner views their own draft evaluation
- WHEN the user clicks "Edit"
- THEN the system SHALL allow navigation to the PA form pre-filled with existing data

#### Scenario: Viewer views evaluation

- GIVEN a viewer navigates to an evaluation detail page
- WHEN the page loads
- THEN the system SHALL display all evaluation data in read-only mode
- AND SHALL NOT show edit controls

### Requirement: Delete Evaluation

The system SHALL allow owners to delete their own evaluations. Deletion SHALL cascade to linked `action_plans` records. The system SHALL prompt for confirmation before deletion.

#### Scenario: Delete evaluation with confirmation

- GIVEN an owner views an evaluation
- WHEN the user clicks "Delete" and confirms
- THEN the system SHALL delete the evaluation and its action plans
- AND redirect to the evaluations list

### Requirement: Auto-save Draft

The system SHALL auto-save evaluation form data to the server every 30 seconds during editing. The draft status SHALL be indicated with a "Draft saved" toast notification.

#### Scenario: Auto-save triggers

- GIVEN the user is editing an evaluation form
- WHEN 30 seconds elapse without manual save
- THEN the system SHALL POST the current form state to the server
- AND SHALL display "Draft saved" toast

### Requirement: Complete Evaluation

The system SHALL mark an evaluation as `completed` when the user submits the final PO form step. Completed evaluations SHALL display final scores and generate recommendations.

#### Scenario: Complete evaluation submission

- GIVEN the user is on the final step of the PO form
- WHEN the user clicks "Complete Evaluation"
- THEN the system SHALL set the evaluation status to `completed`
- AND compute `general_pct`, `pa_pct`, `po_pct`
- AND redirect to the results page