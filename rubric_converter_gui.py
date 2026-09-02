import json
import csv
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk


def convert_rubric_to_csv_or_excel(input_json_path, output_path, output_format):
    with open(input_json_path, 'r') as file:
        rubric_data = json.load(file)
    
    rubric_scale_section = rubric_data['Ratings']
    column_headers = ['Criteria']
    for scale in rubric_scale_section:
        column_headers.append(scale["Rating"])
    column_headers.append('Marks')
    
    rubric_criterion_section = rubric_data['Criteria']
    rows = []
    for criterion in rubric_criterion_section:
        print(criterion)
        if use_name_and_value.get():
            row = [f"{criterion['Criteria']} ({criterion['MaxMark']})"]
        else:
            row = [criterion['Criteria']]
        #row = [criterion['description']]
        row.extend([''] * (len(column_headers) - 1))
        rows.append(row)

    rubric_criterion_scale_section = rubric_data['Criteria']
    criterion_id_to_row_index = {criterion['CriteriaIndex']: index for index, criterion in enumerate(rubric_criterion_section)}
    scale_value_id_to_column_index = {scale["RatingIndex"]: index + 1 for index, scale in enumerate(rubric_scale_section)}

    for entry in rubric_criterion_scale_section:
        row_index = criterion_id_to_row_index[entry['CriteriaIndex']]
        for category in entry['Descriptors']:
            if len(category) != 0:
                column_index = scale_value_id_to_column_index[category['RatingIndex']]
                rows[row_index][column_index] = category['Text']
        rows[row_index][max(scale_value_id_to_column_index.values()) + 1] = entry["MaxMark"]
    
    if output_format == 'CSV':
        with open(output_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(column_headers)
            writer.writerows(rows)
    elif output_format == 'Excel':
        df = pd.DataFrame(rows, columns=column_headers)
        df.to_excel(output_path, index=False)
    
    print("File has been successfully saved at:", output_path)

def select_input_file():
    file_path = filedialog.askopenfilename(filetypes=[("Rubric Files", "*.rbc"), ("All Files", "*.*")])
    input_file_entry.delete(0, tk.END)
    input_file_entry.insert(0, file_path)

def select_output_file():
    output_format = output_format_var.get()
    if output_format == 'CSV':
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")])
    elif output_format == 'Excel':
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx"), ("All Files", "*.*")])
    output_file_entry.delete(0, tk.END)
    output_file_entry.insert(0, file_path)

def run_conversion():
    input_file_path = input_file_entry.get()
    output_file_path = output_file_entry.get()
    output_format = output_format_var.get()
    convert_rubric_to_csv_or_excel(input_file_path, output_file_path, output_format)
    messagebox.showinfo("Success", "File has been successfully saved at:\n" + output_file_path)

# Create the main window
root = tk.Tk()
root.title("Rubric Converter")
use_name_and_value = tk.BooleanVar()

# Create and place the elements
tk.Label(root, text="Select Input .rbc File:").pack(pady=10)
input_file_entry = tk.Entry(root, width=50)
input_file_entry.pack(pady=5)
tk.Button(root, text="Browse", command=select_input_file).pack(pady=5)

tk.Label(root, text="Select Output File:").pack(pady=10)
output_file_entry = tk.Entry(root, width=50)
output_file_entry.pack(pady=5)
tk.Button(root, text="Browse", command=select_output_file).pack(pady=5)

tk.Label(root, text="Select Output Format:").pack(pady=10)
output_format_var = tk.StringVar()
output_format_var.set("CSV")
output_format_menu = ttk.Combobox(root, textvariable=output_format_var, values=("CSV", "Excel"))
output_format_menu.pack(pady=5)

tk.Checkbutton(root, text="Use name + value instead of description for Criteria ", variable=use_name_and_value).pack(pady=10)


tk.Button(root, text="Convert", command=run_conversion).pack(pady=20)

# Run the main loop
root.mainloop()
