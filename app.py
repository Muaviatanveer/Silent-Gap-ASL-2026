import gradio as gr
from fastai.vision.all import *

# Load the model weights
# Note: For the live presentation, ensure this file is in the same folder
try:
    learn = load_learner('resnet50_final.pkl')
except:
    print("Model file not found. Please ensure resnet50_final.pkl is present.")

state = {"text": ""}

def predict_and_spell(img):
    pred, _, _ = learn.predict(img)
    label = str(pred)
    
    if label == 'space': state["text"] += " "
    elif label == 'del': state["text"] = state["text"][:-1]
    elif label == 'nothing': pass
    else:
        if not state["text"].endswith(label):
            state["text"] += label
            
    return label, state["text"]

demo = gr.Interface(
    fn=predict_and_spell,
    inputs=gr.Image(sources=["webcam"], streaming=True),
    outputs=[gr.Textbox(label="Detected Sign"), gr.Textbox(label="Spelled Message")],
    live=True,
    title="Sara's Bridge: Real-Time ASL Speller",
    description="Bridge the gap. Show ASL signs to translate to text."
)

if __name__ == "__main__":
    demo.launch()