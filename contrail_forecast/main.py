"""Prototype for the contrail forecast model pipeline."""

import apache_beam as beam
import beam_utils


def pipeline(root: beam.Pipeline) -> None:
    cocipgrid_results = beam_utils.run_cocipgrid(root)

    _ = (
        cocipgrid_results
        | "Serialize" >> beam.Map(lambda elm: (elm[0], elm[1].to_netcdf()))
        # TODO: write the results here
        # e.g. https://stackoverflow.com/questions/63035772/streaming-pipeline-in-dataflow-to-bigtable-python
    )


def main() -> None:
    # TODO: run your pipeline here
    # e.g.
    # with beam.Pipeline(options=pipeline_options) as p:
    #     pipeline(p)
    pass


if __name__ == "__main__":
    main()
