
Changelog
=========

0.13 (2014-10-22)
-----------------

- Adds Swiss social security number ("Neue AHV Nummer") field.
  [href]

- Adds IBAN schema field.
  [href]

- Adds HexColor schema field.
  [href]

0.12 (2014-06-04)
-----------------

- Adds a script to configure the mail host settings from the commandline.
  [href]

- BeakerSessionDataManager can now also be installed if no session data manager
  exists in the Zope root.
  [href]

0.11 (2014-03-26)
-----------------

- The email validator now strips whitespace before checking.
  [href]

- Adds custom title behavior which allows to set the title/id of an object
  easily.
  [href]

- Adds basegroup class for easy formset/formgroup management on forms.
  [href]

0.10 (2014-03-03)
-----------------

- Adds script to install the BeakerSessionDataManager to a Zope instance.
  [href]

- Adds base classes for forms and views that include helper functions. Subject
  to change as a good middle ground for different modules is found.
  [href]

0.9
---

- The new_dexterity_type function no longer overwrites the 'klass' attribute.
  Fixes #1.

0.8
---

- Adds a safe_html function

- Fixes tools.get_parent returning a non-brain parent for brain input

0.7
---

- Adds a naive profiler function

- Adds a unicode collation sortkey

- Adds a DRY version of http://maurits.vanrees.org/weblog/archive/2009/12/catalog

0.6
---

- Fixes the schemafields from being unwritable by the supermodel

0.5
---

- Adds Email and Website fields for supermodel, schemaeditor, zope.schema

0.4
---

- New function to search for Dexterity FTI's that use a certain schema

- New translator function for translating text with the request language

0.3
---

- Renames utils.py to tools.py

0.2
---

- Adds commonly used javascripts

0.1
---

- Initial release