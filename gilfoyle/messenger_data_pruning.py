from typing import List, Dict, Tuple
from openai import OpenAI
from pydantic import BaseModel
import json
from dotenv import load_dotenv
import textwrap

# Load environment variables
load_dotenv()

class PruningData(BaseModel):
    question: str
    answer: str


class PruningDataList(BaseModel):
    data: List[PruningData]


class MessengerPruner():
    """
    This class will take in the output from the MessageJSONParser
        [
            {
                'text': '...',
                'sender': '...',
            }
        ]

    and return a list of pairs, that are properly pruned (i.e they are good Q&A pairs). It will use
    the OpenAI structured API outputs. 
    """
    def __init__(self, data: List[Dict[str, str]], pruning_system_prompt_file_path: str):
        self.data = data
        self.pruning_system_prompt_file_path = pruning_system_prompt_file_path
        self.client = OpenAI()

    def _load_system_prompt(self) -> str:
        with open(self.pruning_system_prompt_file_path, 'r') as file:
            system_prompt = file.read()
        return system_prompt
    
    def _get_system_prompt(self) -> Dict[str, str]:
        return {
            "role": "system",
            "content": self._load_system_prompt()
        }

    def _load_conversation_json(self) -> List[Dict[str, str]]:
        # load a string version of self.data
        return self.data

    def prune_data(self) -> List[Dict[str, str]]:
        system_prompt = self._get_system_prompt()
        conversation_json = self._load_conversation_json()
        
        # Split conversation JSON into chunks of 25000 characters
        chunk_size = 25000
        conversation_chunks = textwrap.wrap(json.dumps(conversation_json), chunk_size, break_long_words=False, replace_whitespace=False)
        
        all_outputs = []
        
        for chunk in conversation_chunks:
            messages = [
                system_prompt,
                {
                    "role": "user",
                    "content": chunk
                }
            ]
            completion = self.client.beta.chat.completions.parse(
                model="gpt-4o-2024-08-06",
                messages=messages,
                response_format=PruningDataList
            )
            response = completion.choices[0].message.parsed
            
            if isinstance(response, PruningDataList):
                for pruning_data in response.data:
                    all_outputs.append({
                        "question": pruning_data.question,
                        "answer": pruning_data.answer
                    })
        
        return all_outputs


if __name__ == "__main__":
    data = [
        {
            'text': 'hello',
            'sender': 'user'
        }, 
        {
            'text': 'how are you?',
            'sender': 'assistant'
        }
    ]
    parser = MessengerPruner(data=data, pruning_system_prompt_file_path='data/pruning_prompt.txt')
    print(parser.prune_data())




