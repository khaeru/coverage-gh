from pathlib import Path

import coverage


def read_data():
    """Read data from coverage's default storage location & format."""
    cd = coverage.CoverageData()
    cd.read()

    # Print names of measured files relative to the directory containing the report
    base_path = Path(cd.data_filename()).parent
    for filename in cd.measured_files():
        print(Path(filename).relative_to(base_path))
