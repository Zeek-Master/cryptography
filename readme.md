# Transposition Cipher Tool

This project is a simple Transposition Cipher Tool built with Python and Tkinter. It provides a graphical user interface (GUI) to encrypt and decrypt text using a columnar transposition cipher. The application also supports input from both text and files, and it includes functionality to save the processed (encrypted or decrypted) output.

## Modules Used

- **tkinter**: Used to create the GUI interface.
- **tkinter.ttk**: Provides themed widgets such as buttons, labels, frames, etc.
- **tkinter.filedialog**: Allows file selection dialogs (for opening and saving files).
- **tkinter.messagebox**: Displays error and status messages in pop-up windows.
- **tkinter.scrolledtext**: Provides a multi-line text widget with scrollbars.
- **math**: Used to perform mathematical operations (e.g., calculating rows).
- **os**: Used to interact with the operating system for file and directory operations.
- **datetime**: Used within the save functionality to generate unique timestamps for file names.

## Classes and Functions

### `TranspositionCipher` Class

This class contains the core logic for the transposition cipher.

- **`generate_key_order(cipher_key)`**  
  - **Description:**  
    Generates the key order required for the columnar transposition based on the provided cipher key.  
  - **Process:**  
    - Removes duplicate characters while preserving order.
    - Converts characters to uppercase and considers only alphabetic characters.
    - Sorts the unique key alphabetically to determine the column order.
  - **Parameters:**  
    - `cipher_key` (str): The user-provided cipher key.
  - **Returns:**  
    - A tuple `(unique_key, key_order)` where `unique_key` is the processed key and `key_order` is a list indicating the order of columns.

- **`encrypt(message, cipher_key)`**  
  - **Description:**  
    Encrypts a plain text message using the transposition cipher.
  - **Process:**  
    - Generates the key order.
    - Removes spaces and converts the text to uppercase.
    - Pads the message with 'X' so that it fits into a grid.
    - Reads the grid column-by-column choosing columns based on the sorted key order.
  - **Parameters:**  
    - `message` (str): The plain text message.
    - `cipher_key` (str): The cipher key.
  - **Returns:**  
    - The encrypted cipher text (str).

- **`decrypt(cipher_text, cipher_key)`**  
  - **Description:**  
    Decrypts text that was encrypted using the transposition cipher.
  - **Process:**  
    - Generates the key order.
    - Determines the size of the grid and how many characters fit in each column.
    - Fills the grid column-by-column in the correct order.
    - Reads the grid row-by-row to recover the original message.
    - Removes any 'X' padding added during encryption.
  - **Parameters:**  
    - `cipher_text` (str): The encrypted message.
    - `cipher_key` (str): The cipher key.
  - **Returns:**  
    - The decrypted plain text message (str).

### `TranspositionGUI` Class

This class builds and manages the graphical user interface and handles user interactions.

- **`__init__(self, root)`**  
  - **Description:**  
    Initializes the GUI window and components.
  - **Key Actions:**  
    - Sets the window title, fixed size, and centers it on the screen.
    - Initializes current operation mode (encrypt/decrypt).
    - Calls `setup_gui()` to build all GUI elements.

- **`center_window(self)`**  
  - **Description:**  
    Centers the main window on the user’s screen.

- **`setup_gui(self)`**  
  - **Description:**  
    Constructs the entire layout of the application:
    - Title bar and mode toggle buttons.
    - Configuration area for cipher key entry and input method selection.
    - Input section that supports both text and file input.
    - Output area with a save button.
    - Status area to display messages.
  - **Widgets:**  
    - `ttk.Frame`, `ttk.Label`, `ttk.Button`, `ttk.Entry`, `ttk.Radiobutton`, and `scrolledtext.ScrolledText`.

- **`update_key_hint(self, *args)`**  
  - **Description:**  
    Processes the cipher key as soon as it is updated, now displaying the processed key and column order as a hint to the user.

- **`set_mode(self, mode)`**  
  - **Description:**  
    Switches between encryption and decryption modes.
  - **Process:**  
    - Updates the state variable and changes the label of the action button.
    - Clears the output area upon mode change.

- **`toggle_input_method(self)`**  
  - **Description:**  
    Toggles the input section between text input and file input based on user selection.
  - **Widgets Affected:**  
    - Controls the display of text field vs. file selection controls.

- **`browse_file(self)`**  
  - **Description:**  
    Opens a dialog for the user to select a text file to be used as the input.

- **`get_input_text(self)`**  
  - **Description:**  
    Retrieves the text from the appropriate source (either a direct text input or file content).
  - **Process:**  
    - If the file input method is selected, it reads the contents from the chosen file.
    - Otherwise, it gets the text entered in the text widget.

- **`validate_key(self)`**  
  - **Description:**  
    Validates the cipher key entered by the user.
  - **Process:**  
    - Ensures the key is not empty and contains at least 2 unique letters by invoking `generate_key_order`.
  - **Returns:**  
    - The validated key if correct; otherwise, displays an error message.

- **`process_text(self)`**  
  - **Description:**  
    Main function that processes the text based on the current operation mode (encryption or decryption).
  - **Process:**  
    - Retrieves input text and the validated key.
    - Depending on the mode, it calls `encrypt` or `decrypt` from the `TranspositionCipher` class.
    - Displays the result in the output area and shows a corresponding status message.

- **`show_status_message(self, message, msg_type="info")`**  
  - **Description:**  
    Displays a temporary status message to the user.
  - **Features:**  
    - Utilizes color coding and icons to differentiate between success, error, and informational messages.
    - The message auto-dismisses after a few seconds.

- **`save_output(self)`**  
  - **Description:**  
    Saves the processed text (encrypted/decrypted output) to a file.
  - **Process:**  
    - Retrieves the output text.
    - Opens a save file dialog for the user to choose the location.
    - Writes the output text to the file with proper error handling for encoding, permission issues, or OS errors.
    - Displays a message indicating success or failure.

### Main Function

- **`main()`**  
  - **Description:**  
    Entry point for the application. Creates the main Tkinter window and initializes the `TranspositionGUI`.
  - **Usage:**  
    - The function is executed if the module is run as the main program.

## Usage

1. **Start the Application:**  
   Run the script using Python:
   ```sh
   python "Transposition Cryptography.py"

2. **Provide a Cipher Key:**    
    Enter a cipher key (minimum 2 unique letters).
    A hint will show the processed key and the derived column order.

3. **Choose Input Method:**
    Select between typing text directly or choosing a file.
    For file input, use the "Browse" button to select your file.

4. **Encrypt or Decrypt:**
    Use the mode toggle buttons to switch between encryption and decryption.
    Click the action button ("🔒 ENCRYPT TEXT" or "🔓 DECRYPT TEXT") to process the input.

5. **Save the Output:**
    Once processed, view the result in the output area.
    Use the "💾 Save" button to save the output to a text file.


## Summary
    This tool leverages a transposition cipher technique to securely encrypt and decrypt messages. The  code is structured with object-oriented design by separating the transformation logic    (TranspositionCipher) from the user interface logic (TranspositionGUI). The use of Tkinter and its     themed widgets ensures a clean and user-friendly experience.

    Happy encrypting and decrypting! ```