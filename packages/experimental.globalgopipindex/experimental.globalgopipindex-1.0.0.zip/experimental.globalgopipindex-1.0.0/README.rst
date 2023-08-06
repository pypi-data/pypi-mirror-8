Patch GopipIndex to sort objects by 'global' position
=====================================================

By default, Plone GopipIndex (Get object position in parent Index) sorts results only by objects order in their own folder.

While this works for the most common use cases, the resulting order may look weird if it contains results from multiple folders:

    >>> pc = layer['portal']['portal_catalog']
    >>> [brain.getPath() for brain in pc(sort_on='getObjPositionInParent')]
    ['/plone/a/a1', '/plone/b/b1', '/plone/a/a2', '/plone/b/b2', '/plone/a/a3', '/plone/b/b3', '/plone/a', '/plone/b']

This package patches the results to be sorted as follows:

    >>> layer['patch']()
    >>> pc = layer['portal']['portal_catalog']
    >>> [brain.getPath() for brain in pc(sort_on='getObjPositionInParent')]
    ['/plone/a', '/plone/b', '/plone/a/a1', '/plone/a/a2', '/plone/a/a3', '/plone/b/b1', '/plone/b/b2', '/plone/b/b3']

This package may affect the performance of sorting by ``getObjPositionInParent``.

.. image:: https://secure.travis-ci.org/datakurre/experimental.globalgopipindex.png
   :target: http://travis-ci.org/datakurre/experimental.globalgopipindex
