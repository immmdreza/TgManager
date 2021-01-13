import os
from configs import session_path, main_session

def getSessions():
    for file in os.listdir(session_path):
        if file.endswith(".session"):
            r = file.replace('.session', '')
            if r != main_session:
                yield r