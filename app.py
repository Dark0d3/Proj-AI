import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit,
    QVBoxLayout, QHBoxLayout, QMessageBox, QFileDialog
)
import requests
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import speech_recognition as sr
import subprocess
from api import send_request
from commands import check_prompt_type, create_structure, extract_code, write_to_file
import os
import spacy

# Load the trained model
nlp = spacy.load("FileStructures_spacy/model/")

history = []
structpath = None
copy_mem = []

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Proj-AI'
        self.icon_name = 'favicon.png'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon(self.icon_name))
        self.setGeometry(100, 100, 800, 600)

        # Set layout
        main_layout = QVBoxLayout()
        response_layout = QVBoxLayout()
        prompt_layout = QHBoxLayout()

        # Response display
        self.response_text = QTextEdit(self)
        self.response_text.setReadOnly(True)
        response_layout.addWidget(self.response_text)

        # Prompt input
        self.prompt_entry = QLineEdit(self)
        self.prompt_entry.setPlaceholderText("Enter your prompt...")
        prompt_layout.addWidget(self.prompt_entry)

        # Speech input button
        speech_button = QPushButton(self)
        speech_button.setIcon(QIcon('mic_icon.png'))  # Ensure you have a mic icon image named mic_icon.png
        speech_button.clicked.connect(self.recognize_speech)
        prompt_layout.addWidget(speech_button)

        # Submit button
        submit_button = QPushButton(self)
        submit_button.setIcon(QIcon('submit_icon.png'))  # Ensure you have a submit arrow icon image named submit_icon.png
        submit_button.clicked.connect(self.get_ai_response)
        prompt_layout.addWidget(submit_button)

        main_layout.addLayout(response_layout)
        main_layout.addLayout(prompt_layout)

        self.setLayout(main_layout)

    def get_ai_response(self):
        prompt = self.prompt_entry.text()
        if not prompt:
            QMessageBox.critical(self, "Input Error", "Please enter a prompt.")
            return

        if "memorize" in prompt:
            history.append(prompt)
            final_prompt = "\n".join(history)
        else:
            final_prompt = prompt

        category = check_prompt_type(final_prompt)
        action = category_actions.get(category, self.handle_default)
        action(self, final_prompt)

    def handle_api_response(self, prompt):
        """ Send request to API and handle the response. """
        try:
            response = send_request(prompt)
            if response.status_code == 200:
                data = response.json()
                doc = nlp(data['response'])
                copy_mem.append(data['response'])
                category, score = max(doc.cats.items(), key=lambda item: item[1])
                self.response_text.append(f"Categoryfilestruct: {category}, Score: {score}")
                result = data['response']
                self.response_text.append(result)
                if category == "DIRECTORYSTRUCT" and score > 0.5:
                    structure_create = self.show_yes_no_dialog("Found Directory Structure. Do you want to create?")
                    if structure_create:
                        structpath = self.get_directory_path()
                        if structpath:
                            code = extract_code(result)
                            self.response_text.append(f"Created structure: {code}")
                            create_structure(code, structpath)
            else:
                self.response_text.append("Failed to get a valid response from the server.")
        except requests.RequestException as e:
            self.response_text.append(f"Request Exception: {e}")
        except ValueError as e:
            self.response_text.append(f"ValueError: {e}")
        except Exception as e:
            self.response_text.append(f"An unexpected error occurred: {e}")

    def show_yes_no_dialog(self, message):
        reply = QMessageBox.question(self, 'Message', message, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        return reply == QMessageBox.Yes

    def get_directory_path(self):
        try:
            path = QFileDialog.getExistingDirectory(self, "Select Directory")
            if path:
                return path
            else:
                return None
        except Exception as e:
            self.response_text.append(f"An error occurred while selecting directory: {e}")
            return None

    def recognize_speech(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            try:
                audio = recognizer.listen(source)
                speech_text = recognizer.recognize_google(audio)
                self.prompt_entry.setText(speech_text)
            except sr.UnknownValueError:
                QMessageBox.critical(self, "Speech Recognition Error", "Could not understand audio")
            except sr.RequestError:
                QMessageBox.critical(self, "Speech Recognition Error", "Could not request results from the speech recognition service")
            except Exception as e:
                QMessageBox.critical(self, "Speech Recognition Error", f"An error occurred: {e}")

    def execute_windows_command(self, command):
        """ Execute a Windows command and handle the output. """
        try:
            result = subprocess.run(command, check=True, text=True, capture_output=True, shell=True)
            self.response_text.append(result.stdout)
        except subprocess.CalledProcessError as e:
            self.response_text.append(f"An error occurred while executing the command: {e}")
        except Exception as e:
            self.response_text.append(f"An unexpected error occurred: {e}")

    def handle_command(self, prompt):
        """ Handle command-type inputs and execute them as Windows commands. """
        try:
            windows_command = f"cmd /c {prompt}"
            self.execute_windows_command(windows_command)
        except Exception as e:
            self.response_text.append(f"An unexpected error occurred: {e}")

    def handle_query(self, prompt):
        """ Queries are handled by making an API call. """
        try:
            self.handle_api_response(prompt)
        except Exception as e:
            self.response_text.append(f"An unexpected error occurred: {e}")

    def handle_documentation(self, prompt):
        """ Create documentation for the entire project by appending all code to the prompt and writing to a new file. """
        try:
            project_path = self.get_directory_path()
            if not project_path:
                self.response_text.append(f"Project directory not found.")
                return

            all_code = []
            def collect_code(directory):
                for dirpath, _, filenames in os.walk(directory):
                    for filename in filenames:
                        if filename.endswith(('.py', '.cs', '.java', '.csproj', '.cpp')):
                            file_path = os.path.join(dirpath, filename)
                            with open(file_path, 'r', errors='ignore') as file:
                                file_contents = file.read()
                                all_code.append(file_contents)

            collect_code(project_path)
            full_prompt = "\n".join(all_code) + "\n" + prompt + "\nProvide an overview of this project without explaining each method or code."
            self.handle_api_response(full_prompt)
            if not copy_mem:
                self.response_text.append("No data to write.")
                return

            doc_file_path = os.path.join(project_path, 'project_overview.txt')
            try:
                with open(doc_file_path, 'w', errors='ignore') as file:
                    for content in copy_mem:
                        file.write(content)
                        file.write("\n")
                self.response_text.append(f"Project overview written to {doc_file_path} successfully.")
            except Exception as e:
                self.response_text.append(f"Failed to write to file: {e}")
        except Exception as e:
            self.response_text.append(f"An unexpected error occurred: {e}")

    def handle_read_task(self, prompt):
        """ Read file specified in the prompt and append its contents to history. """
        try:
            file_path = prompt.split()[-1]
            with open(file_path, 'r', errors='ignore') as file:
                file_contents = file.read()
                self.handle_api_response(file_contents + " " + prompt + " always write code inside ```code ```")
                write_input = self.show_yes_no_dialog("Do you want to write the output?")
                if write_input:
                    write_to_file(file_path, copy_mem)
        except FileNotFoundError as e:
            self.response_text.append(f"File {file_path} not found: {e}")
        except Exception as e:
            self.response_text.append(f"An unexpected error occurred: {e}")

    def handle_default(self, prompt):
        """ Default handler for unrecognized categories. """
        self.response_text.append("Prompt does not match known categories.")

category_actions = {
    "COMMAND": App.handle_command,
    "NOTACOMMAND": App.handle_query,
    "READ": App.handle_read_task,
    "DOCUMENTATION": App.handle_documentation
}

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Apply QSS style
    with open("style.qss", "r", errors='ignore') as file:
        app.setStyleSheet(file.read())

    ex = App()
    ex.show()
    sys.exit(app.exec_())
