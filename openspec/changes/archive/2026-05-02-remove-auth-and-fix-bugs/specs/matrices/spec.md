# Delta for Matrices Domain

## MODIFIED Requirements

### Requirement: Complete Matrices Data

The system SHALL return complete PA and PO evaluation matrices with all aspects and questions populated. The PA matrix SHALL include questions for all four aspects: PLANEACIÓN, ORGANIZACIÓN, DIRECCIÓN, and CONTROL. The PO matrix SHALL include questions for all three aspects: LOGÍSTICA DE COMPRAS, GESTIÓN DE PRODUCCIÓN, and LOGÍSTICA EXTERNA.
(Previously: PA had data only for PLANEACIÓN; ORGANIZACIÓN, DIRECCIÓN, CONTROL were empty; PO was entirely empty)

#### Scenario: Fetch matrices with complete PA data

- GIVEN the user starts the evaluation wizard
- WHEN the matrices are fetched
- THEN the PA matrix SHALL contain questions for PLANEACIÓN
- AND the PA matrix SHALL contain questions for ORGANIZACIÓN
- AND the PA matrix SHALL contain questions for DIRECCIÓN
- AND the PA matrix SHALL contain questions for CONTROL

#### Scenario: Fetch matrices with complete PO data

- GIVEN the user starts the evaluation wizard
- WHEN the matrices are fetched
- THEN the PO matrix SHALL contain questions for LOGÍSTICA DE COMPRAS
- AND the PO matrix SHALL contain questions for GESTIÓN DE PRODUCCIÓN
- AND the PO matrix SHALL contain questions for LOGÍSTICA EXTERNA

#### Scenario: Matrices accessible without auth

- GIVEN the app operates without authentication
- WHEN `/api/matrices` is called
- THEN the endpoint SHALL return all PA and PO data
- AND SHALL NOT require Bearer token

## ADDED Requirements

### Requirement: Matrices Data Structure

Each question in the matrices MUST include: `id` (unique string), `pregunta` (question text), and `contexto` (context/description). Each aspect MUST have categories, and each category MUST have an array of questions.

#### Scenario: Question structure validation

- GIVEN a question in the matrices
- WHEN the data is inspected
- THEN each question SHALL have a non-empty `id`
- AND each question SHALL have a non-empty `pregunta`
- AND each question SHALL have a non-empty `contexto`

#### Scenario: All PO aspects have questions

- GIVEN the PO matrix
- WHEN the data is inspected
- THEN LOGÍSTICA DE COMPRAS SHALL have at least 2 questions
- AND GESTIÓN DE PRODUCCIÓN SHALL have at least 5 questions
- AND LOGÍSTICA EXTERNA SHALL have at least 1 question
