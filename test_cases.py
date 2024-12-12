import requests
from anthropic import Anthropic
from mistralai import Mistral
from openai import OpenAI, AzureOpenAI

import google.generativeai as genai

# Function to create a prompt to generate mitigating controls
def create_test_cases_prompt(code, language, hardware, application_description):
    prompt =f"""
Act as an expert in embedded systems development and testing with more than 20 years of experience. 
Your task is to generate test cases for running embedded application code in order to identify potential issues such as 
memory allocation errors, CPU utilization problems, system crashes, or other runtime errors. The test cases should 
focus on verifying the stability and efficiency of the embedded system. Give the test cases in language specific test framework.

### Application Details:
- **Programming Language:** {language}
- **Hardware/Platform:** {hardware}
- **Application Code:** {code}
- **Application Description:** {application_description}

Put the test cases inside triple backticks (```) to format the test cases in Markdown. Add a title for each test case and give language specific test cases.
For example:

    ```Test Case
    Given a scenario where the system is under heavy load
    When the system is running multiple processes
    Then the system should not crash and should maintain stable performance

    ```

YOUR RESPONSE (do not add introductory text, just provide the test cases):
"""
    return prompt


# Function to get test cases from the GPT response.
def get_test_cases(api_key, model_name, prompt):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        model_name,
        system_instruction="You are a helpful assistant that provides test cases in Markdown format.",
    )
    response = model.generate_content(prompt)
    
    # Access the content directly as the response will be in text format
    test_cases = response.candidates[0].content.parts[0].text

    return test_cases

# Function to get mitigations from the Azure OpenAI response.
def get_test_cases_azure(azure_api_endpoint, azure_api_key, azure_api_version, azure_deployment_name, prompt):
    client = AzureOpenAI(
        azure_endpoint = azure_api_endpoint,
        api_key = azure_api_key,
        api_version = azure_api_version,
    )

    response = client.chat.completions.create(
        model = azure_deployment_name,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that provides Gherkin test cases in Markdown format."},
            {"role": "user", "content": prompt}
        ]
    )

    # Access the content directly as the response will be in text format
    test_cases = response.choices[0].message.content

    return test_cases

# Function to get test cases from the Google model's response.
def get_test_cases_google(google_api_key, google_model, prompt):
    genai.configure(api_key=google_api_key)
    model = genai.GenerativeModel(
        google_model,
        system_instruction="You are a helpful assistant that provides Gherkin test cases in Markdown format.",
    )
    response = model.generate_content(prompt)
    
    # Access the content directly as the response will be in text format
    test_cases = response.candidates[0].content.parts[0].text

    return test_cases

# Function to get test cases from the Mistral model's response.
def get_test_cases_mistral(mistral_api_key, mistral_model, prompt):
    client = Mistral(api_key=mistral_api_key)

    response = client.chat.complete(
        model = mistral_model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that provides Gherkin test cases in Markdown format."},
            {"role": "user", "content": prompt}
        ]
    )

    # Access the content directly as the response will be in text format
    test_cases = response.choices[0].message.content

    return test_cases

# Function to get test cases from Ollama hosted LLM.
def get_test_cases_ollama(ollama_model, prompt):
    
    url = "http://localhost:11434/api/chat"

    data = {
        "model": ollama_model,
        "stream": False,
        "messages": [
            {
                "role": "system", 
                "content": "You are a helpful assistant that provides Gherkin test cases in Markdown format."},
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
    response = requests.post(url, json=data)

    outer_json = response.json()
    
    # Access the 'content' attribute of the 'message' dictionary
    mitigations = outer_json["message"]["content"]

    return mitigations

# Function to get test cases from the Anthropic model's response.
def get_test_cases_anthropic(anthropic_api_key, anthropic_model, prompt):
    client = Anthropic(api_key=anthropic_api_key)
    response = client.messages.create(
        model=anthropic_model,
        max_tokens=4096,
        system="You are a helpful assistant that provides Gherkin test cases in Markdown format.",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    # Access the text content from the first content block
    test_cases = response.content[0].text

    return test_cases