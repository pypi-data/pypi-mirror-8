Changed Target Tasks Plugin
===========================

A plugin for the pants build system make building and testing
locally edited (or a particular commit's) targets easier.

Details
-------
This creates varients of goals like ``compile`` that, rather than
operate on explicitly provided arguments, find "changed" targets
by consulting the active SCM (eg git) and then operate on those
and (optionally) on their dependees.

Provided goals are:

- ``what-changed``: Lists changed targets (or writes to file)
- ``compile-changed``: Build changed targets
- ``test-changed``: Test changed targets
- ``validate-changed``: Check for dependency rules in changed targets

All of thse take flags which can change how they find targets and
whether or not they include dependees.

Determining what is "changed"
-----------------------------

"changed" is usually determined asking SCM for files with differences
relative to "upstream/master", though this is configurable via the
``--changes-since`` flag or config option.

"changed" can also be determined by ``--diffspec`` (or ``--shas``).
A diffspec can be a single SHA, a aaa..bbb range, a ref or anything
that is meaningful to the SCM to provide a list of changed filenames.

Including Dependees
-------------------
These tasks are useful for checking if ones current changes break
things, without having to know what "things" may have been broken
and need to be built (or tested) to be sure.

However, most changes can not only break the targets in which they
are made, but can easily break a dependee, eg by changing a method
which is called in a dependee. Thus including depnedees of changed
targets in addition to changed targets themselves is often helpful.

- ``--direct-dependees`` or ``--dd``
Include direct dependees of changed targets.
(This is the default behavior, but can be explicitly chosen if defaults
are changed via config.)

- ``--transitive-dependees`` or ``--td``
Include all transitive dependees.

- ``--no-dependees`` or ``--nd``
Include no dependees, and act only on directly changed targets.
