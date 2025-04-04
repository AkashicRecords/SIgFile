#!/usr/bin/env python3

import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

class RecordFormat:
    """Standardized record format for all tracking types."""
    
    @staticmethod
    def create_record(
        record_type: str,
        title: str,
        description: str,
        files: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a standardized record."""
        timestamp = datetime.now().isoformat()
        
        return {
            'type': record_type,
            'title': title,
            'description': description,
            'timestamp': timestamp,
            'files': files or [],
            'metadata': {
                'record_id': f"{record_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'created_at': timestamp,
                **(metadata or {})
            },
            'context': context or {}
        }
    
    @staticmethod
    def export_records(
        records: List[Dict[str, Any]],
        record_type: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Export records in standardized JSON format."""
        return json.dumps({
            'records': records,
            'metadata': {
                'record_type': record_type,
                'total_records': len(records),
                'export_time': datetime.now().isoformat(),
                **(metadata or {})
            }
        }, indent=2)
    
    @staticmethod
    def save_record(
        record: Dict[str, Any],
        base_dir: Path,
        record_type: str
    ) -> Path:
        """Save a record to the appropriate directory."""
        # Create date-based directory structure
        date_dir = base_dir / record_type / datetime.now().strftime('%Y%m%d')
        date_dir.mkdir(parents=True, exist_ok=True)
        
        # Save record
        record_file = date_dir / f"{record['metadata']['record_id']}.json"
        with open(record_file, 'w') as f:
            json.dump(record, f, indent=2)
        
        return record_file
    
    @staticmethod
    def load_records(
        base_dir: Path,
        record_type: str,
        date: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Load records from the appropriate directory."""
        if date is None:
            date = datetime.now().strftime('%Y%m%d')
        
        record_dir = base_dir / record_type / date
        if not record_dir.exists():
            return []
        
        records = []
        for record_file in sorted(record_dir.glob('*.json'), reverse=True):
            with open(record_file) as f:
                records.append(json.load(f))
            if limit and len(records) >= limit:
                break
        
        return records 