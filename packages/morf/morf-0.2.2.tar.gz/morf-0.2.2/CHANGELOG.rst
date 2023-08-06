0.2.3
-----

- Bugfix: calling ``FormRenderer.visible()`` after ``FormRenderer.pop()``
  no longer causes an error.

0.2.2
-----

- An ``after`` argument was added to the @cleans and @validates decorators
  to force a validation/cleaning function to run after another has already
  completed.
- @cleans and @validates functions are no longer called if associated with
  fields that have failed a previous validation check.
- Added ``Form.add_field`` and ``Form.remove_field`` for manipulating fields
  dynamically

0.2.1
-----

- Bound form fields are now only accessible via the ``Form.fields`` dictionary.
  This removes the need to maintain two synchronized mapppings of form fields.
- Form.bind_object no longer requires a positional argument and can now also
  accept dictionaries as arguments
- Bugfix: Choice fields no longer raise ``ValidationError``\s if ``None`` or
  the empty string are used as choice values


0.2
---

- All ``render_*`` methods now return ``markupsafe.Markup`` objects
- An ``exclude`` argument was added to the default ``Form.update_object``
  implementation, allowing subclasses to more easily override the updating of
  specific attributes, and allowing ``Form.update_object`` to manage the
  remainder.


0.1
---

- Initial release
