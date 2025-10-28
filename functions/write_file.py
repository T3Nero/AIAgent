import os

def write_file(working_directory, file_path, content):
    try:
        root = os.path.abspath(working_directory)

        if os.path.isabs(file_path): file = os.path.abspath(file_path)
        else: file = os.path.abspath(os.path.join(working_directory, file_path))

        if os.path.commonpath([root, file]) != root:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(file):
            os.makedirs(os.path.dirname(file), exist_ok=True)
            with open(file, "w") as f:
                f.write(content)

                return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        else:
            with open(file, "w") as f:
                f.write(content)

                return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return f"Error: {e}" 