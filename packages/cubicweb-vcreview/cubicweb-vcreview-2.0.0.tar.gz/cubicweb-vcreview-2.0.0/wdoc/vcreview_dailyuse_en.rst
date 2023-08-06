
Patches
~~~~~~~

A ``Patch`` is the entity in `vcreview`_ 's schema that represents a
mercurial changeset. `vcreview`_ has been conceived for
`evolve`_, thus **one changeset** may have itself several versions. A
``Patch`` is meant to keep track of this changeset evolution.

When a new draft changeset is detected, a new ``Patch`` entity is
created. The name of the ``Patch`` (its title) is the short
description of the changeset (first line of the commit message).

It is also possible to add "magic words" in the commit message to
automatically link a ``Patch`` with a ``Ticket`` (when `vcreview`_ is
used with the `trackervcs`_ cube)

.. _`vcreview`: https://www.cubicweb.org/project/cubicweb-vcreview
.. _`trackervcs`: https://www.cubicweb.org/project/cubicweb-trackervcs


Patches workflow
~~~~~~~~~~~~~~~~

When a patch is being constructed, the related ``Patch`` entity may be
in one of `in-progress`, `pending-review` or `reviewed` states.

Finished ``Patch`` objects are in one of `applied`, `rejected` or
`folded` states.

Submit a patch for review
+++++++++++++++++++++++++

By default, a new ``Patch`` (ie. a new draft changeset) is in the 
`in-progress` state.  It can be moved to the `pending-review` state either from
the web interface or using the mercurial extension provided in
`logilab-devtools <http://hg.logilab.org/master/logilab/devtools>`_.

Note that the matching between the author of a changeset and a
``CWUser`` in the Cubicweb application is done using the email
address.

Reviewing a patch
+++++++++++++++++

When a ``Patch`` enters the `pending-review` state, a reviewer is
designated for this patch, and he is notified by email.

He can then either accept the patch, ask for modifications (normally
with comments, explanations and tasks that should be addressed before
resubmitting an amended changeset), or reject it.

Accepting a patch
+++++++++++++++++

When a patch has been reviewed, it may be integrated. The integration
is just a matter of changing the phase of the changeset.  When the
(draft) changeset linked to a ``Patch`` is set `public` (its phase is
changed from `draft` to `public`), this later ``Patch`` is
automatically set as `applied` state.


Folding a patch
+++++++++++++++

When a changeset is folded in another one, the corresponding ``Patch``
is also put in the `folded` state.


Notification
~~~~~~~~~~~~
To be notified about ``Patch``es activity, you should mark yourself as `interested
in` each desired Repository.

