import os
import json

output_dir = "output_files"

# Create the directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)
with open(r"C:\Users\User\PycharmProjects\YedidAI\data\dataset.json", "r", encoding="utf-8") as file:
    list_of_dicts = json.load(file)
# Loop through the list and write each dictionary to a separate file
for i, dictionary in enumerate(list_of_dicts):
    file_path = os.path.join(output_dir, f"dict_{i+1}.txt")
    with open(file_path, "w") as file:
        json.dump(dictionary, file, indent=4, ensure_ascii=False)

print("Dictionaries have been written to text files.")