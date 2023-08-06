==============
 Introduction
==============

.. note::

   Most of this section is an edited part of the ``README`` file from the
   original Ditz.

Description
===========

Ditz is a simple, light-weight distributed issue tracker designed to work
with distributed version control systems like git, darcs, Mercurial, and
Bazaar.  It can also be used with centralized systems like SVN.

Ditz maintains an issue database directory on disk, with files written in a
line-based and human-editable format.  This directory can be kept under
version control, alongside project code.

Ditz provides a simple, console-based interface for creating and updating
the issue database files, and some basic static HTML generation
capabilities for producing world-readable status pages.

Ditz includes a robust plugin system for adding commands, model fields, and
modifying output.

Ditz currently offers no central public method of bug submission.

Using Ditz
==========

There are several different ways to use Ditz:

1. Treat issue change the same as code change: include it as part of
   commits, and merge it with changes from other developers, resolving
   conflicts in the usual manner.

2. Keep the issue database in the repository but in a separate branch.
   Issue changes can be managed by your VCS, but is not tied directly to
   code commits.

3. Keep the issue database separate and not under VCS at all.

All of these options are supported; the choice of which to use depends on
your workflow.

Option #1 is probably most appropriate for the unsynchronized, distributed
development, since it allows individual developers to modify issue state
with a minimum of hassle.  Option #2 is most suitable for synchronized
development, as issue state change can be transmitted independently of code
change, and can act as a sychronization mechanism.  Option #3 is only
useful with some other distribution mechanism, like a central web
interface.

The Ditz Data Model
===================

By default, Ditz includes the bare minimum set of features necessary for
open-source development.  Features like time spent, priority, assignment of
tasks to developers, due dates, etc., are purposely relegated to the plugin
system.

A Ditz project consists of issues, components and releases.

Issues
    Issues are the fundamental currency of issue tracking.  A Ditz issue is
    either a feature or a bug, but this distinction currently doesn't
    affect anything other than how they're displayed.

    Each issue belongs to exactly one component, and is part of zero or one
    releases.

    Each issues has an exportable id, in the form of 40 random hex
    characters.  This id is "guaranteed" to be unique across all possible
    issues and developers, present and future.  Issue ids are typically not
    exposed to the user.

    Issues also have a non-global, non-exportable name, which is short and
    human-readable.  All Ditz commands use issue names in addition to issue
    ids.  Issue names (but not issue ids) may change in certain
    circumstances, e.g., after a ``ditz drop`` command.

    Issue names can be specified in comments, titles and descriptions, and
    Ditz will automatically rewrite them as necessary when they change.

Components
    There is always one "general" component, named after the project
    itself.  In the simplest case, this is the only component, and the user
    is never bothered with the question of which component to assign an
    issue to.

    Components simply provide a way of organizing issues, and have no real
    functionality.  Issues names are derived from the component they're
    assigned to.

Releases
    A release is the primary grouping mechanism for issues.  Status
    commands like ``ditz status`` and ``ditz todo`` always group issues by
    release.  When a release is 100% complete, it can be marked as
    released, and its issues will cease appearing in Ditz status and todo
    messages.
