import sys
import os
import csv

# Check if folder path and output file name are provided as arguments
if len(sys.argv) != 3:
    print("Please provide the folder path and output file name as arguments.")
    print("Example: ./merge_csv.py /path/to/folder merged_output.csv")
    sys.exit(1)

# Get the folder path and output file name from the arguments
folder_path = sys.argv[1]
output_file = sys.argv[2]

# Check if the provided folder path exists
if not os.path.isdir(folder_path):
    print(f"Folder not found: {folder_path}")
    sys.exit(1)

# Define the full path for the output file
output_path = os.path.join(folder_path, output_file)

# Merge CSV files
merged_data = []
for file_name in os.listdir(folder_path):
    if file_name.endswith(".csv"):
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, "r") as file:
            csv_reader = csv.reader(file)
            merged_data.extend(csv_reader)

# Remove duplicates
merged_data = list(set(tuple(row) for row in merged_data))

# Save merged data to the output file
with open(output_path, "w", newline="") as file:
    csv_writer = csv.writer(file)
    csv_writer.writerows(merged_data)

print(f"Merged CSV files saved to: {output_path}")
