# gilfoyle bot

Inspired by https://www.youtube.com/watch?v=Y1gFSENorEY. 

## Overview

Currently, this reads all of your messages, asks GPT-4o to filter into good question answer pairs (an attempt to prevent horrible quality data to be fine-tuned on), and then we feed this into gpt-4o-mini's free finetuning API. 

Even with the attempt to increase data quality with filteration, it still kind of sucks, although it does mimic the style pretty decently. Need to see how to get even better quality data to avoid a ton of hallucination.

## Directions

1. First, download all your Messenger chat logs (more data is better, because we filter a lot down). https://www.facebook.com/help/messenger-app/713635396288741
2. Move it to the `data/` folder
3. Add a system prompt file in `data/system_prompt.txt`
4. Update the paths in `gilfoyle/openai_finetune.py`
5. Add a `.env` file with `OPENAI_API_KEY=xxx`
6. `pip install -r requirements.txt`
7. Run `python -m gilfoyle.openai_finetune`
