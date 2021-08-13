# IBM STT Customizer
A customizer script for IBM Speech to Text

```bash
pip install --upgrade "ibm-watson>=5.2.2"
```

# Instructions
1. Update credentials inside of customizer_model.py
```
title_scrip('IBM STT Customizer')
api_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
api_url = "https://api.us-south.speech-to-text.watson.cloud.ibm.com/instances/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
stt = instantiate_stt(api_key, api_url)
```
2. Execute the app
```
python3 customizer_model.py language get
```