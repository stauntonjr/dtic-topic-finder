from collections import defaultdict, Counter
import re
from typing import TypedDict, List, Dict, Tuple


class TermScore(TypedDict):
    term: str
    score: int

    
class TopicScore(TypedDict):
    topic: str
    score: int

    
class Result(TypedDict):
    terms: List[TermScore]
    topics: List[TopicScore]


class DTICTopicFinder():
    
    def __init__(self, terms_to_topics: Dict[str, str]) -> None:  
        self.terms_to_topics = terms_to_topics
        
        self.terms = defaultdict(set)
        for term, topic in terms_to_topics.items():
            self.terms[len(term.split())].add(term)
        
        self.term_tokens = {token for term in self.terms_to_topics for token in term.split()}
        
        self.topic_to_category = {}
        self.topic_to_subcategory = {}
        for term, topics in self.terms_to_topics.items():
            for topic in topics:
                cat, subcat, subsubcat = topic.split('; ')
                self.topic_to_category[topic] = cat
                self.topic_to_subcategory[topic] = '; '.join([cat, subcat])
        
    def _gram_find(self, tokens: Tuple[str]) -> None:
        for gram_size in range(min(7, len(tokens)), 0, -1): 
            for i in range(len(tokens) + 1 - gram_size):
                cgram = tokens[i:i+gram_size]
                term = ' '.join(cgram)
                if term in self.terms[gram_size]:
                    self.term_counts[term] += 1
                    self._gram_find(tokens[0:i])
                    self._gram_find(tokens[i+gram_size:])
                    return None
        
    def _set_term_counts(self, text: str) -> None:
        text = re.sub('[\.\;\:]', '', text)
        text = ' '.join([token if token in self.term_tokens else 'X' for token in text.upper().split()])
        text = re.sub('(X ){1,}', 'X ', text)

        spans = [span.strip() for span in text.split('X ') if len(span.strip()) > 2]

        self.term_counts = defaultdict(int)
        for span in spans:
            tokens = tuple(span.split())
            self._gram_find(tokens)
        self.term_counts = dict(sorted(self.term_counts.items(), key=lambda i:-i[1]))
    
    def _get_terms_and_topics(self) -> None:
        subsubcategory_counts = defaultdict(int)
        subcategory_counts = defaultdict(int)
        category_counts = defaultdict(int)

        for subject_term, cnt in self.term_counts.items():
            topics = self.terms_to_topics[subject_term]
            for topic in topics:
                category_counts[self.topic_to_category[topic]] += cnt
                subcategory_counts[self.topic_to_subcategory[topic]] += cnt
                subsubcategory_counts[topic] += cnt

        categories = [i[0] for i in sorted(category_counts.items(), key=lambda i:-i[1])]
        subcategories = [i[0] for i in sorted(subcategory_counts.items(), key=lambda i:-i[1])]
        subsubcategories = [i[0] for i in sorted(subsubcategory_counts.items(), key=lambda i:-i[1])]
        subsubcategories_dict = dict([i for i in sorted(subsubcategory_counts.items(), key=lambda i:-i[1])])
        
        subsubcategories = sorted(
            subsubcategories, 
            key=lambda i: (
                categories.index(i.split('; ')[0]), 
                subcategories.index('; '.join(i.split('; ')[:2])),
                subsubcategories.index(i)
            )
        )
        
        terms = [{"term": term, "score": score} 
                 for term, score in  
            sorted(dict(self.term_counts).items(), key=lambda i:-i[1])]
        
        topics = [{"topic": subsubcategory, "score": subsubcategories_dict[subsubcategory]}
                  for subsubcategory in subsubcategories]
        
        return terms, topics
        
    def __call__(self, text: str, max_topics: int = None, max_terms: int = None) -> Result:
        """Identify topics (DTIC Subject Categories) and terms \
        (DTIC Descriptors/Subject Terms) of text.

            Args:
                text: a string of text for which topics and terms will be identified.
                max_topics: max length of returned topics list.
                max_terms: max length of return terms list.

            Returns:
                A dictionary with key/value pairs for topics and subject_terms.

            Examples:            
            >>> import json
            >>> with open("dtic_term_to_topic.json", "r") as file:
            ...     terms_to_topics = json.load(file)
            >>> dtic = DTICTopicFinder(terms_to_topics)
            >>> result = dtic("i like supersonic wind tunnels.", 1, 1)
            >>> len(result['topics'])
            1
            >>> result['topics'][0]
            {'topic': 'AVIATION TECHNOLOGY; AERODYNAMICS; AERODYNAMICS', 'score': 1}
            >>> result['terms'][0]
            {'term': 'SUPERSONIC WIND TUNNELS', 'score': 1}
            >>> result = dtic("i like perigees and aphelions.", -1, -1)
            >>> len(result['topics'])
            3
            >>> len(result['terms'])
            2
            >>> dtic("i don't like anything.", -1, -1)
            {'topics': [], 'terms': []}
            >>> dtic("i like supersonic wind tunnels.", 0, 0)
            {'topics': [], 'terms': []}
         """
        max_topics = 10 if max_topics is None else max_topics
        max_terms = 10 if max_terms is None else max_terms
        
        self._set_term_counts(text)
        terms, topics = self._get_terms_and_topics()
        
        return {
            "topics": topics if max_topics == -1 else topics[:max_topics],
            "terms": terms if max_terms == -1 else terms[:max_terms]
        }
    
    
if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)