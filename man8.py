from dbconnection1 import get_account_by_gl_contra_code
import csv
from tkinter import StringVar, Tk, filedialog, Button, Entry, Label


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
            'Sun_Date': r['Trans Date'],
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


def write_to_csv(records, output_filename):
    """
    Writes data to a CSV file using the specified format.
    """
    fieldnames = [
        'Trans_Code', 'Account', 'Trans_Date', 'Reference', 'Description',
        'Amount_Excl', 'Tax_Type', 'Amount_Incl', 'Exchange_Rate',
        'Foreign_Amount_Excl', 'Foreign_Amount_Incl', 'Base_VAT', 'Foreign_VAT', 'Sun_Date', 'ROUTES ANAL',
        'CUST_CODE', 'Travel_Date', 'File Type'
    ]

    with open(output_filename, 'w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)


def handle_manipulate_data():
    message_var.set("")
    input_file = input_var.get()
    output_file = output_var.get()
    if input_file and output_file:
        try:
            message_var.set("processing ....")
            records = read_csv(input_file)
            manipulated_data = manipulate_data(records)
            write_to_csv(manipulated_data, output_file)
            message_var.set("Data processed successfully!")
        except FileNotFoundError:
            message_var.set("Error: Input file not found!")
        except Exception as e:
            message_var.set(f"An error occurred: {e}")
    else:
        message_var.set("Please enter both file paths!")


# ... rest of the GUI code (root.mainloop() etc.)
root = Tk()
root.title("CSV Data Manipulation Tool")
root.geometry("600x400")  # Initial size
root.minsize(width=400, height=300)

# Input file path entry
input_var = StringVar()
input_label = Label(root, text="Input File:")
input_label.pack()
input_entry = Entry(root, textvariable=input_var)
input_entry.pack(fill="x")
input_button = Button(root, text="Browse", command=lambda: [
                      input_var.set(filedialog.askopenfilename())])
input_button.pack()

# Output file path entry
output_var = StringVar()
output_label = Label(root, text="Output File:")
output_label.pack()
output_entry = Entry(root, textvariable=output_var)
output_entry.pack(fill="x")
output_button = Button(root, text="Browse", command=lambda: [
                       output_var.set(filedialog.asksaveasfilename(defaultextension=".csv"))])
output_button.pack()

# Process button
process_button = Button(root, text="Process Data",
                        command=handle_manipulate_data)
process_button.pack()

# Message label
message_var = StringVar()
message_label = Label(root, textvariable=message_var)
message_label.pack()

root.mainloop()
