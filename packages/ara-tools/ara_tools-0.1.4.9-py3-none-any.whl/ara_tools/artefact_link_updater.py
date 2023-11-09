import os
import re


class ArtefactLinkUpdater:
   
    def __init__(self, file_system=None):
        self.file_system = file_system or os
    # with optional ":"
    def update_links_in_related_artefacts(self, old_name, new_name, dir_path):
       
    #    CHANGES MADE START
        new_name_formatted = new_name.replace('_', ' ').capitalize()

    #    CHANGES MADE END
        old_name_pattern = re.compile(f"\\b{old_name.replace(' ', '[ _]').replace('_', '[ _]')}\\b", re.IGNORECASE)

        patterns = {
            re.compile(f"Contributes to:?[ ]+([A-Za-z ]+)?{old_name_pattern.pattern}", re.IGNORECASE): f"Contributes to: \\1{new_name_formatted}",
            re.compile(f"Illustrates:?[ ]+([A-Za-z ]+)?{old_name_pattern.pattern}", re.IGNORECASE): f"Illustrates \\1{new_name_formatted}"
        }

        # Iterate over all items in the directory
        for item in self.file_system.listdir(dir_path):
            item_path = self.file_system.path.join(dir_path, item)
            
            # Check if it's a directory, then recurse
            if self.file_system.path.isdir(item_path):
                self.update_links_in_related_artefacts(old_name, new_name, item_path)
            
            # Check if it's a file and not a directory
            elif self.file_system.path.isfile(item_path):
                # Read the content of the file
                with open(item_path, 'r') as file:
                    content = file.read()
                
                # Replace all occurrences of the old name with the new name using regular expressions
                for pattern, new in patterns.items():
                    content = pattern.sub(new, content)
                
                # Write the updated content back to the file
                with open(item_path, 'w') as file:
                    file.write(content)


