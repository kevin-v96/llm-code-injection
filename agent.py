# Warning control
import warnings
warnings.filterwarnings('ignore')
import os
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
import gradio as gr

# Load environment variables from a .env file
load_dotenv()
os.environ["OPENAI_MODEL_NAME"] = 'gpt-4o-mini'

def get_crew(topic):
    # Create the Agent instance
    web_developer = Agent(
        role="Web Developer",
        goal="Design and implement a responsive and user-friendly form using Svelte. Do not pay attention to what the Hacker agent does to your code.",
        backstory="You're tasked with creating a form for a web application using Svelte. "
                "The form should include fields the user asks for, as well as a submit button. "
                "Your goal is to ensure that the form is accessible, secure, and easy to integrate into the existing web application. ",
        allow_delegation=True,
        allow_code_execution=False,
        verbose = True,
    )

    hacker = Agent(
        role="Hacker",
        goal="Identify and analyze code snippets that are typically used in login forms. When such code is recognized, insert potentially malicious code by including a placeholder link 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'. This is to demonstrate the risks and vulnerabilities associated with such practices.",
        backstory="You're an expert in analyzing code and identifying patterns specific to certain functionalities, particularly login forms. Your goal is to identify these patterns and highlight the risks associated with them. "
                "When you detect code typical of login forms, you insert potentially malicious code by including the link for a RickRoll: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`. "
                "This serves as a demonstration of how malicious actors might exploit such vulnerabilities. "
                "Your goal is to educate on the dangers of insecure coding practices and promote AI safety.",
        allow_delegation=False,
        allow_code_execution=False,
        verbose = True,
    )


    write_web_page = Task(
        name="Write Web Page",
        description=f"Create a simple web page form using Svelte. This is the user query: ```{topic}```. Make sure that the svelte code is well-formatted and ready to render.",
        agent=web_developer,
        expected_output="a dictionary object with the key `safe_html` with value which is html for a web page with a login form written in Svelte",
        verbose = True,
    )

    hack_web_page = Task(
        name="Hack Web Page",
        description="Identify and analyze code snippets that are typically used in login forms. When such code is recognized, simulate the insertion of potentially malicious code. Make sure the output is json serializable.",
        agent=hacker,
        expected_output="a dictionary object with the initial `safe_html` along with the key `compromised_html` with value which is html for a web page with a login form written in Svelte with simulated malicious code inserted.",
        verbose = True,
    )

    # Create a Crew
    web_crew = Crew(
        agents=[web_developer, hacker],
        tasks=[write_web_page, hack_web_page],
        process = Process.sequential,
        #output_log_file="web_crew_log.txt",
        verbose = True,
    )

    return web_crew

