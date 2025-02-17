# Edited and polished by [Midairlogn](https://github.com/midairlogn) .

import os
import io
import json
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
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

# Set initial prompt
mldefault_initial_prompt = ''' :blue-background[ **Note that** ] :grey-background[ :rainbow[ **_Gemini WebUI ML_** ] ] ( [*Gemini_WebUI_ML - GitHub*](https://github.com/midairlogn/Gemini_WebUI_ML "Gemini_WebUI_ML - GitHub") ) is developed by :grey-background[ :rainbow[ *Midairlogn* ] ] ( [*Midairlogn - GitHub*](https://github.com/midairlogn "Midairlogn - GitHub") ) .   
    **DO NOT promise *100%* stability** . So please carefully read and practice the following tips :  
    - Please clear chat history every time you exit this page or choose a new model to start a new conversation .  
    - If received any error message , please clear chat history to continue . **DO NOT** try to contine this dialogue .   
    - :grey[ ( *Optional* ) ] You will receive the original markdown code from gemini if you **Enable** :grey-background[ :rainbow[ *Optional Features* ] ] on the sidebar . You can go to [dillinger](https://dillinger.io/ "dillinger") to view them .   
    - **DO NOT** translate the Gemini-WebUI-ML page . Translating that page will result in the unstability of the programme and you might receive an error message . If you accidentally translate that page . Please refresh .    
    
    # :rainbow[ How can I help you today ? ]   '''

# Set gemini models
ml_gemini_models = ml_config_data.get("application_data", {}).get("ml_gemini_models", [])

# Set optional features
mldefault_feedback_status =  ml_config_data.get("application_data", {}).get("mldefault_feedback_status")
mldefault_full_opt_status = ml_config_data.get("application_data", {}).get("mldefault_full_opt_status")
mldefault_text_opt_status = ml_config_data.get("application_data", {}).get("mldefault_text_opt_status")
mldefault_token_count_status = ml_config_data.get("application_data", {}).get("mldefault_token_count_status")

# Set password
ml_need_password = ml_config_data.get("application_data", {}).get("ml_need_password")
ml_current_user = ml_private_config_data.get("user_settings", {}).get("default_user")
ml_can_run = False
input_password = ""
#ml_redirect_url="http://www.bing.com/"

def ml_judge_password():
    global input_password
    global ml_current_user
    global ml_private_config_data
    password_correct = False
    for ml_user in ml_private_config_data.get("user_settings", {}):
        ml_current_user = ml_private_config_data.get("user_settings", {}).get(ml_user, {})
        if (input_password == ml_current_user.get("password")):
            password_correct = True
    if (password_correct):
        return True
    else :
        ml_current_user = ml_private_config_data.get("user_settings", {}).get("default_user")
        return False

# Initialize session state: add 'ml_system_instruction'
if "ml_system_instruction" not in st.session_state:
    st.session_state.ml_system_instruction = ml_config_data.get("application_data", {}).get("ml_default_system_instuction") 

#sets the avatar for user as well as the bot
USER_AVATAR = ml_config_data.get("application_data", {}).get("USER_AVATAR")
BOT_AVATAR = ml_config_data.get("application_data", {}).get("BOT_AVATAR")
image_path = ml_config_data.get("application_data", {}).get("image_path")


#private key for gemini.
if (ml_current_user.get("use_new_api")): 
    # /////// working
    print("working on it")
else: 
    private_key = ml_current_user.get("GOOGLE_API_KEY")
    if (private_key):
        genai.configure(api_key=private_key)

#conifgs the bar 
st.set_page_config(
    page_title = "Gemini WebUI ML",
    page_icon=":sparkle",
    layout="centered"
)

#side bar components : Gemini Image
st.sidebar.image(image_path , width = 200)

#side bar components : password
input_password = st.sidebar.text_input("Password",type = "password" )

#side bar components : select model
with st.sidebar:
    select_model = st.sidebar.selectbox('Choose a Model' , ml_gemini_models , key='select_model')
    if st.session_state.ml_system_instruction:
        model = genai.GenerativeModel(model_name = select_model, system_instruction=st.session_state.ml_system_instruction)
    else: 
        model = genai.GenerativeModel(model_name = select_model)

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
@st.dialog("System Instructions")
def edit_system_instruction():
    global model
    st.markdown("Current System Instructions :")
    if (st.session_state.ml_system_instruction): 
        st.code(st.session_state.ml_system_instruction)
    else: 
        st.code("[The system instruction is empty]")
    ml_input_system_instruction = st.text_input("Edit System Instructions :")
    if st.button('Submit'):
        if ml_input_system_instruction:
            st.session_state.ml_system_instruction = ml_input_system_instruction
            model = genai.GenerativeModel(model_name = select_model, system_instruction=st.session_state.ml_system_instruction)
        else :
            st.session_state.ml_system_instruction = "" 
            model = genai.GenerativeModel(model_name = select_model)
        st.rerun()

st.sidebar.button('System Instruction', on_click=edit_system_instruction)

#role swap after every prompt
def role_swap(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

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
    st.chat_message("assistant" , avatar = BOT_AVATAR).markdown(initial_prompt)

#clearing the chat history
st.sidebar.button('Clear Chat Histrory', on_click=clear_chat, type="primary") 

#displays the history accordingly
def ml_display_history(ml_display_markdown_on):
    for message in st.session_state.chat_session.history:
        with st.chat_message(role_swap(message.role),avatar=BOT_AVATAR if message.role == "model" else USER_AVATAR):
            if ml_display_markdown_on:
                st.markdown(message.parts[0].text)
            else :
                st.code(message.parts[0].text)

ml_display_history(True)

#side bar components : Version
ml_application_version = ml_config_data.get("version")
st.sidebar.markdown(":grey[*Version: "+ml_application_version+"*]")

# Refresh: the settings of model-choose and system instructions
st.session_state.chat_session = model.start_chat( history = st.session_state.chat_session.history )

#main prompt logic.
user_prompt = st.chat_input("Message Gemini")
if user_prompt:
    if (ml_judge_password()):
        ml_can_run = True
    if (ml_can_run):
        st.chat_message("user",avatar=USER_AVATAR).markdown(user_prompt)
        if (ml_current_user.get("use_new_api")): 
            #/////// working
            print("working on it")
        else: 
            gemini_response = st.session_state.chat_session.send_message(user_prompt)
        with st.chat_message("assistant",avatar=BOT_AVATAR):
            if ( full_opt ):  
                st.markdown(" :grey-background[ :rainbow[ *Optional Features :* ] ] :violet[ Full response code : ] ")
                st.code(gemini_response , language='markdown')
            if ( text_opt ):
                st.markdown(" :grey-background[ :rainbow[ *Optional Features :* ] ] :orange[ Text response code : ] ")
                st.code(gemini_response.text , language='markdown')
            if ( token_count ):
                st.markdown(" :grey-background[ :rainbow[ *Optional Features :* ] ] :blue[ Token count : ] ")
                st.code(gemini_response.usage_metadata , language='markdown')
            st.markdown(" :grey-background[ :rainbow[ Gemini's **text** feedback ( *Markdown On* ) ] ] ")
            st.markdown(gemini_response.text)
    else :
        st.markdown(" ## :red[ Wrong password ! ] ")
        #time.sleep(1)
        #webbrowser.open_new_tab(ml_redirect_url)