Changelog
---------

Here you can see the full list of changes between each SQLAlchemy-Defaults release.


0.4.4 (2014-12-30)
^^^^^^^^^^^^^^^^^^

- Added support for Numeric and Float defaults
- Changed integer_defaults config option to numeric_defaults


0.4.3 (2014-10-10)
^^^^^^^^^^^^^^^^^^

- Fixed check constraint handling for other than integer types


0.4.2 (2014-08-04)
^^^^^^^^^^^^^^^^^^

- Fixed sequence as integer default value handling.


0.4.1 (2014-06-13)
^^^^^^^^^^^^^^^^^^

- Fixed datetime and date server_default handling.


0.4.0 (2014-03-26)
^^^^^^^^^^^^^^^^^^

- Added smarter string server_default inspection.


0.3.2 (2013-11-04)
^^^^^^^^^^^^^^^^^^

- Psycopg2 removed from requirements


0.3.1 (2013-10-10)
^^^^^^^^^^^^^^^^^^

- Label no longer available as column property (this was in conflict with SQLAlchemy's own label construct)


0.3.0 (2013-09-17)
^^^^^^^^^^^^^^^^^^

- Python 3 support added


0.2.4 (2013-09-11)
^^^^^^^^^^^^^^^^^^

- Booleans no longer force set to not nullable (not nullable is still the default for this data type)


0.2.3 (2013-09-10)
^^^^^^^^^^^^^^^^^^

- Better checking of boolean and string types for not nullable defaults


0.2.2 (2013-08-27)
^^^^^^^^^^^^^^^^^^

- Added unicode support for string defaults
- Dropped Python 2.5 support


0.2.1 (2013-08-27)
^^^^^^^^^^^^^^^^^^

- Only strings and ints now assigned as server defaults for string columns


0.2.0 (2013-06-17)
^^^^^^^^^^^^^^^^^^

- Added index auto creation for foreign key columns (very useful for postgresql)
- More robust API


0.1.7 (2013-03-14)
^^^^^^^^^^^^^^^^^^

- Added choices as a column attribute


0.1.6 (2013-03-14)
^^^^^^^^^^^^^^^^^^

- Added form_field_class


0.1.5 (2013-01-30)
^^^^^^^^^^^^^^^^^^

- Made is_string utility function support String and Text types


0.1.4 (2013-01-26)
^^^^^^^^^^^^^^^^^^

- Fixed not nullable assignment for UnicodeText types


0.1.3 (2013-01-26)
^^^^^^^^^^^^^^^^^^

- Fixed empty column args handling (again)


0.1.2 (2013-01-26)
^^^^^^^^^^^^^^^^^^

- Fixed empty column args handling


0.1.1 (2013-01-26)
^^^^^^^^^^^^^^^^^^

- Added custom Column class


0.1.0 (2013-01-24)
^^^^^^^^^^^^^^^^^^

- Initial public release
