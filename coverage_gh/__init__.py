import logging
from itertools import groupby

import coverage
from coverage.report import get_analysis_to_report
from coverage.results import Numbers

log = logging.getLogger(__name__)


MAX_ANNOTATIONS = 50


def _get_annotation_message(start_line, end_line):
    if end_line == start_line:
        return f"Added line #L{start_line} not covered by tests"
    else:
        return f"Added lines #L{start_line}-{end_line} not covered by tests"


def get_missing_range(range_list):
    for a, b in groupby(enumerate(range_list), lambda pair: pair[1] - pair[0]):
        b = list(b)
        yield {"start_line": b[0][1], "end_line": b[-1][1]}


def create_single_annotation(error, file_path):
    start_line = error["start_line"]
    end_line = error["end_line"]
    message = _get_annotation_message(start_line, end_line)
    annotation = dict(
        path=file_path,
        start_line=start_line,
        end_line=end_line,
        annotation_level="warning",
        message=message,
    )
    return annotation


def read_data():
    """Read data from coverage's default storage location & format."""
    cov = coverage.Coverage()
    cov.load()

    annotations = []
    total = Numbers()

    # Iterate over files
    for fr, analysis in get_analysis_to_report(cov, morfs=None):
        # Demo usage
        print(f"{analysis.numbers.pc_covered:3.0f}% {fr.relative_filename()}")

        # Generate annotations for the current file
        for missing_range in get_missing_range(analysis.missing):
            annotation = create_single_annotation(missing_range, fr.relative_filename())
            annotations.append(annotation)
            if len(annotations) >= MAX_ANNOTATIONS:
                log.warning("Reached maximum {MAX_ANNOTATIONS}; stopping")

        total += analysis.numbers

    print(f"{total.pc_covered:3.0f}% total")
    print(annotations)
