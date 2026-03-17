# Edited and polished by [Midairlogn](https://github.com/midairlogn) .

import os
import io
import json
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import requests
import mimetypes
import tempfile
import base64
import time
from PIL import Image
import re
import datetime
#import webbrowser
#import time

load_dotenv()

# Read mlconfig.json
def read_config_from_json(filepath):
  """
  read data from a certain .json file

  Args:
    filepath: filepath of JSON 

  Returns:
    JSON configure data
  """
  try:
    with open(filepath, 'r', encoding='utf-8') as f:
      configure_data = json.load(f)
      return configure_data
  except FileNotFoundError:
    print(f"Error：File Not Found: {filepath}")
    return None
  except json.JSONDecodeError:
    print(f"Error：Can Not Decode: {filepath}")
    return None

ml_config_data = read_config_from_json("mlconfig.json")
ml_private_config_data = read_config_from_json("private-config-ml.json")

def ml_print_log(content):
    if ml_private_config_data.get("print_record"):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        prefix = f"[{current_time}] "
        # Create indentation string with length equal to prefix
        indent = " " * len(prefix)
        # Replace newlines with newline + indent
        formatted_content = content.replace('\n', '\n' + indent)
        print(f"{prefix}{formatted_content}")

#role swap after every prompt
def role_swap(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

# Set password
ml_need_password = ml_config_data.get("application_data", {}).get("ml_need_password")
ml_current_user = ml_private_config_data.get("user_settings", {}).get("default_user")
ml_can_run = False
input_password = ""
#ml_redirect_url="http://www.bing.com/"

# Set initial prompt
mldefault_initial_prompt = ''' :blue-background[ **Note that** ] :grey-background[ :rainbow[ **_Gemini WebUI ML_** ] ] ( [*Gemini_WebUI_ML - GitHub*](https://github.com/midairlogn/Gemini_WebUI_ML "Gemini_WebUI_ML - GitHub") ) is developed by :grey-background[ :rainbow[ *Midairlogn* ] ] ( [*Midairlogn - GitHub*](https://github.com/midairlogn "Midairlogn - GitHub") ) .   
    **DO NOT promise *100%* stability** . So please carefully read and practice the following tips :  
    - Please clear chat history every time you exit this page or choose a new model to start a new conversation .  
    - If received any error message , please clear chat history to continue . **DO NOT** try to contine this dialogue .   
    - :grey[ ( *Optional* ) ] You will receive the original markdown code from gemini if you **Enable** :grey-background[ :rainbow[ *Optional Features* ] ] on the sidebar . You can go to [dillinger](https://dillinger.io/ "dillinger") to view them .   
    - **DO NOT** translate the Gemini-WebUI-ML page . Translating that page will result in the unstability of the programme and you might receive an error message . If you accidentally translate that page . Please refresh .    
    
    # :rainbow[ How can I help you today ? ]   '''

# Set optional features
mldefault_feedback_status =  ml_config_data.get("application_data", {}).get("mldefault_feedback_status")
mldefault_full_opt_status = ml_config_data.get("application_data", {}).get("mldefault_full_opt_status")
mldefault_text_opt_status = ml_config_data.get("application_data", {}).get("mldefault_text_opt_status")
mldefault_token_count_status = ml_config_data.get("application_data", {}).get("mldefault_token_count_status")

#conifgs the bar 
st.set_page_config(
    page_title = "Gemini WebUI ML",
    page_icon=":sparkle",
    layout="centered"
)

def ml_set_private_key():
    global ml_current_user
    global ml_newapi_chat_url
    global ml_newapi_headers
    global ml_newapi_payload
    # private key for gemini.
    if (ml_current_user.get("use_new_api")): 
        # set new api posts
        ml_newapi_chat_url = ""
        ml_newapi_headers = {
        "Content-Type": "",
        "Authorization": f""
        }
        ml_newapi_payload = {
        "model": "",
        "messages": [
        ]
        }
    else: 
        private_key = ml_current_user.get("GOOGLE_API_KEY")
        if (private_key):
            genai.configure(api_key=private_key)

def ml_judge_password():
    global input_password
    global ml_current_user
    global ml_private_config_data
    password_correct = False
    for ml_user in ml_private_config_data.get("user_settings", {}):
        ml_current_user_process = ml_private_config_data.get("user_settings", {}).get(ml_user, {})
        if (input_password == ml_current_user_process.get("password")):
            password_correct = True
            ml_current_user = ml_private_config_data.get("user_settings", {}).get(ml_user, {})
    if (password_correct):
        ml_set_private_key()
        return True
    else :
        ml_current_user = ml_private_config_data.get("user_settings", {}).get("default_user")
        return False

#initialize models
#ml_gemini_models = ml_config_data.get("application_data", {}).get("ml_gemini_models", [])
if "ml_gemini_models" not in st.session_state:
    st.session_state.ml_gemini_models = ml_config_data.get("application_data", {}).get("ml_gemini_models", [])

# Set gemini models
def ml_set_gemini_models():
    global ml_config_data
    global ml_current_user
#    if ml_current_user.get("use_new_api"):
    #//// working
#        if "user_models" not in ml_current_user:
            #ml_gemini_models = ml_config_data.get("application_data", {}).get("ml_gemini_models", [])
#            st.session_state.ml_gemini_models = ml_config_data.get("application_data", {}).get("ml_gemini_models", [])
#        else:
#            #ml_gemini_models = ml_current_user.get("user_models", [])
#            st.session_state.ml_gemini_models = ml_current_user.get("user_models", [])
#            st.code("user_models")
        #ml_gemini_models = ml_current_user.get("user_models", [])
#    else:
        #ml_gemini_models = ml_config_data.get("application_data", {}).get("ml_gemini_models", [])
#        st.session_state.ml_gemini_models = ml_config_data.get("application_data", {}).get("ml_gemini_models", [])
    if "private_models" not in ml_private_config_data:
        st.session_state.ml_gemini_models = ml_config_data.get("application_data", {}).get("ml_gemini_models", [])
    else:
        st.session_state.ml_gemini_models = ml_private_config_data.get("private_models", [])

ml_set_gemini_models()

def ml_password_on_change():
    ml_judge_password()
    ml_set_gemini_models()
    #st.code(st.session_state.ml_gemini_models)

# Initialize session state: add 'ml_system_instruction'
if "ml_system_instruction" not in st.session_state:
    st.session_state.ml_system_instruction = ml_config_data.get("application_data", {}).get("ml_default_system_instuction")

# Initialize local chat history for display
if "local_chat_history" not in st.session_state:
    st.session_state.local_chat_history = []

# Initialize uploader key
if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0 

#sets the avatar for user as well as the bot
USER_AVATAR = ml_config_data.get("application_data", {}).get("USER_AVATAR")
BOT_AVATAR = ml_config_data.get("application_data", {}).get("BOT_AVATAR")
image_path = ml_config_data.get("application_data", {}).get("image_path")

ml_set_private_key()

#side bar components : Gemini Image
st.sidebar.image(image_path , width = 200)

#side bar components : password
input_password = st.sidebar.text_input("Password", type = "password" , on_change=ml_password_on_change )

#side bar components : select model
with st.sidebar:
    #select_model = st.sidebar.selectbox('Choose a Model' , ml_gemini_models , key='select_model')
    select_model = st.sidebar.selectbox('Choose a Model' , st.session_state.ml_gemini_models , key='select_model')
    if st.session_state.ml_system_instruction:
        model = genai.GenerativeModel(model_name = select_model, system_instruction=st.session_state.ml_system_instruction)
    else:
        model = genai.GenerativeModel(model_name = select_model)

#side bar components : File Uploader
with st.sidebar:
    st.markdown(" :grey-background[ :rainbow[ *Uploads* ] ] ")
    uploaded_files = st.file_uploader("Upload Media (Images, Docs, and so on...)", accept_multiple_files=True, key=f"uploader_{st.session_state.uploader_key}")

#side bar components : Optional Features
with st.sidebar:
    st.markdown(" :grey-background[ :rainbow[ *Optional Features* ] ] ")
    feedback_status = st.checkbox(" *Show status* ",value= mldefault_feedback_status )
    full_opt = st.toggle(":violet[ Full response code ]",value = mldefault_full_opt_status )
    if ( feedback_status ):
        if ( full_opt ):
            st.markdown(" :green[ *Enabled !* ] ")
        else :
            st.markdown(" :red[ *Disabled !* ] ")
    text_opt = st.toggle(":orange[ Text response code ]",value = mldefault_text_opt_status )
    if ( feedback_status ):
        if ( text_opt ):
            st.markdown(" :green[ *Enabled !* ] ")
        else :
            st.markdown(" :red[ *Disabled !* ] ")
    token_count = st.toggle(":blue[ Token count ]",value = mldefault_token_count_status )
    if ( feedback_status ):
        if ( token_count ):
            st.markdown(" :green[ *Enabled !* ] ")
        else :
            st.markdown(" :red[ *Disabled !* ] ")

# System Instruction: Show and Edit
@st.dialog("System Instructions", width="large")
def edit_system_instruction():
    global model
    st.markdown("Current System Instructions :")
    if (st.session_state.ml_system_instruction): 
        st.code(st.session_state.ml_system_instruction)
    else: 
        st.code("[The system instruction is empty]")
    ml_input_system_instruction = st.text_area("Edit System Instructions :", value = st.session_state.ml_system_instruction)
    st.write(f"Total characters: {len(ml_input_system_instruction)}")
    if st.button('Submit'):
        if ml_input_system_instruction:
            st.session_state.ml_system_instruction = ml_input_system_instruction
            model = genai.GenerativeModel(model_name = select_model, system_instruction=st.session_state.ml_system_instruction)
        else :
            st.session_state.ml_system_instruction = "" 
            model = genai.GenerativeModel(model_name = select_model)
        st.rerun()

st.sidebar.button('System Instruction', on_click=edit_system_instruction)

# Initialising chat
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])
    initial_prompt = mldefault_initial_prompt
    st.chat_message("assistant" , avatar = BOT_AVATAR).markdown(initial_prompt)

#Display all the Chat History 
@st.dialog("All Chat History", width="large") 
def ml_display_all_history_popup():
    st.markdown(" :grey-background[ :rainbow[ *Optional Features :* ] ] :blue[ Overview : ] ")
    st.code(st.session_state.chat_session)
    st.markdown(" :grey-background[ :rainbow[ *Optional Features :* ] ] :violet[ System Instruction : ] ")
    if (st.session_state.ml_system_instruction): 
        st.code(st.session_state.ml_system_instruction)
    else: 
        st.code("[The system instruction is empty]")
    st.markdown(" :grey-background[ :rainbow[ Gemini's **text** feedback ( *Markdown Code* ) ] ] ")
    ml_display_history(False)

st.sidebar.button('Display Chat History', on_click=ml_display_all_history_popup)

#function: clearing the chat history
def clear_chat():
    initial_prompt = mldefault_initial_prompt
    st.session_state.chat_session = model.start_chat(history=[])
    st.session_state.local_chat_history = []
    # Reset local history with initial prompt
    st.session_state.local_chat_history.append({"role": "assistant", "content": initial_prompt})
    st.session_state.uploader_key += 1 # Clear uploader
    # st.chat_message("assistant" , avatar = BOT_AVATAR).markdown(initial_prompt) # handled by display loop now

#clearing the chat history
st.sidebar.button('Clear Chat Histrory', on_click=clear_chat, type="primary") 

#displays the history accordingly
def ml_display_history(ml_display_markdown_on):
    # Sync if local history is empty but chat_session has history (e.g. after restart/reload)
    if not st.session_state.local_chat_history and st.session_state.chat_session.history:
        for message in st.session_state.chat_session.history:
             role = role_swap(message.role)
             try:
                 text_content = message.parts[0].text
             except:
                 text_content = ""
             st.session_state.local_chat_history.append({"role": role, "content": text_content})

    for message in st.session_state.local_chat_history:
        with st.chat_message(message['role'], avatar=BOT_AVATAR if message['role'] == "assistant" else USER_AVATAR):
            # Display text content
            if message.get('content'):
                if ml_display_markdown_on:
                    st.markdown(message['content'])
                else:
                    st.code(message['content'])

            # Display images/files
            if message.get('images'):
                for img_data in message['images']:
                    # Check if it's a PIL Image or bytes or something else
                    try:
                        st.image(img_data, width=200)
                    except:
                        st.markdown(f"*[Attached Media]*")

            # Display videos
            if message.get('videos'):
                for video_data in message['videos']:
                    try:
                        st.video(video_data)
                    except:
                        st.markdown(f"*[Attached Video]*")

ml_display_history(True)

#side bar components : Version
ml_application_version = ml_config_data.get("version")
st.sidebar.markdown(":grey[*Version: "+ml_application_version+"*]")

# Refresh: the settings of model-choose and system instructions
st.session_state.chat_session = model.start_chat( history = st.session_state.chat_session.history )

def get_base64_of_file(file_data):
    return base64.b64encode(file_data).decode('utf-8')

def ml_process_uploaded_files_direct(uploaded_files):
    parts = []
    for uploaded_file in uploaded_files:
        mime_type = uploaded_file.type
        if mime_type.startswith("image"):
            parts.append(Image.open(uploaded_file))
        else:
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name

            #print(f"Uploading {uploaded_file.name} to Gemini...")
            file_ref = genai.upload_file(path=tmp_file_path, mime_type=mime_type)

            # Wait for processing if it's a video
            if mime_type.startswith("video"):
                while file_ref.state.name == "PROCESSING":
                    #print("Processing video...", end='\r')
                    time.sleep(1)
                    file_ref = genai.get_file(file_ref.name)

            parts.append(file_ref)
    return parts

def ml_process_uploaded_files_newapi(uploaded_files):
    content_list = []
    for uploaded_file in uploaded_files:
        mime_type = uploaded_file.type
        # NewAPI/OpenAI mostly supports images via base64
        if mime_type.startswith("image"):
            b64_str = get_base64_of_file(uploaded_file.getvalue())
            content_list.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:{mime_type};base64,{b64_str}"
                }
            })
        else:
            # Handle text/code files
            if mime_type.startswith("text") or mime_type in ["application/json", "text/csv"]:
                 text_content = uploaded_file.getvalue().decode("utf-8")
                 content_list.append({
                     "type": "text",
                     "text": f"File: {uploaded_file.name}\nContent:\n{text_content}"
                 })
    return content_list

# set new api posts
def ml_edit_posts(ml_edit_posts_receive_user_message, newapi_content_parts=None):
    global ml_newapi_chat_url
    global ml_newapi_headers
    global ml_newapi_payload
    ml_newapi_chat_url = ml_current_user.get("new_api_settings", {}).get("ml_newapi_chat_url")
    ml_newapi_Content_Type = ml_current_user.get("new_api_settings", {}).get("Content-Type")
    ml_newapi_Authorization = ml_current_user.get("new_api_settings", {}).get("Authorization")
    ml_newapi_headers["Content-Type"] = ml_newapi_Content_Type
    ml_newapi_headers["Authorization"] = ml_newapi_Authorization
    ml_newapi_payload["model"] = st.session_state.select_model
    ml_newapi_payload_messages_process = []
    if (st.session_state.ml_system_instruction):
        ml_newapi_payload_messages_process.append({ "role": "system", "content": st.session_state.ml_system_instruction})
    for message in st.session_state.chat_session.history:
        # Handle existing history parts (simple text extraction for now)
        try:
             content_text = message.parts[0].text
        except:
             content_text = "[Media content]" # Placeholder if history has media
        ml_newapi_payload_messages_process.append({ "role": role_swap(message.role), "content": content_text})

    # Construct current user message
    if newapi_content_parts:
        final_content = []
        final_content.append({"type": "text", "text": ml_edit_posts_receive_user_message})
        final_content.extend(newapi_content_parts)
        ml_newapi_payload_messages_process.append({ "role": "user", "content": final_content})
    else:
        ml_newapi_payload_messages_process.append({ "role": "user", "content": ml_edit_posts_receive_user_message})

    ml_newapi_payload["messages"] = ml_newapi_payload_messages_process
    #st.code(ml_newapi_payload)

#main prompt logic.
user_prompt = st.chat_input("Message Gemini")
if user_prompt:
    ml_print_log(f"User: {user_prompt}")
    if (ml_judge_password()):
        ml_can_run = True
    if (ml_can_run):
        # Prepare local history entry
        current_user_msg = {"role": "user", "content": user_prompt, "images": [], "videos": []}

        # Display uploaded files locally and prepare for API
        display_images = []
        display_videos = []
        if uploaded_files:
            for uploaded_file in uploaded_files:
                if uploaded_file.type.startswith('image'):
                    # Keep PIL Image for display
                    img = Image.open(uploaded_file)
                    display_images.append(img)
                elif uploaded_file.type.startswith('video'):
                    # Keep video bytes for display
                    video_data = uploaded_file.getvalue()
                    display_videos.append(video_data)
                else:
                    # For non-images/videos, just append a placeholder text to content or similar?
                    # Current requirement focuses on images. For files, we might want to show filename.
                    current_user_msg["content"] += f"\n\n[Attached File: {uploaded_file.name}]"

        current_user_msg["images"] = display_images
        current_user_msg["videos"] = display_videos
        st.session_state.local_chat_history.append(current_user_msg)

        # Display Immediately
        with st.chat_message("user", avatar=USER_AVATAR):
            st.markdown(user_prompt)
            for img in display_images:
                st.image(img, width=200)
            for video in display_videos:
                st.video(video)

        if (ml_current_user.get("use_new_api")):
            newapi_parts = []
            if uploaded_files:
                # Re-seek files because they might have been read
                for f in uploaded_files: f.seek(0)
                newapi_parts = ml_process_uploaded_files_newapi(uploaded_files)

            # Check for images in the previous assistant message (for Banana/NewAPI model continuity)
            if st.session_state.local_chat_history:
                 # The last message is the current user message (just appended)
                 # The one before that should be the assistant's message.
                 if len(st.session_state.local_chat_history) >= 2:
                     last_assistant_msg = st.session_state.local_chat_history[-2]
                     if last_assistant_msg['role'] == 'assistant' and last_assistant_msg.get('images'):
                         for img_url in last_assistant_msg['images']:
                             # Only attach URLs (which likely came from the model), not PIL images (which came from user uploads)
                             if isinstance(img_url, str) and (img_url.startswith("http") or img_url.startswith("data:")):
                                 newapi_parts.append({
                                     "type": "image_url",
                                     "image_url": {
                                         "url": img_url
                                     }
                                 })

            ml_edit_posts(user_prompt, newapi_parts)
            try:
                gemini_response_ml = requests.post(ml_newapi_chat_url, headers=ml_newapi_headers, json=ml_newapi_payload)
                gemini_response_ml.raise_for_status()

                if gemini_response_ml.json():
                    gemini_response = gemini_response_ml.json()
                    gemini_response_text_ml = gemini_response['choices'][0]['message']['content']
                    ml_print_log(f"AI: {gemini_response_text_ml}")

                    # Extract images from response (Markdown)
                    generated_images = []
                    # Regex for ![alt](url) or ![alt](url "title")
                    markdown_images = re.findall(r'!\[.*?\]\(([^)\s]+)(?:\s+".*?")?\)', gemini_response_text_ml)
                    generated_images.extend(markdown_images)

                    gemini_response_usage_ml = gemini_response['usage']

                    # Update Gemini Session History (Text Only)
                    ml_newapi_chat_history_process = st.session_state.chat_session.history
                    ml_newapi_chat_history_process.append({'parts': [{'text': user_prompt}], 'role': 'user'})
                    ml_newapi_chat_history_process.append({'parts': [{'text': gemini_response_text_ml}], 'role': 'model'})
                    st.session_state.chat_session = model.start_chat( history = ml_newapi_chat_history_process )

                    # Update Local History
                    st.session_state.local_chat_history.append({"role": "assistant", "content": gemini_response_text_ml, "images": generated_images})

                    with st.chat_message("assistant",avatar=BOT_AVATAR):
                        if ( full_opt ):
                            st.markdown(" :grey-background[ :rainbow[ *Optional Features :* ] ] :violet[ Full response code : ] ")
                            st.code(gemini_response , language='markdown')
                        if ( text_opt ):
                            st.markdown(" :grey-background[ :rainbow[ *Optional Features :* ] ] :orange[ Text response code : ] ")
                            st.code(gemini_response_text_ml , language='markdown')
                        if ( token_count ):
                            st.markdown(" :grey-background[ :rainbow[ *Optional Features :* ] ] :blue[ Token count : ] ")
                            st.code(gemini_response_usage_ml , language='markdown')
                        st.markdown(" :grey-background[ :rainbow[ Gemini's **text** feedback ( *Markdown On* ) ] ] ")
                        st.markdown(gemini_response_text_ml)
                        for img_url in generated_images:
                            st.image(img_url, width=200)
                else:
                     # Error handling...
                     st.error("No data returned in the response.")

            except Exception as e:
                 st.error(f"Error: {e}")

        else:
            # Direct Gemini Logic
            content_to_send = [user_prompt]
            if uploaded_files:
                for f in uploaded_files: f.seek(0)
                direct_parts = ml_process_uploaded_files_direct(uploaded_files)
                content_to_send.extend(direct_parts)

            try:
                gemini_response = st.session_state.chat_session.send_message(content_to_send)

                # Handle parts for Text and Images
                gemini_response_text_ml = ""
                generated_images_direct = []

                if hasattr(gemini_response, 'parts'):
                    for part in gemini_response.parts:
                        if part.text:
                            gemini_response_text_ml += part.text

                        # Check for inline_data (images)
                        if hasattr(part, 'inline_data') and part.inline_data:
                            img_data = part.inline_data.data
                            img = Image.open(io.BytesIO(img_data))
                            generated_images_direct.append(img)
                else:
                    gemini_response_text_ml = gemini_response.text

                ml_print_log(f"AI: {gemini_response_text_ml}")

                # Update Local History
                st.session_state.local_chat_history.append({
                    "role": "assistant",
                    "content": gemini_response_text_ml,
                    "images": generated_images_direct
                })

                with st.chat_message("assistant",avatar=BOT_AVATAR):
                    if ( full_opt ):
                        st.markdown(" :grey-background[ :rainbow[ *Optional Features :* ] ] :violet[ Full response code : ] ")
                        st.code(gemini_response , language='markdown')
                    if ( text_opt ):
                        st.markdown(" :grey-background[ :rainbow[ *Optional Features :* ] ] :orange[ Text response code : ] ")
                        st.code(gemini_response_text_ml , language='markdown')
                    if ( token_count ):
                        st.markdown(" :grey-background[ :rainbow[ *Optional Features :* ] ] :blue[ Token count : ] ")
                        st.code(gemini_response.usage_metadata , language='markdown')

                    st.markdown(" :grey-background[ :rainbow[ Gemini's **text** feedback ( *Markdown On* ) ] ] ")
                    if gemini_response_text_ml:
                        st.markdown(gemini_response_text_ml)

                    if generated_images_direct:
                        for img in generated_images_direct:
                            st.image(img, width=200)

            except Exception as e:
                st.error(f"Error: {e}")
    else :
        with st.chat_message("user",avatar=USER_AVATAR):
            st.markdown(user_prompt)
            st.code(user_prompt)
        with st.chat_message("assistant",avatar=BOT_AVATAR):
            st.markdown(" ## :red[ Error: ] ")
            st.code("Wrong password !")
            st.markdown(" :red[ Wrong password ! ] ")

    # Clear uploader and refresh view
    st.session_state.uploader_key += 1
    st.rerun()