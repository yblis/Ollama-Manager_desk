from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class OllamaModel:
    name: str
    size: Optional[int] = None
    modified: Optional[datetime] = None
    digest: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: dict) -> 'OllamaModel':
        return cls(
            name=data['name'],
            size=data.get('size', 0),
            modified=datetime.fromisoformat(data['modified']) if 'modified' in data else datetime.now(),
            digest=data.get('digest', '')
        )

@dataclass
class RunningInstance:
    instance_id: str
    model_name: str
    started: datetime
    
    @classmethod
    def from_dict(cls, data: dict) -> 'RunningInstance':
        return cls(
            instance_id=data['instance_id'],
            model_name=data['model'],
            started=datetime.fromisoformat(data['started'])
        )
