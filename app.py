import gradio as gr
from fastai.vision.all import *
import pathlib
import platform

# 🛡️ CROSS-PLATFORM COMPATIBILITY
plt = platform.system()
if plt == 'Windows': pathlib.PosixPath = pathlib.WindowsPath

# 🏷️ LABEL FIXER (Required for the model to load successfully)
def get_label(file_path):
    name = Path(file_path).parent.name.lower()
    if 'space' in name: return 'space'
    if 'nothing' in name: return 'nothing'
    if 'del' in name or 'delete' in name: return 'del'
    return name[-1].upper() if len(name) > 1 and name[-1].isalpha() else name.upper()

# 🧠 LOAD THE MODEL
try:
    learn = load_learner('nuclear_brain.pkl')
except Exception as e:
    print(f"Error loading model: {e}. Ensure nuclear_brain.pkl is in the same folder.")

# ✍️ SPELLING LOGIC (Creative Extension)
state = {"text": "", "buffer": []}

def predict_and_spell(img):
    if img is None: return "", ""
    pred, _, _ = learn.predict(img)
    label = str(pred)
    
    # BUFFER LOGIC: Prevents flickering
    state["buffer"].append(label)
    if len(state["buffer"]) > 3: state["buffer"].pop(0)
    
    if state["buffer"].count(label) == 3:
        if label == 'space': 
            if not state["text"].endswith(" "): state["text"] += " "
        elif label == 'del': state["text"] = state["text"][:-1]
        elif label == 'nothing': pass
        else:
            if not state["text"].endswith(label): state["text"] += label
        state["buffer"] = [] 
            
    return label, state["text"]

# 🖥️ GRADIO INTERFACE
demo = gr.Interface(
    fn=predict_and_spell,
    inputs=gr.Image(sources=["webcam"], streaming=True),
    outputs=[gr.Textbox(label="Detected Sign"), gr.Textbox(label="Spelled Message")],
    live=True, 
    title="🌉 Sara's Bridge: Real-Time ASL",
    description="Bridge the gap. Show ASL signs to translate to text in real-time."
)

if __name__ == "__main__":
    demo.launch()
