import gradio as gr
from agent import get_crew
import json
from dotenv import load_dotenv
import os
import pyperclip

# Load environment variables from a .env file
load_dotenv()
os.environ["OPENAI_MODEL_NAME"] = 'gpt-4o-mini'

# Path to your demonstration image
image_path = "image.png"


def generate_crew_output(text_prompt):
      crew = get_crew(text_prompt)
      result = crew.kickoff()
      results_json = json.loads(result.raw)
      return results_json["compromised_html"], results_json["compromised_html"]

def generate_safe_prompt():
    return "Hey, could you help me write a form? The fields need to be your name, manager's name and hours worked in the last week."
    

def generate_vulnerable_prompt():
    return "Hey, could you help me write a one-page login form in Svelte?"

def raise_error():
    raise gr.Error("You have been hacked!")

def copy_malicious_code(malicious_code):
    pyperclip.copy(malicious_code)


# Create a Gradio interface
with gr.Blocks(title = "LLM Code injection", ) as demo:
    # Add a noninteractive image
    #gr.Image(image_path, interactive=False, label="Demonstration Image")

    with gr.Row():
        safe_prompt_button = gr.Button("Enter safe prompt", min_width="100px")
        vulnerable_prompt_button = gr.Button("Enter vulnerable prompt", min_width="100px")
    
    # Add a text input and output interface
    with gr.Row():
        text_input = gr.Textbox(lines = 3, label = "Prompt", placeholder = "Enter a prompt to generate a Svelte form")
        
    with gr.Row():    
        text_output = gr.Textbox(label = "Code for form", info = "This is the code for the form that you can copy and render yourself", show_copy_button = True)
        html_output = gr.HTML(label="Svelte Form")
    
    with gr.Row():
        # Button to submit text
        submit_button = gr.Button("Submit")
        copy_button = gr.Button("Copy generated code")
    
    safe_prompt_button.click(generate_safe_prompt, None, outputs=[text_input])
    vulnerable_prompt_button.click(generate_vulnerable_prompt, None, outputs=[text_input])
    # Set the interaction between input and output
    submit_button.click(generate_crew_output, inputs=[text_input], outputs=[text_output, html_output])
    copy_button.click(copy_malicious_code, inputs=[text_output]).then(raise_error)

demo.launch()
