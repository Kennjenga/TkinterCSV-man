import tkinter as tk
from tkinter import filedialog
import csv

def read_csv(filename):
    """
    Reads data from a CSV file and returns a list of dictionaries.
    Each dictionary represents a row with keys corresponding to column names.
    """
    records = []
    
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            records.append(row)
    return records

def manipulate_data(records):
    """
    Modifies data based on tax type with specific append behavior.
    """
    new_records = []

    c_code ={
        '150000>15001>1508': 410010,
        '150000>15001>1513': 410010,
        '150004>15006': 450030
    }
    
    for r in records:
        new_row = {
            'Trans_Code': r['Trans Code'],
            'Account': "D" + r['Account'],
            'Trans_Date': r['Trans Date'],
            'Reference': r['Reference'],
            'Description': r['DeSAription'],
            'Amount_Excl': r['Amount Excl'],
            'Tax_Type': r['Tax Type'],
            'Amount_Incl': r['Amount Incl'],
            'Exchange_Rate': r['Exchange Rate'],
            'Foreign_Amount_Excl': r['Foreign Amount Excl'],
            'Foreign_Amount_Incl': r['Foreign Amount Incl'],
            'Sun_Date': r['Trans Date'],
            'CUST_CODE': "D" + r['Account'],
            'Travel_Date': r['Service Date'],
        }

        if r['Tax Type'] == '7':
            new_row['File Type'] = 'H'
            new_row['Account'] = "D" + r['Account']
            new_records.append(new_row.copy())  # Append first row with H
            new_row['File Type'] = 'D'
            new_row['Account'] = c_code[r['GL Contra Code']]
            new_records.append(new_row.copy())
        elif r['Tax Type'] == '1':
            new_row['File Type'] = 'H'
            new_records.append(new_row.copy())  # Append first row with H
            new_row['File Type'] = 'D'
            new_row['Account'] = c_code[r['GL Contra Code']]
            new_records.append(new_row.copy())  # Append second row with D
            new_row['File Type'] = 'V'
            new_row['Account'] = 222080
            new_records.append(new_row.copy())  # Append third row with V
        else:
            # Append with original File Type for other tax types
            new_records.append(new_row)

        
    return new_records

def write_to_csv(records, output_filename):
    """
    Writes data to a CSV file using the specified format.
    """
    fieldnames = [
        'Trans_Code', 'Account', 'Trans_Date', 'Reference', 'Description',
        'Amount_Excl', 'Tax_Type', 'Amount_Incl', 'Exchange_Rate',
        'Foreign_Amount_Excl', 'Foreign_Amount_Incl', 'Base_VAT', 'Sun_Date',
        'CUST_CODE', 'Travel_Date', 'File Type'
    ]

    with open(output_filename, 'w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

def process_file():
    input_file = filedialog.askopenfilename(title="Select Input CSV File", filetypes=[("CSV Files", "*.csv")])
    if input_file:
        trans_file = read_csv(input_file)
        manipulated_data = manipulate_data(trans_file)
        output_file = filedialog.asksaveasfilename(title="Save Output CSV File", defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if output_file:
            write_to_csv(manipulated_data, output_file)
            print(f"Data written to {output_file}")

# Create the main window
root = tk.Tk()
root.title("CSV Data Manipulation")

# Create a button to process the file
process_button = tk.Button(root, text="Process File", command=process_file)
process_button.pack()

# Start the GUI event loop
root.mainloop()
