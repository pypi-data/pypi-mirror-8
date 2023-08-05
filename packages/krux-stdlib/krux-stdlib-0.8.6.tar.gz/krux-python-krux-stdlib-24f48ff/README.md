# krux-stdlib

For API documentation, see
https://staticfiles.krxd.net/foss/docs/pypi/krux-stdlib/

## Using python-krux-stdlib

1.  Add the Krux pip repository and python-krux-stdlib to the top of
    your project's `requirements.pip` file:

        ### Optional - also available on PyPi
        --extra-index-url https://staticfiles.krxd.net/foss/pypi/
        krux-stdlib==0.8.1

## Developing python-krux-stdlib

1.  Clone the repository.

        git clone git@github.com:krux/python-krux-stdlib.git ~/Projects/krux-stdlib

2.  Set up a virtual environment.

        mkdir -p ~/.virtualenv/krux-stdlib && virtualenv ~/.virtualenv/krux-stdlib

3.  Activate the virtual environment.

        source ~/.virtualenv/krux-stdlib/bin/activate

4.  Install the requirements.

        cd ~/Projects/krux-stdlib; pip install -r requirements.pip

5.  Hack away! Make sure to add unit tests.

6.  Make sure you document everything. You can preview the generated
    documentation by running:

        make html

    in the `doc` subdirectory. Then open `doc/github/html/index.html`
    in your favorite browser.

7.  To cut a release, update the VERSION in `setup.py`, merge to the
    `release` branch, and push to GitHub. Jenkins will build and
    upload the new version to the Krux python repository, as well as
    tagging the release in git and updating the documentation.

    Note: To set this kind of workflow up for your own projects, clone
    the python-krux-stdlib Jenkins job :-)
