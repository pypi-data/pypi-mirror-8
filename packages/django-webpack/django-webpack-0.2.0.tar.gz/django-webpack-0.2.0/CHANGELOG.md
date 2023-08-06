Changelog
=========

### 0.2.0 (14/12/2014)

API changes:
- `django_webpack.models.WebpackBundle.output` is now `django_webpack.models.WebpackBundle.path_to_output`
- `django_webpack.models.WebpackBundle.get_output` is now `django_webpack.models.WebpackBundle.get_path_to_output`

Added an optional in-memory cache, triggered by the setting `DJANGO_REACT['CACHE']`.

### 0.1.0 (13/12/2014)

- Initial release

### 0.0.2 (11/12/2014)

Heavy refactor.

Added a test suite.
`django_webpack.webpack.bundle` now offers trivial programmatic access to webpack.
Moved the Webpack configuration settings from settings.py to `django_webpack.models.WebpackBundle`.

### 0.0.1 (7/12/2014)

- Initial release