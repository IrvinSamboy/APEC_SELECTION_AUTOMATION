from dotenv import load_dotenv
import os
load_dotenv(override=True)

class Confing():
    BANNER_URL = os.getenv("BANNER_URL", "https://landing.unapec.edu.do/banner/")
    TEST_EMAIL = os.getenv("TEST_EMAIL")
    TEST_PASSWORD = os.getenv("TEST_PASSWORD")
general_config = Confing()