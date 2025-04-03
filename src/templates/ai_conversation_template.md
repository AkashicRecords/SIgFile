# AI Conversation Record

## Chat Information
- Chat ID: {{ chat_id }}
- Project: {{ project_name }}
- Date: {{ date }}
- Timestamp: {{ timestamp }}

## Conversation Summary
{{ summary }}

## Key Decisions
{% for decision in key_decisions %}
- **{{ decision.type }}**: {{ decision.description }}
  - Rationale: {{ decision.rationale }}
  - Impact: {{ decision.impact }}
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

## Related Changes
{% for change in related_changes %}
- **{{ change.type }}**: {{ change.description }}
  - Files: {{ change.files|join(', ') }}
  - Impact: {{ change.impact }}
{% endfor %}

## Next Steps
{% for step in next_steps %}
- {{ step }}
{% endfor %}

## AI Insights
### Common Topics
{% for topic in ai_insights.common_topics %}
- {{ topic }}
{% endfor %}

### Impact Areas
{% for area in ai_insights.impact_areas %}
- {{ area }}
{% endfor %}

### Decision Patterns
{% for pattern in ai_insights.decision_patterns %}
- **{{ pattern.type }}**: {{ pattern.description }}
  - Frequency: {{ pattern.frequency }}
  - Common Context: {{ pattern.context }}
{% endfor %}

### Code Change Patterns
{% for pattern in ai_insights.code_patterns %}
- **{{ pattern.type }}**: {{ pattern.description }}
  - Files: {{ pattern.files|join(', ') }}
  - Impact Level: {{ pattern.impact_level }}
{% endfor %}

### Learning Points
{% for point in ai_insights.learning_points %}
- {{ point }}
{% endfor %}

### Future Considerations
{% for consideration in ai_insights.future_considerations %}
- {{ consideration }}
{% endfor %} 