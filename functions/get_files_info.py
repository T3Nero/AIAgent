import os
from config import *
from google.genai import types

def get_files_info(working_directory, directory="."):
    try:
        root = os.path.abspath(working_directory)
        target = os.path.abspath(os.path.join(working_directory, directory))

        
        if os.path.commonpath([root, target]) != root:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        if not os.path.isdir(target):
            return f'Error: "{directory}" is not a directory'
        
        lines = []
        for name in os.listdir(target):
            path = os.path.join(target, name)
            is_dir = os.path.isdir(path)
            size = os.path.getsize(path)
            lines.append(f'- {name}: file_size={size} bytes, is_dir={is_dir}')

        return "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"
    

def get_file_content(working_directory, file_path):
    try:
        root = os.path.abspath(working_directory)
        file = os.path.abspath(os.path.join(working_directory, file_path))

        if os.path.commonpath([root, file]) != root:
            f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(file):
            f'Error: File not found or is not a regular file: "{file_path}"'

        truncate_string = ""
        with open(file, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            words = file_content_string.split()

            if len(words) > MAX_CHARS:
                truncate_string = "\n" + f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

            return file_content_string + truncate_string
            





    except Exception as e:
        return f"Error: {e}"
    

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read the contents in the specified file path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the content we wish to read, relative to the working directory",
            ),
        },
    ),
)