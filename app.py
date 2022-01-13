import pandas as pd
import interface

from config import CLIENT_ID, CLIENT_SECRET

if __name__ == '__main__':
    # Open a user interface
    interface.xero_integration().run()


# xero-python-oauth2-starter-master