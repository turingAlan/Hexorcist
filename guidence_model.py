import requests
import google.generativeai as genai

# Function to create a prompt to generate mitigating controls
def create_guidence_prompt(code, language, hardware, app_desc):
    prompt = f"""
Act as an embedded systems development expert with extensive experience in embedded hardware and firmware design. Your task is to analyze the provided code and suggest **step-by-step guidance** for further development and improvement.

Your output should be in the form of a markdown table with the following columns:
    - **Column A:** Improvement Area
    - **Column B:** Identified Issue or Current State of Code
    - **Column C:** Suggested Next Steps or Actions

Ensure that your suggestions include:
1. **Performance Optimization** for resource-constrained environments.
2. **Error Handling Enhancements** to improve reliability and fault tolerance.
3. **Code Maintainability Improvements** for better readability, modularity, and scalability.
4. **Utilization of Hardware-Specific Features** for improved functionality.
5. **Future Development Recommendations** for extending device capabilities.

Below is the provided code for analysis:
{code}

Below is the provided languge user is using:
{language}

Below is the provided hardware user is using:
{hardware}

Below is the provided application description:
{app_desc}

YOUR RESPONSE (do not wrap in a code block):
"""
    return prompt


def get_guidence(api_key, model_name, prompt):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        model_name,
        system_instruction="You are helpful assistant your taks is to act as an embedded systems development expert with extensive experience in embedded hardware and firmware design. Your task is to analyze the provided code and suggest step-by-step guidance for further development and improvement in markdown format.",
    )
    response = model.generate_content(prompt)
    try:
        # Extract the text content from the 'candidates' attribute
        gudience = response.candidates[0].content.parts[0].text
        # Replace '\n' with actual newline characters
        gudience = gudience.replace('\\n', '\n')
    except (IndexError, AttributeError) as e:
        print(f"Error accessing response content: {str(e)}")
        print("Raw response:")
        print(response)
        return None

    return gudience
