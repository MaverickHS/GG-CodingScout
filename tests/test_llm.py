import os
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv()

# Build client so connections can be re-used across
# requests. This only needs to happen once per session.
client = requests.Session()

# Baseten configuration
BASETEN_API_KEY = os.getenv('BASETEN_API_KEY')
BASE_URL = os.getenv('BASE_URL')
MODEL_NAME = os.getenv('MODEL_NAME')

# System message for the tech support assistant
sys_msg = """You are a patient tech support assistant for seniors. Use short sentences. One step at a time. Avoid jargon.

Provide: One simple step to try first in clear instructions. Keep under 5 sentences. 
Use simple words. Assume the user has no technical background and is using iOS and MacOS devices."""

# Test cases
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

print("=" * 80)
print("TESTING BASETEN MODEL DEPLOYMENT")
print("=" * 80)

for case in cases:
    print(f"\n{'='*80}")
    print(f"TEST CASE: {case}")
    print(f"{'='*80}")
    
    resp = client.post(
    "https://model-dq42zk93.api.baseten.co/environments/production/predict",
    headers={"Authorization": f"Api-Key {BASETEN_API_KEY}"},
    json={'stream': False,  # Changed to False for simple JSON response
          'messages': [
              {'role': 'system', 'content': sys_msg},
              {'role': 'user', 'content': f"A senior user says: `{case}` Provide tech support as per the system instructions."}],
          'max_tokens': 200,
          'temperature': 0.4},
    )

    # Check status and parse response
    if resp.status_code == 200:
        result = resp.json()

        # Extract and display response
        if 'choices' in result and len(result['choices']) > 0:
            assistant_message = result['choices'][0]['message']['content']
            print(f"\nRESPONSE:\n{assistant_message}")

            # Display token usage if available
            if 'usage' in result and result['usage']:
                print(f"\nTokens used: {result['usage']['total_tokens']}")
            else:
                print("\nToken usage not available")
        else:
            print(f"Unexpected response format: {result}")
    else:
        print(f"Error {resp.status_code}: {resp.text}")

print(f"\n{'='*80}")
print("ALL TESTS COMPLETED")
print(f"{'='*80}")