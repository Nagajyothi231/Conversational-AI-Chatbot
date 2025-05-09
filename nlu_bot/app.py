import chainlit as cl
import requests

RASA_ENDPOINT = "http://localhost:5005/webhooks/rest/webhook"
#RASA_ENDPOINT = "http://localhost:5050/webhooks/rest/webhook"

SUBCATEGORIES = {
    "Programs": [
        "Academic Programs", "Undergraduate", "Master’s", "MBA", "PhD",
        "DBA", "Executive Education", "Certificate Programs", "Honors Programs"
    ],
    "Faculty": [
        "Jindal School Faculty", "Accounting", "Finance and Managerial Economics",
        "Information Systems", "Marketing", "Operations Management",
        "Organizations, Strategy and International Management", "Faculty Research"
    ],
    "Students": [
        "Student Resources", "Advising", "Career Management Center",
        "Scholarships", "Student Organizations"
    ]
}

@cl.on_chat_start
async def start():
    await cl.Message(
        author="bot",
        content="👋 Hello Comet! I’m your UTD JSOM chatbot 🤖\n\nChoose a topic to get started:"
    ).send()

    await cl.Message(
        author="bot",
        content="Please select a main area:",
        actions=[cl.Action(name="main_title", value=k, label=k) for k in SUBCATEGORIES]
    ).send()

@cl.action_callback("main_title")
async def handle_main_title(action: cl.Action):
    cl.user_session.set("main_title", action.value)
    subcats = SUBCATEGORIES.get(action.value, [])

    await cl.Message(
        author="bot",
        content=f"✅ You selected **{action.value}**.\nNow pick a more specific topic:"
    ).send()

    await cl.Message(
        author="bot",
        content="Choose a subcategory:",
        actions=[cl.Action(name="sub_title", value=sub, label=f"🔹 {sub}") for sub in subcats]
    ).send()

@cl.action_callback("sub_title")
async def handle_sub_title(action: cl.Action):
    cl.user_session.set("sub_title", action.value)

    await cl.Message(
        author="bot",
        content=f"✅ You selected **{action.value}**. Now ask your question!"
    ).send()

@cl.on_message
async def handle_message(message: cl.Message):
    selected_title = cl.user_session.get("sub_title")

    if not selected_title:
        await cl.Message(author="bot", content="⚠️ Please select a subcategory first.").send()
        return

    payload = {
        "sender": "user",
        "message": message.content,
        "metadata": {
            "category": selected_title
        }
    }

    try:
        response = requests.post(RASA_ENDPOINT, json=payload).json()
        if response:
            bot_response = response[0].get("text", "")
            await cl.Message(author="bot", content=bot_response).send()
        else:
            await cl.Message(author="bot", content="⚠️ I didn’t get that. Try rephrasing your question.").send()
    except Exception as e:
        await cl.Message(author="bot", content=f"❌ Error talking to Rasa: {e}").send()
