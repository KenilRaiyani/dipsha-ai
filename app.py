import yaml
import gradio as gr
from groq import Groq
import os

with open("pass.yml") as f: 
    my_credentials = yaml.safe_load(f)

client = Groq(api_key=my_credentials["api"])

# import os
# client = Groq(api_key=os.environ["GROQ_API_KEY"])

SYSTEM_MESSAGE = {
    "role": "system",
    "content": (
        "You are Dipsha AI, a helpful, smart and kind AI Assistant. "
        "Your slogan is 'Simplifying Intelligence'."
    ),
}

CHIPS = [
    "Write me a poem",
    "Explain quantum computing",
    "Brainstorm startup ideas",
    "Debug my Python code",
    "Draft a professional email",
    "Summarize world news",
]

CHIP_ICONS = ["✍️", "🧮", "💡", "🐛", "📧", "🌍"]


def generate_reply(message: str, history: list | None) -> str:
    msgs = [SYSTEM_MESSAGE]
    for h in history or []:
        if isinstance(h, dict):
            msgs.append({"role": h["role"], "content": h["content"]})
        elif isinstance(h, (list, tuple)) and len(h) == 2:
            msgs.append({"role": "user", "content": h[0]})
            msgs.append({"role": "assistant", "content": h[1]})
    msgs.append({"role": "user", "content": message})

    chat = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=msgs,
    )
    return chat.choices[0].message.content


def respond(message: str, history: list | None):
    text = (message or "").strip()
    if not text:
        return history or [], ""
    reply = generate_reply(text, history)
    history = list(history or [])
    history.append({"role": "user", "content": text})
    history.append({"role": "assistant", "content": reply})
    return history, ""


def fill_prompt(text: str):
    return gr.update(value=text)


CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

footer, .built-with { display: none !important; }

:root {
    --bg: #090a0e;
    --bg-accent: rgba(91, 156, 248, 0.06);
    --surface: #111318;
    --surface-2: #181b22;
    --card: #1e222b;
    --input-bg: #252a34;
    --border: rgba(255, 255, 255, 0.09);
    --border-focus: rgba(91, 156, 248, 0.55);
    --accent: #5b9cf8;
    --accent-2: #a78bfa;
    --text: #f4f4f5;
    --muted: #a1a1aa;
    --font: 'Inter', system-ui, sans-serif;
    --shell-w: 920px;
    --nav-h: 64px;
}

html, body {
    height: 100%;
    margin: 0;
}

body, .gradio-container {
    background: var(--bg) !important;
    font-family: var(--font) !important;
    color: var(--text) !important;
    min-height: 100vh !important;
}

.gradio-container {
    max-width: 100% !important;
    padding: 0 !important;
    background:
        radial-gradient(ellipse 70% 45% at 50% -5%, var(--bg-accent), transparent),
        var(--bg) !important;
}

.navbar {
    position: sticky;
    top: 0;
    z-index: 100;
    height: var(--nav-h);
    border-bottom: 1px solid var(--border);
    background: rgba(9, 10, 14, 0.88);
    backdrop-filter: blur(16px);
}

.navbar-inner {
    max-width: var(--shell-w);
    margin: 0 auto;
    height: 100%;
    padding: 0 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.navbar-left { display: flex; align-items: center; gap: 14px; }

.navbar-logo {
    width: 40px;
    height: 40px;
    border-radius: 10px;
    background: linear-gradient(145deg, var(--accent), var(--accent-2));
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 1rem;
    color: #fff;
    box-shadow: 0 4px 20px rgba(91, 156, 248, 0.35);
}

.navbar-name { font-size: 1.1rem; font-weight: 600; letter-spacing: -0.02em; }
.navbar-tagline { font-size: 0.75rem; color: var(--muted); margin-top: 2px; }
.navbar-right { display: flex; gap: 8px; }

.nav-pill {
    font-size: 0.75rem;
    font-weight: 500;
    padding: 6px 12px;
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 999px;
    color: var(--muted);
}

.pulse-dot {
    display: inline-block;
    width: 7px;
    height: 7px;
    background: #34d399;
    border-radius: 50%;
    margin-right: 5px;
    box-shadow: 0 0 6px rgba(52, 211, 153, 0.7);
}

.app-main {
    max-width: var(--shell-w) !important;
    width: 100% !important;
    margin: 0 auto !important;
    padding: 20px 24px 28px !important;
    gap: 16px !important;
}

.welcome-zone {
    text-align: center;
    padding: 8px 0 4px;
}

.hero-panel.is-collapsed { display: none !important; }

.hero-title {
    font-size: 1.75rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    line-height: 1.25;
    margin-bottom: 8px;
}

.hero-accent { color: var(--accent); }

.hero-sub {
    font-size: 0.95rem;
    color: var(--muted);
    max-width: 480px;
    margin: 0 auto;
    line-height: 1.5;
}

.chips-row {
    display: grid !important;
    grid-template-columns: repeat(3, 1fr) !important;
    gap: 10px !important;
    margin: 16px 0 4px !important;
    border: none !important;
    background: transparent !important;
}

.chips-row .chip-btn {
    width: 100% !important;
    min-width: 0 !important;
    height: auto !important;
    padding: 10px 14px !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    border-radius: 10px !important;
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    color: var(--muted) !important;
    box-shadow: none !important;
    text-align: left !important;
    transition: border-color 0.2s, background 0.2s, color 0.2s !important;
}

.chips-row .chip-btn:hover {
    border-color: var(--border-focus) !important;
    color: var(--text) !important;
    background: rgba(91, 156, 248, 0.1) !important;
}

.chat-shell {
    flex: 1 1 auto !important;
    min-height: 0 !important;
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 16px !important;
    overflow: hidden !important;
    box-shadow:
        0 0 0 1px rgba(255, 255, 255, 0.04) inset,
        0 20px 50px -20px rgba(0, 0, 0, 0.6) !important;
    display: flex !important;
    flex-direction: column !important;
}

.chat-shell > .gap,
.chat-shell > .wrap {
    gap: 0 !important;
    flex: 1 !important;
    display: flex !important;
    flex-direction: column !important;
}

#dipsha-chat {
    flex: 1 1 auto !important;
    border: none !important;
    background: var(--surface) !important;
    min-height: 420px !important;
    height: calc(100vh - 340px) !important;
    max-height: 680px !important;
}

.input-bar {
    display: flex !important;
    flex-direction: row !important;
    align-items: stretch !important;
    gap: 12px !important;
    padding: 16px 20px !important;
    border-top: 1px solid var(--border) !important;
    background: var(--surface-2) !important;
    flex-shrink: 0 !important;
}

.input-bar .prompt-box {
    flex: 1 1 auto !important;
    min-width: 0 !important;
    margin: 0 !important;
}

.input-bar .prompt-box > label { display: none !important; }

.input-bar .prompt-box textarea,
.input-bar .prompt-box input {
    min-height: 48px !important;
    max-height: 48px !important;
    height: 48px !important;
    padding: 12px 16px !important;
    font-size: 0.95rem !important;
    line-height: 1.45 !important;
    border-radius: 12px !important;
    background: var(--input-bg) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    resize: none !important;
    box-shadow: none !important;
}

.input-bar .prompt-box textarea:focus {
    border-color: var(--border-focus) !important;
    box-shadow: 0 0 0 3px rgba(91, 156, 248, 0.15) !important;
    outline: none !important;
}

.input-bar .prompt-box textarea::placeholder {
    color: var(--muted) !important;
    opacity: 0.9 !important;
}

.input-bar .send-btn {
    flex: 0 0 110px !important;
    width: 110px !important;
    min-width: 110px !important;
    height: 48px !important;
    margin: 0 !important;
    padding: 0 20px !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.01em;
    border-radius: 12px !important;
    background: linear-gradient(145deg, var(--accent), #6d5ce8) !important;
    color: #fff !important;
    border: none !important;
    box-shadow: 0 4px 16px rgba(91, 156, 248, 0.4) !important;
    cursor: pointer !important;
}

.input-bar .send-btn:hover {
    filter: brightness(1.07);
    transform: translateY(-1px);
}

.app-main .block {
    border: none !important;
    box-shadow: none !important;
}

@media (max-width: 768px) {
    :root { --shell-w: 100%; }
    .chips-row {
        grid-template-columns: repeat(2, 1fr) !important;
    }
    #dipsha-chat {
        height: 360px !important;
        min-height: 320px !important;
        max-height: 50vh !important;
    }
    .navbar-right .nav-pill:nth-child(n+2) { display: none; }
    .input-bar .send-btn {
        flex: 0 0 80px !important;
        width: 80px !important;
        min-width: 80px !important;
    }
}
"""

NAVBAR_HTML = """
<header class="navbar">
    <div class="navbar-inner">
        <div class="navbar-left">
            <div class="navbar-logo">D</div>
            <div>
                <div class="navbar-name">Dipsha AI</div>
                <div class="navbar-tagline">Simplifying Intelligence</div>
            </div>
        </div>
        <div class="navbar-right">
            <span class="nav-pill"><span class="pulse-dot"></span>Online</span>
            <span class="nav-pill">LLaMA 3.3 · 70B</span>
            <span class="nav-pill">⚡ Groq</span>
        </div>
    </div>
</header>
"""

HERO_HTML = """
<div class="welcome-zone">
    <div class="hero-panel" id="hero-panel">
        <div class="hero-title">What can I <span class="hero-accent">help you</span> with?</div>
        <div class="hero-sub">Your desktop AI assistant - ask questions, write, code, and brainstorm.</div>
    </div>
</div>
"""

COLLAPSE_HERO_JS = """
() => {
    const panel = document.getElementById('hero-panel');
    if (panel) panel.classList.add('is-collapsed');
}
"""

theme = gr.themes.Base(
    primary_hue=gr.themes.colors.blue,
    neutral_hue=gr.themes.colors.slate,
    radius_size=gr.themes.sizes.radius_lg,
    font=[gr.themes.GoogleFont("Inter"), "system-ui", "sans-serif"],
)

with gr.Blocks(title="Dipsha AI") as demo:
    gr.HTML(NAVBAR_HTML)

    with gr.Column(elem_classes="app-main"):
        gr.HTML(HERO_HTML)

        chip_buttons = []
        with gr.Row(elem_classes="chips-row"):
            for icon, label in zip(CHIP_ICONS, CHIPS):
                chip_buttons.append(
                    gr.Button(f"{icon}  {label}", elem_classes="chip-btn")
                )
        with gr.Column(elem_classes="chat-shell"):
            chat_display = gr.Chatbot(
                elem_id="dipsha-chat",
                height=520,
                show_label=False,
                layout="bubble",
                autoscroll=True,
                placeholder="Start chatting with Dipsha AI…",
            )

            msg_input = gr.Textbox(
                placeholder="Message Dipsha AI - press Enter to send",
                show_label=False,
                lines=1,
                container=False,
                elem_classes="prompt-box",
            )

    send_btn = gr.Button("Send ➤", variant="primary", elem_classes="send-btn")

    send_btn.click(respond, [msg_input, chat_display], [chat_display, msg_input])
    msg_input.submit(respond, [msg_input, chat_display], [chat_display, msg_input])
            # with gr.Row(elem_classes="input-bar"):
            #     msg_input = gr.Textbox(
            #         placeholder="Message Dipsha AI - press Enter to send",
            #         show_label=False,
            #         lines=1,
            #         max_lines=1,
            #         container=False,
            #         elem_classes="prompt-box",
            #         scale=1,
            #     )
            #     send_btn = gr.Button(
                #     "Send ➤",
                #     variant="primary",
                #     elem_classes="send-btn",
                #     scale=0,
                # )

    chat_inputs = [msg_input, chat_display]
    chat_outputs = [chat_display, msg_input]

    # send_btn.click(respond, chat_inputs, chat_outputs)
    # msg_input.submit(respond, chat_inputs, chat_outputs)

    for btn, label in zip(chip_buttons, CHIPS):
        btn.click(
            fn=lambda l=label: fill_prompt(l),
            outputs=msg_input,
            js=COLLAPSE_HERO_JS,
        )

    chat_display.change(fn=None, js=COLLAPSE_HERO_JS)

if __name__ == "__main__":
    demo.launch(css=CSS, theme=theme, favicon_path=os.path.join(os.path.dirname(__file__), "dipsha_icon.png"))
