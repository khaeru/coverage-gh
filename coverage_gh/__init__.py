import coverage
from coverage.report import get_analysis_to_report
from coverage.results import Numbers


def read_data():
    """Read data from coverage's default storage location & format."""
    cov = coverage.Coverage()
    cov.load()

    total = Numbers()

    # Iterate over files
    for fr, analysis in get_analysis_to_report(cov, morfs=None):
        # Demo usage
        print(f"{analysis.numbers.pc_covered:3.0f}% {fr.relative_filename()}")

        # TODO generate annotations for the current file

        total += analysis.numbers

    print(f"{total.pc_covered:3.0f}% total")
