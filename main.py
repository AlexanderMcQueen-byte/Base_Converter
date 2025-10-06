# Import Kivy App and UI components
from kivy.app import App                     # Base class for Kivy apps
from kivy.uix.boxlayout import BoxLayout     # Layout to arrange widgets vertically/horizontally
from kivy.uix.label import Label             # Text display
from kivy.uix.textinput import TextInput     # User input field
from kivy.uix.button import Button           # Clickable button

# --------------------------
# Number system conversion logic
# --------------------------
# This part is pure Python — it converts numbers between any base (2-36)

DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"  # All valid digits for bases up to 36

# Convert a character to its numeric value (e.g., 'A' -> 10)
def char_to_val(ch):
    return DIGITS.index(ch.upper())  # Convert to uppercase to handle both 'a' and 'A'

# Convert a numeric value to a character (e.g., 10 -> 'A')
def val_to_char(v):
    return DIGITS[v]

# Convert a string in base-N to decimal
def to_decimal(num_str, base):
    neg = num_str.startswith("-")        # Check if number is negative
    if neg:
        num_str = num_str[1:]            # Remove negative sign for calculation
    dec = 0                              # Start with decimal value 0
    for ch in num_str:
        dec = dec * base + char_to_val(ch)  # Multiply previous value by base and add current digit
    return -dec if neg else dec           # Return negative if original number was negative

# Convert decimal to a string in base-N
def from_decimal(dec, base):
    if dec == 0:
        return "0"
    neg = dec < 0
    if neg:
        dec = -dec
    digits = []
    while dec > 0:
        digits.append(val_to_char(dec % base))  # Get remainder and convert to character
        dec //= base                             # Divide by base for next digit
    if neg:
        digits.append("-")                       # Add negative sign if needed
    return "".join(reversed(digits))            # Reverse list and join as string

# Convert from one base to another
def convert(num_str, from_base, to_base):
    dec = to_decimal(num_str, from_base)       # Step 1: convert to decimal
    return from_decimal(dec, to_base)          # Step 2: convert decimal to target base

# --------------------------
# Kivy User Interface
# --------------------------
class ConverterApp(App):
    """
    This is the main Kivy app class.
    It controls what is displayed and how the app behaves.
    """
    def build(self):
        """
        This method builds the UI when the app starts.
        """
        layout = BoxLayout(
            orientation="vertical",   # Arrange elements vertically
            padding=20,              # Space around the layout
            spacing=10               # Space between elements
        )

        # TextInput for entering the number to convert
        self.input_num = TextInput(
            hint_text="Enter number",  # Placeholder text
            multiline=False            # Single-line input
        )

        # TextInput for "From base"
        self.from_base = TextInput(
            hint_text="From base (2-36)",
            multiline=False
        )

        # TextInput for "To base"
        self.to_base = TextInput(
            hint_text="To base (2-36)",
            multiline=False
        )

        # Label to display conversion result
        self.result_label = Label(
            text="Result will appear here"  # Initial text
        )

        # Button to perform conversion
        convert_btn = Button(
            text="Convert"
        )
        convert_btn.bind(on_press=self.do_convert)  # Link button to conversion function

        # Add all widgets to the layout in order
        layout.add_widget(self.input_num)
        layout.add_widget(self.from_base)
        layout.add_widget(self.to_base)
        layout.add_widget(convert_btn)
        layout.add_widget(self.result_label)

        return layout  # Return the layout to be displayed

    def do_convert(self, instance):
        """
        This method runs when the 'Convert' button is pressed.
        It reads the input, performs conversion, and shows result.
        """
        try:
            num = self.input_num.text.strip()          # Get user input and remove extra spaces
            fb = int(self.from_base.text)              # Convert from-base to integer
            tb = int(self.to_base.text)                # Convert to-base to integer
            result = convert(num, fb, tb)             # Use our conversion function
            self.result_label.text = f"Result: {result}"  # Display the result
        except Exception as e:
            # If any error occurs (invalid number or base), show it in the label
            self.result_label.text = f"Error: {e}"

# Entry point of the app
if __name__ == "__main__":
    ConverterApp().run()  # Run the app
