from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Union
from datetime import datetime
from enum import Enum
import json
from pathlib import Path

class RecordType(Enum):
    """Types of records supported by the system."""
    DECISION = "decision"
    CHANGE = "change"
    DEBUG = "debug"
    HANDOFF = "handoff"
    CONVERSATION = "conversation"

class RecordStatus(Enum):
    """Possible statuses for records."""
    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ARCHIVED = "archived"

@dataclass
class RecordMetadata:
    """Metadata common to all records."""
    record_id: str
    record_type: RecordType
    timestamp: str
    author: str
    project: str
    version: str
    status: RecordStatus
    tags: List[str]
    related_records: List[str]

@dataclass
class DecisionContent:
    """Content specific to decision records."""
    title: str
    context: str
    decision: str
    rationale: str
    alternatives: List[str]
    consequences: List[str]
    implementation_status: str
    affected_files: List[str]

@dataclass
class ChangeContent:
    """Content specific to change records."""
    description: str
    purpose: str
    impact: str
    changes: Dict[str, str]
    testing: str
    verification: str
    affected_files: List[str]

@dataclass
class DebugContent:
    """Content specific to debug records."""
    issue: str
    root_cause: str
    solution: str
    prevention: List[str]
    testing: str
    documentation: str
    affected_files: List[str]

@dataclass
class HandoffContent:
    """Content specific to handoff records."""
    summary: str
    current_status: str
    next_steps: List[str]
    risks: List[str]
    dependencies: List[str]

@dataclass
class ConversationContent:
    """Content specific to conversation records."""
    participants: List[str]
    topics: List[str]
    messages: List[Dict[str, str]]
    decisions: List[str]
    action_items: List[str]

@dataclass
class StandardRecord:
    """Standardized record format that supports all record types."""
    metadata: RecordMetadata
    content: Union[DecisionContent, ChangeContent, DebugContent, 
                  HandoffContent, ConversationContent]
    
    def to_json(self) -> str:
        """Convert record to JSON string."""
        return json.dumps(asdict(self), indent=2)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'StandardRecord':
        """Create record from JSON string."""
        data = json.loads(json_str)
        return cls(
            metadata=RecordMetadata(**data['metadata']),
            content=cls._parse_content(data['content'], 
                                     RecordType(data['metadata']['record_type']))
        )
    
    @staticmethod
    def _parse_content(content_data: Dict, record_type: RecordType) -> Union[
        DecisionContent, ChangeContent, DebugContent, HandoffContent, ConversationContent
    ]:
        """Parse content based on record type."""
        content_classes = {
            RecordType.DECISION: DecisionContent,
            RecordType.CHANGE: ChangeContent,
            RecordType.DEBUG: DebugContent,
            RecordType.HANDOFF: HandoffContent,
            RecordType.CONVERSATION: ConversationContent
        }
        return content_classes[record_type](**content_data)
    
    def validate(self) -> List[str]:
        """Validate the record and return list of errors."""
        errors = []
        
        # Validate metadata
        if not self.metadata.record_id:
            errors.append("Missing record_id")
        if not self.metadata.author:
            errors.append("Missing author")
        if not self.metadata.project:
            errors.append("Missing project")
        
        # Validate content based on type
        if isinstance(self.content, DecisionContent):
            if not self.content.title:
                errors.append("Decision missing title")
            if not self.content.decision:
                errors.append("Decision missing decision text")
        
        elif isinstance(self.content, ChangeContent):
            if not self.content.description:
                errors.append("Change missing description")
            if not self.content.changes:
                errors.append("Change missing changes")
        
        elif isinstance(self.content, DebugContent):
            if not self.content.issue:
                errors.append("Debug missing issue")
            if not self.content.solution:
                errors.append("Debug missing solution")
        
        elif isinstance(self.content, HandoffContent):
            if not self.content.summary:
                errors.append("Handoff missing summary")
            if not self.content.current_status:
                errors.append("Handoff missing current status")
        
        elif isinstance(self.content, ConversationContent):
            if not self.content.participants:
                errors.append("Conversation missing participants")
            if not self.content.messages:
                errors.append("Conversation missing messages")
        
        return errors 