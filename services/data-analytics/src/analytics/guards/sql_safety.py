"""SQL safety checks live here.

Production guards must enforce read-only SQL, table allowlists, row limits, timeout
limits, tenant predicates, and rejection of DDL/DML statements before execution.
"""


def validate_read_only(sql: str) -> list[str]:
    normalized = sql.strip().lower()
    warnings: list[str] = []
    if not normalized.startswith("select"):
        warnings.append("Only SELECT statements are allowed.")
    if " limit " not in f" {normalized} ":
        warnings.append("A row limit was added by the service.")
    return warnings
