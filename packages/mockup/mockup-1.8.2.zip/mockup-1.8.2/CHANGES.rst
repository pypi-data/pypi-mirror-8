Changelog
=========

1.8.2 (2014-11-01)
------------------

- Reorganize folders so that javascript is included in the cooked egg.
  [esteele]


1.8.1 (2014-11-01)
------------------

- Size for modals may be specified
  [bloodbare]


v1.8.0 (2014-10-26)
-------------------

- Bower updates, except pickadate and backbone.paginator.
  [thet]

- Cleanup: Remove unused ``*._develop.js`` bundles. Remove unused bundles
  ``toolbar`` and ``tiles``. Remove unused bower dependencies ``domready``,
  ``respond`` and ``html5shiv``. Move all NixOS plattform specific ``*.nix``
  config files to a ``.nix`` subdirectory. Fix index.html markup. Remove unused
  ``__init__.py``.
  [thet]

- Remove licensing and author information from source files. Fixes #421 Fixes
  #422.
  [thet]

- Package metadata changes including removal of deprecated version specifier
  from bower.json.
  [thet]

- Remove bower dependency on ``tinymce-builded``, since the ``tinymce``
  dependency already points to the official builded ``tinymce-dist``
  reposotory. Raise TinyMCE version to 4.1.6.
  [thet]

- Fix Makefile for node versions < and >= 0.11.x.
  [petschki, thet]
