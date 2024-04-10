from openpyxl import Workbook
from openpyxl.styles import PatternFill
from openpyxl.utils import cell as index_to_cell
import os

def guess_delimiter(file_path, potential_delimiters=(',', ';', '|', '\t', '#'), chunk_size=1024):
    """
    Guess the delimiter used in a delimited file.

    Args:
        file_path (str): Path to the file.
        potential_delimiters (str): Delimiters to consider.
        chunk_size (int): Size of the chunk to read from the file.

    Returns:
        str: The most commonly used delimiter.
    """
    delimiter_counts = {delimiter: 0 for delimiter in potential_delimiters}

    with open(file_path, 'r') as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break

            for delimiter in potential_delimiters:
                count = chunk.count(delimiter)
                delimiter_counts[delimiter] += count

    most_common_delimiter = max(delimiter_counts, key=delimiter_counts.get)
    return most_common_delimiter


def compare_delimited_files(file1_path, file2_path, delimiter):
    """
    Compare two delimited files and identify differences.

    Args:
        file1_path (str): Path to the first file.
        file2_path (str): Path to the second file.
        delimiter (str): Delimiter used in the files.

    Returns:
        tuple: A tuple containing:
            - list: List of tuples containing line number, index of differing element, 
                    and the differing element itself.
            - tuple: A tuple containing the following information about the files:
                - int: Number of rows in file 1.
                - int: Number of rows in file 2.
                - int: Number of columns in file 1.
                - int: Number of columns in file 2.
    """
    differences = []  # List to store the indices of differences in file one

    # Initialize line numbers and column numbers
    line_number = 1
    file1_row_number = 0
    file2_row_number = 0
    file1_column_number = 0
    file2_column_number = 0

    # Open files and read lines
    with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
        while True:
            file1_line = file1.readline()
            file2_line = file2.readline()

            # Increment row numbers if lines are present
            if file1_line or file2_line:
                if file1_line:
                    file1_row_number += 1
                if file2_line:
                    file2_row_number += 1
            else:
                break

            # Split lines into fields using the delimiter
            file1_fields = file1_line.strip().split(delimiter)
            file2_fields = file2_line.strip().split(delimiter)

            # Update column numbers if not already set
            if file1_column_number == 0 or file2_column_number == 0:
                file1_column_number = len(file1_fields)
                file2_column_number = len(file2_fields)

            # Determine maximum number of fields among all lines
            max_fields = max(len(file1_fields), len(file2_fields))

            # Compare each pair of fields up to the maximum number of fields
            for index in range(max_fields):
                field1 = file1_fields[index] if index < len(file1_fields) else None
                field2 = file2_fields[index] if index < len(file2_fields) else None

                if field1 != field2:
                    differences.append((line_number, index, field1))

            # Increment line number
            line_number += 1

    return differences, (file1_row_number, file2_row_number, file1_column_number, file2_column_number)


def generate_report(differences, row_column_info):
    """
    Generate a report summarizing the differences between two delimited files.

    Args:
        differences (list): List of tuples containing line number, index of differing element,
                            and the differing element itself.
        row_column_info (tuple): A tuple containing the following information about the files:
            - int: Number of rows in file 1.
            - int: Number of rows in file 2.
            - int: Number of columns in file 1.
            - int: Number of columns in file 2.

    Writes a report to 'report.txt' file containing information about the differences
    between the two files, including any differences in the number of rows or columns
    and the details of differing cells.

    """
    rows_message, cols_message = None, None
    file1_rows, file2_rows, file1_cols, file2_cols = row_column_info

    if not differences:
        with open('report.txt', 'w') as report:
            report.write('No differences found between the files.')
        return
    
    if file1_cols != file2_cols:
        more_cols_file = "new.txt" if file1_cols > file2_cols else "old.txt"
        cols_message = f'Files have different number of columns. {more_cols_file} file has more columns.\n'
    if file1_rows != file2_rows:
        more_rows_file = "new.txt" if file1_rows > file2_rows else "old.txt"
        rows_message = f'Files have different number of rows. {more_rows_file} file has more rows.\n'

    with open('report.txt', 'w') as report:
        if cols_message:
            report.write(cols_message)
        if rows_message:
            report.write(rows_message)
        report.write('Differences found in cells:\n')
        for line_number, col_index, _ in differences:
            col_letter = index_to_cell.get_column_letter(col_index + 1) # Adjusting column_index to 1-based indexing
            cell = f"{col_letter}{line_number}"
            report.write(f'{cell}\n')


def highlight_differences(file1_path, file2_path, output_path, delimiter):
    """
    Compare two delimited files, identify differences, generate a report, and highlight differences in an Excel file.

    Args:
        file1_path (str): Path to the first file.
        file2_path (str): Path to the second file.
        output_path (str): Path to save the Excel file.
        delimiter (str): Delimiter used in the files.

    Returns:
        None
    """
    differences, row_column_info = compare_delimited_files(file1_path, file2_path, delimiter)
    generate_report(differences, row_column_info)

    # Create a new workbook
    wb = Workbook()
    ws = wb.active

    if differences:
        # Copy data from file1 into the new workbook
        with open(file1_path, 'r') as file1:
            for line_number, line in enumerate(file1, start=1):
                line_data = line.strip().split(delimiter)
                for col_index, value in enumerate(line_data, start=1):
                    cell = ws.cell(row=line_number, column=col_index, value=value)

        # Highlight cells with differences
        for line_number, col_index, value in differences:
            cell = ws.cell(row=line_number, column=col_index + 1)  # Adjusting col_index to 1-based indexing
            cell.fill = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")


    else:
        ws['A1'] = 'No differences found between the files.'

    # Save the workbook
    wb.save(output_path)


def main():
    # file1_path = input("Enter the path of the first file: ")
    file1_path = "new.txt"
    file2_path =  "old.txt"
    output_path = "output.xlsx"

    # Validate file paths
    if not (os.path.isfile(file1_path) and os.path.isfile(file2_path)):
        print("Error: One or both of the input files does not exist.")
        return

    try:
        delimiter = guess_delimiter(file1_path)  
        highlight_differences(file1_path, file2_path, output_path, delimiter)
    except PermissionError as e:
        print(f"""Please close all files associated with this 
              comparison, including the report file and re-run the operation""")
        return

if __name__ == "__main__":
    main()
