import pandas as pd
import csv


def read_csv(filename):
    """ Reads data from a CSV file using pandas.

    pandas is a powerful library specifically designed for data analysis
    and offers efficient ways to handle large datasets.
    """
    records = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            records.append(row)
    return records


input_file = "s2a.csv"
print(read_csv(input_file))
