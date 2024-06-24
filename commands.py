import re
import subprocess
import spacy
import os
from defaultCodeSnippets import default_code_snippets,default_code_snippets_dotnet

# Load the trained model
nlp = spacy.load("spacymodels/")

prompt_type_spacy= spacy.load("Operations_spacy/model/")

def execute_command(command):
    try:
        command="touch newfile.txt"
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout if result.stdout else "Command executed successfully, no output."
    except subprocess.CalledProcessError as e:
        return f"Error occurred: {e.stderr}"

def extract_code(text):
    match = re.search(r"```([^`]+)```", text)
    return match.group(1) if match else ""

def translate_to_command(text):
    doc = nlp(text)
    print(doc.ents)
    command_parts = {ent.label_: ent.text for ent in doc.ents}
    command = ""
    # Example command translation logic, adjust based on actual model and needs
    if "COMMAND" in command_parts and "OBJECT_NAME" in command_parts:
        if command_parts["COMMAND"].lower() == "create" and "folder" in doc.text.lower():
            command = f"mkdir {command_parts['OBJECT_NAME']}"
    return command if command else "Command not recognized"


def contains_os_command(text):
    # List of OS commands to check for
    os_commands = ['mkdir', 'cd', 'pwd', 'ls', 'rm', 'cp', 'mv', 'chmod', 'chown', 'echo', 'touch']
    
    # Use regex to find any of the OS commands in the input text
    pattern = r'\b(' + '|'.join(os_commands) + r')\b'
    matches = re.findall(pattern, text)
    
    return matches if matches else None

def check_prompt_type(text):
    doc = prompt_type_spacy(text)
    category, score = max(doc.cats.items(), key=lambda item: item[1])
    print(f"Category: {category}, Score: {score}")
    if score < 0.5:
        category="NOTACOMMAND"
    return category

def sanitize_name(name):
    """Sanitize the folder or file name by removing spaces and non-alphanumeric characters, and ignoring descriptions."""
    # Strip out the description in parentheses if present
    name = re.sub(r'\s+\(.*?\)$', '', name)
    name = re.sub(r'//.*$', '', name)
    name = re.sub(r'#.*$', '', name)
    # Replace spaces with underscores and remove non-alphanumeric characters except underscores and hyphens
    sanitized_name = re.sub(r'\s+', '_', name)  # Replace spaces with underscores
    sanitized_name = re.sub(r'[^\w\s.-]', '', sanitized_name)  # Keep periods and hyphens
    return sanitized_name


def generate_cs_content(filename, path):
    """Generate C# class content dynamically based on file and directory names."""
    class_name = os.path.splitext(filename)[0]
    namespace = os.path.basename(os.path.normpath(path))
    return f"namespace {namespace}\n{{\n    public class {class_name}\n    {{\n        // Add properties and methods here\n    }}\n}}\n"



def create_structure(structure, root_path='.'):
    lines = structure.split('\n')
    path_stack = [root_path if root_path else '.']

    for line in lines:
        depth = line.count('│')
        while len(path_stack) > depth + 1:
            path_stack.pop()

        if '└──' in line or '├──' in line:
            name = line.split('└──')[-1].split('├──')[-1].strip()
            sanitized_name = sanitize_name(name)
            current_path = os.path.join(path_stack[-1], sanitized_name)
            file_extension = os.path.splitext(sanitized_name)[1]

            if file_extension == '.cs':
                print(sanitized_name)
                if sanitized_name in default_code_snippets_dotnet:
                    content= default_code_snippets_dotnet[sanitized_name]
                else:
                    content = generate_cs_content(sanitized_name, path_stack[-1])
            elif file_extension in default_code_snippets:
                content = default_code_snippets[file_extension]
            else:
                content = None

            if content:
                os.makedirs(os.path.dirname(current_path), exist_ok=True)
                with open(current_path, 'w') as file:
                    file.write(content)
                print(f"Created {current_path} with appropriate content.")
            elif file_extension:  # It's a file but no default content
                os.makedirs(os.path.dirname(current_path), exist_ok=True)
                open(current_path, 'w').close()
                print(f"Created empty file {current_path}.")
            else:  # It's a directory
                os.makedirs(current_path, exist_ok=True)
                path_stack.append(current_path)
                print(f"Created directory {current_path}.")


def write_to_file(filename,copy_mem):
    """Writes contents of copy_mem to a file."""
    print("Attempting to write data:", copy_mem)
    if not copy_mem:
        print("No data to write.")
        return

    try:
        with open(filename, 'w') as file:
            for content in copy_mem:
                print(extract_code(content))
                file.write(extract_code(content))
        print(f"Data written to {filename} successfully.")
    except Exception as e:
        print(f"Failed to write to file: {e}")
