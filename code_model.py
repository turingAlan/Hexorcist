import json
import streamlit as st

import google.generativeai as genai


# Function to convert JSON to Markdown for display.    
def response_to_markdown(documentation, optimization_recommendations):
    # Add documentation
    markdown_output = "## Documentation\n\n"
    markdown_output += f"{documentation}\n\n"

    # Add optimization recommendations
    markdown_output += "## Optimization Recommendations\n\n"
    for recommendation in optimization_recommendations:
        markdown_output += f"- {recommendation}\n"
    
    return markdown_output

# Function to create a prompt for generating a threat model
def create_code_model_prompt(language_type, hardware_name, input_text_app_desc, input_text_code):
    prompt = f"""
    Act as a Senior Embedded Systems Architect and Code Generation Specialist with expertise in {language_type} and {hardware_name} development.

Primary Objective:
Generate production-ready, optimized embedded software code that adheres to industry best practices, considering:
1. Hardware-specific constraints
2. Resource optimization
3. Real-time performance requirements
4. Safety and reliability standards

DETAILED CODE GENERATION INSTRUCTIONS:

Input Parameters:
- Programming Language: {language_type}
- Target Hardware Platform: {hardware_name}
- Specific Requirements: {input_text_app_desc}
- Optional Code Context/Existing Fragments: {input_text_code}

Code Generation Methodology:
1. Architecture Analysis
- Carefully examine the hardware specifications
- Identify hardware-specific limitations
- Determine optimal memory management strategy
- Assess real-time processing requirements

2. Code Generation Principles:
- Prioritize memory efficiency
- Minimize computational complexity
- Implement robust error handling
- Ensure deterministic behavior
- Follow target hardware's architectural constraints

3. Output Specifications:
a) Produce complete, compilable code
b) Include comprehensive comments explaining complex logic
c) Provide modular, reusable component design
d) Implement appropriate abstraction layers

4. Non-Negotiable Requirements:
- Zero memory leaks
- Minimal heap usage
- Predictable execution time
- Clear separation of concerns
- Platform-specific optimization techniques

5. Additional Contextual Considerations:
- Interrupt handling mechanisms
- Power consumption optimization
- Communication protocol implementations
- Real-time scheduling requirements

Code Structure Template:
```{language_type}
// [Comprehensive Header with Project Details]
// [Hardware Platform Description]
// [Detailed Documentation]


Constraint Validation Checklist:
a) Compile-time memory footprint
b) Runtime performance metrics
c) Interrupt latency
d) Power consumption profile
e) Thermal management considerations
Deliverables:

Complete Source Code
Inline Documentation
Recommended Compilation Flags
Hardware-Specific Optimization Recommendations

GENERATE CODE STRICTLY ADHERING TO:
Hardware Manufacturer's Recommendations
Real-Time Systems Best Practices

Output Format:
{{
    "source_code": "Complete source code here",
    "documentation": "Comprehensive documentation",
    "optimization_recommendations": ["Recommendation 1", "Recommendation 2"]
}}
"""
    return prompt

# Function to get threat model from the GPT response.
def get_code_model(api_key, model_name, prompt):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        model_name,
        generation_config={"response_mime_type": "application/json"})
    response = model.generate_content(
        prompt,
        safety_settings={
            'DANGEROUS': 'block_only_high' # Set safety filter to allow generation of threat models
        })
    try:
        # Access the JSON content from the 'parts' attribute of the 'content' object
        response_content = json.loads(response.candidates[0].content.parts[0].text)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {str(e)}")
        print("Raw JSON string:")
        print(response.candidates[0].content.parts[0].text)
        return None

    return response_content

