from unit_conversion_grader.commands.conversion_grader import (
    check_unit_existence,
    validate_input,
    grade_response,
)

from unit_conversion_grader.config.enums import (
    Answer,
    UnitCategory,
    TemperatureUnits,
    VolumeUnits,
)
from unit_conversion_grader.config.data import UNITS

import pytest
import rich


# Test check_unit_existence
test_cases_check_unit_existence_temperature = [
    (UNITS, TemperatureUnits.KELVIN.value, UnitCategory.TEMPERATURE.value),
    (UNITS, TemperatureUnits.CELSIUS.value, UnitCategory.TEMPERATURE.value),
    (UNITS, TemperatureUnits.FAHRENHEIT.value, UnitCategory.TEMPERATURE.value),
    (UNITS, TemperatureUnits.RANKINE.value, UnitCategory.TEMPERATURE.value),
]


@pytest.mark.parametrize(
    "dictionary, unit_to_check, expected", test_cases_check_unit_existence_temperature
)
def test_check_unit_existence_temperature(dictionary, unit_to_check, expected):
    result = check_unit_existence(dictionary, unit_to_check)
    assert result == expected


test_cases_check_unit_existence_volume = [
    (UNITS, VolumeUnits.LITERS.value, UnitCategory.VOLUME.value),
    (UNITS, VolumeUnits.TABLESPOONS.value, UnitCategory.VOLUME.value),
    (UNITS, VolumeUnits.CUBIC_INCHES.value, UnitCategory.VOLUME.value),
    (UNITS, VolumeUnits.CUPS.value, UnitCategory.VOLUME.value),
    (UNITS, VolumeUnits.CUBIC_FEET.value, UnitCategory.VOLUME.value),
    (UNITS, VolumeUnits.GALLONS.value, UnitCategory.VOLUME.value),
]


@pytest.mark.parametrize(
    "dictionary, unit_to_check, expected", test_cases_check_unit_existence_volume
)
def test_check_unit_existence_volume(dictionary, unit_to_check, expected):
    result = check_unit_existence(dictionary, unit_to_check)
    assert result == expected


test_cases_check_unit_existence_nonexistent = [
    (UNITS, "KELvin", None),
    (UNITS, "NoneExist", None),
    (UNITS, "", None),
    (UNITS, None, None),
]


@pytest.mark.parametrize(
    "dictionary, unit_to_check, expected", test_cases_check_unit_existence_nonexistent
)
def test_check_unit_existence_volume(dictionary, unit_to_check, expected):
    result = check_unit_existence(dictionary, unit_to_check)
    assert result == expected


# Test validate_input


def test_validate_input_invalid_from_unit(mocker):
    mocker.patch(
        "unit_conversion_grader.commands.conversion_grader.check_unit_existence",
        side_effect=[UnitCategory.TEMPERATURE.value, None],
    )
    result = validate_input("Dummy_Unit", TemperatureUnits.FAHRENHEIT.value, "25")
    assert result == None


def test_validate_input_invalid_to_unit(mocker):
    mocker.patch(
        "unit_conversion_grader.commands.conversion_grader.check_unit_existence",
        side_effect=[UnitCategory.TEMPERATURE.value, None],
    )
    result = validate_input(TemperatureUnits.CELSIUS.value, "Dummy_Unit", "25")
    assert result == None


def test_validate_input_invalid_from_and_to_unit(mocker):
    mocker.patch(
        "unit_conversion_grader.commands.conversion_grader.check_unit_existence",
        side_effect=[None, None],
    )
    result = validate_input("Dummy_Unit", "Dummy_Unit", "25")
    assert result == None


def test_validate_input_different_unit_categories(mocker):
    mocker.patch(
        "unit_conversion_grader.commands.conversion_grader.check_unit_existence",
        side_effect=[UnitCategory.TEMPERATURE.value, UnitCategory.VOLUME.value],
    )
    result = validate_input(
        TemperatureUnits.FAHRENHEIT.value, VolumeUnits.CUPS.value, "25"
    )
    assert result == None


def test_validate_input_invalid_input_value(mocker):
    mocker.patch(
        "unit_conversion_grader.commands.conversion_grader.check_unit_existence",
        side_effect=[UnitCategory.TEMPERATURE.value, UnitCategory.TEMPERATURE.value],
    )
    result = validate_input(
        TemperatureUnits.FAHRENHEIT.value, TemperatureUnits.FAHRENHEIT.value, "dog"
    )
    assert result == None


def test_validate_input_valid_temperature(mocker):
    mocker.patch(
        "unit_conversion_grader.commands.conversion_grader.check_unit_existence",
        side_effect=[UnitCategory.TEMPERATURE.value, UnitCategory.TEMPERATURE.value],
    )
    result = validate_input(
        TemperatureUnits.FAHRENHEIT.value, TemperatureUnits.FAHRENHEIT.value, "25"
    )
    assert result == UnitCategory.TEMPERATURE.value


def test_validate_input_valid_volume(mocker):
    mocker.patch(
        "unit_conversion_grader.commands.conversion_grader.check_unit_existence",
        side_effect=[UnitCategory.VOLUME.value, UnitCategory.VOLUME.value],
    )
    result = validate_input(VolumeUnits.LITERS.value, VolumeUnits.TABLESPOONS, "25")
    assert result == UnitCategory.VOLUME.value


def test_validate_input_unexpected_exception(mocker):
    mocker.patch(
        "unit_conversion_grader.commands.conversion_grader.check_unit_existence",
        side_effect=Exception("This is a deliberate exception"),
    )
    result = validate_input(VolumeUnits.LITERS.value, VolumeUnits.TABLESPOONS, "25")
    assert result == None


# Test grade_response

# Test grade_response when user response is not a number
def test_grade_response_non_numeric_user_response(mocker):
    mocker.patch(
        "unit_conversion_grader.utils.common.is_valid_numeric_string",
        return_value=False,
    )
    mocker.patch(
        "unit_conversion_grader.commands.conversion_grader.validate_input",
        return_value=UnitCategory.TEMPERATURE.value,
    )
    result = grade_response(
        "30", TemperatureUnits.KELVIN.value, TemperatureUnits.CELSIUS.value, "dog"
    )
    assert result == Answer.INCORRECT


# Test grade_response when user response is incorrect
def test_grade_response_incorrect_response(mocker):
    mocker.patch(
        "unit_conversion_grader.utils.common.is_valid_numeric_string",
        return_value=True,
    )
    mocker.patch(
        "unit_conversion_grader.commands.conversion_grader.validate_input",
        return_value=UnitCategory.TEMPERATURE.value,
    )
    mocker.patch(
        "unit_conversion_grader.utils.common.convert_units", return_value=-241.1
    )
    result = grade_response(
        "32", TemperatureUnits.KELVIN.value, TemperatureUnits.CELSIUS.value, "-241.01"
    )
    assert result == Answer.INCORRECT


# Test grade_response when from_unit/to_unit/input_value is invalid
def test_grade_response_invalid_input(mocker):
    mocker.patch(
        "unit_conversion_grader.utils.common.is_valid_numeric_string", return_value=True
    )
    mocker.patch(
        "unit_conversion_grader.commands.conversion_grader.validate_input",
        return_value=None,
    )
    result = grade_response(
        "dog", TemperatureUnits.KELVIN.value, TemperatureUnits.CELSIUS.value, "-241.1"
    )
    assert result == Answer.INVALID


# Test grade_response when from_unit is equal to to_unit but input_value is different from user_response
def test_grade_response_same_unit_incorrect_user_response(mocker):
    mocker.patch(
        "unit_conversion_grader.utils.common.is_valid_numeric_string",
        return_value=True,
    )
    mocker.patch(
        "unit_conversion_grader.commands.conversion_grader.validate_input",
        return_value=UnitCategory.TEMPERATURE.value,
    )
    result = grade_response(
        "32", TemperatureUnits.CELSIUS.value, TemperatureUnits.CELSIUS.value, "31"
    )
    assert result == Answer.INCORRECT


# Test grade_response when convert_units returns None
def test_grade_response_failed_convert_units(mocker):
    mocker.patch(
        "unit_conversion_grader.utils.common.is_valid_numeric_string",
        return_value=True,
    )
    mocker.patch(
        "unit_conversion_grader.commands.conversion_grader.validate_input",
        return_value=UnitCategory.TEMPERATURE.value,
    )
    mocker.patch("unit_conversion_grader.utils.common.convert_units", return_value=None)

    result = grade_response(
        "32", TemperatureUnits.CELSIUS.value, VolumeUnits.LITERS.value, "305.2"
    )
    assert result == Answer.INVALID


test_grade_response_correct_answer = [
    (
        "32.0",
        TemperatureUnits.FAHRENHEIT.value,
        TemperatureUnits.CELSIUS.value,
        "0",
        Answer.CORRECT,
    ),
    (
        "32.0",
        TemperatureUnits.KELVIN.value,
        TemperatureUnits.CELSIUS.value,
        "-241.15",
        Answer.CORRECT,
    ),
    (
        "32.0",
        TemperatureUnits.KELVIN.value,
        TemperatureUnits.KELVIN.value,
        "32.0",
        Answer.CORRECT,
    ),
    (
        "32.01",
        TemperatureUnits.KELVIN.value,
        TemperatureUnits.KELVIN.value,
        "32.013",
        Answer.CORRECT,
    ),
]


@pytest.mark.parametrize(
    "input_value, from_unit, to_unit, user_response, expected",
    test_grade_response_correct_answer,
)
def test_grade_response_correct_response(
    input_value, from_unit, to_unit, user_response, expected, mocker
):
    mocker.patch(
        "unit_conversion_grader.utils.common.is_valid_numeric_string",
        return_value=True,
    )
    mocker.patch(
        "unit_conversion_grader.commands.conversion_grader.validate_input",
        return_value=UnitCategory.TEMPERATURE.value,
    )
    mocker.patch(
        "unit_conversion_grader.utils.common.convert_units", return_value=user_response
    )
    # Test correct response
    result = grade_response(input_value, from_unit, to_unit, user_response)
    assert result == Answer.CORRECT
