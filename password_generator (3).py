import tkinter as tk
from tkinter import ttk, messagebox
import secrets
import string
import pyperclip


class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Random Password Generator")
        self.root.geometry("720x720")
        self.root.resizable(False, False)
        self.root.configure(bg="#101820")

        self.history = []

        self.length_var = tk.IntVar(value=16)
        self.upper_var = tk.BooleanVar(value=True)
        self.lower_var = tk.BooleanVar(value=True)
        self.number_var = tk.BooleanVar(value=True)
        self.symbol_var = tk.BooleanVar(value=True)
        self.ambiguous_var = tk.BooleanVar(value=False)

        self.build_interface()

    def build_interface(self):
        title = tk.Label(
            self.root,
            text="SECURE PASSWORD GENERATOR",
            font=("Segoe UI", 22, "bold"),
            bg="#101820",
            fg="#00D4FF"
        )
        title.pack(pady=(25, 5))

        subtitle = tk.Label(
            self.root,
            text="Generate strong and cryptographically secure passwords",
            font=("Segoe UI", 10),
            bg="#101820",
            fg="#B8C4CE"
        )
        subtitle.pack(pady=(0, 20))

        main_frame = tk.Frame(
            self.root,
            bg="#182530",
            padx=25,
            pady=20
        )
        main_frame.pack(padx=30, fill="both", expand=True)

        length_label = tk.Label(
            main_frame,
            text="Password Length",
            font=("Segoe UI", 11, "bold"),
            bg="#182530",
            fg="white"
        )
        length_label.pack(anchor="w")

        length_frame = tk.Frame(main_frame, bg="#182530")
        length_frame.pack(fill="x", pady=(5, 20))

        self.length_scale = tk.Scale(
            length_frame,
            from_=8,
            to=64,
            orient="horizontal",
            variable=self.length_var,
            bg="#182530",
            fg="white",
            troughcolor="#334653",
            highlightthickness=0,
            activebackground="#00D4FF",
            font=("Segoe UI", 9)
        )
        self.length_scale.pack(side="left", fill="x", expand=True)

        self.length_value = tk.Label(
            length_frame,
            text="16",
            font=("Segoe UI", 12, "bold"),
            bg="#182530",
            fg="#00D4FF",
            width=4
        )
        self.length_value.pack(side="right")

        self.length_scale.config(command=self.update_length)

        types_label = tk.Label(
            main_frame,
            text="Character Types",
            font=("Segoe UI", 11, "bold"),
            bg="#182530",
            fg="white"
        )
        types_label.pack(anchor="w", pady=(0, 8))

        options_frame = tk.Frame(main_frame, bg="#182530")
        options_frame.pack(fill="x")

        self.create_checkbox(
            options_frame,
            "Uppercase (A-Z)",
            self.upper_var,
            0,
            0
        )

        self.create_checkbox(
            options_frame,
            "Lowercase (a-z)",
            self.lower_var,
            0,
            1
        )

        self.create_checkbox(
            options_frame,
            "Numbers (0-9)",
            self.number_var,
            1,
            0
        )

        self.create_checkbox(
            options_frame,
            "Symbols (!@#$)",
            self.symbol_var,
            1,
            1
        )

        self.create_checkbox(
            options_frame,
            "Exclude Ambiguous Characters",
            self.ambiguous_var,
            2,
            0
        )

        password_label = tk.Label(
            main_frame,
            text="Generated Password",
            font=("Segoe UI", 11, "bold"),
            bg="#182530",
            fg="white"
        )
        password_label.pack(anchor="w", pady=(20, 8))

        password_frame = tk.Frame(
            main_frame,
            bg="#0B1116",
            padx=10,
            pady=10
        )
        password_frame.pack(fill="x")

        self.password_entry = tk.Entry(
            password_frame,
            font=("Consolas", 15, "bold"),
            bg="#0B1116",
            fg="#00FFB3",
            insertbackground="white",
            relief="flat",
            justify="center"
        )
        self.password_entry.pack(fill="x")

        button_frame = tk.Frame(main_frame, bg="#182530")
        button_frame.pack(pady=15)

        self.generate_button = tk.Button(
            button_frame,
            text="GENERATE PASSWORD",
            command=self.generate_password,
            font=("Segoe UI", 10, "bold"),
            bg="#00A8CC",
            fg="white",
            activebackground="#007C99",
            activeforeground="white",
            relief="flat",
            padx=18,
            pady=10,
            cursor="hand2"
        )
        self.generate_button.pack(side="left", padx=5)

        self.copy_button = tk.Button(
            button_frame,
            text="COPY TO CLIPBOARD",
            command=self.copy_password,
            font=("Segoe UI", 10, "bold"),
            bg="#334653",
            fg="white",
            activebackground="#425B6B",
            relief="flat",
            padx=18,
            pady=10,
            cursor="hand2"
        )
        self.copy_button.pack(side="left", padx=5)

        strength_label = tk.Label(
            main_frame,
            text="Password Strength",
            font=("Segoe UI", 11, "bold"),
            bg="#182530",
            fg="white"
        )
        strength_label.pack(anchor="w", pady=(5, 5))

        self.strength_progress = ttk.Progressbar(
            main_frame,
            orient="horizontal",
            length=500,
            mode="determinate",
            maximum=100
        )
        self.strength_progress.pack(fill="x")

        self.strength_text = tk.Label(
            main_frame,
            text="Strength: Not Generated",
            font=("Segoe UI", 10, "bold"),
            bg="#182530",
            fg="#B8C4CE"
        )
        self.strength_text.pack(pady=(5, 15))

        history_label = tk.Label(
            main_frame,
            text="Generation History - Last 5",
            font=("Segoe UI", 11, "bold"),
            bg="#182530",
            fg="white"
        )
        history_label.pack(anchor="w")

        self.history_list = tk.Listbox(
            main_frame,
            height=5,
            bg="#0B1116",
            fg="#D8E4EC",
            selectbackground="#00A8CC",
            selectforeground="white",
            font=("Consolas", 10),
            relief="flat"
        )
        self.history_list.pack(fill="x", pady=(7, 0))

        footer = tk.Label(
            self.root,
            text="Passwords are generated locally and are not stored permanently.",
            font=("Segoe UI", 9),
            bg="#101820",
            fg="#71808C"
        )
        footer.pack(pady=10)

    def create_checkbox(self, parent, text, variable, row, column):
        checkbox = tk.Checkbutton(
            parent,
            text=text,
            variable=variable,
            bg="#182530",
            fg="#D8E4EC",
            selectcolor="#0B1116",
            activebackground="#182530",
            activeforeground="white",
            font=("Segoe UI", 9),
            anchor="w"
        )
        checkbox.grid(
            row=row,
            column=column,
            sticky="w",
            padx=5,
            pady=4
        )

    def update_length(self, value):
        self.length_value.config(text=str(int(float(value))))

    def get_character_sets(self):
        selected_sets = []

        uppercase = string.ascii_uppercase
        lowercase = string.ascii_lowercase
        numbers = string.digits
        symbols = string.punctuation

        if self.ambiguous_var.get():
            ambiguous = "O0oIl1"
            uppercase = "".join(c for c in uppercase if c not in ambiguous)
            lowercase = "".join(c for c in lowercase if c not in ambiguous)
            numbers = "".join(c for c in numbers if c not in ambiguous)

        if self.upper_var.get():
            selected_sets.append(uppercase)

        if self.lower_var.get():
            selected_sets.append(lowercase)

        if self.number_var.get():
            selected_sets.append(numbers)

        if self.symbol_var.get():
            selected_sets.append(symbols)

        return selected_sets

    def validate_settings(self):
        length = self.length_var.get()
        selected = self.get_character_sets()

        if length < 8:
            messagebox.showerror(
                "Invalid Length",
                "Password length must be at least 8 characters."
            )
            return False

        if len(selected) == 0:
            messagebox.showerror(
                "No Character Type",
                "Please select at least two character types."
            )
            return False

        if len(selected) < 2:
            messagebox.showerror(
                "Selection Required",
                "Please select at least two character types."
            )
            return False

        for character_set in selected:
            if len(character_set) == 0:
                messagebox.showerror(
                    "Invalid Selection",
                    "One selected character type is empty."
                )
                return False

        if length < len(selected):
            messagebox.showerror(
                "Length Too Short",
                "Password length must be greater than or equal to "
                "the number of selected character types."
            )
            return False

        return True

    def secure_shuffle(self, characters):
        characters = list(characters)

        for i in range(len(characters) - 1, 0, -1):
            j = secrets.randbelow(i + 1)
            characters[i], characters[j] = characters[j], characters[i]

        return "".join(characters)

    def generate_password(self):
        if not self.validate_settings():
            return

        length = self.length_var.get()
        selected_sets = self.get_character_sets()

        password_characters = []

        for character_set in selected_sets:
            index = secrets.randbelow(len(character_set))
            password_characters.append(character_set[index])

        all_characters = "".join(selected_sets)

        remaining = length - len(password_characters)

        for _ in range(remaining):
            index = secrets.randbelow(len(all_characters))
            password_characters.append(all_characters[index])

        password = self.secure_shuffle(password_characters)

        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)

        self.update_strength(password)

        self.add_to_history(password)

    def update_strength(self, password):
        score = 0

        length = len(password)

        if length >= 8:
            score += 20

        if length >= 12:
            score += 15

        if length >= 16:
            score += 15

        if any(c.isupper() for c in password):
            score += 15

        if any(c.islower() for c in password):
            score += 15

        if any(c.isdigit() for c in password):
            score += 10

        if any(c in string.punctuation for c in password):
            score += 10

        score = min(score, 100)

        self.strength_progress["value"] = score

        if score < 40:
            text = "Strength: Weak"
        elif score < 70:
            text = "Strength: Medium"
        elif score < 90:
            text = "Strength: Strong"
        else:
            text = "Strength: Very Strong"

        self.strength_text.config(text=text)

    def copy_password(self):
        password = self.password_entry.get()

        if not password:
            messagebox.showwarning(
                "No Password",
                "Generate a password before copying."
            )
            return

        try:
            pyperclip.copy(password)

            messagebox.showinfo(
                "Copied",
                "Password copied to clipboard successfully."
            )

        except Exception as error:
            messagebox.showerror(
                "Clipboard Error",
                f"Unable to copy password.\n\n{error}"
            )

    def add_to_history(self, password):
        self.history.insert(0, password)

        if len(self.history) > 5:
            self.history.pop()

        self.history_list.delete(0, tk.END)

        for index, item in enumerate(self.history, start=1):
            masked = self.mask_password(item)
            self.history_list.insert(
                tk.END,
                f"{index}. {masked}"
            )

    def mask_password(self, password):
        if len(password) <= 4:
            return "*" * len(password)

        return (
            password[:2]
            + "*" * (len(password) - 4)
            + password[-2:]
        )


def main():
    root = tk.Tk()

    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "Horizontal.TProgressbar",
        troughcolor="#0B1116",
        background="#00D4FF",
        bordercolor="#0B1116",
        lightcolor="#00D4FF",
        darkcolor="#00D4FF"
    )

    app = PasswordGenerator(root)

    root.mainloop()


if __name__ == "__main__":
    main()