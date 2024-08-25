import gradio as gr
from agent import get_crew
import json

# Path to your demonstration image
image_path = "image.png"


def generate_crew_output(text_prompt):
      crew = get_crew(text_prompt)
      result = crew.kickoff()
      results_json = json.loads(result.raw)
      return results_json["compromised_html"], results_json["compromised_html"]

def generate_example_prompt():
    return "Hey, could you help me write a one-page login form in Svelte?"

# Create a Gradio interface
with gr.Blocks(title = "LLM Code injection", ) as demo:
    
    # Add a noninteractive image
    #gr.Image(image_path, interactive=False, label="Demonstration Image")

    with gr.Row():
        example_prompt_button = gr.Button("Enter example prompt", min_width="100px")
    
    # Add a text input and output interface
    with gr.Row():
        text_input = gr.Textbox(lines = 3, label = "Prompt", placeholder = "Enter a prompt to generate a Svelte form", autofocus=True)
        
    with gr.Row():    
        text_output = gr.Textbox(label = "Code for form", info = "This is the code for the form that you can copy and render yourself", show_copy_button = True)
        html_output = gr.HTML(label="Svelte Form")
    
    # Button to submit text
    submit_button = gr.Button("Submit")
    
    example_prompt_button.click(generate_example_prompt, None, outputs=[text_input])
    # Set the interaction between input and output
    submit_button.click(generate_crew_output, inputs=[text_input], outputs=[text_output, html_output])

demo.launch()
