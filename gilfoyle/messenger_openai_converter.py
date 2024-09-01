import json
from typing import List, Dict, Optional
from gilfoyle.messenger_data_pruning import MessengerPruner

MAX_MESSAGE_LENGTH = 2000

class MessageJSONParser:
    """
    Parses a JSON file containing messages from Facebook Messenger.
    """
    def __init__(self, json_file: str, system_prompt_file: str, our_name: str):
        self.json_file = json_file
        self.system_prompt_file = system_prompt_file
        self.our_name = our_name
        self.data = {}
        self.system_prompt = None

    def _read_json(self):
        """
        Reads the JSON file and stores the data in the instance variable.
        """
        with open(self.json_file, 'r', encoding='utf-8') as file:
            raw_data = file.read()
            data = json.loads(raw_data)
        self.data = data
    
    def _read_system_prompt(self):
        """
        Reads the system prompt file and stores the prompt in the instance variable.
        """
        with open(self.system_prompt_file, 'r') as file:
            self.system_prompt = file.read()
    
    def _get_message_text(self, message: Dict) -> Optional[Dict[str, str]]:
        """
        Extracts the text and sender from a message dictionary if it contains text content.
        Ignores messages with photos or shares.
        """
        if 'photos' in message or 'share' in message:
            return None
        
        if 'content' not in message:
            return None

        return {
            'text': message['content'].encode('latin1').decode('utf8'),
            'sender': message['sender_name']
        }

    def _parse_messages(self) -> List[Dict[str, str]]:
        """
        Parses the messages from the JSON file. Converts them to a format where it is 
        [
            {
                'question': '...',
                'answer': '...',
            }
        ]

        """

        if len(self.data) == 0:
            self._read_json()
        
        if self.system_prompt is None:
            self._read_system_prompt()
        
        # TODO: @avyayv figure out how to handle group chats
        if len(self.data['participants']) != 2:
            return []

        clean_messages = []

        # messages are stored in reverse chronological order
        messages = self.data['messages'][::-1]
        for message in messages:
            clean_message = self._get_message_text(message)
            if clean_message is None:
               continue
            
            # check last clean_message, we don't want multiple of one person talking in a row, so combine them
            if len(clean_messages) > 0 and clean_messages[-1]['sender'] == clean_message['sender']:
                clean_messages[-1]['text'] += '. ' + clean_message['text']
            else:
                clean_messages.append(clean_message)

        # prune these messages
        pruner = MessengerPruner(data=clean_messages, pruning_system_prompt_file_path='data/pruning_prompt.txt')
        clean_messages = pruner.prune_data()

        return clean_messages
    
    def _get_system_prompt(self):

        """
        Retrieves the system prompt, reading from file if not already loaded.
        """

        if self.system_prompt is None:
            self._read_system_prompt()
            
        return {
            "role": "system",
            "content": self.system_prompt
        }
    
    def _get_gpt_message(self, message: Dict[str, str]):

        """
        Formats a message dictionary into the format expected by GPT, assigning roles based on the sender.
        
        Input is: 
        {
            'question': '...',
            'answer': '...'
        }

        """
        return [ 
            self._get_system_prompt(), 
            {
                "role": "user",
                "content": message["question"]
            },
            {
                "role": "assistant",
                "content": message["answer"]
            }
        ]
    
    def get_openai_message_format(self):

        """
        Takes messages from _parse_messages and converts them to 

        { 
            "messages": [
                {"role": "user", "content": ... },
                {"role": "assistant", "content": ...}
            ]
        }

        """

        result_messages = []
        
        clean_messages = self._parse_messages()

        for message in clean_messages:
            result_messages.append(self._get_gpt_message(message))

        return result_messages

if __name__ == '__main__':
    parser = MessageJSONParser('data/your_facebook_activity/messages/inbox/vigneshvaradarajan_1933986433594071/message_1.json', 'data/system_prompt.txt', 'Avyay Varadarajan')
    print(parser.get_openai_message_format())
