"""
Texttable summarizer
"""


import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from sklearn.feature_extraction.text import CountVectorizer



from LTTL.Segment import Segment
from LTTL.Segmentation import Segmentation

nlp = spacy.load("en_core_web_sm")

def summarize1(document):
    """
    https://medium.com/luisfredgs/automatic-text-summarization-made-simple-with-python-f9c3c645e34a
    """
    doc = nlp(document)
    corpus = [sent.text.lower() for sent in doc.sents ]
    cv = CountVectorizer(stop_words=list(STOP_WORDS))   
    cv_fit=cv.fit_transform(corpus)    
    word_list = cv.get_feature_names();    
    count_list = cv_fit.toarray().sum(axis=0)
    word_frequency = dict(zip(word_list,count_list))
    val=sorted(word_frequency.values())
    higher_word_frequencies = [word for word,freq in word_frequency.items() if freq in val[-3:]]
    # gets relative frequency of words
    higher_frequency = val[-1]
    for word in word_frequency.keys():  
        word_frequency[word] = (word_frequency[word]/higher_frequency)
    sentence_rank={}
    for sent in doc.sents:
        for word in sent :       
            if word.text.lower() in word_frequency.keys():            
                if sent in sentence_rank.keys():
                    sentence_rank[sent]+=word_frequency[word.text.lower()]
                else:
                    sentence_rank[sent]=word_frequency[word.text.lower()]
    top_sentences=(sorted(sentence_rank.values())[::-1])
    top_sent=top_sentences[:1]
    summary=[]
    for sent,strength in sentence_rank.items():  
        if strength in top_sent:
            summary.append(sent)
        else:
            continue
    for i in summary:
        print(i,end=" ")
    return summary

def summarize2(document):
    return "summary"

def main():
    """Programme principal"""
    global out_object
    
    annotation_key = "summarize"
    function_select = "1"
    summarize_functions = {
        "1": summarize1
    }

    segments = list()
    for segment in in_object:
        if segment.annotations.get(annotation_key, False):
            annotations = segment.annotations.copy()
            annotations["summary"] = summarize_functions[function_select](segment.get_content())
            segments.append(Segment(
                str_index=segment.str_index,
                start=segment.start,
                end=segment.end,
                annotations=annotations
            ))
        else:
            segments.append(segment)

    out_object = Segmentation(segments)


if __name__ == "builtins":
    if in_object:
        main()
