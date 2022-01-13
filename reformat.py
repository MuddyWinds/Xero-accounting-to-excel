import json
import pandas as pd
from pathlib import Path


def find_in_list_of_list(mylist, char):
    for sub_list in mylist:
        if char in sub_list:
            return mylist.index(sub_list)
    raise ValueError("'{char}' is not in list".format(char = char))


def reformatting_json(json_file, json_headers):
    # Store temporary data before casting into dataframe
    data_rows = []

    for section in json_file:
        # Row 5: Date
        if (section['RowType'] == "Header"):
            data_rows.append(list(map(lambda x: x['Value'], section['Cells'])))
        
        # Other rows except Asset and Liabilities
        if (section['RowType'] == "Section" and section['Title'] not in ["Assets", "Liabilities"]):
            temp_data = list(map(lambda x: [column["Value"] for column in x["Cells"]], section["Rows"]))
            data_rows += temp_data
   
    format_in_excel(data_rows, json_headers)

def check_float(potential_f):
    try:
        float(potential_f)
        return True
    except ValueError:
        return False

def write_row(worksheet, row_num, row_data, formatting):
    for ele in range(len(row_data)):
        worksheet.write(row_num, ele, row_data[ele], formatting)

def format_in_excel(data, headers):
    file_name = str(Path.home() / "Downloads") + '/xero_balance_sheet.xlsx'
    sheet_name1 = "Sheet1"
    col_num = len(data[0]) - 1

    # Convert all numbers to float
    for ele in range(len(data)):
        for i in range(len(data[ele])):
            data[ele][i] = float(data[ele][i]) if check_float(data[ele][i]) else data[ele][i]

    # Insert new row to sub-totals
    data.insert(1, [])
    data.insert(2, ["Assets"])
    data.insert(3, [])
    data.insert(4, ["Bank"])
    data.insert(find_in_list_of_list(data, "Total Bank") + 1, [])
    data.insert(find_in_list_of_list(data, "Total Bank") + 2, ['Current Assets'])
    data.insert(find_in_list_of_list(data, "Total Current Assets") + 1, [])
    data.insert(find_in_list_of_list(data, "Total Current Assets") + 2, ['Fixed Assets'])
    data.insert(find_in_list_of_list(data, "Total Fixed Assets") + 1, [])
    data.insert(find_in_list_of_list(data, "Total Assets") + 1, [])
    data.insert(find_in_list_of_list(data, "Total Assets") + 2, ['Liabilities'])
    data.insert(find_in_list_of_list(data, "Total Assets") + 3, [])
    data.insert(find_in_list_of_list(data, "Total Assets") + 4, ['Current Liabilities'])
    data.insert(find_in_list_of_list(data, "Total Current Liabilities") + 1, [])
    data.insert(find_in_list_of_list(data, "Total Current Liabilities") + 2, ['Non-Current Liabilities'])
    data.insert(find_in_list_of_list(data, "Total Non-Current Liabilities") + 1, [])
    data.insert(find_in_list_of_list(data, "Total Liabilities") + 1, [])
    data.insert(find_in_list_of_list(data, "Net Assets") + 1, [])
    data.insert(find_in_list_of_list(data, "Net Assets") + 2, ['Equity'])

    # Add spacing to data
    asset_num = find_in_list_of_list(data, "Assets") + 1
    liabilities_num = find_in_list_of_list(data, "Liabilities")
    total_lia_num = find_in_list_of_list(data, "Total Liabilities") 

    for i in range(len(data[asset_num:liabilities_num - 3])):
        if data[asset_num + i] != []:
            ele = data[asset_num + i]
            data[asset_num + i] = ["  " + ele[0]] + ele[1:] if len(ele) > 1 else ["  " + ele[0]]

    for i in range(len(data[liabilities_num + 1:total_lia_num])):
        if data[liabilities_num + i + 1] != []:
            ele = data[liabilities_num + i + 1]
            data[liabilities_num + i + 1] = ["  " + ele[0]] + ele[1:] if len(ele) > 1 else ["  " + ele[0]]

    # Remove default column names
    df = pd.DataFrame(data)
    df.columns = df.iloc[0]
    df = df[1:]
     
    # Add the data
    writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
    df.to_excel(writer, sheet_name=sheet_name1, startrow = 4, index=False)
    
    # Re-format in excel
    workbook = writer.book
    worksheet = writer.sheets[sheet_name1]

    # Default font type: Aerial
    cell_format = workbook.add_format()
    cell_format.set_font_name("Arial")  # Font
    cell_format.set_font_size(9)
    worksheet.set_column(0, col_num, None, cell_format)

    currency_format = workbook.add_format({'num_format':'$#,##0.00'})
    worksheet.conditional_format(9, 1, len(data) + 6, col_num, {'type': 'no_blanks', 'format': currency_format})
    
    # Remove default date borders
    date_format = workbook.add_format()
    date_format.set_border(0)
    date_format.set_bold()
    write_row(worksheet, 4, data[0], date_format)
    
    # Bold sub-headings
    sub_heading = workbook.add_format({'bold': 1})
    worksheet.conditional_format(0, 0, len(data), 0, {'type': 'cell', 'criteria': 'equal to', 'value': '"Assets"', 'format': sub_heading})
    worksheet.conditional_format(0, 0, len(data), 0, {'type': 'cell', 'criteria': 'equal to', 'value': '"  Bank"', 'format': sub_heading})
    worksheet.conditional_format(0, 0, len(data), 0, {'type': 'cell', 'criteria': 'equal to', 'value': '"  Current Assets"', 'format': sub_heading})
    worksheet.conditional_format(0, 0, len(data), 0, {'type': 'cell', 'criteria': 'equal to', 'value': '"  Fixed Assets"', 'format': sub_heading})
    worksheet.conditional_format(0, 0, len(data), 0, {'type': 'cell', 'criteria': 'equal to', 'value': '"  Current Liabilities"', 'format': sub_heading})
    worksheet.conditional_format(0, 0, len(data), 0, {'type': 'cell', 'criteria': 'equal to', 'value': '"  Non-Current Liabilities"', 'format': sub_heading})
    worksheet.conditional_format(0, 0, len(data), 0, {'type': 'cell', 'criteria': 'equal to', 'value': '"Equity"', 'format': sub_heading})
    worksheet.conditional_format(0, 0, len(data), 0, {'type': 'cell', 'criteria': 'equal to', 'value': '"Liabilities"', 'format': sub_heading})

    sub_totals_format = workbook.add_format({'bold': 1})

    # Merge cells and add titles & sub-titles
    title_format = workbook.add_format()
    title_format.set_bold()
    title_format.set_font_name("Arial")
    title_format.set_font_size(12)
    title_format.set_align("center")
    worksheet.merge_range(0, 0, 0, col_num, headers[0], title_format)

    title2_format = workbook.add_format()    # Format cannot be dynamically changed
    title2_format.set_bold()
    title2_format.set_font_name("Arial")
    title2_format.set_font_size(10)
    title2_format.set_align("center")
    worksheet.merge_range(1, 0, 1, col_num, headers[1], title2_format)
    worksheet.merge_range(2, 0, 2, col_num, headers[2], title2_format)

    # Underline sub-totals
    sub_total_underline = workbook.add_format()
    sub_total_underline.set_bold()
    sub_total_underline.set_font_name("Arial")
    sub_total_underline.set_font_size(9)
    sub_total_underline.set_bottom()
    
    write_row(worksheet, find_in_list_of_list(data, "  Total Bank") + 4, data[find_in_list_of_list(data, "  Total Bank")], sub_total_underline)
    write_row(worksheet, find_in_list_of_list(data, "  Total Current Assets") + 4, data[find_in_list_of_list(data,"  Total Current Assets")], sub_total_underline)
    write_row(worksheet, find_in_list_of_list(data, "  Total Fixed Assets") + 4, data[find_in_list_of_list(data,"  Total Fixed Assets")], sub_total_underline)
    write_row(worksheet, find_in_list_of_list(data, "  Total Current Liabilities") + 4, data[find_in_list_of_list(data,"  Total Current Liabilities")], sub_total_underline)
    write_row(worksheet, find_in_list_of_list(data, "  Total Non-Current Liabilities") + 4, data[find_in_list_of_list(data,"  Total Non-Current Liabilities")], sub_total_underline)
    
    # Double-underline total assets and total liabilities
    sub_header_underline = workbook.add_format()
    sub_header_underline.set_bold()
    sub_header_underline.set_font_name("Arial")
    sub_header_underline.set_font_size(9)
    sub_header_underline.set_bottom(6)

    write_row(worksheet, find_in_list_of_list(data, "Total Assets") + 4, data[find_in_list_of_list(data, "Total Assets")], sub_header_underline)
    write_row(worksheet, find_in_list_of_list(data, "Total Liabilities") + 4, data[find_in_list_of_list(data, "Total Liabilities")], sub_header_underline)
    write_row(worksheet, find_in_list_of_list(data, "Net Assets") + 4, data[find_in_list_of_list(data, "Net Assets")], sub_header_underline)
    write_row(worksheet, find_in_list_of_list(data, "Total Equity") + 4, data[find_in_list_of_list(data, "Total Equity")], sub_header_underline)

    # Set colunm width
    worksheet.set_column(0, 0, 23.14)
    worksheet.set_column(1, 2, 13.57)

    writer.save()
