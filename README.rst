Integrate Python coverage & GitHub Actions
******************************************

🚧 This code is a work in progress, not ready for use.

This repo provides a minimal Python package and GitHub Actions for reporting the outcomes of Python `coverage <>`_ as a check and annotations on a GitHub pull request.
Most users—especially those with public repositories—will want to use services like Codecov, Coveralls, etc., which are much more fully-featured.
These services also provide paid options for private repositories with professional support, which you should consider paying for if your organization can afford to.
If not, then ``coverage-gh`` fills the niche as "poor man's" option for private repos".

Thanks to `amitds1997/pytest-annotate-pr <https://github.com/amitds1997/pytest-annotate-pr>`_ for demo code for interacting with GitHub's API, heavily adapted here.
