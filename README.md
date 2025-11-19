# Repo Explainer

**Upload any Github repo as zip file to the app -> "Repo Explainer" generates Explanation within 15 seconds**

## Features
- Understands entire repos (not just one file)
- Explains architecture, setup, gotchas
- Uses **MiniMax-M2-Stable** with 200K context
- Official OpenAI Python SDK (just change base_url)
- Live streaming response

## Live Demo
👉 https://youtu.be/AdqcMqjTJno?si=wm7E0mX167dxI29E

## How to run Locally
- First add the api key by creating a
  ```bash
  ./streamlit/secrets.toml

- then, save your api key in secrets.toml file as
  ```bash
  MINIMAX_API_KEY="<your_api_key>"

- then run
```bash
uv add -r requirements.txt
streamlit run app.py

