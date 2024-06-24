import spacy
from spacy.util import minibatch, compounding
from spacy.training import Example
from training_data import TRAIN_DATA

# Create a blank English NLP object
nlp = spacy.blank("en")

# Define the configuration for the TextCategorizer
config = {
    "model": {
        "@architectures": "spacy.TextCatEnsemble.v2",
        "linear_model": {
            "@architectures": "spacy.TextCatBOW.v3",
            "exclusive_classes": True,
            "ngram_size": 1,
            "no_output_layer": False
        },
        "tok2vec": {
            "@architectures": "spacy.Tok2Vec.v2",
            "embed": {
                "@architectures": "spacy.MultiHashEmbed.v2",
                "width": 64,
                "rows": [2000, 2000, 500, 1000, 500],
                "attrs": ["NORM", "LOWER", "PREFIX", "SUFFIX", "SHAPE"],
                "include_static_vectors": False
            },
            "encode": {
                "@architectures": "spacy.MaxoutWindowEncoder.v2",
                "width": 64,
                "window_size": 1,
                "maxout_pieces": 3,
                "depth": 2
            }
        }
    },
    "threshold": 0.0
}

# Add the TextCategorizer to the pipeline with the configuration
textcat = nlp.add_pipe("textcat", config=config)

# Add labels to the text classifier
textcat.add_label("DIRECTORYSTRUCT")
textcat.add_label("NOTDIRECTORYSTRUCT")

# Create the training data examples
train_data = [Example.from_dict(nlp.make_doc(text), cats) for text, cats in TRAIN_DATA]

# Train the model
def train_model(nlp, train_data):
    optimizer = nlp.initialize()
    for i in range(10):
        losses = {}
        batches = minibatch(train_data, size=compounding(4.0, 32.0, 1.001))
        for batch in batches:
            for example in batch:
                nlp.update([example], sgd=optimizer, drop=0.5, losses=losses)
        print(f"Losses at iteration {i}: {losses}")

train_model(nlp, train_data)
nlp.to_disk("model/")
