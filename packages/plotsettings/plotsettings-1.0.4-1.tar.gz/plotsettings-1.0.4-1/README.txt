================
plotsettings
================

The difference between publishing figures using just *matplotlib* **(A)**, and using *matplotlib*
with *plotsettings* **(B)**:

.. image:: https://dl.dropboxusercontent.com/u/35392962/annotated_example.jpg
   :width: 600
   :height: 279

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
    
    * Cell (use argument 'Cell')
    * Copeia (use argument 'Copeia')
    * Deep Sea Research II (use argument 'DSRII')
    * Ecology Letters (use argument 'EcolLett')
    * Global Change Biology (use argument 'GlobChangeBio')
    * Global Environmental Change (use argument 'GlobEnvChange')
    * Integrative and Comparative Biology (use argument 'IntCompBiol')
    * Journal of Experimental Biology (use argument 'JEB')
    * Limnology and Oceanography (use argument 'LimnolOcean')
    * Marine Ecology Progress Series (use argument 'MEPS')
    * Nature magazine (use argument 'Nature')
    * Oecologia (use argument 'Oecologia')
    * Proceedings of the National Academy of Sciences, USA (use argument 'PNAS')
    * Proceedings of the Royal Society B (use argument 'ProcRoySocB')
    * Public Library of Science One (use argument 'PLOSOne')
    * Public Library of Science Biology (use argument 'PLOSBio')
    * Science magazine (use argument 'Science')
    * Presentation (okay, this is not a journal but it's still useful for outputting 
      figures to presentation slides; access with the argument 'Presentation')

Don't see the journal you want on the list (say you want to publish in the `Proceedings 
of the 6th ACM Workshop on Next Generation Mobile Computing for Dynamic Personalised 
Travel Planning <http://dl.acm.org/citation.cfm?id=2307874&picked=prox>`_)? Compile your 
own list of journals by creating a python file containing a single dictionary with 
settings for every journal *you* use! You can specify any parameters that are accepted 
by *matplotlib.rcParams* as well as the column width, gutter width, page height and the
way that multi-panel figures are labeled.

Also, a **Bonus**!:

	* 1-line labeling of all the subplots in a figure (e.g. with '(a)', '(b)', '(c)' 
	  etc.) using the standalone function *panel_labels* or the method 
	  *Set.panel_labels*!

----------------
Installation
----------------
*plotsettings* has only been tested in Python 2.7

Install through pip::

	$ pip install plotsettings

Requires the following non-standard libraries:

     * *matplotlib*

Because preferred installation of matplotlib can vary depending on the operating system, 
matplotlib will not automatically be installed as a dependency. Instead, installation will 
raise an exception if matplotlib cannot be found in the pythonpath. In this case, please 
install matplotlib via your preferred method, most of which are explained `by matplotlib 
<http://matplotlib.org/users/installing.html>`_

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

	publishable.panel_labels(fig = fig, position = 'outside', case = 'lower', 
							 prefix = '', suffix = '.', fontweight = 'bold')

to create the labels ('a.', 'b.', 'c.' ...) in bold letters outside the top-left corner
of each subplot.

Custom journal settings can be used by specifying a python file on the PYTHONPATH::

	publishable = plotsettings.Set('my_journal_name', 'module_name')

The file 'module_name' should contain a single dictionary named *journals* with the 
following structure::

    journals = {'journal1':      {'rcParams':     {'param1': value1,
                                                   'param2': value2 ...}, 
                                  'figsize':      {'param1': value1,
                                                   'param2': value2 ...},
                                  'panel_labels': {'param1': value1,
                                                   'param2': value2 ...},
                'journal2':      {'rcParams':     {'param1': value1,
                                                   'param2': value2 ...}, 
                                  'figsize':      {'param1': value1,
                                                   'param2': value2 ...},
                                  'panel_labels': {'param1': value1,
                                                   'param2': value2 ...},
                'journal3'...
                }

where 'journalx' are the identifying names of academic journals (e.g. 'Nature'), with
the specifications for each journal being divided into 3 dictionaries:

    * *rcParams*: All parameters are optional. Any valid input to pyplot.rcParams (for
      example font name and sizes, default linewidths) is accepted. Definitions of valid 
      keys to rcParams can be found `here <http://matplotlib.org/users/customizing.html>`_.
    * *figsize*: Set figure dimension calculations. Requires the parameters column_width, 
      gutter_width, and units. The parameter max_height is optional. See below for details.
    * *panel_labels*: Set default panel labels (i.e. the text that identifies each subplot in
      a figure as A, B, C, etc.). All parameters are optional. See below for details.
  
The possible non-rcParams parameters are:
    
    * *figsize*:
    
        * *column_width* (required) - the maximum width a figure is allowed to be while still 
          fitting withing a single column.
        * *gutter_width* (required) - the width of the gutter (space between columns). This can 
          usually be found by comparing the maximum width that a journal allows for a single-
          column figure with the maximum width of a 2-column figure. For example, PLoS One
          allows a 1-column figure to be 83 mm in width and a 2-column figure to be 173.5 mm,
          meaning that the gutter width (173.5 - 83*2) must be 7.5 mm wide.
        * *max_height* (optional) - the maximum height a figure is allowed to be while fitting 
          on a single page (i.e. the page height).
        * *units* (required) - the units in which the above are reported. Can be one of 'mm', 
          'cm', 'inch', or 'pts'
    
    * panel_labels:
    
        * *fontweight* (optional) - the font weight of panel annotations (e.g. A, B, C etc.).
          Default is 'bold'
        * *case* (optional) - whether to capitalize ('upper') or not capitalize
          ('lower') the panel labels.
        * *prefix* (optional) - characters to prepend to panel label (e.g. if the desired
          label style is (A), (B), etc., set label_prefix to ')').
        * *suffix* (optional) - characters to append to panel label (e.g. if the desired
          label style is a., b., etc., set label_suffix = '.')
        * *fontsize* (optional) - font size in pts of the label. Defaults to rcParams['font.size']

--------------
Changelog
--------------
**1.0.4-1 (NOVEMBER/14/2014)**

	* Removed deprecated keywords from default journal parameters

**1.0.4 (OCTOBER/20/2014)**

	* Added ability for *panel_labels* method to automatically detect axes that contain only
	  colorbars and not label them (use detect_colorbars = True). This method relies on the
	  assumption that colorbar axes are not navigable (e.g. cannot be panned or zoomed in the
	  interactive figure). This property was chosen because it seems to work both for colorbars
	  created by *pyplot.colorbar()* as well as those created explicitly in a new axis such as
	  using the AxesGrid toolkit.

**1.0.3 (OCTOBER/15/2014)**

	* package *matplotlib* is no longer explicitly required in setup.py. Installation will raise
	  an error if matplotlib is not present - please install in your preferred way.

**1.0.2 (OCTOBER/15/2014)**

	* Changed format of dictionary specifying journal settings. Settings for each journal are
	  now divided between the dictionaries 'rcParams', 'figsize' and 'panel_labels' instead of 
	  being amalgamated into a single dictionary.
	* Added journals Science, Integrative and Comparative Zoology, Copeia, Cell, Global Change 
	  Biology, Global Environmental Change, Limnology and Oceanography, Nature, PLOS Biology
	  and Oecologia to the list of natively supported publications.
	* Added method *panel_labels* to class *Set* to allow panel labels (e.g. A, B, C etc.)
	  to automatically follow default settings for the journal (e.g. boldface, uppercase, etc.)

**1.0.1 (OCTOBER/14/2014)**

	* Fixed bug that made *plotsettings.Set* unable to find the default *journals* module
	* Added function *panel_labels* for convenient, 1-line addition of formatted panel 
	  labels (e.g. A, B, C) to every subplot in a figure.
	* Added 'Presentation' as a journal type for PowerPoint slides

**1.0.0 (OCTOBER/13/2014)**

	* First release

