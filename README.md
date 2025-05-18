# Multi-LLM Consensus Builder

A powerful tool that leverages multiple Large Language Models (ChatGPT, Gemini, and Claude) to reach consensus on answers through an iterative process of merging and refinement.

## Features

- Utilizes multiple LLM providers (OpenAI, Google, Anthropic)
- Iterative consensus-building process
- Automatic response merging and refinement
- Configurable maximum iterations
- Detailed logging of the consensus process

## Prerequisites

- Python 3.8+
- API keys for:
  - OpenAI (GPT-4)
  - Google (Gemini)
  - Anthropic (Claude)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd llm_consensus
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with your API keys:
```
OPENAI_API_KEY_personal=your_openai_key
GEMINI_API_KEY=your_gemini_key
ANTHROPIC_API_KEY=your_anthropic_key
```

## Usage

Run the main script:
```bash
python llm_consensus.py
```

The script will prompt you to enter questions, and it will use multiple LLMs to reach a consensus on the answer.

## How It Works

1. The system sends your question to all configured LLMs
2. Responses are collected and analyzed
3. If consensus isn't reached, the system:
   - Merges responses
   - Asks for feedback
   - Iterates until consensus or max iterations reached
4. Returns the final consensus answer

## License

Copyright (c) 2025 Yonathan Guttel

## Contributing

Feel free to submit issues and enhancement requests! 