"""
Copyright (c) 2025 Yonathan Guttel

Multi-LLM Consensus Builder
A tool that uses multiple Large Language Models (ChatGPT, Gemini, and Claude) 
to reach consensus on answers through an iterative process of merging and refinement.
"""

import os
from typing import List, Dict, TypedDict, Optional
import openai
from google import genai
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize API clients
openai.api_key = os.getenv("OPENAI_API_KEY_personal")
anthropic = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

class ModelResponse(TypedDict):
    agrees: bool
    response: str

class LLMConsensus:
    def __init__(self):
        self.models = {
            "ChatGPT": self._ask_chatgpt,
            "Gemini": self._ask_gemini,
            "Claude": self._ask_claude
        }
        self.max_iterations = 5

    def _ask_chatgpt(self, prompt: str) -> ModelResponse:
        response = openai.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[{"role": "user", "content": prompt}]
        )
        content = response.choices[0].message.content
        
        try:
            parts = content.split('\n', 1)
            agrees = parts[0].strip().lower() == 'true'
            response_text = parts[1].strip() if len(parts) > 1 else content
            return {"agrees": agrees, "response": response_text}
        except:
            return {"agrees": False, "response": content}

    def _ask_gemini(self, prompt: str) -> ModelResponse:
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        response = client.models.generate_content(
            model='gemini-2.0-flash', contents=prompt
        )
        content = response.text
        
        try:
            parts = content.split('\n', 1)
            agrees = parts[0].strip().lower() == 'true'
            response_text = parts[1].strip() if len(parts) > 1 else content
            return {"agrees": agrees, "response": response_text}
        except:
            return {"agrees": False, "response": content}

    def _ask_claude(self, prompt: str) -> ModelResponse:
        response = anthropic.messages.create(
            model="Claude 3.5 Haiku",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        content = response.content[0].text
        
        try:
            parts = content.split('\n', 1)
            agrees = parts[0].strip().lower() == 'true'
            response_text = parts[1].strip() if len(parts) > 1 else content
            return {"agrees": agrees, "response": response_text}
        except:
            return {"agrees": False, "response": content}

    def _create_merge_prompt(self, question: str, responses: Dict[str, ModelResponse]) -> str:
        prompt = f"Original question: {question}\n\n"
        prompt += "Here are the responses from other AI models:\n\n"
        for model, resp in responses.items():
            prompt += f"{model}:\n{resp['response']}\n\n"
        prompt += """Please merge these responses into a single, comprehensive answer that combines the best aspects of each response. 
Your response should be in the following format:

True
[Merged response that combines the best aspects of all previous responses]

The first line must be 'True' to indicate you're providing a merged response."""
        return prompt

    def _create_feedback_prompt(self, question: str, responses: Dict[str, ModelResponse]) -> str:
        prompt = f"Original question: {question}\n\n"
        prompt += "Here are the responses from other AI models:\n\n"
        for model, resp in responses.items():
            prompt += f"{model}:\n{resp['response']}\n\n"
        prompt += """Please review these responses and provide your feedback in the following format:

True
[Your merged response that combines the best aspects of all responses]

OR

False
[Your detailed response explaining why you disagree and what should be changed]

The first line must be exactly 'True' or 'False' to indicate whether you agree with the merged approach."""
        return prompt

    def _check_consensus(self, responses: Dict[str, ModelResponse]) -> bool:
        # Check if all models agree
        return all(response["agrees"] for response in responses.values())

    def get_consensus(self, question: str) -> str:
        iteration = 0
        responses = {}
        merged_response = None
        
        while iteration < self.max_iterations:
            print(f"\nIteration {iteration + 1}:")
            
            # Get initial responses from all models
            for model_name, model_func in self.models.items():
                if iteration == 0:
                    prompt = question
                elif iteration == 1:
                    # First feedback round - ask to merge responses
                    prompt = self._create_merge_prompt(question, responses)
                else:
                    # Subsequent rounds - ask for feedback on merged response
                    prompt = self._create_feedback_prompt(question, responses)
                
                print(f"\nAsking {model_name}...")
                response = model_func(prompt)
                responses[model_name] = response
                print(f"{model_name}'s agreement status: {'Agrees' if response['agrees'] else 'Disagrees'}")
                print(f"{model_name}'s response: {response['response'][:200]}...")

                # Store the first merged response
                if iteration == 1 and model_name == list(self.models.keys())[0]:
                    merged_response = response["response"]

            # Check for consensus
            if self._check_consensus(responses):
                print("\nConsensus reached! All models agree on the merged response.")
                return merged_response if merged_response else list(responses.values())[0]["response"]

            iteration += 1

        print("\nMaximum iterations reached without consensus.")
        return merged_response if merged_response else list(responses.values())[0]["response"]

def main():
    # Check for API keys
    required_keys = ["OPENAI_API_KEY_personal", "GEMINI_API_KEY"]#, "ANTHROPIC_API_KEY"]
    missing_keys = [key for key in required_keys if not os.getenv(key)]
    
    if missing_keys:
        print(f"Error: Missing API keys for: {', '.join(missing_keys)}")
        print("Please set these environment variables in a .env file")
        return

    consensus = LLMConsensus()
    
    while True:
        question = input("\nEnter your question (or 'quit' to exit): ")
        if question.lower() == 'quit':
            break
            
        print("\nStarting consensus building process...")
        final_answer = consensus.get_consensus(question)
        
        print("\nFinal Merged Answer:")
        print(final_answer)

if __name__ == "__main__":
    main() 