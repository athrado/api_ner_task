from collections import Counter
from collections import defaultdict
import re
import spacy

from app.config import span

nlp = spacy.load('en_core_web_sm')


def extract_content(full_text):
    """Extract the book content without header and footer
    when loading from Project Gutenberg website. 

    Args:
        full_text (str): Text body.

    Returns:
        str: Extracted book content.
    """

    if "PROJECT GUTENBERG" in full_text:

        start_seq = r"\*\*\*\s+START.*?\*\*\*"
        end_seq = r"\*\*\*\s+END.*?\*\*\*"

        content_text = re.search(
            '{}(.*){}'.format(start_seq, end_seq), full_text, re.DOTALL).group(1).strip()


        # Minor tag cleaning
        content_text = re.sub('_', ' ', content_text)
        content_text = re.sub('--', ' ', content_text)
        content_text = re.sub('\r\n', ' ', content_text)

        return content_text

    else:
        return full_text


def extract_ne_counts(full_text, span=span):
    """_sumDetect names and locations mentioned within given text span.mary_

    Args:
        text (str): Text in which to search for people and locations.
        span (int, optional): Search range to both sides of name. Defaults to config.span.
    Returns:
        list: Named Entity count reponse.
    """

    # Trim and parse text
    content_text = extract_content(full_text)
    doc = nlp(content_text)

    # Find people in text
    people = [(ent.text, ent.start, ent.end)
              for ent in doc.ents if ent.label_ == 'PERSON']

    person_loc = defaultdict(list)
    person_count = defaultdict(int)

    # Search span to left and right of people for locations 
    for (person, start, end) in people:

        # Search span based on person position and text limits
        start_point = max(0, start-span)
        end_point = min(end+span, len(doc))

        locs = [
            (ent.text, ent.start) for ent in doc[start_point:end_point].ents 
            if ent.label_ == 'GPE']

        person_count[person] += 1
        person_loc[person] += locs

    # for person in person_loc:
    #     person_loc[person] = [
    #         text for (text, _) in list(set(person_loc[person]))]
        
    # Remove location that are counted multiple times (same start token)
    person_loc = {person: [text for (text, _) in list(set(person_loc[person]))] 
                    for person in person_loc}

    # Sort by counts and re-format
    loc_count = {ent_text: [{'name': k, 'count': v} for k, v in sorted(Counter(sorted(person_loc[ent_text])).items(), key=lambda item: item[1], reverse=True)]
                 for ent_text in person_loc.keys()}

    # Sort people by occurences
    person_count = dict(
        sorted(person_count.items(), key=lambda item: item[1], reverse=True))

    # Prepare output response
    ner_count_response = [{'name': person,
                     'count': person_count[person],
                     'assosciated_places':loc_count[person]} for person in person_count]

    return ner_count_response
