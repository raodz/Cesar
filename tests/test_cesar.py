import pytest
import pandas as pd
import sys
from io import StringIO
from operations.cesar import Cypher

HISTORY_COL_NAMES = ["txt", "shift", "direction", "shifted_txt", "time_of_crypting"]
EMPTY_HISTORY_DF = pd.DataFrame(columns=HISTORY_COL_NAMES)


@pytest.mark.parametrize(
    "text, shift, expected_enscryption",
    [
        ("Ala ma kota", 2, "Cnc oc mqvc"),
        ("Zalety i przywary", 4, "3epixC m tvDCAevC"),
        ("Zima 1999", 1, "0jnb 2aaa"),
        ("Idę na 100%!", 3, "Lgę qd 433%!"),
        ("Żółć", 14, "Żółć"),
        (" ", 5, " "),
        ("ღ", 7, "ღ"),
    ],
)
def test_should_return_enscrypted_text(text, shift, expected_enscryption):
    actual_enscryption = Cypher.cesar(text, shift, EMPTY_HISTORY_DF)
    assert actual_enscryption == expected_enscryption


@pytest.mark.parametrize(
    "text, shift, expected_enscryption",
    [
        ("Cnc oc mqvc", 2, "Ala ma kota"),
        ("3epixC m tvDCAevC", 4, "Zalety i przywary"),
        ("0jnb 2aaa", 1, "Zima 1999"),
        ("Lgę qd 433%!", 3, "Idę na 100%!"),
        ("Żółć", 14, "Żółć"),
        (" ", 5, " "),
        ("ღ", 7, "ღ"),
    ],
)
def test_should_return_descrypted_text(text, shift, expected_enscryption):
    actual_enscryption = Cypher.cesar(text, shift, EMPTY_HISTORY_DF, False)
    assert actual_enscryption == expected_enscryption


def test_should_return_blank_str_as_encryption_of_blank_str():
    actual_enscryption = Cypher.cesar("", 5, EMPTY_HISTORY_DF)
    assert actual_enscryption == ""


def test_should_return_blank_str_as_decryption_of_blank_str():
    actual_enscryption = Cypher.cesar("", 5, EMPTY_HISTORY_DF, False)
    assert actual_enscryption == ""


def test_should_return_encryptions_for_texts_in_json_file():
    captured_output = StringIO()
    sys.stdout = captured_output
    Cypher.crypt_from_json("json_data.json", EMPTY_HISTORY_DF)
    sys.stdout = sys.__stdout__
    assert captured_output.getvalue() == (
        "abcdeffght shifted by 2: cdefghhijv\n"
        "wrgaw shifted by 3: zujdz\n"
        "sdgsdagsafgh shifted by 5: xilxiflxfklm\n"
    )


def test_should_return_no_data_message_for_wrong_json_data():
    captured_output = StringIO()
    sys.stdout = captured_output
    Cypher.crypt_from_json("wrong_json_data.json", EMPTY_HISTORY_DF)
    sys.stdout = sys.__stdout__
    assert captured_output.getvalue() == "NO DATA shifted by 0: NO DATA\n"


def test_should_return_no_data_message_for_empty_json_data():
    captured_output = StringIO()
    sys.stdout = captured_output
    Cypher.crypt_from_json("empty_json_file.json", EMPTY_HISTORY_DF)
    sys.stdout = sys.__stdout__
    assert captured_output.getvalue() == (
        "Incorrect file - the file has to be .json " "with correct content\n"
    )


def test_should_return_incorrect_file_message_for_incorrect_file():
    captured_output = StringIO()
    sys.stdout = captured_output
    Cypher.crypt_from_json("not_json_data.notjson", EMPTY_HISTORY_DF)
    sys.stdout = sys.__stdout__
    assert captured_output.getvalue() == (
        "Incorrect file - the file has to be .json " "with correct content\n"
    )
