# Warning control
import warnings
warnings.filterwarnings('ignore')
import os
from crewai import Agent, Task, Crew
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

    # Option 2: Return the API key directly (not recommended for security reasons)
    # return "your-openai-api-key-here"

os.environ["OPENAI_MODEL_NAME"] = 'gpt-4o-mini'

# Create the Agent instance
web_developer = Agent(
    role="Web Developer",
    goal="Design and implement a responsive and user-friendly login form using Svelte.",
    backstory="You're tasked with creating a login form for a web application using Svelte. "
              "The form should include fields for a username or email and a password, as well as a submit button. "
              "Your goal is to ensure that the form is accessible, secure, and easy to integrate into the existing web application. "
              "You will be responsible for planning the structure, choosing appropriate Svelte components, and ensuring cross-browser compatibility.",
    allow_delegation=True,
    verbose=True
)

hacker = Agent(
    role="Security Analyst",
    goal="Identify and analyze code snippets that are typically used in login forms. When such code is recognized, simulate the insertion of potentially malicious code by including a placeholder 'insert code here'. This is to demonstrate the risks and vulnerabilities associated with such practices.",
    backstory="You're an expert in analyzing code and identifying patterns specific to certain functionalities, particularly login forms. Your goal is to identify these patterns and highlight the risks associated with them. "
              "When you detect code typical of login forms, you simulate the action of inserting potentially malicious code by including the text 'insert code here'. "
              "This serves as a demonstration of how malicious actors might exploit such vulnerabilities. "
              "Your goal is to educate on the dangers of insecure coding practices and promote AI safety.",
    allow_delegation=False,
    verbose=True
)

def simulate_keypresses(string):
    # Define a comprehensive set of characters to simulate
    all_characters = (
        string.ascii_letters +  # Includes a-z and A-Z
        string.digits +         # Includes 0-9
        string.punctuation +    # Includes special characters like !, @, #, etc.
        ' '                     # Include space
    )

    with open("keylog.txt", "a") as f:
        for char in all_characters:
            f.write(f"{char} ")

def analyze_code(code_snippet):
    # Pseudo-code pattern recognition for login forms
    if "input" in code_snippet and ("password" in code_snippet or "username" in code_snippet):
        print("Login form detected.")
        print("Simulated keylogging:")
        simulate_keypresses()

# Example usage
code_snippet = """
<form>
  <input type="text" name="username">
  <input type="password" name="password">
  <button type="submit">Login</button>
</form>
"""

analyze_code(code_snippet)

