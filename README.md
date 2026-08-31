# Lab 1 – Requirements Engineering & UML Use-Case Modelling

**Problem Statement #13 – Patient Health Record Consent Management System**

## Group Members
- M P Shashank — PES1UG24AM160
- Narayanan Arun — PES1UG24AM172
- Nishanth N — PES1UG24AM179
- Nishitha S — PES1UG24AM180

## Shared Deliverables
- Requirements Table: exactly 5 Functional Requirements (FR-001 to FR-005) and 2 Non-Functional Requirements (NFR-001 and NFR-002).
- UML Use-Case Diagram: shared by the group, with at least 3 actors, at least 5 use cases, and `«include»`/`«extend»` relationships.
- Editable draw.io source and PDF export.

## Individual Use-Case Flows
Each member has a different core use-case flow, as required for the group submission:
- M P Shashank — UC-01 Authenticate Patient
- Narayanan Arun — UC-02 Grant Time-Bounded Consent
- Nishanth N — UC-03 Revoke Consent
- Nishitha S — UC-06 Access Medical Records

## Use Cases in Shared UML
1. UC-01 – Authenticate Patient
2. UC-02 – Grant Consent
3. UC-03 – Revoke Consent
4. UC-04 – View Consent Status
5. UC-05 – Verify Doctor
6. UC-06 – Access Medical Records
7. UC-07 – Record Audit Event
8. UC-08 – Deny Access for Expired Consent

## Relationships
- Grant Consent `«include»` Verify Doctor
- Grant Consent `«include»` Record Audit Event
- Revoke Consent `«include»` Record Audit Event
- Access Medical Records `«include»` Record Audit Event
- Deny Access for Expired Consent `«extend»` Access Medical Records
