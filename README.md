# Lab 1 – Requirements Engineering & UML Use-Case Modelling

**Problem Statement:** #13 – Patient Health Record Consent Management System

## Team
- M P Shashank — PES1UG24AM160
- Narayanan Arun — PES1UG24AM172
- Nishanth N — PES1UG24AM179
- Nishitha S — PES1UG24AM180

## Deliverables
- Requirements Table – exactly 5 Functional Requirements and 2 Non-Functional Requirements.
- UML Use-Case Diagram – actors, primary use cases, `«include»`, and `«extend»` relationships.
- Use-Case Flow – UC-02 Grant Time-Bounded Consent with Preconditions, Postconditions, Main Success Scenario, and Alternate Flow.

## Use Cases
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

## Files
- `Requirements_Table_Google_Docs_Ready.docx`
- `UML_Use_Case_Diagram.drawio`
- `UML_Use_Case_Diagram.pdf`
- `Use_Case_Flow_UC02_Grant_Consent.docx`
- `Use_Case_Flow_UC02_Grant_Consent.pdf`
