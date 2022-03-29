Integrate Python coverage & GitHub Actions
******************************************

This repo provides a minimal Python package and GitHub Action for reporting the outcomes of Python `coverage <https://coverage.readthedocs.io>`_ as a check and annotations on a GitHub pull request.

Most users—especially those with public repositories—will want to use services like `Codecov <https://codecov.io>`_, `Coveralls <https://coveralls.io/>`_. These services provide free options for public repos with many more features, and paid options for private repos with professional support.
You should consider paying for these if your organization can afford it!
If not, then ``coverage-gh`` fills the niche as "poor man's" option for private repos.

Usage
=====
The action assumes your workflow invokes ``coverage`` (e.g. using `pytest-cov <https://github.com/pytest-dev/pytest-cov/>`_) to generate a date file, named .coverage by default.
This is the only file needed by the action, i.e., you do not need to give arguments like ``pytest … --cov-report=xml`` unless otherwise needed.

.. code-block:: yaml

   - uses: khaeru/codecov-gh@v1
     with:
       # Token used to report checks. Required.
       token: ${{ github.token }}

       # Location of the coverage data file. Optional.
       #
       # Default: .coverage, in the GitHub Actions workspace directory.
       data-file: .coverage

       # Percent coverage required for the check to pass. Optional.
       #
       # This is a floating-point number between 0 and 100.
       #
       # Default: 100.0
       threshold: 100.0

License & credits
=================

Copyright © 2022 Paul Natsuo Kishimoto <mail@paul.kishimoto.name>.
Licensed under the GNU General Public License, version 3.0 or later.

Thanks to `amitds1997/pytest-annotate-pr <https://github.com/amitds1997/pytest-annotate-pr>`_ for demo code for interacting with GitHub's API, heavily adapted here.
