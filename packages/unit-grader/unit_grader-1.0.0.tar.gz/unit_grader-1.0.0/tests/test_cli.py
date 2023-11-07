# tests/test_main.py

import typer
import rich
import os
from typer.testing import CliRunner
import pytest
from pytest_mock import mocker
from unit_conversion_grader.cli import (
    app,
    grade_conversion,
    get_version,
    version_callback,
    app_name,
)
from unit_conversion_grader.commands.conversion_grader import grade_response, Answer

# Create a CliRunner for testing the CLI app
runner = CliRunner()

# Mock the grade_response function to simulate its behavior
@pytest.fixture
def mock_grade_response(mocker):
    mocker.patch(
        "unit_conversion_grader.commands.conversion_grader.grade_response",
        return_value=Answer.CORRECT,
    )


# Test the grade_response function
def test_grade_response():
    result = grade_response("32", "Celsius", "Kelvin", "305.2")
    assert result == Answer.CORRECT


# Test the grade_conversion CLI command
def test_grade_conversion(mock_grade_response):
    input_value = "32"
    from_unit = "Celsius"
    to_unit = "Kelvin"
    student_response = "305.2"
    result = runner.invoke(
        app,
        [
            "--input-value",
            "32",
            "--from-unit",
            "Celsius",
            "--to-unit",
            "Kelvin",
            "--student-response",
            "305.2",
        ],
    )
    assert result.exit_code == 0
    assert "Result:" in result.output


def test_get_version(mocker):
    version_content = "1.0.0"

    # Create a mocker fixture to mock the open function
    mock_open = mocker.patch(
        "builtins.open", mocker.mock_open(read_data=version_content)
    )

    # Call the get_version function
    version = get_version()

    # Assert that the returned version matches the expected version_content
    assert version == version_content


def test_version_callback(mocker, capsys):
    value = True

    mocked_get_version = mocker.patch(
        "unit_conversion_grader.cli.get_version", return_value="1.0.0"
    )
    # Call the version_callback function with the mocked get_version
    version_callback(value)

    # Capture the output using capsys
    captured = capsys.readouterr()
    output = captured.out.strip()

    # Assert the output
    assert output == f"{app_name} version 1.0.0"
