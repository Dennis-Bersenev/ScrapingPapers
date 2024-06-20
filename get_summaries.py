"""
Obtains abstracts for all papers citing the paper of interest, and gets a LM to decide which, if any, of those are relevant to some research topic.
(User specifies the paper and the research topic.)
"""

from key import SS_KEY as SS_API_KEY
from key import proxies
from urllib.request import Request, urlopen

import os
import json
import os
import time
import requests
import re
import random 


# All you gotta do is get GPT to scan through these and ask it about the relevance !