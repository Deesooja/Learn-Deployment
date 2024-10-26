import logging
from datetime import datetime
import sys
import traceback

class Logger:
    def __init__(self, file_name):
        self.logging = logging
        self.logging.basicConfig(filename=f'Logs/{file_name}.log', level=logging.INFO)
    
    def info(self, data):
        logging.info(f' {datetime.now()} : {data}')
    
    def warning(self, data):
        logging.warning(f' {datetime.now()} : {data}')
    
    def error(self, data):
        try:
            line_number = traceback.extract_tb(sys.exc_info()[2])[0][1]
        except:
            line_number = None
            
        logging.error(f' {datetime.now()} : LineNumber :- {line_number} : {data}')




# with open('../Logs/app.log', 'r') as log_file:
#     print(type(log_file))
#     for line in log_file:
#         print(type(line))
#         print(line)
#         print(line[14:33])
#     # print(log_file.read())   
        
        
       
        
        
