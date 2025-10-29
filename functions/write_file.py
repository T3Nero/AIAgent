import os
from google.genai import types

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

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes specified content to an existing file or creates a file if it does not already exist, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the file we wish to write content into, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content we want to be written into the file, relative to the file path"
            )
        },
    ),
) 