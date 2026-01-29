# Support Scout - AI First Responder for Elder Tech Support

An AI-powered tech support system that provides elder-friendly assistance, attempts to resolve issues, and intelligently categorizes cases for human agent handoff.

---


## Development Phases

✓ Deploy Mistral LLM
✓ Configure and test Mistral Deployment
- Deploy HF categorization model through truss
- Test categorization model independently
- Connect the two models together
- Build frontend with Gradio

---

## Architecture

```
┌─────────────────────────────────────────────┐
│         GRADIO FRONTEND  (Layer 1)           │
│  - Large text input for problem description │
│  - Elder-friendly UI (big fonts/buttons)    │
│  - Two-click feedback system                │
└────────────────┬────────────────────────────┘
                 │
┌────────────────▼────────────────────────────┐
│       BASETEN API LAYER (Layer 2)           │
│  - Endpoint 1: Mistral 7B (Support LLM) ✓   │
│  - Endpoint 2: DeBERTa (Classifier)         │
└────────────────┬────────────────────────────┘
                 │
┌────────────────▼────────────────────────────┐
│         DATA LAYER (Layer 3)                │
│  - CSV logging (timestamp, issue, category) │
│  - Conversation history storage             │
└─────────────────────────────────────────────┘
```

---

## Features Implemented

### Elder-Friendly Support LLM
- **Model**: Mistral 7B Instruct
- **Optimization**: Low temperature (0.4), max 150 tokens
- **Style**: Short sentences, no jargon, one step at a time
- **Speed**: 2-5 seconds per response

### Intelligent Categorization
- **Model**: DeBERTa-v3 zero-shot classifier
- **Categories**:
  - Password Issue
  - App Navigation
  - Device Setup
  - Email Problem
  - Security Concern
  - Other
- **Output**: Category + confidence score

---

## Tech Stack

- **LLM**: Mistral 7B Instruct (4-bit quantized)
- **Classifier**: DeBERTa-v3 base (zero-shot)
- **Deployment**: Baseten + Truss
- **Frontend** (upcoming): Gradio
- **Python**: 3.14.2
