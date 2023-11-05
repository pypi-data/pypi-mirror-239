import os

from dotenv import load_dotenv

load_dotenv()


######################
# nlp model definition
######################

DEFAULT_MODEL = "all-mpnet-base-v2"

######################
# base dimension table definition
######################

BONSAI_ACTIVITY_API = "https://lca.aau.dk/api/activity-names"
BONSAI_API_KEY = os.environ.get("BONSAI_API_KEY")
