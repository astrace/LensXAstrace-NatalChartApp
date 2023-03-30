import argparse
from natal_chart import generate

def main():
    parser = argparse.ArgumentParser(
        prog="natal_chart_cli",
        description="Generate a natal chart based on birth information",
        epilog="Example usage: natal_chart_cli.py '2022-01-01T12:00:00' '40.7128,-74.0060'",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "local_time",
        help=(
            "Local date and time of birth in ISO 8601 format (YYYY-MM-DDTHH:MM:SS)."
            " This represents the local time at the provided birth location."
        )
    )
    parser.add_argument(
        "location",
        help=(
            "Geographical coordinates of birth location in the format 'LAT,LON',"
            " where LAT is the latitude and LON is the longitude."
        )
    )
    parser.add_argument(
        "--local", action="store_true",
        help=(
            "Generate natal chart locally. This is useful for visual testing."
            " When running locally, the program will read image files from the local"
            " file system instead of fetching them from S3."
        )
    )

    args = parser.parse_args()
    
    im = generate(args.local_time, args.location, args.local)
    im.show()


