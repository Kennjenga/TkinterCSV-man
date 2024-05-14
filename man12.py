import tkinter as tk
from dbconnection1 import check_and_update_GL_contra_codes, get_account_by_gl_contra_code
from tkinter import filedialog
import threading
import csv


def home_page():
    home_frame = tk.Frame(main_frame)

    def read_csv(filename):
        """Reads data from a CSV file and returns a list of dictionaries."""
        records = []
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                records.append(row)
        return records

    def manipulate_data(records):
        """
        Modifies data based on tax type with specific append behavior.
        Uses a dictionary for tax type-specific processing functions.
        """
        new_records = []
        tax_type_handlers = {
            '7': handle_tax_type_7,
            '1': handle_tax_type_1,
        }

        for r in records:
            new_row = {
                'Trans_Code': r['Trans Code'],
                'Account': r["Account"],
                'GL_Contra_Code': r['GL Contra Code'],
                'Trans_Date': r['Trans Date'],
                'Reference': r['Reference'],
                'Description': r['DeSAription'],
                'Amount_Excl': r['Amount Excl'],
                'Tax_Type': r['Tax Type'],
                'Amount_Incl': r['Amount Incl'],
                'Exchange_Rate': r['Exchange Rate'],
                'Foreign_Amount_Excl': r['Foreign Amount Excl'],
                'Foreign_Amount_Incl': r['Foreign Amount Incl'],
                'Base_VAT': (float(r['Amount Incl']) - float(r['Amount Excl'])),
                'Foreign_VAT': (float(r['Foreign Amount Incl']) - float(r['Foreign Amount Excl'])),
                'Sun_Date': r['Trans Date'].replace("/", ""),
                'ROUTES ANAL': get_route_anal_code(r['GL Contra Code']),
                'CUST_CODE': "D" + r['Account'],
                'Travel_Date': r['Service Date'],
            }
            handler = tax_type_handlers.get(new_row['Tax_Type'])
            if handler:
                # Process using tax type handler
                new_records.extend(handler(new_row.copy()))

            else:
                # Append with original File Type for other tax types
                new_records.append(new_row)

        for row in new_records:
            row.pop('GL_Contra_Code', None)
        return new_records

    def get_route_anal_code(GLC_code):
        # Split the account value by '>'
        parts = GLC_code.split('>')

        # Check if the last part matches the longer pattern
        if len(parts) == 3:
            return parts[-1]  # Set to the last part
        else:
            return '1501'  # Default value

    def write_to_csv(records, output_file):
        """
        Writes data to a CSV file using the specified format.
        """
        fieldnames = [
            'Trans_Code', 'Account', 'Trans_Date', 'Reference', 'Description',
            'Amount_Excl', 'Tax_Type', 'Amount_Incl', 'Exchange_Rate',
            'Foreign_Amount_Excl', 'Foreign_Amount_Incl', 'Base_VAT', 'Foreign_VAT', 'Sun_Date', 'ROUTES ANAL',
            'CUST_CODE', 'Travel_Date', 'File Type'
        ]

        with open(output_file, 'w', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(records)

    def handle_manipulate_data():
        message_var.set("")
        input_file = input_var.get()
        output_file = output_var.get()
        if input_file and output_file:
            message_var.set("Processing...")
            # Start data processing in a separate thread
            thread = threading.Thread(
                target=process_data, args=(input_file, output_file))
            thread.start()
        else:
            message_var.set("Please enter both file paths!")

    def handle_tax_type_7(row):
        """Handles data processing for tax type '7'."""
        return [
            {**row, 'File Type': 'H', 'Account': "D" + row['Account']},
            {**row, 'File Type': 'D',
             'Account': get_account_by_gl_contra_code(row['GL_Contra_Code'])},
        ]

    def handle_tax_type_1(row):
        """Handles data processing for tax type '1'."""
        return [
            {**row, 'File Type': 'H', 'Account': "D" + row['Account']},
            {**row, 'File Type': 'D',
                'Account': get_account_by_gl_contra_code(row['GL_Contra_Code'])},
            {**row, 'File Type': 'V', 'Account': 222080},
        ]

    def process_data(input_file, output_file):
        try:
            records = read_csv(input_file)
            manipulated_data = manipulate_data(records)
            write_to_csv(manipulated_data, output_file)
            message_var.set("Data processed successfully!")
        except FileNotFoundError:
            message_var.set("Error: Input file not found!")
        except Exception as e:
            message_var.set(f"An error occurred: {e}")

    # Input file path entry
    input_var = tk.StringVar()
    input_label = tk.Label(home_frame, text="Input File:")
    input_label.pack()
    input_entry = tk.Entry(home_frame, textvariable=input_var)
    input_entry.pack(fill="x")
    input_button = tk.Button(home_frame, text="Browse", command=lambda: input_var.set(
        filedialog.askopenfilename()))
    input_button.pack()

    # Output file path entry
    output_var = tk.StringVar()
    output_label = tk.Label(home_frame, text="Output File:")
    output_label.pack()
    output_entry = tk.Entry(home_frame, textvariable=output_var)
    output_entry.pack(fill="x")
    output_button = tk.Button(home_frame, text="Browse", command=lambda: output_var.set(
        filedialog.asksaveasfilename(defaultextension=".csv")))
    output_button.pack()

    # Process button
    process_button = tk.Button(
        home_frame, text="Process Data", command=handle_manipulate_data)
    process_button.pack()

    # Message label
    message_var = tk.StringVar()
    message_label = tk.Label(home_frame, textvariable=message_var)
    message_label.pack()

    home_frame.pack(expand=True, fill="both", padx=10, pady=10)
    home_frame.configure(width=400, height=400)


def GL_code():
    def handle_submit():
        message_var.set("")
        gl_contra_code = GL_code_var.get()
        account = int(Account_var.get())

        account_info = check_and_update_GL_contra_codes(
            gl_contra_code, account, message_var)

    GLframe = tk.Frame(main_frame)
    GLframe.pack(expand=True, fill="both", padx=10, pady=10)

    GL_code_var = tk.StringVar()
    GL_code_label = tk.Label(GLframe, text="Enter GL Contra Code")
    GL_code_label.pack()
    GL_code_Entry = tk.Entry(GLframe, textvariable=GL_code_var)
    GL_code_Entry.pack()

    Account_var = tk.StringVar()
    Account_label = tk.Label(GLframe, text="Enter Account")
    Account_label.pack()
    Account_Entry = tk.Entry(GLframe, textvariable=Account_var)
    Account_Entry.pack()

    submit_button = tk.Button(GLframe, text="Submit", command=handle_submit)
    submit_button.pack()

    message_var = tk.StringVar()
    result_label = tk.Label(GLframe, textvariable=message_var)
    result_label.pack()


def indicate(page):
    for fm in main_frame.winfo_children():
        fm.destroy()
        root.update()
    page()


root = tk.Tk()
root.title("CSV Data Manipulation Tool")
root.resizable(width=True, height=True)
root.minsize(width=500, height=400)

options_frame = tk.Frame(root, bg="#cfc542")
main_frame = tk.Frame(root)
home_btn = tk.Button(options_frame, text="Csv_Home", font=(
    'Bold', 10), fg='#dde3c1', bd=0, bg='#616050', command=lambda: indicate(home_page))
home_btn.place(x=10, y=100)

GL_contra = tk.Button(options_frame, text="GL_Codes", font=(
    'Bold', 10), fg='#dde3c1', bd=0, bg='#616050', command=lambda: indicate(GL_code))
GL_contra.place(x=10, y=200)

options_frame.pack(side=tk.LEFT, fill="y")
options_frame.pack_propagate(False)
options_frame.configure(width=100, height=100)

main_frame.pack(side=tk.LEFT, expand=True, fill="both")
main_frame.configure(height=400, width=500)
home_page()
root.mainloop()
