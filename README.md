# contrail-forecast

> Generate contrail forecasts by running [pycontrails](https://py.contrails.org) models with [Apache Beam](https://beam.apache.org/).

**This project is currently a work in progress.**

## Documentation

Documentation is written in [MyST Markdown](https://myst-parser.readthedocs.io/en/v0.15.0/using/syntax.html) and [reStructuredText](http://docutils.sourceforge.net/rst.html) then built into HTML and PDF with [Sphinx](https://www.sphinx-doc.org/en/master/).

To build documentation, install the `["docs"]` dependencies and run

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
