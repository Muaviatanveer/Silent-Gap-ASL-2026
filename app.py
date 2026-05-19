import gradio as gr
from fastai.vision.all import *
import json
import os

# --- DATABASE LOGIC ---
USER_DB_FILE = "users_db.json"

def load_users():
    if not os.path.exists(USER_DB_FILE):
        return {"admin": "bridge2024"} # Default user
    with open(USER_DB_FILE, "r") as f:
        return json.load(f)

def save_user(username, password):
    users = load_users()
    if username in users:
        return False, "Username already exists!"
    users[username] = password
    with open(USER_DB_FILE, "w") as f:
        json.dump(users, f)
    return True, "Account created successfully! Please Login."

def authenticate(username, password):
    users = load_users()
    if username in users and users[username] == password:
        return True
    return False

# --- AI LOGIC ---
learn = load_learner('nuclear_brain.pkl')

def predict_and_spell(img, current_text, buffer):
    if img is None: return "", current_text, buffer
    
    pred, _, _ = learn.predict(img)
    label = str(pred)
    
    buffer.append(label)
    if len(buffer) > 3: buffer.pop(0)
    
    if buffer.count(label) == 3:
        if label == 'space': 
            if not current_text.endswith(" "): current_text += " "
        elif label == 'del': 
            current_text = current_text[:-1]
        elif label == 'nothing': pass
        else:
            if not current_text.endswith(label): current_text += label
        buffer = [] 
            
    return label, current_text, buffer

# --- STYLING ---
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;600&display=swap');

body, .gradio-container {
    background: linear-gradient(135deg, #090a0f, #1b2735) !important;
    font-family: 'Inter', sans-serif !important;
    color: #ffffff !important;
}

.glass-panel {
    background: rgba(255, 255, 255, 0.03) !important;
    backdrop-filter: blur(15px) !important;
    border-radius: 20px !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8) !important;
    padding: 40px !important;
    margin: 20px auto !important;
}

.auth-card {
    max-width: 450px !important;
    margin: 100px auto !important;
}

.title-text {
    font-family: 'Orbitron', sans-serif !important;
    text-align: center;
    color: #ffffff;
    text-shadow: 0 0 15px #0984E3;
}

.detected-label textarea {
    font-family: 'Orbitron', sans-serif !important;
    font-size: 70px !important;
    text-align: center !important;
    color: #00f2fe !important;
    background: transparent !important;
    border: none !important;
}

.message-box textarea {
    font-size: 32px !important;
    color: #00e676 !important;
    background: rgba(0, 0, 0, 0.4) !important;
    border: 1px solid #00e676 !important;
}

.primary-btn {
    background: linear-gradient(45deg, #0984E3, #00f2fe) !important;
    border: none !important;
    color: white !important;
    font-weight: bold !important;
}
"""

# --- UI BUILD ---
with gr.Blocks(css=custom_css, theme=gr.themes.Base()) as demo:
    
    # Session States
    text_state = gr.State("")
    buffer_state = gr.State([])
    
    # 1. LOGIN / REGISTER UI
    with gr.Column(visible=True, elem_classes="glass-panel auth-card") as auth_panel:
        gr.Markdown("# 🌉 SARA'S BRIDGE\n### Secure Neural Portal", elem_classes="title-text")
        
        with gr.Tabs():
            with gr.TabItem("Login"):
                login_user = gr.Textbox(label="Username", placeholder="Enter username...")
                login_pw = gr.Textbox(label="Password", type="password")
                login_btn = gr.Button("UNLOCk ACCESS", elem_classes="primary-btn")
                login_msg = gr.Markdown()

            with gr.TabItem("Register"):
                reg_user = gr.Textbox(label="New Username", placeholder="Choose a name...")
                reg_pw = gr.Textbox(label="New Password", type="password")
                reg_btn = gr.Button("CREATE ACCOUNT", variant="secondary")
                reg_msg = gr.Markdown()

    # 2. MAIN APPLICATION UI (Hidden by default)
    with gr.Column(visible=False, elem_classes="glass-panel") as main_app:
        gr.Markdown("# 🌉 Sara's Bridge", elem_classes="title-text")
        gr.Markdown("<p style='text-align:center'>AI-Powered Sign Language Translation Active</p>")
        
        with gr.Row():
            with gr.Column(scale=2):
                input_img = gr.Image(sources=["webcam"], streaming=True, label="Neural Feed")
            
            with gr.Column(scale=1):
                gr.Markdown("### 🧠 Interpretation")
                out_label = gr.Textbox(label="", elem_classes="detected-label")
                clear_btn = gr.Button("🗑️ PURGE", variant="stop")

        gr.Markdown("### 📡 Spelled Message")
        out_text = gr.Textbox(label="", placeholder="System ready...", elem_classes="message-box")

    # --- BUTTON LOGIC ---
    
    # Register logic
    def handle_register(u, p):
        if len(u) < 3 or len(p) < 3:
            return "Username/Password too short!"
        success, msg = save_user(u, p)
        return msg

    reg_btn.click(handle_register, [reg_user, reg_pw], reg_msg)

    # Login logic
    def handle_login(u, p):
        if authenticate(u, p):
            # Hide auth panel, show main app
            return gr.update(visible=False), gr.update(visible=True), f"Welcome, {u}!"
        return gr.update(visible=True), gr.update(visible=False), "Invalid Credentials"

    login_btn.click(
        handle_login, 
        [login_user, login_pw], 
        [auth_panel, main_app, login_msg]
    )

    # Core Logic
    input_img.stream(
        fn=predict_and_spell, 
        inputs=[input_img, out_text, buffer_state], 
        outputs=[out_label, out_text, buffer_state]
    )
    
    clear_btn.click(
        lambda: ("", "", []), 
        outputs=[out_label, out_text, buffer_state]
    )

# Launch
demo.launch(share=True)
