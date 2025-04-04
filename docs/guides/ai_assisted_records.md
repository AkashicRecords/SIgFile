# AI-Assisted Record Creation Guide

## Overview
The AI-assisted record creation feature helps you create high-quality records through conversational interaction with an AI assistant. This guide explains how to use this feature effectively.

## Basic Usage

### Creating Records with AI
```bash
# Create a decision record
sigfile record create --type decision --ai

# Create a change record
sigfile record create --type change --ai

# Create a debug record
sigfile record create --type debug --ai
```

### Interactive Mode
When using AI assistance, the system will:
1. Ask questions about the record
2. Validate your responses
3. Suggest improvements
4. Create the final record

Example interaction:
```bash
$ sigfile record create --type decision --ai
AI: Let's create a decision record. What's the title of this decision?
You: Implement AI-assisted record creation
AI: Great! Can you describe the context for this decision?
You: We need to improve record creation efficiency...
```

### Batch Mode
For creating multiple records:
```bash
# Create multiple records in batch
sigfile record create --type change --ai --batch
```

## Advanced Features

### Validation
```bash
# Validate an AI response
sigfile record validate --ai-response response.json

# Validate and correct errors
sigfile record validate --ai-response response.json --correct
```

### Custom Prompts
```bash
# Use a custom prompt template
sigfile record create --type decision --ai --prompt custom_prompt.json
```

### Response Format
AI responses are structured as JSON:
```json
{
    "title": "Decision Title",
    "context": "Background information...",
    "decision": "The decision made...",
    "rationale": "Reasoning...",
    "alternatives": ["Option 1", "Option 2"],
    "consequences": ["Impact 1", "Impact 2"]
}
```

## Best Practices

1. **Be Specific**
   - Provide detailed context
   - Include relevant examples
   - Mention constraints

2. **Review Responses**
   - Check for completeness
   - Verify accuracy
   - Request clarifications

3. **Use Validation**
   - Validate responses
   - Correct errors
   - Ensure consistency

4. **Batch Processing**
   - Group related records
   - Use consistent formats
   - Review in bulk

## Error Handling

### Common Errors
1. **Incomplete Information**
   - Solution: Provide more context
   - Command: `sigfile record create --type decision --ai --retry`

2. **Validation Errors**
   - Solution: Use correction mode
   - Command: `sigfile record validate --ai-response response.json --correct`

3. **Format Issues**
   - Solution: Check response structure
   - Command: `sigfile record validate --ai-response response.json --format`

### Debugging
```bash
# Enable debug mode
sigfile record create --type decision --ai --debug

# View AI conversation
sigfile record show --conversation record_id
```

## Examples

### Decision Record
```bash
$ sigfile record create --type decision --ai
AI: What's the title of this decision?
You: Implement AI-assisted record creation
AI: What's the context for this decision?
You: We need to improve record creation efficiency...
```

### Change Record
```bash
$ sigfile record create --type change --ai
AI: What changes are you making?
You: Adding AI assistance to record creation
AI: What's the purpose of these changes?
You: To improve efficiency and quality...
```

### Debug Record
```bash
$ sigfile record create --type debug --ai
AI: What issue are you debugging?
You: AI response validation errors
AI: What's the root cause?
You: Incomplete response format...
```

## Related Commands

- `sigfile record list`: List existing records
- `sigfile record show`: Display record details
- `sigfile record update`: Update existing records
- `sigfile record validate`: Validate records

## Troubleshooting

1. **AI Not Responding**
   - Check internet connection
   - Verify API keys
   - Restart the CLI

2. **Validation Errors**
   - Review response format
   - Check required fields
   - Use correction mode

3. **Performance Issues**
   - Use batch mode
   - Reduce response size
   - Enable caching

## Support

For additional help:
- Use `sigfile record --help`
- Check the documentation
- Contact support 