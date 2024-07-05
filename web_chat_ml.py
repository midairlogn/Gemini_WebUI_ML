# Edited and polished by [Midairlogn](https://github.com/midairlogn) .


import os
import io
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

mldefult_initial_prompt = ''' :blue-background[ **Note that** ] :grey-background[ :rainbow[ **_Gemini WebUI ML_** ] ] ( [*Gemini_WebUI_ML - GitHub*](https://github.com/midairlogn/Gemini_WebUI_ML "Gemini_WebUI_ML - GitHub") ) is developed by :grey-background[ :rainbow[ *Midairlogn* ] ] ( [*Midairlogn - GitHub*](https://github.com/midairlogn "Midairlogn - GitHub") ) .   
    **DO NOT promise *100%* stability** . So please carefully read and practice the following tips :  
    - Please clear chat history every time you exit this page or choose a new model to start a new conversation .  
    - If received any error message , please clear chat history to continue . **DO NOT** try to contine this dialogue .   
    - :grey[ ( *Optional* ) ] You will receive the original markdown code from gemini if you **Enable** :grey-background[ :rainbow[ *Optional Features* ] ] on the sidebar . You can go to [dillinger](https://dillinger.io/ "dillinger") to view them .   
    
    # :rainbow[ How can I help you today ? ]   '''

mldefult_full_opt_status = False
mldefult_text_opt_status = True

#sets the avatar for user as well as the bot
USER_AVATAR = "👤"
BOT_AVATAR = "✨"
image_path = "Google-Gemini-AI-Logo.png"


#private key for gemini.
private_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=private_key)


#conifgs the bar 
st.set_page_config(
    page_title = "Gemini WebUI ML",
    page_icon=":sparkle",
    layout="centered"
)

#side bar components
with st.sidebar:
    st.image(image_path , width = 200)
    select_model = st.sidebar.selectbox('Choose a Model' , ['gemini-1.5-flash' , 'gemini-1.5-pro' , 'gemini-1.0-pro' , 'gemini-pro' , 'gemini-pro-vision'] , key='select_model')
    if select_model == 'gemini-1.5-flash':
        model = genai.GenerativeModel('gemini-1.5-flash')
    if select_model == 'gemini-1.5-pro':
        model = genai.GenerativeModel('gemini-1.5-pro')
    if select_model == 'gemini-1.0-pro':
        model = genai.GenerativeModel('gemini-1.0-pro')
    if select_model == 'gemini-pro':
        model = genai.GenerativeModel('gemini-pro')
    if select_model == 'gemini-pro-vision':
        model_vision = genai.GenerativeModel('gemini-pro-vision')

with st.sidebar:
    st.markdown(" :grey-background[ :rainbow[ *Optional Features* ] ] ")
    full_opt = st.toggle(":violet[ Full feedback code ]",value = mldefult_full_opt_status )
    if ( full_opt ):
        st.markdown(" :green[ *Enabled !* ] ")
    else :
        st.markdown(" :red[ *Disabled !* ] ")
    text_opt = st.toggle(":orange[ Text feedback code ]",value = mldefult_text_opt_status )
    if ( text_opt ):
        st.markdown(" :green[ *Enabled !* ] ")
    else :
        st.markdown(" :red[ *Disabled !* ] ")

#role swap after every prompt
def role_swap(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

#initialising chat.
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])
    initial_prompt = mldefult_initial_prompt
    st.chat_message("assistant" , avatar = BOT_AVATAR).markdown(initial_prompt)

#clearing the chat history
def clear_chat():
    initial_prompt = mldefult_initial_prompt
    st.session_state.chat_session = model.start_chat(history=[])
    st.chat_message("assistant" , avatar = BOT_AVATAR).markdown(initial_prompt)
st.sidebar.button('Clear Chat Histrory',on_click=clear_chat) 

#displays the history accordingly
for message in st.session_state.chat_session.history:
    with st.chat_message(role_swap(message.role),avatar=BOT_AVATAR if message.role == "model" else USER_AVATAR):
         st.markdown(message.parts[0].text)

#main prompt logic.
user_prompt = st.chat_input("Message Gemini")
if user_prompt:
    st.chat_message("user",avatar=USER_AVATAR).markdown(user_prompt)
    gemini_response = st.session_state.chat_session.send_message(user_prompt)
    with st.chat_message("assistant",avatar=BOT_AVATAR):
        if ( full_opt ):  
            st.markdown(" :grey-background[ :rainbow[ *Optional Features :* ] ] :violet[ Full feedback code : ] ")
            st.code(gemini_response , language='markdown')
        if ( text_opt ):
            st.markdown(" :grey-background[ :rainbow[ *Optional Features :* ] ] :orange[ Text feedback code : ] ")
            st.code(gemini_response.text , language='markdown')
        st.markdown(" :grey-background[ :rainbow[ Gemini's **text** feedback ( *Markdown On* ) ] ] ")
        st.markdown(gemini_response.text)