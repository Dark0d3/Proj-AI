import spacy
from spacy.training import Example

TRAIN_DATA = [
    ("Create a project structre in dotnet", {"entities": [(0, 6, "COMMAND"), (9, 25, "OBJECT_TYPE"), (28, 35, "OBJECT_NAME")]}),
    ("Create a folder named Projects", {"entities": [(0, 6, "COMMAND"), (9, 16, "OBJECT_TYPE"), (23, 31, "OBJECT_NAME")]}),
    ("Delete the file example.txt", {"entities": [(0, 6, "COMMAND"), (13, 17, "OBJECT_TYPE"), (18, 30, "OBJECT_NAME")]}),
    ("Move testfile to the Documents folder", {"entities": [(0, 4, "COMMAND"), (5, 14, "OBJECT_NAME"), (18, 32, "DESTINATION")]}),
    ("Open Photoshop", {"entities": [(0, 4, "COMMAND"), (5, 14, "APPLICATION")]}),
    ("Set volume to 50%", {"entities": [(0, 3, "COMMAND"), (4, 10, "SETTING"), (14, 18, "VALUE")]}),
    ("Restart the computer", {"entities": [(0, 7, "COMMAND"), (12, 20, "OBJECT")]}),
    ("Unzip archive.zip in the current directory", {"entities": [(0, 5, "COMMAND"), (6, 13, "OBJECT_NAME"), (17, 41, "LOCATION")]}),
    ("Rename the file report.docx to report_final.docx", {"entities": [(0, 6, "COMMAND"), (17, 26, "OBJECT_NAME"), (30, 48, "NEW_NAME")]}),
    ("Copy the folder Photos to the backup drive", {"entities": [(0, 4, "COMMAND"), (13, 19, "OBJECT_NAME"), (23, 34, "DESTINATION")]}),
    ("List all files in the Downloads folder", {"entities": [(0, 4, "COMMAND"), (18, 29, "LOCATION")]}),
    ("Create a zip file from the folder Reports", {"entities": [(0, 6, "COMMAND"), (12, 21, "OBJECT_TYPE"), (30, 37, "OBJECT_NAME")]}),
    ("Remove the directory old_backups", {"entities": [(0, 6, "COMMAND"), (16, 28, "OBJECT_NAME")]}),
    ("Display the contents of the folder Documents", {"entities": [(0, 7, "COMMAND"), (28, 36, "OBJECT_NAME")]}),
    ("Extract the zip file archive.zip to the desktop", {"entities": [(0, 7, "COMMAND"), (16, 24, "OBJECT_NAME"), (32, 40, "DESTINATION")]}),
]

# Load the blank model
nlp = spacy.blank('en')

# Set up the pipeline
if 'ner' not in nlp.pipe_names:
    ner = nlp.create_pipe('ner')
    nlp.add_pipe('ner')
else:
    ner = nlp.get_pipe('ner')

# Add new entity labels to the NER
for _, annotations in TRAIN_DATA:
    for ent in annotations['entities']:
        ner.add_label(ent[2])

# Training the NER model
other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
with nlp.disable_pipes(*other_pipes):  # only train NER
    optimizer = nlp.begin_training()
    for itn in range(30):  # More iterations might be needed for a real scenario
        for text, annotations in TRAIN_DATA:
            doc = nlp.make_doc(text)
            example = Example.from_dict(doc, annotations)
            nlp.update([example], sgd=optimizer)

nlp.to_disk('Spacymodels/')



