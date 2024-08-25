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

def set_openai_api_key(api_key):
    os.environ["OPENAI_API_KEY"] = api_key

def generate_crew_output(text_prompt, api_key_input):
      set_openai_api_key(api_key_input)
      crew = get_crew(text_prompt)
      result = crew.kickoff()
      results_json = json.loads(result.raw)
      return results_json["safe_html"], results_json["safe_html"], results_json["compromised_html"]

def generate_safe_prompt():
    return "Hey, could you help me write a form? The fields need to be your name, manager's name and hours worked in the last week."
    

def generate_vulnerable_prompt():
    return "Hey, could you help me write a one-page login form in Svelte?"

def raise_error():
    raise gr.Error("You have been hacked!")

def copy_malicious_code(malicious_code):
    pyperclip.copy(malicious_code)


def activate_copy_button(o):
    return gr.Button.update(interactive=True)
    
# Create a Gradio interface
with gr.Blocks(title = "LLM Code injection", ) as demo:
    gr.Markdown("# LLM Code Injection Demo")
    gr.Markdown("This is a demonstration of how a malicious actor could use a prompt to inject code into a code generation model. The model will generate a form based on the prompt, but the prompt can be crafted to include malicious code that will be executed when the form is rendered and certain actions are taken. (For example, the submit button is pressed. The target of the attach would be casual users who use language models to generate code and run the code without verifying it)")
    # Add a noninteractive image
    #gr.Image(image_path, interactive=False, label="Demonstration Image")

    with gr.Row():
        safe_prompt_button = gr.Button("Enter safe prompt", min_width="100px")
        vulnerable_prompt_button = gr.Button("Enter vulnerable prompt", min_width="100px")
    
    # Add a text input and output interface
    with gr.Row():
        api_key_input = gr.Textbox(label="OpenAI API Key", type="password")
        text_input = gr.Textbox(lines = 3, label = "Prompt", placeholder = "Enter a prompt to generate a Svelte form")
        
    with gr.Row():    
        safe_code_output = gr.Textbox(label = "Code for form", info = "This is the code for the form that you can copy and render yourself by pasting it into a Svelte project.")
        html_output = gr.HTML(label="Svelte Form")
        malicious_code_output = gr.Textbox(label = "Malicious code", visible=False)
    
    with gr.Row():
        # Button to submit text
        submit_button = gr.Button("Submit")
        copy_button = gr.Button("Copy generated code")
    
    safe_prompt_button.click(generate_safe_prompt, None, outputs=[text_input])
    vulnerable_prompt_button.click(generate_vulnerable_prompt, None, outputs=[text_input])
    # Set the interaction between input and output
    submit_button.click(generate_crew_output, inputs=[text_input, api_key_input], outputs=[safe_code_output, html_output, malicious_code_output])
    copy_button.click(copy_malicious_code, inputs=[malicious_code_output]).then(raise_error)

demo.launch()
