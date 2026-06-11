from analytics.guards.sql_safety import validate_read_only


def test_validate_read_only_warns_on_mutation() -> None:
    warnings = validate_read_only("delete from users")

    assert "Only SELECT statements are allowed." in warnings
