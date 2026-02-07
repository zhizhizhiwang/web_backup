import os
import shutil

if __name__ == "__main__":
    if os.path.exists("crawls"): 
        shutil.rmtree("crawls")
    os.mkdir("crawls")