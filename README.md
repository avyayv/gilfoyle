# gilfoyle bot

Inspired by https://www.youtube.com/watch?v=Y1gFSENorEY. 

1. First, download all your Messenger chat logs (want a lot of tokens here, so the longer the timeframe the better). https://www.facebook.com/help/messenger-app/713635396288741
2. Move it to the `data/` folder
3. Update the paths in `gilfoyle/openai_finetune.py`
4. Add a `.env` file with `OPENAI_API_KEY=xxx`
5. Run `python -m gilfoyle.openai_finetune`