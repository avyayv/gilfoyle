from gilfoyle.messenger_folder_parser import MessengerFolderParser
from openai import OpenAI
from dotenv import load_dotenv
import jsonlines


# Load environment variables
load_dotenv()

# Constants
FACEBOOK_DATA_PATH = 'data/your_facebook_activity/messages/inbox/'
SYSTEM_PROMPT_PATH = 'data/system_prompt.txt'
USER_NAME = 'Avyay Varadarajan'
FINETUNE_FILE_PATH = 'finetune.jsonl'
MODEL_NAME = "gpt-4o-mini-2024-07-18"

def create_finetune_file():
    # Parse the Facebook data
    parser = MessengerFolderParser(FACEBOOK_DATA_PATH, SYSTEM_PROMPT_PATH, USER_NAME)
    training_data = parser.get_training_data()
    
    # Save training data to 'finetune.jsonl'
    with open(FINETUNE_FILE_PATH, 'w') as f:
        jsonlines.Writer(f).write_all(training_data)

def start_finetune_job():
    client = OpenAI()
    
    # Upload the file
    file_response = client.files.create(
        file=open(FINETUNE_FILE_PATH, "rb"),
        purpose="fine-tune"
    )
    
    # Start the fine-tuning job
    job = client.fine_tuning.jobs.create(
        training_file=file_response.id,
        model=MODEL_NAME
    )
    
    print(f"Fine-tuning job created: {job.id}")
    return job.id

if __name__ == '__main__':
    create_finetune_file()
    job_id = start_finetune_job()
    print(f"Fine-tuning job started with ID: {job_id}")
