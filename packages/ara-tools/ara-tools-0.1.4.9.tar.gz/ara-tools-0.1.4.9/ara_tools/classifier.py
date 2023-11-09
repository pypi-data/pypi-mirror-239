class Classifier:

    valid_classifiers = {
        "vision": "vision",
        "businessgoal": "goals",
        "capability": "capabilities",
        "keyfeature": "keyfeatures",
        "feature": "features",
        "epic": "epics",
        "story": "stories",
        "task": "tasks",
        "tasklist": "tasks",
        "example": "examples",
    }
    
    classifier_order = [
        "vision",
        "businessgoal",
        "capability",
        "keyfeature",
        "epic",
        "story",
        "example",
        "feature",
        "task",
        "tasklist",
        "issue",
    ]

    artefact_title = {
        "vision": "Vision statement",
        "businessgoal": "Business goal",
        "capability": "Capability",
        "keyfeature": "Key feature",
        "epic": "Epic",
        "story": "User story",
        "example": "Example",
        "feature": "Feature",
        # Use a non-capturing group for "Task list" or "Task" to ensure the capturing group is consistent
        "task": "(?:Task list|Task)"
    }



    @staticmethod
    def get_sub_directory(classifier):
        return Classifier.valid_classifiers.get(classifier)

    @staticmethod
    def is_valid_classifier(classifier):
        return classifier in Classifier.valid_classifiers

    @staticmethod
    def ordered_classifiers():
        return Classifier.classifier_order

    @staticmethod
    def get_artefact_title(classifier):
        return Classifier.artefact_title.get(classifier)
