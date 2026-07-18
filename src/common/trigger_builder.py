from src.common import DBManager


class TriggerBuilder:

    def create_all_triggers(self, table_name: str, db_manager: DBManager) -> None:
        self._create_trigger_after_insert(table_name, db_manager)
        self._create_trigger_after_update(table_name, db_manager)
        self._create_trigger_after_delete(table_name, db_manager)

    def _create_trigger_after_insert(
        self, table_name: str, db_manager: DBManager
    ) -> None:
        db_manager.cursor.execute(f"DROP TRIGGER IF EXISTS tr_{table_name}_ai")

        query = f"""
                CREATE TRIGGER tr_{table_name}_ai
                AFTER INSERT ON {table_name}
                FOR EACH ROW
                BEGIN
                INSERT INTO audit_logs (table_name, action, record_id, column_name, old_value, new_value, changed_at, changed_by_staff_id)
                VALUES ('{table_name}', 'INSERT', NEW.id, NULL, NULL, NULL, NOW(), @user);
                END
                """

        db_manager.cursor.execute(query)

    def _create_trigger_after_update(
        self, table_name: str, db_manager: DBManager
    ) -> None:
        db_manager.cursor.execute(f"DROP TRIGGER IF EXISTS tr_{table_name}_au")

        query = "SELECT COLUMN_NAME FROM information_schema.columns WHERE TABLE_NAME = %s AND TABLE_SCHEMA = 'airline'"
        values = [table_name]

        columns: list[str] = db_manager.retrieve(query, values)

        inserts = ""
        for column in columns:
            inserts += f"""
                        IF NOT (OLD.{column} <=> NEW.{column}) THEN
                            INSERT INTO audit_logs (table_name, action, record_id, column_name, old_value, new_value, changed_at, changed_by_staff_id)
                            VALUES ('{table_name}', 'UPDATE', OLD.id, '{column}', OLD.{column}, NEW.{column}, NOW(), @user);
                        END IF;
                        """

        query: str = f"""
                CREATE TRIGGER tr_{table_name}_au
                AFTER UPDATE ON {table_name}
                FOR EACH ROW
                BEGIN
                {inserts}
                END
                """

        db_manager.cursor.execute(query)

    def _create_trigger_after_delete(
        self, table_name: str, db_manager: DBManager
    ) -> None:
        db_manager.cursor.execute(f"DROP TRIGGER IF EXISTS tr_{table_name}_ad")

        query: str = f"""
                CREATE TRIGGER tr_{table_name}_ad
                AFTER DELETE ON {table_name}
                FOR EACH ROW
                BEGIN
                INSERT INTO audit_logs (table_name, action, record_id, column_name, old_value, new_value, changed_at, changed_by_staff_id)
                VALUES ('{table_name}', 'DELETE', OLD.id, NULL, NULL, NULL, NOW(), @usuario);
                END
                """

        db_manager.cursor.execute(query)
