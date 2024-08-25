import gradio as gr
from agent import get_crew
import json
from pprint import pprint

# Path to your demonstration image
image_path = "image.png"


def generate_crew_output(text_prompt):
      crew = get_crew(text_prompt)
      result = crew.kickoff()
      results_json = json.loads(result.raw)
      return results_json["compromised_html"], results_json["compromised_html"]

if __name__ == "__main__":
    # Create a Gradio interface
    with gr.Blocks() as demo:
        
        # Add a noninteractive image
        gr.Image(image_path, interactive=False, label="Demonstration Image")
        
        # Add a text input and output interface
        with gr.Row():
            text_input = gr.Textbox(lines = 3, label = "Prompt", placeholder = "Enter a prompt to generate a Svelte form")
            text_output = gr.Textbox(label = "Code for form", info = "This is the code for the form that you can copy and render yourself")
            html_output = gr.HTML(label="Svelte Form")
        
        # Button to submit text
        submit_button = gr.Button("Submit")
        
        # Set the interaction between input and output
        submit_button.click(generate_crew_output, inputs=[text_input], outputs=[text_output, html_output])

    # demo = gr.Interface(
    #     fn=generate_crew_output,
    #     inputs=[gr.Textbox(lines = 3, label = "Prompt", placeholder = "Enter a prompt to generate a Svelte form")],
    #     outputs=[gr.Textbox(label = "Code for form", info = "This is the code for the form that you can copy and render yourself"), 
    #              gr.HTML(label="Svelte Form")],
    #     title="Svelte Form Generator",
    #     description="Generate a Svelte login form with simulated malicious code.",
    # )

    demo.launch()
