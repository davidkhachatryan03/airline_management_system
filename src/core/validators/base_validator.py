from collections.abc import Sequence

from src.common.types import RowId, RowIdentityKey

class BaseValidator:

    def check_existence(self, list_one: Sequence[RowId] | Sequence[RowIdentityKey], list_two: Sequence[RowId] | Sequence[RowIdentityKey]) -> bool:
        missing_ids = set(list_one) - set(list_two)
        
        if missing_ids:
            return False
            
        return True