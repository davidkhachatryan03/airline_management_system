from typing import Any

class BaseEntity:
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