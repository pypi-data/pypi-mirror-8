========
Usage
========

To use Exreporter in any project:

.. code-block:: python

    from exreporter import exreporter
    from exreporter.credentials import GithubCredentials

    credentials = GithubCredentials(
        user="username", repo="reponame", auth_token="personaltoken")
    exreporter.report_github_issue(credentials=credentials, labels=['Bug'])



Exreporter in Django Project
----------------------------

Exreporter requires following Django settings in ``settings.py``:

.. code-block:: python

    EXREPORTER_GITHUB_USER = "username"
    EXREPORTER_GITHUB_REPO = "reponame"
    EXREPORTER_GITHUB_AUTH_TOKEN = "personaltoken"
    EXREPORTER_GITHUB_LABELS = ['Bug']

And then add Exreporter's middleware in ``settings.py``:

.. code-block:: python

  MIDDLEWARE_CLASSES = (
      ...
      'exreporter.contrib.django_middlewares.ExreporterGithubMiddleware',
  )
