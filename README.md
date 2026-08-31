# Lab 1 – Requirements Engineering & UML Use-Case Modelling

**Student:** Nishitha S  
**SRN:** PES1UG24AM180  
**Problem Statement:** #13 – Patient Health Record Consent Management System

## Deliverables
1. `Requirements_Table_Google_Docs_Ready.docx` – exactly 5 FRs and 2 NFRs with ID, Type, Description, Priority, Acceptance Criteria and Rationale. The DOCX is formatted for direct upload/opening in Google Docs.
2. `UML_Use_Case_Diagram.drawio` – editable draw.io source.
3. `UML_Use_Case_Diagram.pdf` – PDF export of the use-case diagram.
4. `Use_Case_Flow_UC02_Grant_Consent.docx` – one-page use-case flow with Preconditions, Postconditions, Main Success Scenario and one Alternate Flow.

## UML coverage
Actors: Patient, Clinic Administrator, Verified Clinic Doctor.

The diagram contains at least one `«include»` and one `«extend»` relationship:
- Grant Consent `«include»` Verify Doctor
- Grant/Revoke/Access `«include»` Record Audit Event
- Deny Access for Expired Consent `«extend»` Access Medical Records

## Google Docs / draw.io
- Upload `Requirements_Table_Google_Docs_Ready.docx` to Google Drive and choose **Open with → Google Docs** if a native Google Doc is required.
- Open `UML_Use_Case_Diagram.drawio` in draw.io / diagrams.net to edit or re-export.
