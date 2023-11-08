import os
import sys
import pathlib
import shutil
import time
import datetime
import pandas as pd
import knockknock
import matplotlib.pyplot as plt

sys.path.insert(0, '../src/FinToolsAP/')

import LocalDatabase

# set printing options
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', shutil.get_terminal_size()[0])
pd.set_option('display.float_format', lambda x: '%.5f' % x)

# directory for loacl wrds database 

# linux
LOCAL_WRDS_DB = pathlib.Path('/home/andrewperry/Documents')

# mac
#LOCAL_WRDS_DB = pathlib.Path('/Users/andrewperry/Desktop')

def main():

    DB = LocalDatabase.LocalDatabase(save_directory = LOCAL_WRDS_DB, 
                                     database_name = 'WRDS'
                                    )
    
    s = time.time()
    df = DB.query_DB(DB.DBP.CRSP.CRSP_M, ticker = 'C', add_vars = 'comnam')

    e = time.time()
    print(f'loaded = {e - s}')
    print(df)
    print(df.info())
    mem = df.memory_usage(index = True, deep = True)
    print(f'total memory = {mem.sum()}')
    print(f'GiB = {round(mem.sum() / 10 ** 9, 2)}')
    print(df.ticker.nunique())
    



WEBHOOK_URL = 'https://hooks.slack.com/services/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'
@knockknock.slack_sender(webhook_url = WEBHOOK_URL,
                         channel = 'test',
                         user_mentions = ['U01DNFEHKEV'])
def TEST_query_CRSP(): # change to name of file
    main()

if __name__ == "__main__":
    if(os.getlogin() == 'andrewperry'):
        TEST_query_CRSP() # change to name of file
    else:
        main()