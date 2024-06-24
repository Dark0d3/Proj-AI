import subprocess
from api import send_request
from commands import check_prompt_type,create_structure,extract_code,write_to_file
import json
import os

import spacy

# Load the trained model
nlp = spacy.load("FileStructures_spacy/model/")

history = []
structpath = None
copy_mem=[]

def process_input():
    prompt = input("Enter your prompt: ")
    if prompt.lower() == "/bye":
        return False  # Signal the program to exit

    if "memorize" in prompt:
        history.append(prompt)
        final_prompt = "\n".join(history)
    else:
        final_prompt = prompt

    category = check_prompt_type(final_prompt)
    action = category_actions.get(category, handle_default)
    action(final_prompt)
    return True

def handle_api_response(prompt):
    """ Send request to API and handle the response. """
    response = send_request(prompt)
    if response.status_code == 200:
        data = response.json()
        doc = nlp(data['response'])
        copy_mem.append(data['response'])
        category, score = max(doc.cats.items(), key=lambda item: item[1])
        print(f"Categoryfilestruct: {category}, Score: {score}")
        result = data['response']
        print(result)
        if category == "DIRECTORYSTRUCT" and score > 0.5:
            stucturecreate=input("Found Directory Structure do you want to create?(y/n)")
            if stucturecreate == "y":
                structpath = input("give desired path")
                code = extract_code(result)
                print("Created structure"+code)
                create_structure(code,structpath)

    else:
        print("Failed to get a valid response from the server.")

def execute_windows_command(command):
    """ Execute a Windows command and handle the output. """
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True, shell=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("An error occurred while executing the command:", e)

def handle_command(prompt):
    """ Handle command-type inputs and execute them as Windows commands. """
    # Constructing the command for Windows CMD
    windows_command = f"cmd /c {prompt}"
    execute_windows_command(windows_command)

def handle_query(prompt):
    """ Queries are handled by making an API call. """
    handle_api_response(prompt)


def handle_documentation(prompt):
    """ Create documentation for the entire project by appending all code to the prompt and writing to a new file. """
    try:
        project_path = input("Enter the path to the project directory: ")
        if not os.path.exists(project_path):
            print(f"Project directory {project_path} not found.")
            return

        all_code = []
        
        # Recursive function to collect code from all files in the project directory
        def collect_code(directory):
            for dirpath, _, filenames in os.walk(directory):
                for filename in filenames:
                    if filename.endswith(('.py', '.cs', '.java', '.csproj', '.cpp')):  # Adjust file extensions as needed
                        file_path = os.path.join(dirpath, filename)
                        with open(file_path, 'r') as file:
                            file_contents = file.read()
                            all_code.append(file_contents)

        collect_code(project_path)
        
        # Append all collected code to the prompt
        full_prompt = "\n".join(all_code) + "\n" + prompt + "\nProvide an overview of this project without explaining each method or code."
        
        # Process the full prompt (including all code)
        handle_api_response(full_prompt)
        
        if not copy_mem:
            print("No data to write.")
            return

        # Write the response to a new file
        doc_file_path = os.path.join(project_path, 'project_overview.txt')
        try:
            with open(doc_file_path, 'w') as file:
                for content in copy_mem:
                    file.write(content)
                    file.write("\n")
            print(f"Project overview written to {doc_file_path} successfully.")
        except Exception as e:
            print(f"Failed to write to file: {e}")

    except Exception as e:
        print(f"An error occurred: {e}")

def handle_read_task(prompt):
    """ Read file specified in the prompt and append its contents to history. """
    try:
        # Assuming the file path is always at the end of the prompt for simplicity
        print("inside handle_read_task")
        file_path = prompt.split()[-1]
        with open(file_path, 'r') as file:
            file_contents = file.read()
            handle_api_response(file_contents+" "+ prompt+" always write code inside ```code ```")
            write_input=input("Do you want to write the output?(y/n)")
            if write_input == "y":
                print(copy_mem)
                write_to_file(file_path,copy_mem=copy_mem)

        #history.append(file_contents+" "+ prompt)
    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def handle_default(prompt):
    """ Default handler for unrecognized categories. """
    print("Prompt does not match known categories.")

category_actions = {
    "COMMAND": handle_command,
    "NOTACOMMAND": handle_query,
    "READ":handle_read_task,
    "DOCUMENTATION":handle_documentation
}

if __name__ == "__main__":
    while process_input():
        continue  # Keep processing until user types '/bye'
