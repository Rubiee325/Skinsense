## Ethics, Equity, and Privacy Notes

### Ethical use and harm reduction

- SkinMorph is a **research prototype** and should only be used in supervised, experimental contexts.
- Any deployment involving patients or the public must:
  - Obtain appropriate **ethical approval** (e.g., IRB/REC).
  - Provide **clear disclosures** about limitations and non-clinical status.
  - Avoid replacing in-person dermatology evaluation.

### Fairness and bias

- Public dermoscopy datasets are often biased toward:
  - Lighter skin tones.
  - Images from high-resource specialist centers.
  - Certain geographies and age groups.
- These biases can lead to **systematically worse performance**, especially:
  - In darker skin tones (Fitzpatrick V–VI).
  - For underrepresented lesion types.
- Operators should:
  - Collect and annotate data across **diverse skin tones** and demographics.
  - Monitor **performance gaps** and false-negative rates by subgroup.
  - Involve dermatologists, patients, and communities in governance and review.

### Consent, data use, and retention

- Any real-world use must ensure:
  - **Informed consent** for data capture and model use.
  - Explicit, separate consent for:
    - Research use beyond direct care.
    - Future model training or external sharing.
  - Simple ways for individuals to **withdraw consent** and request deletion.
- Recommended data retention policy:
  - Store only what is necessary for the defined purpose.
  - Define and document retention duration.
  - Periodically review and purge stale or unused records.

### Privacy and security

- Default repo configuration is to keep data **local to the user’s machine**.
- Any networked or cloud deployment should:
  - Use **TLS** for all network traffic.
  - Encrypt data at rest where supported.
  - Restrict access via authentication and authorization.
  - Log and monitor access, with incident response plans.

### Transparency and explainability

- Grad-CAM overlays can help users and clinicians see **where** the model is focusing, but:
  - They do not guarantee that the model is using clinically meaningful features.
  - They should never be treated as definitive explanations of model reasoning.
- Interfaces should:
  - Clearly label outputs as **model estimates**.
  - Provide context about uncertainty and limitations.

### Accountability and governance

- If SkinMorph is extended for clinical contexts, organizations should:
  - Establish an **AI governance committee** with dermatologists, ethicists, and patient representatives.
  - Maintain documentation of:
    - Training data sources.
    - Evaluation protocols and results.
    - Known limitations and mitigations.
  - Implement ongoing **monitoring for performance drift** and harm.






