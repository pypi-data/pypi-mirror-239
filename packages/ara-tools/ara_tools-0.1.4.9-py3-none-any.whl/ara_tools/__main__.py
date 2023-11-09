import os
import sys
import argparse
from .file_creator import FileCreator
from .artefact_renamer import ArtefactRenamer
from .filename_validator import is_valid_filename
from .classifier_validator import is_valid_classifier
from .template_manager import SpecificationBreakdownAspects

def cli():
    parser = argparse.ArgumentParser(description="Ara tools for creating files and directories.")
    parser.add_argument("action", help="Action to perform (e.g. 'create', 'delete', 'list','rename')")
    parser.add_argument("parameter", help="Filename for create/delete/rename action, or tags for list action", nargs="?")
    parser.add_argument("classifier", help="Classifier for the file to be created/deleted/renamed", nargs="?")
    parser.add_argument("aspect", help="Specification breakdown aspect", nargs="?")
    

    args = parser.parse_args()

    file_creator = FileCreator()
    artefact_renamer = ArtefactRenamer()

    if args.action.lower() == "create":
        if args.parameter and args.classifier and args.aspect:
            sba = SpecificationBreakdownAspects()
            try:
                sba.create(args.parameter, args.classifier, args.aspect)
            except ValueError as ve:
                print(f"Error: {ve}")
                sys.exit(1)
            return
        if not is_valid_filename(args.parameter):  # Assuming first parameter as filename
            print("Invalid filename provided. Please provide a valid filename.")
            sys.exit(1)

        if not is_valid_classifier(args.classifier):
            print("Invalid classifier provided. Please provide a valid classifier.")
            sys.exit(1)

        template_path = os.path.join(os.path.dirname(__file__), 'templates')
        print(f"in __main__ file_creator.run called with {args.parameter}, {args.classifier} and {template_path}")
        file_creator.run(args.parameter, args.classifier, template_path)
    elif args.action.lower() == "delete":
        file_creator.delete(args.parameter, args.classifier)

    elif args.action.lower() == "rename":
        
        if not is_valid_filename(args.parameter):  # Assuming first parameter as filename
            print("Invalid filename provided. Please provide a valid filename.")
            sys.exit(1)

        if not is_valid_classifier(args.classifier):
            print("Invalid classifier provided. Please provide a valid classifier.")
            sys.exit(1)

        if not is_valid_filename(args.aspect):  # Assuming aspect is the new name
            print("Invalid new filename provided. Please provide a valid filename.")
            sys.exit(1)

        artefact_renamer.rename(args.parameter,args.aspect, args.classifier)
        
    elif args.action.lower() == "list":
        if args.parameter:
            tags = args.parameter
            file_creator.list_files(tags=tags)
        else:
            file_creator.list_files()
    else:
        print("Invalid action provided. Type ara -h for help")
        sys.exit(1)

if __name__ == "__main__":
    cli()
