# xero-python-oauth-starter

This application used OAuth 2.0 authentication to get accounting data from Xero, then re-formmat them into excel readable files.

## Getting Started
### Global installation: 
* (1) Kviy UI (to be replaced by React in future)
* Please copy the following code and paste them in the terminal:
* python -m pip install --upgrade pip wheel setuptools
* python -m pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew
* python -m pip install kivy.deps.gstreamer

* (2) Pip Version == 9.0.3
* Please upgrade pip for compatibility
* python -m pip install pip==9.0.3 

* Remarks:
* Please use python 3.7 or below for implmentation.
* Otherwise, ImportError: cannot import name 'Mapping' from 'collections'.


### Local installation
* Create new python virtual environment by running `python3 -m venv venv`
* Activate new virtual environment by running `source venv/bin/activate` (for mac) or `.\venv\Scripts\activate.bat` (for Windows)
* Install project dependencies by running `pip install -r requirements.txt`


## Configure API keys
* Create a `config.py` file in the root directory of this project & add the 2 variables
```python
CLIENT_ID = "...client id string..."
CLIENT_SECRET = "...client secret string..."
```

