## Gender-refs

A Python script that uses the crossref API to guess the gender of every author  in a bibtex file. Inspired by [this tweet](https://twitter.com/DrLouiseSlater/status/1158307826445496322?s=20).

Assuming gender from someone's name can be very inaccurate, and this methodology is unable to account for non-binary people. **These results should be used as a starting point for discussions around gender diversity in academic reference lists.** For more information on the gender identification methodology, please refer to [this page](https://pypi.org/project/gender-guesser/), which outlines the algorithm used for the gender classification.

## Requirements

- Python 3

## Installation

Clone or download this repo and install the dependencies using:

```
pip install -r requirements.txt
```

## Using the tool

### Before you start

If you are going to be using this code intensively, please replace my email address in the file called `EMAIL` with your own. This will allow [Crossref](https://github.com/CrossRef/rest-api-doc#etiquette) to better track who is using their service.

### Running the code

The tool is run from the command line using a single argument, the filename of a bibtex file you wish to analyze:

```
python gender-refs.py references.bib
```

Running the code on the provided example bibtex file should give results that look like this:

```

	Found 129 references.
	References without a DOI cannot be processed.


Unknown: 19
Mostly male: 3
Male: 195
Female: 29
Androgynous: 7
Mostly female: 2
Total authors processed: 255

```

## Contributing

If you have suggestions for how to improve this tool, open an issue, and I will try and resolve it, or feel free to open a pull request and fix it yourself!
