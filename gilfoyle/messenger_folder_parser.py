import os
from gilfoyle.messenger_openai_converter import MessageJSONParser
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class MessengerFolderParser:
    def __init__(self, folder_path: str, system_prompt: str, our_name: str):
        self.folder_path = folder_path
        self.system_prompt = system_prompt
        self.our_name = our_name
    
    def _parse_training_data(self):
        outputs = []
        for folder in os.listdir(self.folder_path):
            # first check that folder is actually a folder
            if not os.path.isdir(os.path.join(self.folder_path, folder)):
                continue
        
            conversation_outputs = []

            # check if 'message_01.json' is in `folder`
            if 'message_1.json' in os.listdir(os.path.join(self.folder_path, folder)):
                convert = MessageJSONParser(os.path.join(self.folder_path, folder, 'message_1.json'), self.system_prompt, self.our_name)
                message_outputs = convert.get_openai_message_format()
                for message_output in message_outputs:
                    if len(message_output) > 1:
                        output = {"messages": message_output}
                        conversation_outputs.append(output)

            outputs.extend(conversation_outputs)
            print(f"Processed folder: {folder}, {len(conversation_outputs)} messages")
        return outputs
    
    def get_training_data(self) -> List[Dict[str, Any]]:
        return self._parse_training_data()
