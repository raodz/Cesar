# Cesar 1.0

Cesar 1.0 is a Python program used to encrypt and decrypt texts with the Caesar cipher. It has the ability to save the history of operations in the form of a database.

## Installation

The program can be installed directly by pulling this repository.

## Usage

After executing the ```main.py``` file Cesar 1.0 asks the user if they want to load an existing database with a history of operations. Otherwise a new history table is being created.

Next the menu is being shown. There are six options:<br>
	    1. Encrypt single text<br>
            2. Decrypt single text<br>
            3. Encrypt many texts from .json file<br>
            4. Decrypt many texts from .json file<br>
            5. Show history<br>
	    6. Exit program

Options 1. and 2. lead to request for a text and a number of sign shift.<br>
Options 3. and 4. lead to request for a path to the .json file containing the information above.<br>
Option 5. allows to see records of all the operations including those from loaded history file.<br>
Option 6. lead to the question about saving the history and then the program is stopped.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
