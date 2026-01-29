"""
The `Model` class is an interface between the ML model that you're packaging and the model
server that you're running it on.

The main methods to implement here are:
* `load`: runs exactly once when the model server is spun up or patched and loads the
   model onto the model server. Include any logic for initializing your model, such
   as downloading model weights and loading the model into memory.
* `predict`: runs every time the model server is called. Include any logic for model
  inference and return the model output.

See https://truss.baseten.co/quickstart for more.
"""
from transformers import pipeline

CATEGORIES = [
    "Password Issue",
    "App Navigation",
    "Device Setup",
    "Email Problem",
    "Security Concern",
    "Hardware Issue",
    "Software Update",
    "Connectivity Problem",
    "Performance Issue",
    "Installation Help",
    "Other"
]


class Model:
    def __init__(self, **kwargs):
        self.classifier = None

    def load(self):
        # Load zero-shot classifier
        try:
            self.classifier = pipeline(
                "zero-shot-classification",
                model="MoritzLaurer/deberta-v3-base-zeroshot-v2.0"
            )
        except Exception as e:
            self.classifier = None
            print(f"Failed to load classifier pipeline: {e}")

    def predict(self, input):
        # Classify
        if self.classifier is None:
            raise RuntimeError("Classifier pipeline is not loaded.")
        result = self.classifier(input, candidate_labels=CATEGORIES)

        return {
            "category": result["labels"][0],
            "confidence": round(result["scores"][0], 4)
        }
