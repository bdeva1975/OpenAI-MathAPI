```markdown
# OpenAI Tool Example: Square Root Calculator

This project demonstrates how to use the OpenAI API to create a simple tool for calculating the square root of a number. The tool interacts with the model to perform mathematical operations by utilizing defined functions.

## Features

- **Functionality**: The tool calculates the square root of a given number.
- **Environment Variables**: Uses `dotenv` to load environment variables, ensuring sensitive information such as API keys are kept secure.
- **Error Handling**: Includes error handling to manage situations where the function fails.
- **Modular Design**: Easily extendable to include more mathematical operations or other operations by adding new functions to the tool list.

## Requirements

- Python 3.x
- OpenAI Python client
- `dotenv` for environment variable management

## Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/bdeva1975/OpenAI-MathAPI
   cd OpenAI-MathAPI
   ```

2. **Install Dependencies**:
   ```bash
   pip install openai python-dotenv
   ```

3. **Create a `.env` File**: In the project directory, create a `.env` file and add your OpenAI API key:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   ```

4. **Run the Script**:
   ```bash
   python tool_use.py
   ```

## Usage

The script defines a tool that calculates the square root of a number. The user can modify the input number by changing the message in the `message_list` section.

## Example

- Input: "What is the square root of 49?"
- Output: 7.0

## License

This project is licensed under the MIT License.
```

Feel free to customize the README further based on your preferences or any additional features you might want to highlight!
