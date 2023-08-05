bdgt welcomes contributions. This document will guide you through the process.

# Fork

Fork the project on github and checkout your copy:

    $ git clone git@github.com:username/bdgt.git
    $ cd bdgt
    $ git remote add upstream git://github.com/jonblack/bdgt.git


# Branch

All contributions must be provided in a branch that originates from the
`develop` branch. It's useful to give your branch a useful name, e.g:
`feature-support-format-x` or `bugfix-parse-error`.

    $ git checkout -b my-feature-branch develop

Now you can implement your changes.

# Test

bdgt has both acceptance and unit tests. The acceptance tests are written using
[behave](http://pythonhosted.org//behave/) and the unit tests using
[nose](http://nose.readthedocs.org/en/latest/).

Run the existing tests to make sure your change hasn't broken anything.

To run the acceptance tests:

    $ behave

To run the unit tests:

    $ nosetests --with-coverage --cover-package=bdgt --cover-erase

The unit tests also output code coverage. Ensure that your change is covered by
a unit test.

If your change introduces new commands or changes the output, ensure that
there is an acceptance test to cover the scenario.

# Commit

Make sure git knows who you are:

    $ git config --global user.name "John Doe"
    $ git config --global user.email "j.doe@example.com"

Writing good commit logs is important. A commit log should describe what
changed and why. Follow these guidelines when writing one:

* The first line should be 50 characters or less and contain a short
  description of the change;
* Keep the second line blank;
* Wrap all other lines at 72 columns.

# Push

Push the changes you've made to your copy of bdgt on github:

    $ git push origin my-feature-branch

# Pull-Request

Go to github and create a pull-request. See [Sending a pull-request][1] for
more details.

[1]: https://help.github.com/articles/using-pull-requests/#sending-the-pull-request
