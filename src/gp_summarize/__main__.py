import argparse
from .__init__ import name, __version__
parser = argparse.ArgumentParser(description='Summarize academic papers using Gemini API')
parser.add_argument('paths', nargs='+', help='Path(s) to one or more files')
parser.add_argument('-d', '--output-dir', help='Output directory for intermediate files')
parser.add_argument('-o', '--output', help='Output file for summary')
parser.add_argument('-l', '--language', choices=['de', 'en', 'es', 'fr', 'ja', 'ko', 'zh'], default=None, help='Specify the output language')
parser.add_argument('-m', '--model', default='gemini-2.5-flash-preview-05-20', help='Specify the Gemini model to use')
parser.add_argument('--version', action='version', version=f'{name} {__version__}')
parser.add_argument('--suffix', help='Suffix to add to the output file name')
parser.add_argument('--ccache', action='store_true', default=False, help='Enable context caching')
args = parser.parse_args()

import os
if os.name == 'nt':  # Check if the system is Windows
    from glob import glob
    paths = []
    for path in args.paths:
        paths.extend(glob(path))
else:
    paths = args.paths

pdfs = len(paths)
if args.output:
    if args.output_dir:
        parser.error("Output directory (-d) cannot be specified when an output file (-o) is provided.")
    if pdfs > 1:
        parser.error("Output file (-o) cannot be specified when multiple PDF files are provided.")

from dotenv import load_dotenv
load_dotenv()

from .summarize import summarize
from . import gemini
from .lang import selector

lang_module = selector.init(args.language)

model = args.model
if not model.startswith("models/"):
    model = "models/" + args.model

generation_config = {
    "temperature": 0.5,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

def main():
    for i, path in enumerate(paths, 1):
        if i > 1:
            print()
        print(f"==== PDF {i}/{pdfs}: {path}")
        summary, output, stats = summarize(
            model,
            generation_config,
            lang_module.system_instruction,
            lang_module,
            path,
            args.output,
            args.output_dir,
            args.suffix,
            f"PDF {i}/{pdfs}, ",
            args.ccache,
        )
        with open(output, "w", encoding="utf-8") as f:
            f.write(summary)
        print(f"Summary saved: {output}")
        print("Statistics:")
        gemini.show_stats(stats, "- ")
