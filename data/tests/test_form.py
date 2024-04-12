from unittest.mock import patch
import pytest
import data.form as form

def test_get_form():
    form_data = form.get_form()
    assert isinstance(form_data, list)
    assert len(form_data) > 0
    for field in form_data:
        assert form.FLD_NM in field
        assert isinstance(field[form.FLD_NM], str)
        assert len(field[form.FLD_NM]) > 0


def test_get_form_descr():
    form_descr = form.get_form_descr()
    assert isinstance(form_descr, dict)
    assert len(form_descr) > 0
    for key, value in form_descr.items():
        assert form.FLD_NM in value
        assert isinstance(value[form.FLD_NM], str)
        assert len(value[form.FLD_NM]) > 0


def test_get_fld_names():
    field_names = form.get_fld_names()
    assert isinstance(field_names, list)
    assert len(field_names) > 0
    for name in field_names:
        assert isinstance(name, str)
        assert len(name) > 0



@pytest.mark.parametrize("user_input", ["test_input"])  # Use parametrize to test with different input values
def test_get_input(monkeypatch, user_input):
    # Mock the input function to return the predefined user input
    monkeypatch.setattr('builtins.input', lambda _: user_input)

    # Define the parameters for the get_input function
    dflt = "Default: "
    opt = "(Optional) "
    qstn = "Enter your input: "

    # Call the get_input function
    result = form.get_input(dflt, opt, qstn)

    # Assert that the result matches the predefined user input
    assert result == user_input