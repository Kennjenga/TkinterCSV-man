Method 1: Using a bash script  
tr '\t' ',' < your_data.tsv > your_data_comma.csv

Method 2: using python libraries  
import csv

def convert_tsv_to_csv(input_filename, output_filename):  
 """ Converts a tab-delimited CSV file to a comma-separated CSV file.

Args:  
 input_filename: Path to the tab-delimited CSV file.  
 output_filename: Path to the output comma-separated CSV file.  
 """  
 with open(input_filename, 'r') as infile, open(output_filename, 'w', newline='') as outfile:  
 reader = csv.reader(infile, delimiter='\t') # Read data with tab delimiter  
 writer = csv.writer(outfile)  
 writer.writerows(reader) # Write data with comma delimiter

# Example usage

convert_tsv_to_csv('your_data.tsv', 'your_data_comma.csv')

# selecting distinct

CREATE TABLE UniqueOrders AS
SELECT DISTINCT OrderID
FROM Orders;

# if column name already exists

INSERT INTO UniqueOrders (OrderID)
SELECT DISTINCT OrderID
FROM Orders;

# To create read and write

CREATE TABLE UniqueOrders (
OrderID INT PRIMARY KEY
);

INSERT INTO UniqueOrders (OrderID)
SELECT DISTINCT OrderID
FROM Orders;

# Building an executable

py -m pip install pyinstaller
py -m PyInstaller myfile.py --onefile
