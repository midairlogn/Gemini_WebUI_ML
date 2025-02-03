# Edited and polished by [Midairlogn](https://github.com/midairlogn) .


import os
import io
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
#import webbrowser
#import time

load_dotenv()

mldefault_initial_prompt = ''' :blue-background[ **Note that** ] :grey-background[ :rainbow[ **_Gemini WebUI ML_** ] ] ( [*Gemini_WebUI_ML - GitHub*](https://github.com/midairlogn/Gemini_WebUI_ML "Gemini_WebUI_ML - GitHub") ) is developed by :grey-background[ :rainbow[ *Midairlogn* ] ] ( [*Midairlogn - GitHub*](https://github.com/midairlogn "Midairlogn - GitHub") ) .   
    **DO NOT promise *100%* stability** . So please carefully read and practice the following tips :  
    - Please clear chat history every time you exit this page or choose a new model to start a new conversation .  
    - If received any error message , please clear chat history to continue . **DO NOT** try to contine this dialogue .   
    - :grey[ ( *Optional* ) ] You will receive the original markdown code from gemini if you **Enable** :grey-background[ :rainbow[ *Optional Features* ] ] on the sidebar . You can go to [dillinger](https://dillinger.io/ "dillinger") to view them .   
    - **DO NOT** translate the Gemini-WebUI-ML page . Translating that page will result in the unstability of the programme and you might receive an error message . If you accidentally translate that page . Please refresh .    
    
    # :rainbow[ How can I help you today ? ]   '''

mldefault_feedback_status = False
mldefault_full_opt_status = False
mldefault_text_opt_status = True
mldefault_token_count_status = True

ml_need_password = True
ml_password = os.getenv("CUSTOMER_PASSWORD")
ml_can_run = False
input_password = ""
#ml_redirect_url="http://www.bing.com/"

if ( ml_password == "" ) : 
    ml_need_password = False

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
    if (ml_need_password):
        input_password = st.text_input("Password",type = "password" )
    select_model = st.sidebar.selectbox('Choose a Model' , ['gemini-2.0-flash-exp' , 'gemini-1.5-flash' , 'gemini-1.5-pro' , 'gemini-1.5-flash-8b' , 'gemini-1.0-pro'] , key='select_model')
    model = genai.GenerativeModel(select_model)
    if ( select_model == 'gemini-2.0-flash-exp' ):
        mldefault_full_opt_status = True
    else :
        mldefault_full_opt_status = False


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

#role swap after every prompt
def role_swap(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

#initialising chat.
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])
    initial_prompt = mldefault_initial_prompt
    st.chat_message("assistant" , avatar = BOT_AVATAR).markdown(initial_prompt)

#clearing the chat history
def clear_chat():
    initial_prompt = mldefault_initial_prompt
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
    if (ml_need_password):
        if (input_password == ml_password):
            ml_can_run = True
    else :
        ml_can_run = True

    if (ml_can_run):
        st.chat_message("user",avatar=USER_AVATAR).markdown(user_prompt)
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
