try:
    import importlib.resources as importlib_resources
except ImportError:
    # In PY<3.7 fall-back to backported `importlib_resources`.
    import importlib_resources
    
import json
with importlib_resources.open_text("dtic_topic_finder", "dtic_term_to_topic.json") as file:
    terms_to_topics = json.load(file)  
    
from .dtic_topic_finder import DTICTopicFinder
dtic = DTICTopicFinder(terms_to_topics)




