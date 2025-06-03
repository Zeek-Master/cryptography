import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import math
import os

class TranspositionCipher:
    @staticmethod
    def generate_key_order(cipher_key):
        """Generate column order based on alphabetical sorting of cipher key"""
        # Remove duplicates while preserving order, convert to uppercase
        seen = set()
        unique_key = ''.join(char.upper() for char in cipher_key if char.upper() not in seen and not seen.add(char.upper()) and char.isalpha())
        
        if len(unique_key) < 2:
            raise ValueError("Cipher key must contain at least 2 unique letters")
        
        # Create list of (character, original_index) pairs
        char_index_pairs = [(char, i) for i, char in enumerate(unique_key)]
        
        # Sort by character to get alphabetical order
        sorted_pairs = sorted(char_index_pairs, key=lambda x: x[0])
        
        # Extract the order (which original positions come in alphabetical order)
        key_order = [pair[1] for pair in sorted_pairs]
        
        return unique_key, key_order
    
    @staticmethod
    def encrypt(message, cipher_key):
        """Encrypt message using transposition cipher with given cipher key"""
        # Generate key order from cipher key
        unique_key, key_order = TranspositionCipher.generate_key_order(cipher_key)
        cols = len(unique_key)
        
        # Remove spaces and convert to uppercase for consistency
        message = message.replace(' ', '').upper()
        
        # Calculate number of rows
        rows = math.ceil(len(message) / cols)
        
        # Pad message with 'X' if necessary
        padded_message = message.ljust(rows * cols, 'X')
        
        # Create grid and fill it row by row
        grid = []
        for i in range(rows):
            row = []
            for j in range(cols):
                idx = i * cols + j
                row.append(padded_message[idx])
            grid.append(row)
        
        # Read columns in the order specified by key_order
        cipher_text = ''
        for col_index in key_order:
            for row in range(rows):
                cipher_text += grid[row][col_index]
        
        return cipher_text
    
    @staticmethod
    def decrypt(cipher_text, cipher_key):
        """Decrypt cipher text using transposition cipher with given cipher key"""
        # Generate key order from cipher key
        unique_key, key_order = TranspositionCipher.generate_key_order(cipher_key)
        cols = len(unique_key)
        rows = math.ceil(len(cipher_text) / cols)
        
        # Calculate how many characters should be in each column
        total_chars = len(cipher_text)
        chars_per_col = total_chars // cols
        extra_chars = total_chars % cols
        
        # Create empty grid
        grid = [['' for _ in range(cols)] for _ in range(rows)]
        
        # Fill grid column by column in key order
        char_index = 0
        for col_index in key_order:
            # Determine how many characters this column should have
            col_length = chars_per_col + (1 if col_index < extra_chars else 0)
            
            for row in range(col_length):
                if char_index < len(cipher_text):
                    grid[row][col_index] = cipher_text[char_index]
                    char_index += 1
        
        # Read grid row by row to get original message
        decrypted = ''
        for row in range(rows):
            for col in range(cols):
                if grid[row][col] != '':
                    decrypted += grid[row][col]
        
        # Remove padding 'X' from the end
        return decrypted.rstrip('X')

class TranspositionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Transposition Cipher Tool")
        
        # Make window fixed size and non-resizable
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        
        # Center the window on screen
        self.center_window()
        
        # Current operation mode
        self.current_mode = tk.StringVar(value="encrypt")
        
        self.setup_gui()
    
    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        width = 800
        height = 600
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def setup_gui(self):
        # Remove scrollable canvas - use direct frame approach for fixed layout
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill='both', expand=True)
        
        # Title section - more compact
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill='x', pady=(0, 15))
        
        title_label = ttk.Label(title_frame, text="🔐 Transposition Cipher Tool", 
                               font=('Arial', 16, 'bold'), foreground='#2c3e50')
        title_label.pack(side='left')
        
        # Mode toggle buttons
        mode_frame = ttk.Frame(title_frame)
        mode_frame.pack(side='right')
        
        self.encrypt_btn = ttk.Button(mode_frame, text="ENCRYPT", 
                                     command=lambda: self.set_mode("encrypt"))
        self.encrypt_btn.pack(side='left', padx=(0, 5))
        
        self.decrypt_btn = ttk.Button(mode_frame, text="DECRYPT", 
                                     command=lambda: self.set_mode("decrypt"))
        self.decrypt_btn.pack(side='left')
        
        # Configuration section - more compact
        config_frame = ttk.LabelFrame(main_frame, text="Configuration", padding="10")
        config_frame.pack(fill='x', pady=(0, 10))
        
        # Key input - horizontal layout
        key_frame = ttk.Frame(config_frame)
        key_frame.pack(fill='x', pady=(0, 8))
        
        ttk.Label(key_frame, text="Cipher Key:", font=('Arial', 9, 'bold')).pack(side='left')
        self.key_var = tk.StringVar(value="SECRET")
        key_entry = ttk.Entry(key_frame, textvariable=self.key_var, width=20, font=('Arial', 10))
        key_entry.pack(side='left', padx=(10, 0))
        
        # Key hint - compact
        self.key_hint = ttk.Label(config_frame, text="", font=('Arial', 8), foreground='#666666')
        self.key_hint.pack(anchor='w')
        
        # Input method selection - horizontal
        method_frame = ttk.Frame(config_frame)
        method_frame.pack(fill='x', pady=(5, 0))
        
        ttk.Label(method_frame, text="Input:", font=('Arial', 9, 'bold')).pack(side='left')
        self.input_method = tk.StringVar(value="text")
        
        ttk.Radiobutton(method_frame, text="Text", variable=self.input_method, 
                       value="text", command=self.toggle_input_method).pack(side='left', padx=(10, 0))
        ttk.Radiobutton(method_frame, text="File", variable=self.input_method, 
                       value="file", command=self.toggle_input_method).pack(side='left', padx=(10, 0))
        
        # Input section - reduced height
        input_frame = ttk.LabelFrame(main_frame, text="Input", padding="10")
        input_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        # File selection frame
        self.file_frame = ttk.Frame(input_frame)
        
        file_row = ttk.Frame(self.file_frame)
        file_row.pack(fill='x')
        
        ttk.Label(file_row, text="File:", font=('Arial', 9, 'bold')).pack(side='left')
        
        self.file_path_var = tk.StringVar()
        file_entry = ttk.Entry(file_row, textvariable=self.file_path_var, 
                              state='readonly', font=('Arial', 9))
        file_entry.pack(side='left', fill='x', expand=True, padx=(5, 5))
        
        ttk.Button(file_row, text="Browse", command=self.browse_file).pack(side='right')
        
        # Text input frame
        self.text_frame = ttk.Frame(input_frame)
        
        self.input_text = scrolledtext.ScrolledText(self.text_frame, height=6, wrap=tk.WORD,
                                                   font=('Consolas', 10))
        self.input_text.pack(fill='both', expand=True)
        
        # Action button
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(pady=5)
        
        self.action_btn = ttk.Button(action_frame, text="🔒 ENCRYPT TEXT", 
                                    command=self.process_text)
        self.action_btn.pack()
        
        # Output section - reduced height
        output_frame = ttk.LabelFrame(main_frame, text="Output", padding="10")
        output_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        # Output header with save button
        output_header = ttk.Frame(output_frame)
        output_header.pack(fill='x', pady=(0, 5))
        
        ttk.Label(output_header, text="Result:", font=('Arial', 9, 'bold')).pack(side='left')
        ttk.Button(output_header, text="💾 Save", command=self.save_output).pack(side='right')
        
        self.output_text = scrolledtext.ScrolledText(output_frame, height=6, wrap=tk.WORD,
                                                    font=('Consolas', 10))
        self.output_text.pack(fill='both', expand=True)
        
        # Status frame - compact
        self.status_frame = ttk.Frame(main_frame)
        self.status_frame.pack(fill='x', pady=(5, 0))
        
        # Bind key change event
        self.key_var.trace('w', self.update_key_hint)
        
        # Initialize
        self.set_mode("encrypt")
        self.toggle_input_method()
        self.update_key_hint()
        
    def update_key_hint(self, *args):
        """Update the key order hint when key changes"""
        try:
            cipher_key = self.key_var.get()
            if cipher_key:
                unique_key, key_order = TranspositionCipher.generate_key_order(cipher_key)
                hint_text = f"Processed key: {unique_key} → Column order: {[i+1 for i in key_order]}"
                self.key_hint.configure(text=hint_text)
            else:
                self.key_hint.configure(text="")
        except Exception:
            self.key_hint.configure(text="⚠️ Invalid key - use at least 2 unique letters")
        
    def set_mode(self, mode):
        """Set the current operation mode"""
        self.current_mode.set(mode)
        
        # Update button appearance
        if mode == "encrypt":
            self.encrypt_btn.configure(style='Accent.TButton')
            self.decrypt_btn.configure(style='TButton')
            self.action_btn.configure(text="🔒 ENCRYPT TEXT")
        else:
            self.encrypt_btn.configure(style='TButton')
            self.decrypt_btn.configure(style='Accent.TButton')
            self.action_btn.configure(text="🔓 DECRYPT TEXT")
        
        # Clear output when switching modes
        self.output_text.delete("1.0", tk.END)
        
    def toggle_input_method(self):
        """Toggle between text and file input methods"""
        # Hide both frames first
        self.file_frame.pack_forget()
        self.text_frame.pack_forget()
        
        # Show the selected frame
        if self.input_method.get() == "file":
            self.file_frame.pack(fill='x', pady=(5, 0))
        else:
            self.text_frame.pack(fill='both', expand=True, pady=(5, 0))
    
    def browse_file(self):
        """Open file dialog to select input file"""
        file_path = filedialog.askopenfilename(
            title="Select file to process",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            self.file_path_var.set(file_path)
    
    def get_input_text(self):
        """Get input text from either text widget or file"""
        if self.input_method.get() == "file":
            file_path = self.file_path_var.get()
            if not file_path:
                messagebox.showerror("Error", "Please select a file")
                return None
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except Exception as e:
                messagebox.showerror("Error", f"Error reading file: {str(e)}")
                return None
        else:
            text = self.input_text.get("1.0", tk.END).strip()
            if not text:
                messagebox.showerror("Error", "Please enter some text")
                return None
            return text
    
    def validate_key(self):
        """Validate the cipher key"""
        try:
            cipher_key = self.key_var.get().strip()
            if not cipher_key:
                messagebox.showerror("Error", "Please enter a cipher key")
                return None
            
            # Test if key is valid by trying to generate key order
            unique_key, key_order = TranspositionCipher.generate_key_order(cipher_key)
            return cipher_key
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return None
        except Exception as e:
            messagebox.showerror("Error", f"Invalid cipher key: {str(e)}")
            return None
    
    def process_text(self):
        """Process text based on current mode"""
        text = self.get_input_text()
        key = self.validate_key()
        
        if text is None or key is None:
            return
        
        try:
            cipher = TranspositionCipher()
            
            if self.current_mode.get() == "encrypt":
                result = cipher.encrypt(text, key)
                success_msg = "Text encrypted successfully!"
            else:
                result = cipher.decrypt(text, key)
                success_msg = "Text decrypted successfully!"
            
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", result)
            
            # Show success message
            self.show_status_message(success_msg, "success")
            
        except Exception as e:
            messagebox.showerror("Error", f"Operation failed: {str(e)}")
    
    def show_status_message(self, message, msg_type="info"):
        """Show status message"""
        # Clear existing status messages
        for widget in self.status_frame.winfo_children():
            widget.destroy()
        
        # Choose color based on message type
        if msg_type == "success":
            bg_color = '#d4edda'
            fg_color = '#155724'
            icon = "✅"
        elif msg_type == "error":
            bg_color = '#f8d7da'
            fg_color = '#721c24'
            icon = "❌"
        else:
            bg_color = '#d1ecf1'
            fg_color = '#0c5460'
            icon = "ℹ️"
        
        # Create status message
        status_label = tk.Label(self.status_frame, text=f"{icon} {message}", 
                               font=('Arial', 10, 'bold'), 
                               bg=bg_color, fg=fg_color, 
                               padx=15, pady=8, relief='solid', borderwidth=1)
        status_label.pack(fill='x')
        
        # Remove after 3 seconds
        self.root.after(3000, lambda: status_label.destroy())
    
    def save_output(self):
        """Save output text to file - FIXED VERSION"""
        try:
            # Get output text and strip only trailing whitespace to preserve formatting
            output = self.output_text.get("1.0", tk.END)
            # Remove the automatic newline that tkinter adds at the end
            if output.endswith('\n'):
                output = output[:-1]
                
            if not output or output.strip() == "":
                messagebox.showerror("Error", "No output to save")
                return
            
            # Suggest filename based on mode and current timestamp
            import datetime
            mode = self.current_mode.get()
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Open save dialog - FIXED: Removed problematic parameters
            file_path = filedialog.asksaveasfilename(
                title="Save output file",
                defaultextension=".txt",
                filetypes=[
                    ("Text files", "*.txt"),
                    ("All files", "*.*")
                ]
            )
            
            # Check if user cancelled the dialog
            if not file_path:
                return
            
            # Ensure the directory exists
            directory = os.path.dirname(file_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
            
            # Write file with explicit encoding and error handling
            with open(file_path, 'w', encoding='utf-8', newline='') as f:
                f.write(output)
            
            # Verify the file was created and has content
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                self.show_status_message(f"File saved successfully to: {os.path.basename(file_path)}", "success")
            else:
                raise Exception("File was created but appears to be empty")
                
        except PermissionError:
            error_msg = "Permission denied. Please choose a different location or run as administrator."
            messagebox.showerror("Permission Error", error_msg)
            self.show_status_message("Save failed: Permission denied", "error")
            
        except FileNotFoundError:
            error_msg = "The specified path was not found. Please check the file path."
            messagebox.showerror("Path Error", error_msg)
            self.show_status_message("Save failed: Path not found", "error")
            
        except OSError as e:
            error_msg = f"Operating system error: {str(e)}"
            messagebox.showerror("OS Error", error_msg)
            self.show_status_message(f"Save failed: {str(e)}", "error")
            
        except UnicodeEncodeError as e:
            error_msg = f"Text encoding error: {str(e)}"
            messagebox.showerror("Encoding Error", error_msg)
            self.show_status_message("Save failed: Text encoding error", "error")
            
        except Exception as e:
            error_msg = f"Unexpected error while saving: {str(e)}"
            messagebox.showerror("Save Error", error_msg)
            self.show_status_message(f"Save failed: {str(e)}", "error")

def main():
    root = tk.Tk()
    app = TranspositionGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
