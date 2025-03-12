# Psychology Counseling AI Agent

## Overview
MindIO is an AI-powered mental health counseling system designed to provide empathetic support through interactive dialogues. The system leverages advanced language models to deliver personalized responses, coping strategies, and mental health resources tailored to each user's needs.

## Key Features
- **Adaptive Conversation Flow**: Automatically transitions between different counseling stages based on user responses
- **Knowledge-Enhanced Responses**: Integrates external knowledge bases to provide accurate information on mental health topics
- **Multi-Provider Support**: Compatible with various AI providers including OpenAI, DeepSeek, Qwen, SilicoFlow, and Ollama
- **Streamlined Chat Interface**: Clean, user-friendly interface focused on the counseling experience

## Project Structure
The project is organized into several modules, each responsible for specific functionalities:

- **/**: Contains the main application code.
  - **agents/**: Implements various agent types for handling user interactions.
  - **prompts/**: Contains system prompts and templates for guiding conversations.
  - **tools/**: Includes utility functions for psychological test, etc.


## Installation
1. Clone the repository:
   ```
   git clone https://github.com/rendao/mindio.git
   ```
2. Navigate to the project directory:
   ```
   cd mindio
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
There are two ways to start the MindIO application:

### 1. Streamlit Web Interface (Recommended)
To launch the interactive web interface, run:
```
streamlit run run.py
```

### 2. Console Interface
To start the application, run the following command:
```
python console.py
```
Follow the on-screen prompts to interact with the counseling assistant.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.
