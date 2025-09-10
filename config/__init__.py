from dotenv import load_dotenv
import os
load_dotenv(override=True)

class Confing():
    BANNER_URL  = os.getenv("BANNER_URL", "https://landing.unapec.edu.do/banner/")
    
general_config = Confing()