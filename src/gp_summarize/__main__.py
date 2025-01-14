import argparse
from .__init__ import name, __version__
parser = argparse.ArgumentParser(description='Summarize academic papers using Gemini API')
parser.add_argument('pdf_paths', nargs='+', help='Path(s) to one or more PDF files')
parser.add_argument('-d', '--output-dir', help='Output directory for intermediate files')
parser.add_argument('-o', '--output', help='Output file for summary')
parser.add_argument('-l', '--language', choices=['de', 'en', 'es', 'fr', 'ja', 'ko', 'zh'], default=None, help='Specify the output language')
parser.add_argument('--version', action='version', version=f'{name} {__version__}')
args = parser.parse_args()

import os
if os.name == 'nt':  # Check if the system is Windows
    from glob import glob
    pdf_paths = []
    for path in args.pdf_paths:
        pdf_paths.extend(glob(path))
else:
    pdf_paths = args.pdf_paths

pdfs = len(pdf_paths)
if args.output:
    if args.output_dir:
        parser.error("Output directory (-d) cannot be specified when an output file (-o) is provided.")
    if pdfs > 1:
        parser.error("Output file (-o) cannot be specified when multiple PDF files are provided.")

from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

from .summarize import summarize
from . import gemini
from .lang import selector

lang_module = selector.init(args.language)

max_rpm  = 10  # maximum requests per minute

model = genai.GenerativeModel(
    model_name="models/gemini-2.0-flash-exp",
    generation_config={
        "temperature": 0.5,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    },
    system_instruction=lang_module.system_instruction,
)

def main():
    for i, pdf_path in enumerate(pdf_paths, 1):
        if i > 1:
            print()
        print(f"==== PDF {i}/{pdfs}: {pdf_path}")
        summary, output, stats = summarize(
            max_rpm, model, lang_module,
            pdf_path, args.output, args.output_dir,
            f"PDF {i}/{pdfs}, ",
        )
        with open(output, "w", encoding="utf-8") as f:
            f.write(summary)
        print(f"Summary saved: {output}")
        print("Statistics:")
        gemini.show_stats(stats, "- ")
