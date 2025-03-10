# ✨Gemini-WebUI-ML✨

![Gemini-logo](https://raw.githubusercontent.com/midairlogn/Gemini_WebUI_ML/main/Google-Gemini-AI-Logo.png)

Edited and polished by [*Midairlogn*](https://github.com/midairlogn) .

This captivating Streamlit application harnesses the power of Gemini's API key to forge an immersive chatbot that elevates user interactions to new heights. Its intuitive interface empowers users to engage in natural, free-flowing conversations with the chatbot, leveraging Gemini's robust natural language processing capabilities.

Through the seamless integration of Gemini's API key, the chatbot boasts an unparalleled knowledge base and the remarkable ability to engage in meaningful conversations. It effortlessly answers user queries, provides factual information, offers assistance, or simply engages in casual banter, mimicking human-like interactions.

## Screenshots

![Screenshot](https://raw.githubusercontent.com/midairlogn/Gemini_WebUI_ML/main/screenshots/screenshot1.png)

![Screenshot](https://raw.githubusercontent.com/midairlogn/Gemini_WebUI_ML/main/screenshots/screenshot2.png)

## Some tips
* Please clear chat history every time you exit this page or choose a new model to start a new conversation .    
* If received any error message , please clear chat history to continue . DO NOT try to contine this dialogue .    
* ( Optional ) You will receive the original markdown code from gemini if you Enable *Optional Features* on the sidebar . You can go to [dillinger](https://dillinger.io/) to view them .   
* **DO NOT** translate the Gemini-WebUI-ML page . Translating that page will result in the unstability of the programme and you might receive an error message . If you accidentally translate that page . Please refresh .    
     
## Clone this repository   
```
git clone https://github.com/midairlogn/Gemini_WebUI_ML.git
```   

## Preparation : Gemini's API key

To replicate the project in local host you must obtain a gemini api key from the follwing website [here](https://ai.google.dev/) and include them in the `private-config-ml.json` as shown in the `private-config-ml.example.json` .    
  
    
And make sure that Gemini is supported in your region .  

**DO keep your API Key private . DO NOT share it with others !**


## Set up ( Requirements ) 

```
pip install -r requirements.txt
```

* google-generativeai
* streamlit
* python-dotenv

## Password     
To ensure safety , password has now been added . Anyone wanting to access Gemini without the right password will only get the message `Wrong Password !` in response .    
You can set your password in `private-config-ml.json` as is shown in `private-config-ml.example.json`       

## Launch

#### Just type :  
```
streamlit run web_chat_ml.py
```
#### On Windows , you can also 
* run `launch.bat`
#### Customize your port    
- The default port is `6951` . However , you can customize your port by using the following command to launch :   
```
streamlit run web_chat_ml.py --server.port [INTEGER]
```    
Replace `[INTEGER]` with the port you want this programme to run on .    
> *Note that:* Don't use port 3000 which is reserved for internal development.    
- Or alternatively you can edit `config.toml` , find this line :    
```
[server]
port=6951
```    
Replace `6951` with any port you want this programme to run on .   
> *Note that:* Don't use port 3000 which is reserved for internal development.    

## Supported gemini models
- [x] gemini-2.0-flash ( *new* )
- [x] gemini-1.5-flash ( *recommended* )
- [x] gemini-1.5-pro ( *recommended* )
- [x] gemini-1.5-flash-8b
- [x] gemini-1.0-pro
- [x] Support [*New API*](https://github.com/Calcium-Ion/new-api)    
- [x] And many more ( explore for yourself )
> *Note that:*  You can add other models by editing `private-config-ml.json.json`: `"private_models"`. Also, you can add other models by editing `mlconfig.json`: `"application_data"`: `"ml_gemini_models"`    
**Priority:** `private-config-ml.json.json`: `"private_models"` > `mlconfig.json`: `"application_data"`: `"ml_gemini_models"`    

## Supported input
- [x] text ( including *System Instructions* )
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
- [x] ( If you enable *Optional Features* ) usage metadata ( which includes `prompt_token_count` , `candidates_token_count` and `total_token_count`)

