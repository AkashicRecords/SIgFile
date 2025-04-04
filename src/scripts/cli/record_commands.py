import click
from pathlib import Path
from datetime import datetime
import json
from typing import Optional, List
from ..models.record_format import (
    StandardRecord, RecordMetadata, RecordType, RecordStatus,
    DecisionContent, ChangeContent, DebugContent, HandoffContent, ConversationContent
)
from ..models.record_manager import RecordManager
from ..models.ai_record_assistant import AIRecordAssistant

@click.group()
def record():
    """Manage project records."""
    pass

@record.command()
@click.option('--type', type=click.Choice([t.value for t in RecordType]), required=True)
@click.option('--project', required=True)
@click.option('--author', required=True)
@click.option('--ai/--no-ai', default=False)
def create(type: str, project: str, author: str, ai: bool):
    """Create a new record."""
    manager = RecordManager(project)
    
    if ai:
        assistant = AIRecordAssistant(manager)
        click.echo("Using AI assistance to gather record information...")
        
        if type == RecordType.DECISION.value:
            record_path = click.get_current_context().invoke(
                assistant.create_decision_record_with_ai, author=author
            )
        elif type == RecordType.CHANGE.value:
            record_path = click.get_current_context().invoke(
                assistant.create_change_record_with_ai,
                files=[],  # Will be gathered by AI
                author=author
            )
        elif type == RecordType.DEBUG.value:
            record_path = click.get_current_context().invoke(
                assistant.create_debug_record_with_ai,
                issue="",  # Will be gathered by AI
                author=author
            )
    else:
        # Manual record creation
        metadata = RecordMetadata(
            record_id=f"{type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            record_type=RecordType(type),
            timestamp=datetime.now().isoformat(),
            author=author,
            project=project,
            version="1.0",
            status=RecordStatus.DRAFT,
            tags=[],
            related_records=[]
        )
        
        if type == RecordType.DECISION.value:
            content = DecisionContent(
                title=click.prompt("Title"),
                context=click.prompt("Context"),
                decision=click.prompt("Decision"),
                rationale=click.prompt("Rationale"),
                alternatives=click.prompt("Alternatives (comma-separated)").split(","),
                consequences=click.prompt("Consequences (comma-separated)").split(","),
                implementation_status="pending",
                affected_files=[]
            )
        elif type == RecordType.CHANGE.value:
            content = ChangeContent(
                description=click.prompt("Description"),
                purpose=click.prompt("Purpose"),
                impact=click.prompt("Impact"),
                changes={},
                testing=click.prompt("Testing"),
                verification=click.prompt("Verification"),
                affected_files=[]
            )
        elif type == RecordType.DEBUG.value:
            content = DebugContent(
                issue=click.prompt("Issue"),
                root_cause=click.prompt("Root Cause"),
                solution=click.prompt("Solution"),
                prevention=click.prompt("Prevention (comma-separated)").split(","),
                testing=click.prompt("Testing"),
                documentation=click.prompt("Documentation"),
                affected_files=[]
            )
        
        record = StandardRecord(metadata=metadata, content=content)
        record_path = manager.add_entry(
            record_type=type,
            content=asdict(content),
            author=author
        )
    
    click.echo(f"Created record: {record_path}")

@record.command()
@click.argument('record_path')
@click.option('--status', type=click.Choice([s.value for s in RecordStatus]))
@click.option('--tag', multiple=True)
def update(record_path: str, status: Optional[str], tag: List[str]):
    """Update an existing record."""
    manager = RecordManager(Path(record_path).parent)
    
    if status:
        manager.update_record(
            record_path,
            "status_update",
            {"status": status},
            click.get_current_context().params.get('author', 'unknown')
        )
    
    if tag:
        manager.update_record(
            record_path,
            "tag_update",
            {"tags": list(tag)},
            click.get_current_context().params.get('author', 'unknown')
        )
    
    click.echo(f"Updated record: {record_path}")

@record.command()
@click.argument('record_path')
def validate(record_path: str):
    """Validate a record."""
    manager = RecordManager(Path(record_path).parent)
    record = StandardRecord.from_json(Path(record_path).read_text())
    
    errors = record.validate()
    if errors:
        click.echo("Validation errors:")
        for error in errors:
            click.echo(f"- {error}")
    else:
        click.echo("Record is valid")

@record.command()
@click.argument('record_path')
def show(record_path: str):
    """Display a record."""
    record = StandardRecord.from_json(Path(record_path).read_text())
    click.echo(record.to_json())

@record.command()
@click.option('--type', type=click.Choice([t.value for t in RecordType]))
@click.option('--status', type=click.Choice([s.value for s in RecordStatus]))
@click.option('--tag')
@click.option('--author')
def list(type: Optional[str], status: Optional[str], tag: Optional[str], author: Optional[str]):
    """List records matching criteria."""
    manager = RecordManager(".")  # Current directory
    # Implementation would search for matching records
    click.echo("Listing records...")  # Placeholder 