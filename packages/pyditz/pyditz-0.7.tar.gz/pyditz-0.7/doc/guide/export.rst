================================
 Exporting and Archiving Issues
================================

.. highlight:: ditzsession

To keep the public (who may not have access to |PD|) apprised of the
current status of your project, you can *export* the database.  Currently
there's only one export format available: HTML.  To do an export, you use
the :kbd:`html` command.  By default, it writes an HTML summary of things
to files in a directory called :file:`html`.  If you give an argument,
it'll use that instead.  Here's an example:

.. command: html .ditz-html

.. literalinclude:: /include/html.txt

For an example of the HTML output itself, see the output from |PD|\'s issue
tracker here__.  The only thing that may not be obvious when browsing the
HTML is that you can click on table headers, which sorts the table on that
field.  Clicking again reverses the sort order.

__ ../_static/index.html

When you decide that a previously-released release and its issues is no
longer useful to keep around in your issue database, you can *archive* it
using the :kbd:`archive` command.  This moves all issues from that release
to an archive directory.  If not specified, it is ``ditz-archive-<num>``
where, ``<num>`` is the release number.

.. command: archive 1.0 .ditz-archive-1.0

.. literalinclude:: /include/archive.txt
