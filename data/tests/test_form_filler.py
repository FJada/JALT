from unittest.mock import patch
import data.form_filler as ff


def test_get_fld_names():
    ret = ff.get_fld_names(ff.TEST_FLD_DESCRIPS)
    assert isinstance(ret, list)
    assert ff.TEST_FLD in ret


def test_get_form_descr():
    ret = ff.get_form_descr(ff.TEST_FLD_DESCRIPS)
    assert isinstance(ret, dict)
    assert ff.TEST_FLD in ret


def test_get_query_fld_names():
    fld_descrips = ff.TEST_FLD_DESCRIPS
    query_field_names = ff.get_query_fld_names(fld_descrips)
    assert isinstance(query_field_names, list)
    assert len(query_field_names) == 1  # One query field name expected
    assert 'test field' in query_field_names
    

def test_get_input(monkeypatch):
    user_input = "test input"
    monkeypatch.setattr('builtins.input', lambda _: user_input)

    dflt = "Default: "
    opt = "(Optional) "
    qstn = "Enter your input: "

    result = ff.get_input(dflt, opt, qstn)
    assert result == user_input
    

@patch('data.form_filler.get_input', return_value='Y')
def test_form(mock_get_input):
    assert isinstance(ff.form(ff.TEST_FLD_DESCRIPS), dict)