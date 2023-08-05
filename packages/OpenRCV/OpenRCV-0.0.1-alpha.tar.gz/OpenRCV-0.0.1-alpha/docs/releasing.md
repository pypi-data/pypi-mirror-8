Releasing OpenRCV
=================

This document contains detailed step-by-step instructions for
maintainers of OpenRCV on how to release both the first version and new
versions of the project.

For instructions on installing or using the application, or for instructions
on contributing, consult the README or [project page][open-rcv-project]
instead.


Contents
--------

1.  Background
2.  One-time setup
    * 2.1. Set up PyPI user accounts
    * 2.2. Create `.pypirc` file
3.  Releasing a new version
    * 3.1. Finalize source
        * 3.1.1. Review issues
        * 3.1.2. Update HISTORY file
        * 3.1.4. Bump version number
        * 3.1.5. Update `long_description` file
        * 3.1.6. Make sure tests pass
        * 3.1.3. Double-check `MANIFEST.in`
    * 3.2. Merge to release branch, if necessary
    * 3.30. Create an `sdist`
    * 3.40. Register version on PyPI
        * Registration troubleshooting
    * 3.4. Upload version to PyPI
    * 3.5. Tag the commit


1\. Background
-------------

This document explains how to package and release new versions of OpenRCV
to the Python Package Index, or [PyPI](http://pypi.python.org/pypi)
(pronounced Pie-pee-EYE).

Correctly putting your project on PyPI lets users install your project
simply by typing:

    $ pip install openrcv

For more information on installing and packaging Python projects in
general, see the ["Python Packaging User Guide"][pug].

Also look at the project's [`setup.py`][setup.py] file to see how things
work.  As time goes on, you should feel free to modify `setup.py` and
its supporting code to better suit the project's needs.

The release process documented here assumes that you have already
installed pip and setuptools as described in this
[Packaging User Guide tutorial][pug-tutorial].


2. One-time setup
-----------------

This section describes setup steps that you need to do only once.


### 2.1. Set up PyPI user accounts

Create a user account on PyPI if you do not already have one, as well as
a test user account.

If OpenRCV already exists on PyPI, you will also need write permissions on that
project (i.e. to have the "Maintainer" or "Owner" role for the project).
A current project owner can grant you those permissions.

We also recommend creating a user account on the
[test PyPI server](http://testpypi.python.org/pypi).  The test server lets
you try things out, though the server is not always up.  The `-r/--repository`
option to `setup.py` (which we describe below) lets you designate this server.


### 2.2. Create `.pypirc` file

The [`.pypirc` file](http://docs.python.org/dev/distutils/packageindex.html#the-pypirc-file)
is a plain-text configuration file that stores your PyPI credentials.  The
`setup.py` script uses it when you interact with PyPI via the command-line.
We recommend starting out with a `.pypirc` file like the following, which
also enables access to the test server.  The file should be placed in your
home directory:

    [distutils]
    index-servers =
        pypi
        test

    [pypi]
    repository: http://pypi.python.org/pypi
    username: <username>

    [test]
    repository: http://testpypi.python.org/pypi
    username: <username>


3. Releasing a new version
--------------------------

This section describes in detail the steps to release a new version of OpenRCV,
assuming the above setup steps have been followed.


### 3.1. Finalize source

This section describes steps to prepare the source code for release.  Most
of these steps involve committing changes to files.

In many workflows, the source code is normally in a non-release branch at
this time (e.g. in a `development` branch).  One exception is if the code
has already been merged to the release branch but additional finalizations
are found needed.


#### 3.1.1 Review issues

XXX:


#### 3.1.2 Update HISTORY file

XXX:


#### 3.1.4. Bump version number

XXX:

For versioning your project, you may want to consider semantic versioning:
http://semver.org.


#### 3.1.5. Update `long_description` file

PyPI uses the long_description argument to setup() as what to display
for a project home page.  For nice rendering, this text should be
reStructuredText, which has extension `.rst`.

This project's `setup.py` obtains this text from the file
[`setup_long_description.txt`](setup_long_description.txt).  Thus, this
file should be updated prior to releasing.

To update the file:

    $ python setup.py update_long_desc

And then commit any changes.

It helps to check the long_description file prior to pushing to PyPI because
if PyPI encounters any problems, it will render the long description as
plain-text instead of as HTML.  To check the file, convert it to HTML yourself
using the same process that PyPI uses.  After installing Docutils
(http://docutils.sourceforge.net/), run--

    $ python setup.py --long-description | rst2html.py --no-raw > temp.html

Also see:

  http://docs.python.org/dev/distutils/uploading.html#pypi-package-display
  http://bugs.python.org/issue15231

You can also view the long description file on GitHub as a sanity check.


#### 3.1.6. Make sure tests pass

XXX:


#### 3.1.3 Double-check `MANIFEST.in` (i.e. the `sdist` contents)

You will soon upload a source distribution of the project (aka `sdist`)
to PyPI.

The file `MANIFEST.in` is what tells `setup.py` what files to include
in the source distribution, in addition to those files that `setup.py`
automatically includes.

To validate that `MANIFEST.in` is correct (and hence that the `sdist`
contents are what you expect), run the following--

    $ check-manifest

If the command reports any files missing from git or missing from the
sdist, consider adding those files to git or adding them to the list
of files in `setup.cfg` that `check-manifest` should ignore.

For more information, visit the [`check-manifest` home page][check-manifest].


### 3.2. Merge to release branch

XXX:

* Discuss master/development
* Okay to make changes after this
* May want to wait a bit before next step


### 3.30. Create an `sdist` (or source distribution)

Run the following to create a source distribution:

    $ python setup.py sdist

This creates a `dist` directory inside your repo and generates a
`*.tar.gz` file inside that directory.  The command examines the
`MANIFEST.in` file to know what files to include.


### 3.40. Register version on PyPI

Once the repository is ready, register the version on PyPI.

Registering on PyPI adds an entry to PyPI for the version without uploading
any code.  Registering creates a page and URL for the version
(e.g. [http://pypi.python.org/pypi/Pizza/0.1.0](http://pypi.python.org/pypi/Pizza/0.1.0)),
stores metadata about the version, and adds the current "long_description"
to the version's page after converting it to HTML.

The [Python Packaging User Guide][pug] recommends using the
[registration form][pypi-registration] on the PyPI web site since this
method is secure.  Using `python setup.py register` is insecure because
it passes your credentials in plain-text.

The web form allows you to upload a `PKG-INFO` file instead of typing
the information manually into the form fields.  To obtain a `PKG-INFO`
file, unzip the *.tar.gz sdist file.  The `PKG-INFO` file should be
inside that directory.

Each time you create a new version for release, you should register that
version.  If you make a mistake or find that the metadata is not correct
after registering, it is okay to correct the source code and register again.
Subsequent registrations will overwrite the metadata previously stored for
that version.


#### Registration troubleshooting

If the long description shows up on PyPI as plain-text rather than HTML,
then the conversion to HTML failed.  See the `long_description` section
above for advice on troubleshooting conversion to HTML.  Also see
the bug report for PyPI
[bug #3539253](https://sourceforge.net/tracker/?func=detail&aid=3539253&group_id=66150&atid=513503).

If you get an error like the following after registering:

    Upload failed (401): You must be identified to edit package information

then there may be a problem with your `.pypirc` file.  Review the `.pypirc`
section above for possible issues.


### 3.4. Upload version to PyPI

After registering the version on PyPI,
[upload](http://docs.python.org/distutils/packageindex.html) the package
to PyPI:

    $ python setup.py sdist upload

This generates a `*.tar.gz` file by running `python setup.py sdist` and
then uploads the resulting file to the corresponding version on PyPI.
See prior sections of this document for more information on sdists.

You can use the `--repository/-r` option with the upload command just like
you can with register.  The project's upload command also prompts for
confirmation with the PyPI server name just like with register.

Unlike with the register command, PyPI does not let you "correct" an upload
after uploading.  You need to go through the process of creating a new
version, which means repeating the steps above as necessary.


### 3.5. Tag the commit

After registering and uploading a new version, it is good practice to
tag the corresponding commit in the repository.  This records for the future
where in the repository the version came from.  Some helpful commands to do
this follow.

To list current tags:

    $ git tag -l -n3

(The three says to display three lines of each tag's annotation, when an
annotation exists.)  To create an annotated tag (i.e. a tag with a
description):

    $ git tag -m "version annotation" "0.1.0"

To push a tag to a remote repository:

    $ git push --tags <repository> 0.1.0


[check-manifest]: https://github.com/mgedmin/check-manifest
[open-rcv-project]: https://github.com/cjerdonek/open-rcv
[pandoc]: http://johnmacfarlane.net/pandoc/
[pug]: https://packaging.python.org/en/latest/
[pug-tutorial]: https://packaging.python.org/en/latest/tutorial.html
[setup.py]: ../setup.py
