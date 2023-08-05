================
plotsettings
================
---------------
Highlights
---------------
Tearing your hair out trying to make your figures conform to the author guidelines
for a particular journal? Got rejected from PNAS and can't bring yourself to change
all the fonts for submission to PLOS ONE? Let *plotsettings* make it easy for you!
*plotsettings* is a convenient way of making sure your figures fit the requirements
for publication. One line is sufficient to choose a target journal, and just one
more line to automatically output figures that fit cleanly into 1, 2 or even 1.5
columns! You can even set the aspect ratio of your figure and be warned if your 
figure gets taller than the height of one page. In fact, *plotsettings* already knows 
the appropriate font, text size, and figure dimensions for all of these journals:

    * Proceedings of the Royal Society B (use argument 'ProcRoySocB')
    * Public Library of Science One (use argument 'PLOSONE')
    * Deep Sea Research II (use argument 'DSRII')
    * Marine Ecology Progress Series (use argument 'MEPS')
    * Journal of Experimental Biology (use argument 'JEB')
    * Proceedings of the National Academy of Sciences, USA (use argument 'PNAS')
    * Ecology Letters (use argument 'EcolLett')
    * Presentation (okay, this is not a journal but it's still useful for outputting 
      figures to presentation slides; access with the argument 'Presentation')

Don't see the journal you want on the list (say you want to publish in the `Proceedings 
of the 6th ACM Workshop on Next Generation Mobile Computing for Dynamic Personalised 
Travel Planning <http://dl.acm.org/citation.cfm?id=2307874&picked=prox>`_)? Compile your 
own list of journals by creating a python file containing a single dictionary with 
settings for every journal *you* use! You can specify any parameters that are accepted 
by *matplotlib.rcParams* as well as the column width, gutter width and page height.

Also, as a **Bonus**:

	* 1-line labeling of all the subplots in a figure (e.g. with '(a)', '(b)', '(c)' 
	  etc.) using the function *panel_labels*!

----------------
Installation
----------------
*plotsettings* has only been tested in Python 2.7

Install through pip::

	$ pip install plotsettings

Requires the following non-standard libraries:

     * *matplotlib*

----------------
Usage
----------------
First set the journal you want to submit to::

	publishable = plotsettings.Set('MEPS') # Lets publish in Marine Ecology Progress Series!

Then set the dimensions of a particular figure with the line::

    publishable.set_figsize(n_columns = 1, n_rows = 1)

This will cause the next figure that is drawn to be 1 column wide (81 mm for MEPS) x 1 
row high (the concept of 'rows' is a little made up, but the default is that one row is
equal to one column width multiplied by the golden ratio, so in this case 50.1 mm). Once 
the first figure is drawn, we can set the next figure to be 2 columns wide and 1 row 
tall and this time set the row height to be equal to the column width like this::

    publishable.set_figsize(2, 1, aspect_ratio = 1)

Importantly, *plotsettings* doesn't just calculate the width of a 2-column figure as two
times the width of one column, but includes the width of the gutter (the space between
columns on a page) as well. Therefore, the figure that follows the above line will end
up being 169 mm wide (2 columns of 81 mm each plus a 7 mm gutter) and 81 mm tall (row
height = 1*column width).

Once the figure has been created, conveniently add labels to each subplot (if you have a
multipart figure)::

	publishable.panel_labels(fig = None, position = 'outside', case = 'lowercase', 
							 prefix = '', suffix = '.', fontweight = 'bold')

to create the labels ('a.', 'b.', 'c.' ...) in bold letters outside the top-left corner
of each subplot.

Custom journal settings can be used by specifying a python file on the PYTHONPATH::

	publishable = plotsettings.Set('my_journal_name', 'module_name')

The file 'module_name' should contain a single dictionary named *journals* with the 
following structure::

    journals = {'some_journal': {'key1': value, 'key2': value},
                'another_journal': {'key1': value, 'key2': value}}

where 'some_journal' is the identifying name of an academic journal (e.g. 'Nature') and
'key1', 'key2' correspond either to valid keys for *matplotlib.rcParams* (for example the
font name and size) or to one of 'column_width', 'gutter_width', 'max_height' or 'units'. 
Each of these non-rcParams keys except for 'max_height' is required. For an example of 
this kind of dictionary, see the module 'journals' in this package. Definitions of valid 
keys to *rcParams* can be found `here <http://matplotlib.org/users/customizing.html>`_. 
The non-rcParams keys are:

    * *column_width* (required) - the maximum width a figure is allowed to be while still 
      fitting within a single column.
    * *gutter_width* (required) - the width of the gutter (space between columns). This can 
      usually be found by comparing the maximum width that a journal allows for a single-
      column figure with the maximum width of a 2-column figure. For example, PLOS ONE
      allows a 1-column figure to be 83 mm in width and a 2-column figure to be 173.5 mm,
      meaning that the gutter width (173.5 - 83*2) is 7.5 mm wide.
    * *max_height* (optional) - the maximum height a figure is allowed to be while fitting 
      on a single page (i.e. the page height).
    * *units* (required) - the units in which the above are reported. Can be one of 'mm', 
      'cm', 'inch', or 'pts'

--------------
Version
--------------
1.0.1 - Not extensively tested. Please email to let me know of any issues.

Changelog
============
**1.0.1 (OCTOBER/13/2014)**

	* Fixed bug that made *plotsettings.Set* unable to find the default *journals* module
	* Added function *panel_labels* for convenient, 1-line addition of formatted panel 
	  labels (e.g. A, B, C) to every subplot in a figure.
	* Added 'Presentation' as a journal type for PowerPoint slides

**1.0.0 (OCTOBER/13/2014)**

	* First release

