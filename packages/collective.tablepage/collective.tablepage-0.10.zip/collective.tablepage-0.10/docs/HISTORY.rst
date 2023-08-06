Changelog
=========

0.10 (2014-10-22)
-----------------

- New columns: "*Date*" and "*Date/Time*".
  This close `#7`__
  [keul]
- Some visual changes to very small tables
  [keul]

__ https://github.com/RedTurtle/collective.tablepage/issues/7

0.9 (2014-10-01)
----------------

Special thanks to `Petri Savolainen`__ for lot of stuff done in this release

__ https://github.com/petri

- When editing table, row's uuid is put on ``data-uid`` attribute on row 
  [keul]
- Removed useless fieldset legend when editing a row.
  This close `#13`__
  [keul]
- Fixed updated row count message when using the refresh button
  [keul]
- Caches are now pre-populated at write time, not when the first read
  attempt happen. This will also fix a catalog index bug with Computed
  columns
  [keul]
- Fixed issue in Link and File columns: was not possible to delete submitted
  data but only possible to change it
  [keul]
- Fixed critical bug: when deleting a row, following rows were still indexed
  with old (wrong) position value. This will lead to strage behavior when
  searches are performed
  [keul]
- Implemented the computed vocabulary feature: vocabulary source can be taken
  from a TALES evaluation (close `#10`__)
  [petri, keul]
- Multi tables view was not using batchin or search
  [keul]
- Search form method from ``POST`` to ``GET`` (batching was using ``GET`` already)
  [keul]
- Removed min number of rows needed for enabling DataTables (close `#16`__)
  [keul]
- Usability improvements. When using DataTables and we don't have any row groups,
  move the (unique) "*Add row*" button in the lower section (close `#11`__)
  [keul]
- Fixed an issue that store icons absolute URL in the cache for "linkable"
  columns (close `#14`__)
  [keul]

__ https://github.com/RedTurtle/collective.tablepage/issues/13
__ https://github.com/RedTurtle/collective.tablepage/issues/10
__ https://github.com/RedTurtle/collective.tablepage/issues/16
__ https://github.com/RedTurtle/collective.tablepage/issues/11
__ https://github.com/RedTurtle/collective.tablepage/issues/14

0.8.1 (2014-07-23)
------------------

- Migration fixes from older releases
  [keul]
- Some minimal JSHint cleanup on the 3rd party ``jquery.dataTables.rowGrouping.js``
  file that sometimes can create problems with compression. Also provided
  a pre-minified version. See `#14279`__).
  [keul]

__ https://dev.plone.org/ticket/14279

0.8 (2014-07-11)
----------------

- Added Finnish translation
  [petri]
- Fixed encoding issue with vocabulary values using selection column
  (close `#5`__)
  [keul]

__ https://github.com/RedTurtle/collective.tablepage/issues/5

0.8b3 (2014-06-26)
------------------

- Yet another Plone 3 compatibility fix
  [keul]
- Fixed critical bug in search: path was not used for
  finding labels
  [keul]
- Fixing AdvancedQuery integration and removing unused indexes. 
  This fix critical bug that make query look for
  "access inactive portal content" permission
  [keul]
- Fixed an evil bug that populate caches of computed fields with
  bad values when search are performed
  [keul]

0.8b2 (2014-06-04)
------------------

- Part of the migration step from 0.8a2 was missing
  [keul]

0.8b1 (2014-06-03)
------------------

- Purge cache command was only working for indexed columns
  [keul]
- uuid was not provided when CSV upload feature was used
  [keul]
- Prevent `BadRequest` exception when uploading the same file twice
  [keul]
- Restored usage of labels, also with search
  [keul]
- Fixed a bug with labels and batching: starting item were
  skipped if a label from previous page was present
  [keul]

0.8a2 (2014-05-20)
------------------

- Fix compatibility errors with documents created with version 0.7 and below
  [keul]
- ``icon:`` and ``title:`` features also for internal links
  [keul]
- Error migrating from 0.7: the catalog was created inside the
  ``portal_setup`` tool!
  [keul]
- Added a new "refresh catalog" command on tables
  [keul]
- Indexing of cached values is now trying to invalidating cache first.
  This prevent infinite caching of computed columns
  [keul] 
- Changes to cache generation, to reduce ConflictError
  [keul]

0.8a1 (2014-04-30)
------------------

- Fixed a bug that break CSV export when computed columns are used
  [keul]
- Added minimal Link colums diplay prefs (a fixed link text or icon)
  [keul]
- Fixed wrong column configuration cache
  [keul]
- Fixed appearence of "No rows" section on Plone that are not using
  ``plone.batching``
  [keul]
- Enable DataTables only if we have some rows to show. This fix visual
  issues with some layouts
  [keul]
- Link column: put the ``external`` value for ``rel`` for external links and not
  for internal ones
  [keul]
- Added search features
  [keul]

0.7 (2014-03-19)
----------------

- Multiple tables view was unreachable on emtpy tables
  [keul]
- The jquery.dataTables.rowGrouping.js plugin is disabled by default
  [keul]
- Multiple multi-files columns in the same table was not working
  [keul]
- Fixed minor JavaScript errors
  [keul]
- Styles fixes: main column (HTML) label is a little bigger that default
  Plone form labels
  [keul]
- Prevent new label from load a wrong default text
  [keul]
- Do not display empty icon in link column
  [keul]
- New "*insertType*" configuration (new row at the end or beginning of groups)
  [keul]
- New column type: "Computed"
  [keul]
- Fixed a problem with link-like columns and cache. Do not return object absolute_url
  because a backend URL could be cached. Instead use the *resolveuid* URL and run
  table through portal_trasform when in view.
  Drawback of the approach: when editing the table's URLs still use *resolveuid*
  [keul]
- Added batching/pagination
  [keul]

0.6 (2014-02-25)
----------------

- Multiple tables view was not properly display HTML
  [keul]
- Added caching for rendered columns. This will speed up
  a little/lot table rendering
  [keul]
- Moved inline JavaScript to separate resource files
  [keul]
- Show/Hide command now act also on page header and footer
  (Zen Mode!)
  [keul]

0.5 (2014-02-06)
----------------

- The ``unique`` validator was preventing record update
  [keul]
- Monetary column will pad the final zero in less that 2 decimal
  are supplied (123.5 will be 123.50)
  [keul]

0.5b4 (2014-02-04)
------------------

- Fixed a bug that break link columns when the linked content is no more
  [keul]
- Fixed error when validating old rows, created before version 0.5
  [keul]

0.5b3 (2014-01-31)
------------------

- Do not use the HTML 5 ``number`` type anymore because
  of `Google Chrome stupidity`__
  [keul]
- Fixed a Python 2.4 bug in interpreting CSV format
  [keul]
- Do not fail the whole import procedure if a CSV row is missing
  some columns
  [keul] 

__ http://code.google.com/p/chromium/issues/detail?id=78520

0.5b2 (2014-01-29)
------------------

- Fixed error when editing old rows, created before version 0.5
  [keul]
- The import from CSV form can be used when no configuration has been given.
  A basical configuration will be guessed by columns headers
  [keul]
- Select colum now enforce vocabulary values
  [keul]
- New column type: "Monetary"
  [keul]
- When exporting in CSV, always quote data. This prevent some fancy
  Excel/OpenOffice interpretation
  [keul]
- Column validator can be executed also when importing from CSV
  [keul]

0.5b1 (2014-01-13)
------------------

- Soft dependency on jQuery DataTables plus "*Row Grouping Add-on*".
  This add new features like live-search in table, batching and colum sorting.
  [keul]
- Added a JavaScript command for expand/collapse available view when editing
  (this can help in cases where you added a lot of columns)
  [keul]
- Fixed critical error in the "Files" column; when selecting existing file
  the column id was ignored
  [keul]
- Added new feature: registering validators
  [keul]
- Added validator for required field
  [keul]
- Added validator for unique field
  [keul]
- New field type: "Email", for inserting an text in e-mail format
  [keul]
- New field type: "Numeric", for inserting an text in numerical format
  [keul]

0.4.1 (2014-01-03)
------------------

- Added uninstall profile
  [keul]
- Fixed bug in finding duplicate rows when importing from CSV
  (close `#1`__) [keul]

__ https://github.com/RedTurtle/collective.tablepage/issues/1

0.4 (2013-11-14)
----------------

- Do not display selection checkbox if I can't delete a row
  [keul]
- Raise lifecycle events properly when creating files
  [keul]
- New field type: "Files", for uploading a set of files to
  be rendered in the same cell
  [keul]
- Labels inside the table are now supported
  [keul]
- New view for displaying data on multiple tables
  [keul]
- New field type: "Link", for inserting an URL or an internal
  reference
  [keul]
- CSV export done by backend get UUIDs when applicable
  [keul]
- CSV import now validate data: do not import every text you
  read from the file
  [keul]
- CSV import now transform URL/path to valid content uuids  
  [keul]

0.3 (2013-10-18)
----------------

- Different versioning message when a row is changed
  or modified [keul]
- Added missing versioning attempt when using CSV upload
  [keul]
- Fixed a performance/security problem: data inside text cells
  were transformed to HTML without any check (and this was also
  *really* slow)
  [keul]
- Can now delete multiple (or all) rows
  [keul]
- CSV import is not importing anymore inside wrong colum when an
  unknow header is found
  [keul]

0.2 (2013-10-11)
----------------

- Fixed missing translations [keul]
- Do not display "download as CSV" for empty tables [keul]
- Added an option for choosing when display headers [keul]
- Handle loading of duplicate file id: file is not loaded twice but
  same reference is kept [keul]
- Do not display "Edit table" or row's commands if no configuration
  has been set [keul]

0.1.2 (2013-09-27)
------------------

- fixed encoding error on columns headers [keul]
- fixed encoding error on editing rows [keul]

0.1.1 (2013-09-23)
------------------

- Fixed UnicodeDecodeError problem with non-ASCII chars [keul]

0.1 (2013-09-19)
----------------

- Initial release
