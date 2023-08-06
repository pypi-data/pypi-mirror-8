Changelog
=========

1.0.2 (2014-11-06)
------------------

- Use IAnnotations to store info on the transmogrifier context, instead
  of supersekrit attributes.
  [mj]

- Added workaround for sqlalchemy versions > 0.7.2 where sqlalchemy.exceptions
  is gone in favour of sqlalchemy.exc.
  [pilz]


1.0.1 (2008-09-17)
------------------

- The keys in the returned dictionary need to be normal strings.
  [fschulze, soerensigfusson]


1.0 (2008-05-22)
----------------

- Initial release
  [wichert, mj]
