from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Baseten configuration
BASETEN_API_KEY = os.getenv('BASETEN_API_KEY')
BASE_URL = os.getenv('BASE_URL')
MODEL_NAME = os.getenv('MODEL_NAME')

client = OpenAI(
    api_key=BASETEN_API_KEY,
    base_url=BASE_URL
)

sys_msg = """You are a patient tech support assistant for seniors. Use short sentences. One step at a time. Avoid jargon.

Provide: One simple step to try first in clear instructions. Keep under 5 sentences. 
Use simple words. Assume the user has no technical background and is using iOS and MacOS devices."""

"""
# Define test cases
cases = [
    "I can't remember my email password",
    "My phone screen is too dark",
    "How do I video call my grandkids?",
]
"""

print("Enter a test case for the tech support assistant:")
cases = [input()]

# Test all cases
print("=" * 80)
print("TESTING BASETEN MODEL DEPLOYMENT")
print("=" * 80)

for case in cases:
    print(f"\n{'='*80}")
    print(f"TEST CASE: {case}")
    print(f"{'='*80}")
    
    # Make API call
    response_chat = client.chat.completions.create(
        model=MODEL_NAME, # type: ignore to suppress type checking error
        messages=[
            {
                "role": "system", "content": sys_msg},
                {"role": "user", "content": f"A senior user says: `{case}` Provide tech support as per the system instructions."}
        ],
        temperature=0.1,
        max_tokens=100,
    )

    # Extract and display response
    assistant_message = response_chat.choices[0].message.content
    print(f"\nRESPONSE:\n{assistant_message}")

    # Display token usage if available
    if response_chat.usage:
        print(f"\nTokens used: {response_chat.usage.total_tokens}")
    else:
        print("\nToken usage not available")

print(f"\n{'='*80}")
print("ALL TESTS COMPLETED")
print(f"{'='*80}")