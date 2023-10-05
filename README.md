# DTIC Topic Finder

This Topic Finder uses [DTIC](https://discover.dtic.mil)'s [broad, multi-disciplinary subject-term vocabulary](https://discover.dtic.mil/thesaurus/) to match supplied text to a [Subject Category Taxonomy](https://discover.dtic.mil/thesaurus/subject-categories/) and returns the best matching Subject Terms and Topics.

## Install with Pip
Use this in your environment:

`pip install git+https://bitbucket.org/redhorsecorp/dtic-topic-finder.git`

## Include in an Image Build
Add this project as a submodule to your repository:

`git submodule add https://bitbucket.org/redhorsecorp/dtic-topic-finder _submodules/dtic-topic-finder`

The submodule can then be installed from within the repository:

`pip install _submodules/dtic-topic-finder`

And included in your Dockerfile like:

```docker
# Install submodule packages
  COPY _submodules/dtic-topic-finder _submodules/dtic-topic-finder
  RUN pip install _submodules/dtic-topic-finder--upgrade
```

## Use in your code
```>>>from dtic_topic_finder import dtic
>>>your_text = """Hypersonic vehicles can travel at Mach 5. \
  Their aerodynamics cause heat that ionizes air into plasma around the hull. \ 
  Some use scramjets or ramjets for propulsion."""
>>>dtic(your_text)
>>>{'topics': [{'topic': 'PROPULSION, ENGINES AND FUELS; JET AND GAS TURBINE ENGINES; JET AND GAS TURBINE ENGINES', 'score': 2}, {'topic': 'AVIATION TECHNOLOGY; AIRCRAFT; RESEARCH AND EXPERIMENTAL AIRCRAFT', 'score': 1}, {'topic': 'SPACE TECHNOLOGY; UNMANNED SPACECRAFT; UNMANNED SPACECRAFT', 'score': 1}, {'topic': 'MECHANICAL, INDUSTRIAL, CIVIL AND MARINE ENGINEERING; SURFACE TRANSPORTATION AND EQUIPMENT; SURFACE TRANSPORTATION AND EQUIPMENT', 'score': 1}, {'topic': 'PHYSICS; THERMODYNAMICS; THERMODYNAMICS', 'score': 1}, {'topic': 'ATMOSPHERIC; ATMOSPHERIC PHYSICS; ATMOSPHERIC PHYSICS', 'score': 1}], 'terms': [{'term': 'HYPERSONIC VEHICLES', 'score': 1}, {'term': 'TRAVEL', 'score': 1}, {'term': 'HEAT', 'score': 1}, {'term': 'AIR', 'score': 1}, {'term': 'SCRAMJETS', 'score': 1}, {'term': 'RAMJETS', 'score': 1}]}```

  


