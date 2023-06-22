# Xero Python OAuth Starter

This application uses OAuth 2.0 authentication to extract accounting data from Xero and reformat it into Excel-readable files.

## Getting Started
### Prerequisites
(1) **Kivy UI**: This application currently uses Kivy UI. It is planned to be replaced by React in the future.  

Install Kivy UI by running the following commands in your terminal:
```bash
python -m pip install --upgrade pip wheel setuptools
python -m pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew
python -m pip install kivy.deps.gstreamer
```

(2) **Pip Version 9.0.3**: This application requires Pip version 9.0.3 for compatibility. Upgrade Pip by running:
```bash
python -m pip install pip==9.0.3
```

**Notes:**
Please use Python 3.7 or below for implementation. Otherwise, you may encounter an ImportError related to the 'Mapping' import from 'collections'.


### Local installation
(1) Create a new Python virtual environment by running: 
```bash
python3 -m venv venv
```  
(2) Activate the new virtual environment by running: 
```bash
source venv/bin/activate`    # For mac
```
or 
```bash
.\venv\Scripts\activate.bat`   # For Windows  
```
(3) Install project dependencies by running
```bash
pip install -r requirements.txt
```


## Configure API keys
(1) Create a config.py file in the root directory of this project  
(2) Add the CLIENT_ID and CLIENT_SECRET variables with their respective values:
```python
CLIENT_ID = "...client id string..."
CLIENT_SECRET = "...client secret string..."
```

