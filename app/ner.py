from collections import Counter
from collections import defaultdict
import re
import spacy

span = 100

nlp = spacy.load('en_core_web_sm')


def extract_content(text_body):

    if "PROJECT GUTENBERG" in text_body:

        start_seq = r"\*\*\*\s+START.*?\*\*\*"
        end_seq = r"\*\*\*\s+END.*?\*\*\*"

        book_content = re.search(
            '{}(.*){}'.format(start_seq, end_seq), text_body, re.DOTALL).group(1).strip()

        book_content = re.sub('_', ' ', book_content)
        book_content = re.sub('--', ' ', book_content)
        book_content = re.sub('\r\n', ' ', book_content)

        return book_content

    else:
        return text_body


def extract_names_and_counts(text_body):

    book_content = extract_content(text_body)
    doc = nlp(book_content)

    people = [(ent.text, ent.start, ent.end)
              for ent in doc.ents if ent.label_ == 'PERSON']

    person_loc = defaultdict(list)
    person_count = defaultdict(int)

    for (ent_text, start, end) in people:

        start_point = max(0, start-span)
        end_point = min(end+span, len(doc))

        locs = [
            ent.text for ent in doc[start_point:end_point].ents if ent.label_ == 'GPE']

        person_count[ent_text] += 1
        person_loc[ent_text] += locs

    loc_count = {ent_text: [{'name': k, 'count': v} for k, v in sorted(Counter(person_loc[ent_text]).items(), key=lambda item: item[1], reverse=True)]
                 for ent_text in person_loc.keys()}

    person_count = dict(
        sorted(person_count.items(), key=lambda item: item[1], reverse=True))

    count_output = [{'name': person,
                     'count': person_count[person],
                     'assosciated_places':loc_count[person]} for person in person_count]

    return count_output
