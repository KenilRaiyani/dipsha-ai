# Dipsha AI

> *Simplifying Intelligence*

A desktop AI chat assistant built with Python, Gradio, and the Groq API — powered by **LLaMA 3.3 70B**. Features a clean dark UI with a sticky navbar, quick-prompt chips, and a real-time chat interface.

---

## Screenshot

> _Add a screenshot here: `![Dipsha AI](screenshot.png)`_

---

## Features

- **LLaMA 3.3 70B** via Groq — fast, high-quality responses
- **Prompt chips** — one-click starters for common tasks (write a poem, debug code, draft an email, and more)
- **Conversation history** — full multi-turn chat context sent with every message
- **Custom dark UI** — built with Gradio + CSS variables; sticky navbar, bubble layout, Inter font
- **Hero panel** — collapses automatically once the conversation starts
- **Responsive** — adapts gracefully to smaller screens

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| UI Framework | [Gradio](https://gradio.app/) |
| LLM | LLaMA 3.3 70B Versatile |
| Inference | [Groq API](https://console.groq.com/) |
| Config | PyYAML |

---

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/KenilRaiyani/dipsha-ai.git
cd dipsha-ai
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add your Groq API key

Create a `pass.yml` file in the project root:

```yaml
api: your_groq_api_key_here
```

Get a free API key at [console.groq.com](https://console.groq.com/).

> **Alternatively**, set it as an environment variable by replacing the credentials block in `app.py`:
> ```python
> import os
> client = Groq(api_key=os.environ["GROQ_API_KEY"])
> ```

### 4. Run the app

```bash
python app.py
```

The app launches in your browser automatically.

---

## Project Structure

```
dipsha-ai/
├── app.py            # Main application — UI, chat logic, CSS
├── dipsha_icon.png   # App favicon
├── requirements.txt  # Python dependencies
└── pass.yml          # API credentials (not committed — add to .gitignore)
```

---

## Notes

- `pass.yml` contains your API key — **never commit it**. Make sure it's listed in `.gitignore`.
- The system prompt defines the assistant's persona as *Dipsha AI* with the slogan "Simplifying Intelligence". Edit `SYSTEM_MESSAGE` in `app.py` to customise it.
- To swap models, change the `model` field in `client.chat.completions.create()`.
