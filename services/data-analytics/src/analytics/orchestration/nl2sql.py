from contracts import ScopeObject


class MockNL2SQL:
    async def generate(self, question: str, scope: ScopeObject) -> dict:
        project = scope.project_uuids[0] if scope.project_uuids else "unknown"
        sql = (
            "select metric_name, value "
            "from project_metrics "
            "where project_id = :project_id limit 50"
        )
        return {
            "sql": sql,
            "rows": [{"metric_name": "activities_completed", "value": 12, "project_id": project}],
            "columns": ["metric_name", "value"],
            "warnings": [],
        }
