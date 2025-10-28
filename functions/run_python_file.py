import os, subprocess, sys

def run_python_file(working_directory, file_path, args=[]):
    try:
        root = os.path.abspath(working_directory)
        file = os.path.abspath(file_path) if os.path.isabs(file_path) else os.path.abspath(os.path.join(root, file_path))

        if os.path.commonpath([root, file]) != root:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(file):
            return f'Error: File "{file_path}" not found.'

        if not file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'
       
        completed_process = subprocess.run([sys.executable, file, *args], 
                                 cwd=root, 
                                 timeout=30, 
                                 capture_output=True, 
                                 text=True, 
                                 check=False)
        
        if not completed_process.stdout and not completed_process.stderr:
            return "No output produced."
        
        parts = [f"STDOUT: {completed_process.stdout}", f"STDERR: {completed_process.stderr}"]
        if completed_process.returncode != 0:
            parts.append(f"Process exited with code {completed_process.returncode}")
        return "\n".join(parts)

        
    
    except Exception as e:
        return f"Error: executing Python file: {e}"