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
