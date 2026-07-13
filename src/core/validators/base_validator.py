from src.common.types import CurrentStatusId, RowId, RowIdentityKey

class BaseValidator:

    def check_existence(self, list_one: list[RowId] | list[RowIdentityKey], list_two: list[RowId] | list[RowIdentityKey]) -> bool:
        missing_ids = set(list_one) - set(list_two)
        
        if missing_ids:
            return False
            
        return True
    
    def check_statuses(self, statuses: list[CurrentStatusId]) -> bool:
        return not False in statuses