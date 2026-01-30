import gradio as gr
import requests
import os
import csv
import time
import threading
from dotenv import load_dotenv

load_dotenv()

client = requests.Session()
BASETEN_API_KEY = os.getenv('BASETEN_API_KEY')
user_problem = ""

SYS_MSG = """You are a patient tech support assistant for seniors. Use short sentences. One step at a time. Avoid jargon.

Provide: One simple step to try first in clear instructions. Keep under 5 sentences.
Use simple words. Assume the user has no technical background and is using iOS and MacOS devices."""

def get_ai_response(problem):
    global user_problem
    user_problem = problem

    resp = client.post(
        "https://model-dq42zk93.api.baseten.co/environments/production/predict",
        headers={"Authorization": f"Api-Key {BASETEN_API_KEY}"},
        json={'stream': False,
              'messages': [
                  {'role': 'system', 'content': SYS_MSG},
                  {'role': 'user', 'content': f"A senior user says: `{problem}` Provide tech support as per the system instructions."}],
              'max_tokens': 200,
              'temperature': 0.4},
    )

    if resp.status_code == 200:
        result = resp.json()
        if 'choices' in result and len(result['choices']) > 0:
            return result['choices'][0]['message']['content']
    return "Sorry, I couldn't get a response. Please try again."

def categorize_problem(problem):
    resp = client.post(
        "https://model-4w5gj0p3.api.baseten.co/development/predict",
        headers={"Authorization": f"Api-Key {BASETEN_API_KEY}"},
        json=problem,
    )
    return resp.json()

def show_loading(problem):
    if not problem.strip():
        return gr.update(value="", visible=False), gr.update(visible=False), "", problem
    return gr.update(value="Loading...", visible=True), gr.update(visible=False), "", problem

def submit_problem(problem, start_time):
    if not problem.strip():
        return gr.update(value="", visible=False), gr.update(visible=False), gr.update(visible=False), ""
    response = get_ai_response(problem)
    elapsed = time.time() - start_time
    timer_text = f"Response generated in {elapsed:.1f} seconds"
    return gr.update(value=response, visible=True), gr.update(visible=True), gr.update(visible=False), timer_text

def handle_yes():
    return gr.update(visible=False), gr.update(visible=True), "Thank you! We're glad we could help. Please share your info so we can follow up:"

def handle_no():
    return gr.update(visible=False), gr.update(visible=True), "Sorry to hear that. Please share your info and we'll create a ticket:"

def validate_email(email):
    return "@" in email and "." in email

def validate_phone(phone):
    digits = ''.join(c for c in phone if c.isdigit())
    return len(digits) == 10

def save_to_csv(name, email, phone, category):
    with open("user_data.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([name, email, phone, category])

def submit_info_yes(name, email, phone):
    save_to_csv(name, email, phone, "Problem Solved")
    return f"Thank you {name}! Your information has been saved. We appreciate your feedback!", gr.update(visible=True)

def categorize_and_save(name, email, phone, problem):
    category = categorize_problem(problem)
    save_to_csv(name, email, phone, category)

def submit_info_no(name, email, phone):
    global user_problem
    threading.Thread(target=categorize_and_save, args=(name, email, phone, user_problem)).start()
    return f"Thank you {name}! A ticket has been created and I will reach out shortly.", gr.update(visible=True)

def start_over():
    return "", gr.update(value="", visible=False), gr.update(visible=False), gr.update(visible=False), "", "", "", "", gr.update(visible=False), ""

with gr.Blocks() as demo:
    gr.Image("GoodGrandsonLogo.PNG", show_label=False, container=False, width=100)

    problem_input = gr.Textbox(label="Enter your tech problem", placeholder="Type your problem here...")
    submit_btn = gr.Button("Submit")

    response_output = gr.Textbox(label="Suggested Troubleshooting", interactive=False, elem_id="response", scale=2, visible=False)
    timer_display = gr.Markdown("")

    with gr.Row(visible=False) as feedback_row:
        gr.Markdown("**Did this fix your problem?**")
        yes_btn = gr.Button("Yes")
        no_btn = gr.Button("No")

    with gr.Column(visible=False) as info_form:
        info_message = gr.Markdown("")
        name_input = gr.Textbox(label="Name")
        email_input = gr.Textbox(label="Email")
        phone_input = gr.Textbox(label="Phone Number")
        submit_info_btn = gr.Button("Submit Info")

    result_message = gr.Markdown("")
    start_over_btn = gr.Button("Start Over", visible=False)

    # track if user clicked yes or no
    user_clicked_yes = gr.State(False)
    start_time = gr.State(0)

    def capture_start_time():
        return time.time()

    submit_btn.click(
        capture_start_time,
        outputs=[start_time]
    ).then(
        show_loading,
        inputs=[problem_input],
        outputs=[response_output, feedback_row, timer_display, problem_input]
    ).then(
        submit_problem,
        inputs=[problem_input, start_time],
        outputs=[response_output, feedback_row, info_form, timer_display]
    )

    yes_btn.click(
        handle_yes,
        outputs=[feedback_row, info_form, info_message]
    ).then(lambda: True, outputs=[user_clicked_yes])

    no_btn.click(
        handle_no,
        outputs=[feedback_row, info_form, info_message]
    ).then(lambda: False, outputs=[user_clicked_yes])

    def submit_info_handler(name, email, phone, clicked_yes):
        errors = []
        if not validate_email(email):
            errors.append("Please enter a valid email address (must contain @ and .)")
        if not validate_phone(phone):
            errors.append("Please enter a valid 10-digit phone number")
        if errors:
            return "\n\n".join(errors), gr.update(visible=False)
        if clicked_yes:
            return submit_info_yes(name, email, phone)
        else:
            return submit_info_no(name, email, phone)

    submit_info_btn.click(
        submit_info_handler,
        inputs=[name_input, email_input, phone_input, user_clicked_yes],
        outputs=[result_message, start_over_btn]
    )

    start_over_btn.click(
        start_over,
        outputs=[problem_input, response_output, feedback_row, info_form, name_input, email_input, phone_input, result_message, start_over_btn, timer_display]
    )

demo.launch()