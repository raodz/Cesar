import string
import json
import pandas as pd
from datetime import datetime

SIGNS = string.ascii_letters + string.digits


class Cypher:
    @staticmethod
    def cesar(
        original_txt: str,
        shift: int,
        history: pd.DataFrame,
        encrypting_mode: bool = True,
    ) -> str:

        mode = 1 if encrypting_mode else -1
        mode_name = "encrypting" if encrypting_mode else "decrypting"

        shifted_txt = ""
        for sign in original_txt:
            if sign in SIGNS:
                try:
                    shifted_sign = SIGNS[SIGNS.index(sign) + shift * mode]
                except IndexError:
                    shifted_sign = SIGNS[
                        SIGNS.index(sign) + (shift - len(SIGNS)) * mode
                    ]
            else:
                shifted_sign = sign
            shifted_txt += shifted_sign
        new_history_record = [
            original_txt,
            shift,
            mode_name,
            shifted_txt,
            datetime.now(),
        ]
        history.loc[len(history)] = new_history_record

        return shifted_txt

    @staticmethod
    def crypt_from_json(
        file_path: str, history: pd.DataFrame, encrypting_mode: bool = True
    ):
        try:
            with open(file_path) as file:
                data_to_crypt = json.load(file)
                for data in data_to_crypt:
                    txt, shift = data.get("txt", "NO DATA"), data.get("shift", 0)
                    shifted_data = Cypher.cesar(
                        txt, shift, history, encrypting_mode=encrypting_mode
                    )
                    print(f"{txt} shifted by {shift}: " f"{shifted_data}")
        except json.decoder.JSONDecodeError:
            print("Incorrect file - the file has to be .json with correct content")
