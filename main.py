import os
import time
import pandas as pd
from operations.cesar import Cypher
from operations.db_functions import db_to_df, df_to_db


class Facade:
    def __init__(self):
        self.__is_running = True
        self.choices = {
            "1": self._single_encrypt,
            "2": self._single_decrypt,
            "3": self._multiple_encrypt,
            "4": self._multiple_decrypt,
            "5": self._show_history,
            "6": self._end_program,
        }
        self.__history_col_names = [
            "txt",
            "shift",
            "direction",
            "shifted_txt",
            "time_of_crypting",
        ]
        self.__no_history_path = True

        while self.__no_history_path:
            self._history_file = input(
                "Welcome to Cesar 1.0!\n"
                "Provide a path to the history file or press "
                "ENTER to create a new history"
            )
            if os.path.isfile(self._history_file) or self._history_file == "":
                self.__no_history_path = False

        if self._history_file == "":
            self.history = pd.DataFrame(columns=self.__history_col_names)
        else:
            self.history = db_to_df(self._history_file)

        self._loop()

    def _loop(self):
        while self.__is_running:
            self._show_menu()
            self._get_and_execute_choice()

    def _show_menu(self):
        menu = (
            "MENU\n"
            "1. Encrypt single text\n"
            "2. Decrypt single text\n"
            "3. Encrypt many texts from .json file\n"
            "4. Decrypt many texts from .json file\n"
            "5. Show history\n"
            "6. Exit\n"
        )
        print(menu)

    def _get_and_execute_choice(self):
        user_choice = input("Choose a mode")

        self.choices.get(user_choice, self._show_error)()

    def _show_error(self):
        print("Incorrect choice - Try again!")

    def _single_encrypt(self):
        original_txt = input("Provide the text to encrypt")
        shift = int(input("Provide the shift of the encryption"))
        shifted_txt = Cypher.cesar(original_txt, shift, self.history)
        print(f"{original_txt} shifted by {shift}: {shifted_txt}")

    def _single_decrypt(self):
        original_txt = input("Provide the text to decrypt")
        shift = int(input("Provide the shift of the decryption"))
        shifted_txt = Cypher.cesar(
            original_txt, shift, self.history, encrypting_mode=False
        )
        print(f"{original_txt} shifted back by {shift}: {shifted_txt}")

    def _multiple_encrypt(self):
        file_path = input("Provide the file path")
        Cypher.crypt_from_json(file_path, self.history)

    def _multiple_decrypt(self):
        file_path = input("Provide the file path")
        Cypher.crypt_from_json(file_path, self.history, encrypting_mode=False)

    def _show_history(self):
        print(self.history)

    def _end_program(self):
        self._save = ""
        while self._save not in ("Y", "n"):
            self._save = input(
                "Do you want to save the operations history as a " "database? (Y/n)"
            )
            if self._save == "Y":
                if not os.path.exists("dbs"):
                    os.mkdir("dbs")
                db_name = f"dbs//history{int(time.time())}.db"
                df_to_db(self.history, db_name)
                print(f"History saved in the {db_name} file")
        print("Thank you for using Cesar 1.0!")
        self.__is_running = False


def main():
    Facade()


if __name__ == "__main__":
    main()
