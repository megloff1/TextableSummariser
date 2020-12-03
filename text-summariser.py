"""
Texttable summarizer
"""

from LTTL.Segment import Segment
from LTTL.Segmentation import Segmentation

def summarize(document):
	return """This is a summary"""

def main():
    """Programme principal"""
    global out_object

    segments = list()
    for segment in in_object:
        annotations = segment.annotations.copy()
        annotations["summary"] = summarize(segment.get_content())
        segments.append(Segment(
            str_index=segment.str_index,
            start=segment.start,
            end=segment.end,
            annotations=annotations
        ))

    out_object = Segmentation(segments)


if __name__ == "builtins":
    if in_object:
        main()
