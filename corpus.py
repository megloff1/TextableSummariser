"""
Script pour widget "Python Script" dans Orange-Canvas pour
creer une segmentation a partir de DBpedia:
    un segment contient le texte de la description dbpedia
    et une annotation avec le nom de la personne
"""

import re
from SPARQLWrapper import SPARQLWrapper, JSON
from LTTL.Segmentation import Segmentation
from LTTL.Segment import Segment
from LTTL.Input import Input
 
sparql_endpoint = SPARQLWrapper("http://dbpedia.org/sparql")
sparql_endpoint.setReturnFormat(JSON)
query = """
select distinct ?subject ?name ?abstract where {
  ?subject a dbo:Artist;
           dbo:abstract ?abstract;
           foaf:name ?name;
           rdfs:label ?label .
   FILTER (lang(?abstract) = 'en')
   FILTER (lang(?name) = 'en')
   FILTER (lang(?label) = 'en')
} LIMIT 100

"""
sparql_endpoint.setQuery(query)

documents = sparql_endpoint.queryAndConvert()

# Changement de structure:
documents = {entry["name"]["value"]:entry["abstract"]["value"] for entry in documents["results"]["bindings"] }

segmentation = Input(" ".join(documents.values()))

segments = list()

start = 0
for name, text in documents.items():
    length = len(text)
    segments.append(
        Segment(
            str_index=segmentation[0].str_index,
            start = start,
            end=start + length,
            annotations={"id": name}
        )
    )
    start = start + length + 1

out_object = Segmentation(segments)

