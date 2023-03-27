import os
from datetime import datetime

filename = 'jobs.csv'

modified_time = os.path.getmtime(filename)
modified_time_str = datetime.fromtimestamp(modified_time).strftime('%Y-%m-%d %H:%M:%S')
print(f"{filename} was last modified at {modified_time_str}")
