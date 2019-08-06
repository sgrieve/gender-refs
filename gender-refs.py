import bibtexparser
import requests
import sys
import urllib.parse as url
import gender_guesser.detector as gender
from collections import Counter
from nameparser import HumanName

def load_email():
    with open('EMAIL') as f:
        return url.quote(f.readline().strip())

def output_formatter(category, count):
    header = category.capitalize().replace('_', ' ').replace('Andy', 'Androgynous')
    return '{}: {}'.format(header, count)

def load_bibtex(filename):
    try:
        with open(filename) as bibtex_file:
            return bibtexparser.load(bibtex_file)
    except FileNotFoundError:
        sys.exit('ERROR: Bibtex file, {}, not found.'.format(filename))
    except KeyError:
        sys.exit('ERROR: Bibtex file appears to be incorrectly formatted.\n'
                 'Check for missing brackets around dates or mismatched brackets.')


refs = load_bibtex(sys.argv[1])
headers = {'User-Agent': 'GenderCheck/0.1 (https://swdg.io; mailto:{})'.format(load_email())}

d = gender.Detector(case_sensitive=False)
genders = []

print('\n\n\tFound {} references.'.format(len(refs.entries)))
print('\tReferences without a DOI cannot be processed.\n\n')

for ref in refs.entries:
    try:
        doi = url.quote(ref['doi'])
        query = 'https://api.crossref.org/works/{}'.format(doi)
        r = requests.get(query, headers=headers)
        try:
            for author in r.json()['message']['author']:
                name = author['given']
                name = HumanName(name)

                # Check for people with a first initial rather than a first name
                if name.is_an_initial(name.first):
                    # These people may use a middle name as their given name
                    if len(name.middle) > 1:
                        genders.append(d.get_gender(name.middle))
                else:
                    # Seems like a first name we can process
                    genders.append(d.get_gender(name.first))

        except:
            # No author record - possibly citing an organisation, or invalid DOI
            pass

    except:
        # Call to Crossref has failed in a bad way
        pass

counts = Counter(genders)
total_count = 0

for c in counts.items():
    print(output_formatter(*c))
    total_count += c[1]

print('Total authors processed: {}\n\n'.format(total_count))
