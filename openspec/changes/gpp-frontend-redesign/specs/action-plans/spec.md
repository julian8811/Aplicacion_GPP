# Action Plans Specification

## Purpose

CRUD operations for action plan items linked to evaluations. Each action plan has: element reference, action description, responsible party, due date, and completion status.

## Requirements

### Requirement: Create Action Plan Item

The system SHALL allow owners to create action plan items linked to an evaluation. Required fields: element, action description, responsible, due_date. The status SHALL default to "pending".

#### Scenario: Create action plan item

- GIVEN the user is on the action plans page for an evaluation
- WHEN the user fills in element, action, responsible, due_date and clicks "Create"
- THEN the system SHALL save the action plan item with status "pending"
- AND display it in the action plans list

### Requirement: List Action Plan Items

The system SHALL display action plan items in a table with columns: Element, Action, Responsible, Due Date, Status. Items SHALL be filterable by status and sortable by due_date.

#### Scenario: List action plans

- GIVEN the evaluation has 5 action plan items
- WHEN the user navigates to `/evaluations/:id/action-plans`
- THEN the system SHALL display all 5 items in a table

#### Scenario: Filter by status

- GIVEN the evaluation has pending and completed action items
- WHEN the user selects filter "pending"
- THEN the system SHALL display only pending items

### Requirement: Edit Action Plan Item

The system SHALL allow owners to edit any field of their own action plan items. Viewers SHALL NOT see edit controls.

#### Scenario: Owner edits action plan

- GIVEN an owner views an action plan item
- WHEN the user clicks "Edit" and modifies the action text
- THEN the system SHALL save the updated item
- AND display "Saved" toast

### Requirement: Delete Action Plan Item

The system SHALL allow owners to delete action plan items. Deletion SHALL require confirmation.

#### Scenario: Delete action plan item

- GIVEN an owner views an action plan item
- WHEN the user clicks "Delete" and confirms
- THEN the system SHALL remove the item from the database

### Requirement: Mark as Complete

The system SHALL allow owners to toggle an action plan item's status between "pending" and "completed". When marked complete, the system SHALL record the completion date.

#### Scenario: Mark action as complete

- GIVEN a pending action plan item
- WHEN the user clicks the checkbox
- THEN the system SHALL set status to "completed"
- AND record the completion date