import bibtexparser
import sys
import urllib.parse as url
import gender_guesser.detector as gender
from collections import Counter
from nameparser import HumanName
import aiohttp
import asyncio


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

def build_queries(refs):
    queries = []
    for ref in refs.entries:
        try:
            doi = url.quote(ref['doi'])
            queries.append('https://api.crossref.org/works/{}'.format(doi))
        except:
            pass
    return queries

def detect_genders(results):
    d = gender.Detector(case_sensitive=False)
    genders = []

    try:
        for record in results:
            for name in record['message']['author']:

                name = HumanName(name['given'])

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

    return genders

async def fetch(session, url):
    async with session.get(url) as response:
        try:
            return await response.json()
        except:
            # DOI not found by crossref, or another http error.
            print(response.status, response.text)

async def crossref_call(urls):
    # headers = {'User-Agent': 'genderrefs/0.1 (https://swdg.io; mailto:{})'.format(load_email())}
    tasks = []
    async with aiohttp.ClientSession() as session:
        for url in urls[:3]:
            tasks.append(fetch(session, url))
        responses = await asyncio.gather(*tasks)
        return responses


refs = load_bibtex(sys.argv[1])
queries = build_queries(refs)
loop = asyncio.get_event_loop()
results = loop.run_until_complete(crossref_call(queries))
genders = detect_genders(results)

print('\n\n\tFound {} references.'.format(len(refs.entries)))
print('\tReferences without a DOI cannot be processed.\n\n')

counts = Counter(genders)
total_count = 0

for c in counts.items():
    print(output_formatter(*c))
    total_count += c[1]

print('Total authors processed: {}\n\n'.format(total_count))
