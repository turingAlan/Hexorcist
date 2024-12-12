![Hexorcist Logo](hexorcistLogo.webp)

Hexorcist is an AI-powered tool for embedded systems development. Leveraging Large Language Models (LLMs), Hexorcist generates hardware- and language-specific code, with a strong emphasis on Rust, tailored for the user’s selected hardware. Users can choose from a list of supported hardware and receive optimized code, development guidance, and best practices to accelerate their embedded development process.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)

## Features
- Simple and user-friendly interface
- Generates hardware-specific code based on user-selected hardware
- Strong emphasis on Rust for embedded systems development
- Multi-modal: Use architecture diagrams, flowcharts, etc., as inputs to enhance code generation
- Provides step-by-step guides for embedded development
- Suggests best practices and optimization tips for selected hardware
- Supports models accessed via OpenAI API, Azure OpenAI Service, Google AI API, Mistral API, or 🆕 locally hosted models via Ollama
- Available as a Docker container image for easy deployment
- 🆕 Environment variable support for secure configuration

## Installation

### Option 1: Cloning the Repository

1. Clone this repository:

    ```bash
    git clone https://github.com/turingAlan/Hexorcist.git
    ```

2. Change to the cloned repository directory:

    ```bash
    cd hexorcist
    ```

3. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up environment variables:
   
   a. Copy the `.env.example` file to a new file named `.env`:
   ```
   cp .env.example .env
   ```
   
   b. Edit the `.env` file and add your API keys:
   ```
   GOOGLE_API_KEY=your_actual_github_api_key
   ```

### Option 2: Using Docker Container

1. Create a `.env` file with your API keys as described in step 4 of Option 1.

## Usage

### Option 1: Running the Streamlit App Locally

1. Run the Streamlit app:

    ```bash
    streamlit run main.py
    ```

2. Open the app in your web browser using the provided URL.

3. Follow the steps in the Streamlit interface to use Hexorcist.

### Option 2: Using Docker Container

1. Run the Docker container, mounting the `.env` file:

    ```bash
    docker build -t hexorcist .
    docker run --env-file .env -p 8501:8501 hexorcist
    ```

2. Open a web browser and navigate to `http://localhost:8501` to access the app running inside the container.

3. Follow the steps in the Streamlit interface to use Hexorcist.
