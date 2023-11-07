from pyrecipes import utils


def test_clean_text():
    text = "01_this_is_a_test"
    assert utils.clean_text(text) == " 1) This is a test"


def test_extract_leading_number():
    text = "02_this_is_another_test"
    assert utils.extract_leading_numbers(text) == 2


def test_assert_text_border():
    text = "testing"
    assert utils.text_border(text) == "===========\n= testing =\n==========="
    assert (
        utils.text_border(text, symbol="+", side_symbol="|", padding=3)
        == "+++++++++++++++\n|   testing   |\n+++++++++++++++"
    )
