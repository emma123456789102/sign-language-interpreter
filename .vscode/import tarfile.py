import tarfile

# Path to your uploaded file
file_path = "C:\Users\Emma Davidson\Downloads\com.xreal.xr.tar.gz"
extract_to = "/workspaces/sign-language-interpreter/unity/.vscode/com_xreal_xr_extracted"

# Extract
with tarfile.open(file_path, "r:gz") as tar:
    tar.extractall(path=extract_to)

print(f"Extracted to: {extract_to}")
