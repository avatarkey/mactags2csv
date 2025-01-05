import subprocess
import csv

# Output CSV file
output_file = "tagged_files.csv"

# Tags to exclude
exclude_tags = ["Red", "Blue", "Yellow", "Orange", "Purple", "Green", "Gray", "Work"]  # Add the tags you want to exclude here


# Write CSV header
with open(output_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Tag", "File Name", "Date Created", "File Size", "File Type"])

# Build the mdfind query to exclude specific tags
query = "kMDItemUserTags == '*'"
for tag in exclude_tags:
    query += f" && kMDItemUserTags != '{tag}'"

# Find all files with any tag except the excluded ones
result = subprocess.run(["mdfind", query], capture_output=True, text=True)
files = result.stdout.splitlines()

# Loop through each file
for file_path in files:
    # Get the tags for the file
    tags_result = subprocess.run(["mdls", "-name", "kMDItemUserTags", file_path], capture_output=True, text=True)
    tags_output = tags_result.stdout.strip()
    
    # Extract tags from the output
    if tags_output.startswith("kMDItemUserTags = ("):
        tags = tags_output.split("(", 1)[1].rsplit(")", 1)[0]  # Extract content inside parentheses
        tags = tags.replace('"', "").replace(", ", ",")  # Clean up tags
    else:
        tags = ""  # No tags found

    # Get file details
    file_name = file_path.split("/")[-1]
    date_created = subprocess.run(["mdls", "-name", "kMDItemFSCreationDate", file_path], capture_output=True, text=True).stdout.split("= ")[1].strip()
    file_size = subprocess.run(["mdls", "-name", "kMDItemFSSize", file_path], capture_output=True, text=True).stdout.split("= ")[1].strip()
    file_type = subprocess.run(["mdls", "-name", "kMDItemKind", file_path], capture_output=True, text=True).stdout.split("= ")[1].strip().strip('"')

    # Append to CSV
    with open(output_file, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([tags, file_name, date_created, file_size, file_type])

print(f"CSV file created: {output_file}")