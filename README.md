
# ✨Gemini-WebUI-ML✨

Original code : https://github.com/lgsurith/Gemini_Web_UI  

Edited and polished by [*Midairlogn*](https://github.com/midairlogn) .

This captivating Streamlit application harnesses the power of Gemini's API key to forge an immersive chatbot that elevates user interactions to new heights. Its intuitive interface empowers users to engage in natural, free-flowing conversations with the chatbot, leveraging Gemini's robust natural language processing capabilities.

Through the seamless integration of Gemini's API key, the chatbot boasts an unparalleled knowledge base and the remarkable ability to engage in meaningful conversations. It effortlessly answers user queries, provides factual information, offers assistance, or simply engages in casual banter, mimicking human-like interactions.

## Preparation : Gemini's API key

To replicate the project in local host you must obtain a gemini api key from the follwing website [here](https://ai.google.dev/) and include them in the .env as shown in the .env-example.    
    
And make sure that Gemini is supported in your region .  

**DO keep your API Key private . DO NOT share it with others !**


## Set up ( Requirements ) 

```
  pip install -r requirements.txt
```

* google-generativeai
* streamlit
* python-dotenv

## Launch

#### Just type :  
```
streamlit run web_chat_ml.py
```
#### On Windows , you can also 
* run `launch.bat`


## Supported gemini models
- [x] gemini-1.5-flash
- [x] gemini-1.5-pro
- [x] gemini-1.0-pro
- [x] gemini-pro
- [x] gemini-pro-vision

## Supported input
- [x] text
- [ ] image
- [ ] video
- [ ] pdf 
- [ ] others

## Supported output
- [x] text
- [ ] image
- [ ] video
- [ ] pdf 
- [ ] others
- [x] ( If you enable *Optional Features* ) Gemini's feedback code


## Screenshot
[Screenshot.png]([https://raw.githubusercontent.com/midairlogn/Gemini_WebUI_ML/main/screenshot.png?token=GHSAT0AAAAAACUPGT3JKCOQOFQWQVCVCZ6OZUHSEUA](https://github.com/midairlogn/Gemini_WebUI_ML/blob/main/screenshot.png))

