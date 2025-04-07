# Check-Foursquare-Open-Source

Foursquare's Open Source Places data _typically_ is released on or around the sixth of the month. However, the [web page](https://docs.foursquare.com/data-products/docs/access-fsq-os-places) rarely reflects the updated release vintage. Consequently, checking to see if data has been released requires regularly checking the bucket contents using the [AWS CLI](https://aws.amazon.com/cli/). Rather than continually checking, I let the script `scripts/check-available.py` do the work for me.
## Getting Started

1 - Clone this repo.

2 - Create a `config/secrets.ini` file with Pushover credentials. The following can be used as a template.

```
[PUSHOVER]
USER_KEY=
API_TOKEN=
```

2 - Create an environment with dependencies. NOTE: This uses `conda`, so you will need at least [miniconda](https://www.anaconda.com/docs/getting-started/miniconda/install) installed.
    
```
        > make env
```

3 - Run the script using `make check`, or set up a scheduled task to run the script using the environment located in `./env`.

## BumpVersion Cliff Notes

[Bump2Version](https://github.com/c4urself/bump2version) is preconfigured based on hints from [this article on Medium](https://williamhayes.medium.com/versioning-using-bumpversion-4d13c914e9b8).

If you want to...

- apply a patch, `bumpversion patch`
- update version with no breaking changes (minor version update), `bumpversion minor`
- update version with breaking changes (major version update), `bumpversion major`
- create a release (tagged in vesrion control - Git), `bumpversion --tag release`

<p><small>Project based on the <a target="_blank" href="https://github.com/knu2xs/cookiecutter-geoai">cookiecutter GeoAI project template</a>. This template, in turn, is simply an extension and light modification of the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
