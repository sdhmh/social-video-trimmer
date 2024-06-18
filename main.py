import argparse
from pathlib import Path
from whatsapp import whatsapp_editor


def validate_file(f) -> Path:
    if not Path(f).exists():
        # Argparse uses the ArgumentTypeError to give a rejection message like:
        # error: argument input: x does not exist
        raise argparse.ArgumentTypeError("{0} does not exist".format(f))
    return Path(f)

def validate_dir(d) -> Path:
    directory = Path(d)
    directory.mkdir(exist_ok=True)
    return directory

parser = argparse.ArgumentParser()

parser.add_argument(
    "-i",
    "--input",
    dest="filename",
    required=True,
    type=validate_file,
    help="Relative Path to the input file",
    metavar="FILE",
)
parser.add_argument(
    "-d",
    "--output-directory",
    dest="output_dir",
    type=validate_dir,
    default="processed/",
    help="Relative Path to the output directory",
    metavar="DIRECTORY",
)
parser.add_argument(
    "-suf",
    "--output-suffix",
    dest="output_suffix",
    default="",
    help="Text to be appended after the filename",
    metavar="SUFFIX",
)
parser.add_argument(
    "-ext",
    "--output-ext",
    dest="output_ext",
    default=".mp4",
    help="Output Extension of the new File",
    metavar="EXT",
)


subparsers = parser.add_subparsers(
    title="platforms", dest='platform'
)
subparser_whatsapp = subparsers.add_parser("whatsapp", help="Generate for Whatsapp")
subparser_whatsapp.add_argument(
    "-s",
    "--status",
    action="store_true",
    help="Generate 30s clip from the source video (compatible with Whatsapp Web)",
)
subparser_whatsapp.add_argument(
    "-n",
    "--no-encoding",
    action="store_false",
    help="(Only for Linux) Don't encode the output file in libx264 (doesn't require libx264 to be installed). Not recommended on Linux, instead install libx264 (Highly Recommended)",
)


args = parser.parse_args()

if args.platform == "whatsapp":
    whatsapp_editor(args.filename, args.output_dir, whatsapp_web_compatible=args.no_encoding, status=args.status, ext=args.output_ext, output_suffix=args.output_suffix + ".whatsapp")
