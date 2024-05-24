"""
Curates the pruned data by splitting it up into those with/without the source code.
One will then be used for training via RL.
The other will  be used as the test set.
"""


from key import KEY as OPENAI_API_KEY
import json
import os
import pickle
import openai
import time
from scrapegraphai.graphs import SearchGraph
from queryagent import QueryAgent 

openai.api_key = OPENAI_API_KEY

