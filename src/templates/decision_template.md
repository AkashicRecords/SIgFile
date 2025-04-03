# Project Decision Record

## Decision Information
- Decision ID: {{ decision_id }}
- Project: {{ project_name }}
- Date: {{ date }}
- Timestamp: {{ timestamp }}

## Description
{{ description }}

## Rationale
{{ rationale }}

## Impact Assessment
### Level
{{ impact.level }}

### Areas Affected
{% for area in impact.areas %}
- {{ area }}
{% endfor %}

### Expected Outcomes
{% for outcome in impact.outcomes %}
- {{ outcome }}
{% endfor %}

### Risks and Mitigations
{% for risk in impact.risks %}
- **Risk**: {{ risk.description }}
  - Severity: {{ risk.severity }}
  - Mitigation: {{ risk.mitigation }}
{% endfor %}

## Alternative Approaches
{% for alt in alternatives %}
### {{ alt.name }}
- Description: {{ alt.description }}
- Pros:
{% for pro in alt.pros %}
  - {{ pro }}
{% endfor %}
- Cons:
{% for con in alt.cons %}
  - {{ con }}
{% endfor %}
- Why Not Chosen: {{ alt.rejection_reason }}
{% endfor %}

## Code Changes
{% for change in code_changes %}
### {{ change.file }}
- Type: {{ change.type }}
- Description: {{ change.description }}
```{{ change.language }}
{{ change.content }}
```
{% endfor %}

## Related Decisions
{% for decision in related_decisions %}
- [{{ decision.id }}] {{ decision.description }}
  - Relationship: {{ decision.relationship }}
  - Impact on Current Decision: {{ decision.impact }}
{% endfor %}

## Implementation Plan
### Steps
{% for step in implementation_plan.steps %}
1. {{ step }}
{% endfor %}

### Timeline
{{ implementation_plan.timeline }}

### Required Resources
{% for resource in implementation_plan.resources %}
- {{ resource }}
{% endfor %}

### Risks and Contingencies
{% for risk in implementation_plan.risks %}
- **Risk**: {{ risk.description }}
  - Probability: {{ risk.probability }}
  - Impact: {{ risk.impact }}
  - Contingency Plan: {{ risk.contingency }}
{% endfor %}

## Success Criteria
{% for criterion in success_criteria %}
- {{ criterion }}
{% endfor %}

## Future Considerations
{% for consideration in future_considerations %}
- {{ consideration }}
{% endfor %}

## Review Notes
{% for note in review_notes %}
### {{ note.date }} - {{ note.reviewer }}
{{ note.content }}
{% endfor %} 