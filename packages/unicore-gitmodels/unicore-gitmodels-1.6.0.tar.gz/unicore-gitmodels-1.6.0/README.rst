Unicore Gitmodels
=================

Definition of models used for python-gitmodel

.. image:: https://travis-ci.org/praekelt/unicore-gitmodels.svg
    :target: https://travis-ci.org/praekelt/unicore-gitmodels

Installation
------------

::

  $ pip install unicore-gitmodels



Usage
-----

::

  # models.py

  from unicore_gitmodels.models import GitPageModel, GitCategoryModel

  ws = Workspace('/path/to/repo/.git')
  GitPage = ws.register_model(GitPageModel)
  GitCategory = ws.register_model(GitCategoryModel)

::

  # views.py

  page = GitPage(title='a title', slug='a-title', content='some sample content')
  page.save(True, message="sample git commit")
