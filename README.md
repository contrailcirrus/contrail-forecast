# Contrail Forecast Specification

Contrail forecast data and API specification.
Hosted at [contrailcirrus.github.io/contrail-forecast](https://contrailcirrus.github.io/contrail-forecast/index.html).

## Develop

Documentation is written in [MyST Markdown](https://myst-parser.readthedocs.io/en/v0.15.0/using/syntax.html) and [reStructuredText](http://docutils.sourceforge.net/rst.html) then built into HTML and PDF with [Sphinx](https://www.sphinx-doc.org/en/master/).

To build documentation, install `["docs"]` dependencies (`pip install -e ".[docs]"`) and run

```bash
$ make docs-build
```

To serve html documentation, run:

```bash
$ make docs-serve
```

To build pdf documentation, you must have [pandoc](https://pandoc.org/installing.html) and a [LaTeX distribution](https://www.latex-project.org/get/) installed.

```bash
$ make docs-pdf
```

## License

[Apache License 2.0](LICENSE)
