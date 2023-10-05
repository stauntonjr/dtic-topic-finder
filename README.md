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



