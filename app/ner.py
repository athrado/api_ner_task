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

        # Extract text between header and footer markers
        content_text = re.search(
            '{}(.*){}'.format(start_seq, end_seq), full_text, re.DOTALL)

        if content_text is None:
            return full_text

        content_text = content_text.group(1).strip()

        # Minor tag cleaning
        content_text = re.sub('_', ' ', content_text)
        content_text = re.sub('--', ' ', content_text)
        content_text = re.sub('\r\n', ' ', content_text)

        return content_text

    else:
        return full_text


def extract_ne_counts(full_text, span=span, merge_appositions=False):
    """Detect names and locations mentioned within given text span.

    Args:
        text (str): Text in which to search for people and locations.
        span (int, optional): Search range to both sides of name. 
            Defaults to config.span.
        merge_appositions (bool): Merge location appositions like Paris, France
            into one count with area specification. Defaults to False.
            
    Returns:
        list: Named entity count reponse.
    """

    # Trim and parse text
    content_text = extract_content(full_text)
    doc = nlp(content_text)

    # Find people entities in text
    people = [(ent.text.strip(), ent.start, ent.end)
              for ent in doc.ents if ent.label_ == 'PERSON']

    person_loc = defaultdict(list)
    person_count = defaultdict(int)
    area_dict = defaultdict(dict)

    # Search span to left and right of people for locations
    for (person, start, end) in people:

        # Set search span based on person position and text limits:
        # Use first word if span goes beyond beginning of text
        start_point = max(0, start-span)
        # Use last word if span goes beyond end of text
        end_point = min(end+span, len(doc))

        locs = [
            (ent.text, ent.start, ent.end) for ent in doc[start_point:end_point].ents
            if ent.label_ == 'GPE']
        
        # ----------------------

        # Little addition to handle instances like "Rome, Italy" or "Chigaco, Illinois"
        if merge_appositions:
        
            drops = []
            
            for i in range(len(locs)-1):
                first_ent_end = locs[i][2]
                sec_ent_start = locs[i+1][1]
                    
                # If the two locations are next to each other, seperated by one word
                if (first_ent_end + 1 == sec_ent_start):

                    # And if they are seperated by a commma
                    if (doc[first_ent_end:sec_ent_start][0].text == ','):

                        # And if it is not an enumeration (looking at next word)
                        if (doc[locs[i+1][2]+1:][0].text not in ['and', 'or', ',']):

                            # Use the first location mention only,
                            # drop the second, but keep in area_dict
                            locs[i] = (locs[i][0], first_ent_end, locs[i+1][2])
                            drops.append(i+1)
                            area_dict[person][locs[i][0]] = locs[i+1][0]

            # Drop the second locations to avoid redudnancy
            locs = [loc for i, loc in enumerate(locs) if i not in drops]    

        # ---------------------- 
        
        person_count[person] += 1
        person_loc[person] += locs


    # Remove locations that are counted multiple times (same start token)
    person_loc = {person: [loc_name for (loc_name, _, _) in list(set(person_loc[person]))]
                  for person in person_loc}

    # Sort locations by counts and re-format
    loc_count = {person: [{'name': k, 'count': v}
                            for k, v in sorted(Counter(sorted(person_loc[person])).items(), 
                                               key=lambda item: item[1], reverse=True)] 
                                               for person in person_loc.keys()}
    

    # Add the second location as additional area information
    if merge_appositions:
        for pers in area_dict.keys():
            if pers in loc_count.keys():
                loc_count[pers] = [{**loc_counts, 'area':area_dict[pers][loc_counts['name']]} 
                                if loc_counts['name'] in area_dict[pers].keys() 
                                else loc_counts 
                                for loc_counts in loc_count[pers]]
                
    # Sort people by occurences
    person_count = dict(
        sorted(person_count.items(), key=lambda item: item[1], reverse=True))

    # Prepare output response
    ner_count_response = [{'name': person,
                           'count': person_count[person],
                           'assosciated_places':loc_count[person]} 
                           for person in person_count]
    
    return ner_count_response


# If not interesting in person counts but total location counts:

# # Sum up all the location counts 
# person_count = {person : sum([place.get('count', 0) 
#                               for place in loc_count[person]]) 
#                               for person in person_loc.keys()}