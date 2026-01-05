## Regulatory Checklist (Non-exhaustive, for Future Clinical-Grade Versions)

> This checklist is informational only and does not constitute legal or regulatory advice.

### 1. Intended use and risk classification

- [ ] Define a precise **intended use statement** (who, what, where, conditions).
- [ ] Identify jurisdiction(s) (e.g., US, EU, UK) and applicable frameworks:
  - FDA Software as a Medical Device (SaMD) guidance.
  - EU MDR / IVDR classification for software.
  - MHRA (UK) SaMD guidance.
- [ ] Determine risk class (e.g., FDA Class II, EU Class IIa+) with regulatory experts.

### 2. Quality management and documentation

- [ ] Establish a **Quality Management System** (QMS) conformant with e.g., ISO 13485.
- [ ] Maintain:
  - Software requirements and design documentation.
  - Risk management file (ISO 14971).
  - Verification and validation plans and reports.
  - Cybersecurity and data protection documentation.

### 3. Data, training, and validation

- [ ] Document all training/validation datasets, including:
  - Sources, time ranges, sites, and inclusion/exclusion criteria.
  - Demographic distributions, including skin tone and ethnicity where available.
  - Labeling procedures and adjudication process.
- [ ] Conduct:
  - Retrospective validation on held-out data.
  - Prospective clinical validation in intended-use settings.
  - Subgroup analysis (e.g., Fitzpatrick I–VI, age, sex, site).

### 4. Performance claims and labeling

- [ ] Define **performance metrics** and thresholds (e.g., sensitivity, specificity, NPV).
- [ ] Ensure claims in documentation and marketing:
  - Match validated performance.
  - Clearly describe populations where data are sparse.
- [ ] Provide user-facing labeling that explains:
  - Indications and contraindications.
  - Limitations and known failure modes.
  - Appropriate user training and expertise.

### 5. Human factors and UI/UX

- [ ] Perform formative and summative **human factors / usability testing**.
- [ ] Confirm that:
  - Risk information is legible and not misleading.
  - Warnings and alerts are clear.
  - Workflows fit into clinical practice without unsafe shortcuts.

### 6. Post-market surveillance and monitoring

- [ ] Define a **post-market surveillance plan**, including:
  - Collection of real-world performance data.
  - Complaint and incident handling.
  - Procedures for field safety corrective actions and recalls.
- [ ] Monitor for:
  - Performance drift over time.
  - New biases as deployment expands to new populations.

### 7. Cybersecurity and data protection

- [ ] Implement secure development lifecycle practices.
- [ ] Conduct regular:
  - Vulnerability assessments and penetration testing.
  - Third-party dependency reviews.
- [ ] Ensure compliance with:
  - HIPAA (US) or applicable health privacy laws.
  - GDPR (EU) or equivalent data protection frameworks.

### 8. Change management

- [ ] Establish a process for:
  - Versioning and tracking model updates.
  - Assessing regulatory impact of each change.
  - Re-validation or re-approval where required.






