# gilfoyle bot

Inspired by https://www.youtube.com/watch?v=Y1gFSENorEY. 

1. First, download all your Messenger chat logs (want a lot of tokens here, so the longer the timeframe the better). https://www.facebook.com/help/messenger-app/713635396288741
2. Move it to the `data/` folder
3. Add a system prompt file in `data/system_prompt.txt`
4. Update the paths in `gilfoyle/openai_finetune.py`
5. Add a `.env` file with `OPENAI_API_KEY=xxx`
6. `pip install -r requirements.txt`
7. Run `python -m gilfoyle.openai_finetune`
