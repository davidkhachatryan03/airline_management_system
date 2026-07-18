import pytest

from src.entities.route import Route


def test_route_valid_input(route: Route) -> None:
    assert route.id == 5
    assert route.flight_number == "AR1234"
    assert route.origin == "EZE"
    assert route.destination == "COR"
    assert route.distance_km == 645
    assert route.duration_min == 90


@pytest.mark.parametrize(
    "field, value, exception, message",
    [
        ("id", "1", TypeError, "The type the id is not int."),
        ("id", 0, ValueError, "The id can not be negative or zero."),
        ("id", -10, ValueError, "The id can not be negative or zero."),
        (
            "flight_number",
            123456,
            TypeError,
            "The type of 123456 is not str.",
        ),
        (
            "flight_number",
            "      ",
            ValueError,
            "The flight number can not be empty.",
        ),
        (
            "flight_number",
            "AR123",  
            ValueError,
            "The flight number must be 6 characters long.",
        ),
        (
            "flight_number",
            "AR12345", 
            ValueError,
            "The flight number must be 6 characters long.",
        ),
        (
            "origin",
            123,
            TypeError,
            "The type of 123 is not str.",
        ),
        (
            "origin",
            "   ",
            ValueError,
            "The origin can not be empty.",
        ),
        (
            "origin",
            "AR", 
            ValueError,
            "The origin must be 3 characters long.",
        ),
        (
            "origin",
            "ARGE",  
            ValueError,
            "The origin must be 3 characters long.",
        ),
        (
            "destination",
            123,
            TypeError,
            "The type of 123 is not str.",
        ),
        (
            "destination",
            "   ",
            ValueError,
            "The destination can not be empty.",
        ),
        (
            "destination",
            "CO",  
            ValueError,
            "The destination must be 3 characters long.", 
        ),
        (
            "destination",
            "CORB",  # 4 caracteres
            ValueError,
            "The destination must be 3 characters long.",  
        ),
        ("distance_km", "100", TypeError, "The type of 100 is not int."),
        ("distance_km", 0, ValueError, "The distance km can not be negative or zero."),
        (
            "distance_km",
            -50,
            ValueError,
            "The distance km can not be negative or zero.",
        ),
        ("duration_min", "120", TypeError, "The type of 120 is not int."),
        ("duration_min", 0, ValueError, "The duration min can not be negative or zero."),
        (
            "duration_min",
            -15,
            ValueError,
            "The duration min can not be negative or zero.",
        ),
    ],
)
def test_invalid_route(route: Route, field, value, exception, message) -> None:
    test_data: dict = route.to_dict()
    test_data[field] = value

    with pytest.raises(exception, match=message):
        Route(**test_data)