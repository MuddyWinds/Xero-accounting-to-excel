import json
import pandas as pd
from pathlib import Path


# Function to find index of a sublist containing a character
def find_in_list_of_list(mylist, char):
    for sub_list in mylist:
        if char in sub_list:
            return mylist.index(sub_list)
    raise ValueError("'{char}' is not in list".format(char=char))

# Function to reformat JSON file
def reformatting_json(json_file, json_headers):
    # Store temporary data before casting into dataframe
    data_rows = []

    for section in json_file:
        # Add date row
        if section['RowType'] == "Header":
            data_rows.append(list(map(lambda x: x['Value'], section['Cells'])))

        # Add other rows except Asset and Liabilities
        if section['RowType'] == "Section" and section['Title'] not in ["Assets", "Liabilities"]:
            temp_data = list(map(lambda x: [column["Value"] for column in x["Cells"]], section["Rows"]))
            data_rows += temp_data

    format_in_excel(data_rows, json_headers)

# Function to check if a value can be converted to float
def check_float(potential_f):
    try:
        float(potential_f)
        return True
    except ValueError:
        return False

# Function to write a row in the worksheet
def write_row(worksheet, row_num, row_data, formatting):
    for ele in range(len(row_data)):
        worksheet.write(row_num, ele, row_data[ele], formatting)

# Function to format data in excel
def format_in_excel(data, headers):
    file_name = str(Path.home() / "Downloads") + '/xero_balance_sheet.xlsx'
    sheet_name1 = "Sheet1"

    # Convert all numbers to float
    for ele in range(len(data)):
        for i in range(len(data[ele])):
            data[ele][i] = float(data[ele][i]) if check_float(data[ele][i]) else data[ele][i]

    # Add formatted rows to the data
    add_formatted_rows(data)

    # Create a dataframe and remove default column names
    df = pd.DataFrame(data)
    df.columns = df.iloc[0]
    df = df[1:]

    # Add the data to excel
    writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
    df.to_excel(writer, sheet_name=sheet_name1, startrow=4, index=False)

    # Re-format in excel
    reformat_excel(writer, sheet_name1, headers, data)

    writer.save()

# Function to add formatted rows to the data
def add_formatted_rows(data):
    formatted_rows = [
        (1, []),
        (2, ["Assets"]),
        (3, []),
        (4, ["Bank"]),
        (find_in_list_of_list(data, "Total Bank") + 1, []),
        (find_in_list_of_list(data, "Total Bank") + 2, ['Current Assets']),
        (find_in_list_of_list(data, "Total Current Assets") + 1, []),
        (find_in_list_of_list(data, "Total Current Assets") + 2, ['Fixed Assets']),
        (find_in_list_of_list(data, "Total Fixed Assets") + 1, []),
        (find_in_list_of_list(data, "Total Assets") + 1, []),
        (find_in_list_of_list(data, "Total Assets") + 2, ['Liabilities']),
        (find_in_list_of_list(data, "Total Assets") + 3, []),
        (find_in_list_of_list(data, "Total Assets") + 4, ['Current Liabilities']),
        (find_in_list_of_list(data, "Total Current Liabilities") + 1, []),
        (find_in_list_of_list(data, "Total Current Liabilities") + 2, ['Non-Current Liabilities']),
        (find_in_list_of_list(data, "Total Non-Current Liabilities") + 1, []),
        (find_in_list_of_list(data, "Total Liabilities") + 1, []),
        (find_in_list_of_list(data, "Net Assets") + 1, []),
        (find_in_list_of_list(data, "Net Assets") + 2, ['Equity'])
    ]

    for index, row in formatted_rows:
        data.insert(index, row)

    format_data_rows(data)

# Function to format data rows
def format_data_rows(data):
    asset_num = find_in_list_of_list(data, "Assets") + 1
    liabilities_num = find_in_list_of_list(data, "Liabilities")
    total_lia_num = find_in_list_of_list(data, "Total Liabilities")

    for i in range(len(data[asset_num:liabilities_num])):
        if i % 2 != 0:
            data[asset_num + i].insert(0, "Less")
            data[asset_num + i].insert(2, "Net Book Value")

    for i in range(len(data[liabilities_num:total_lia_num])):
        if i % 2 != 0:
            data[liabilities_num + i].insert(0, "Less")
            data[liabilities_num + i].insert(2, "Net Book Value")

# Function to reformat excel
def reformat_excel(writer, sheet_name, headers, data):
    workbook = writer.book
    worksheet = writer.sheets[sheet_name]

    # Define formats
    header_format = workbook.add_format({
        'bold': True,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': '#C0C0C0',
        'border': 1
    })

    section_format = workbook.add_format({
        'bold': True,
        'align': 'left',
        'fg_color': '#D3D3D3',
        'border': 1
    })

    section_total_format = workbook.add_format({
        'bold': True,
        'fg_color': '#D3D3D3',
        'border': 1
    })

    section_less_format = workbook.add_format({
        'bold': True,
        'align': 'left',
        'border': 1
    })

    # Write headers
    for i in range(len(headers)):
        worksheet.write(4, i, headers[i], header_format)

    # Write sections titles
    for ele in range(len(data)):
        if data[ele] in [["Assets"], ["Liabilities"], ["Equity"]]:
            write_row(worksheet, ele, data[ele], section_format)
        elif data[ele] in [["Total Assets"], ["Total Liabilities"], ["Total Equity"]]:
            write_row(worksheet, ele, data[ele], section_total_format)
        elif "Less" in data[ele]:
            write_row(worksheet, ele, data[ele], section_less_format)

    # Set column widths
    worksheet.set_column(0, 0, 20)
    worksheet.set_column(1, 1, 20)
    worksheet.set_column(2, 2, 20)
