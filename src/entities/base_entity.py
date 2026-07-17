from typing import Any
from uuid import UUID

class BaseEntity:

    id: int | UUID

    def to_dict(self) -> dict[str, Any]:
        result = {}
        
        for key in dir(self):
            if key.startswith('_'):
                continue
                
            if key == 'identity_key':
                continue
                
            value = getattr(self, key)
            
            if callable(value):
                continue
                
            if isinstance(value, BaseEntity):
                result[key] = value.to_dict()
                
            elif isinstance(value, list) and len(value) > 0 and isinstance(value[0], BaseEntity):
                result[key] = [item.to_dict() for item in value]
                
            else:
                result[key] = value
                
        return result
    
    def __eq__(self, other: 'BaseEntity') -> bool:
        if type(self) is not type(other):
            return False
            
        return self.to_dict() == other.to_dict()

    def __hash__(self) -> int:
        return hash((type(self), self.id))