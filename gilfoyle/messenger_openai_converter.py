import json
from typing import List, Dict, Optional

MAX_MESSAGE_LENGTH = 2000

class MessageJSONParser:
    """
    Parses a JSON file containing messages from Facebook Messenger.
    """
    def __init__(self, json_file: str, system_prompt_file: str, our_name: str):
        self.json_file = json_file
        self.system_prompt_file = system_prompt_file
        self.our_name = our_name
        self.data = None
        self.system_prompt = None

    def _read_json(self):
        """
        Reads the JSON file and stores the data in the instance variable.
        """
        with open(self.json_file, 'r') as file:
            data = json.load(file)
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
            'text': message['content'],
            'sender': message['sender_name']
        }

    def _parse_messages(self) -> List[Dict[str, str]]:
        """
        Parses the messages from the JSON file. Converts them to a format where it is 
        [
            {
                'text': '...',
                'sender': '...',
            }
        ]

        """

        if self.data is None:
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
        """

        return {
            "role": "assistant" if message['sender'] == self.our_name else "user",
            "content": message['text']
        }
    
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

        result_messages = [
            [   
                self._get_system_prompt()
            ]
        ]
        
        curr_list = 0

        clean_messages = self._parse_messages()

        for message in clean_messages:
            if len(result_messages[curr_list]) < MAX_MESSAGE_LENGTH:
                result_messages[curr_list].append(self._get_gpt_message(message))
            else:
                # first add the system prompt
                result_messages.append([
                    self._get_system_prompt()
                ])
                result_messages[curr_list+1].append(self._get_gpt_message(message))
                curr_list += 1

        
        for conversation in result_messages:
            # check that the last message is from the assistant
            if conversation[-1]['role'] != 'assistant':
                conversation.pop()

        return [
            {
                "messages": conversation
            }
            for conversation in result_messages
        ]
            




