# Gemini Paper Summarizer

## Overview

A command-line tool that uses Gemini API to generate summaries of academic papers.

Supports output in multiple languages: Chinese, English, French, German, Japanese, Korean, and Spanish.

## Examples

See the [examples](examples) directory for sample outputs, including summaries of:

- [(2017) Attention Is All You Need](https://arxiv.org/abs/1706.03762v7)

### Other Summaries in Japanese

- [(2018) What you can cram into a single vector: Probing sentence embeddings for linguistic properties](https://7shi.hateblo.jp/entry/2025/01/09/032708)
- [(2018) Improving language understanding by generative pre-training](https://7shi.hateblo.jp/entry/2025/01/08/023518)
- [(2018) BERT: Pre-training of deep bidirectional Transformers for language understanding](https://7shi.hateblo.jp/entry/2025/01/09/011331)
- [(2019) BERT rediscovers the classical NLP pipeline](https://7shi.hateblo.jp/entry/2025/01/09/014758)
- [(2019) Linguistic knowledge and transferability of contextual representations](https://7shi.hateblo.jp/entry/2025/01/09/024710)
- [(2019) A Structural Probe for Finding Syntax in Word Representations](https://7shi.hateblo.jp/entry/2025/01/09/030338)
- [(2019) What does BERT look at? An analysis of BERT’s attention](https://7shi.hateblo.jp/entry/2025/01/09/034240)
- [(2022) Symbolic Knowledge Distillation: from General Language Models to Commonsense Models](https://7shi.hateblo.jp/entry/2025/02/02/114424)
- [(2023) A Benchmark for Learning to Translate a New Language from One Grammar Book](https://7shi.hateblo.jp/entry/2025/02/02/165257)
- [(2023) Text Embeddings Reveal (Almost) As Much As Text](https://7shi.hateblo.jp/entry/2025/01/05/203512)

Meta

- [(2024) Large Concept Models: Language Modeling in a Sentence Representation Space](https://7shi.hateblo.jp/entry/2025/01/04/232224)
- [(2025) Brain-to-Text Decoding: A Non-invasive Approach via Typing](https://7shi.hateblo.jp/entry/2025/02/11/145100)

DeepSeek

- [(2024) DeepSeek LLM: Scaling open-source language models with longtermism.](https://7shi.hateblo.jp/entry/2025/01/07/225023)
- [(2024) DeepSeek-V2: A strong, economical, and efficient Mixture-of-Experts language model.](https://7shi.hateblo.jp/entry/2025/01/07/234352)
- [(2024) DeepSeek-Coder-V2: Breaking the barrier of closed-source models in code intelligence.](https://7shi.hateblo.jp/entry/2025/01/07/235825)
- [(2024) DeepSeek-V3 Technical Report](https://7shi.hateblo.jp/entry/2025/01/08/000133)
- [(2025) DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning](https://7shi.hateblo.jp/entry/2025/01/28/225747)

## Prerequisites

- Python 3.10+
- Gemini API Key (obtain from [Google AI Studio](https://aistudio.google.com/))

Note: If you find it difficult to set up the environment locally, please refer to the following Google Colab Notebook by @shoei05 (explained in Japanese):

- [論文要約 gemini-paper-summarizer を Google Colab で使用する](https://colab.research.google.com/drive/1yj02UYLNjXvz4nInB5zGzvrcawaJ_Mua?usp=sharing)

## Installation

1. Clone the repository
2. Install dependencies:
   ```
   uv sync
   ```
3. Create a `.env` file in the project directory with your Gemini API key:
   ```bash
   GEMINI_API_KEY=your_api_key_here
   ```

## Usage

```bash
uv run gp-summarize path/to/paper.pdf
```

The tool will generate several markdown files with different types of summaries:

1. A translation of the paper's title and abstract
2. A summary of the entire paper
3. A JSON structure of the paper's chapters and sections
4. Individual summaries (not translations) for each main section
5. Summaries of 1-4 above combined into a single file

The output files will be named based on the input filename. Files 1-4 above will be saved in a directory and numbered continuously (e.g., `paper/001.md`, `paper/002.md`, etc.). The combined file will be named `paper.md`.

Note: If the process is interrupted (e.g. by Ctrl+C or by a 429 rate limit error, etc.), the process can be re-run smoothly, because any existing output files will be skipped.

### Output Format

For each prompt, the tool generates a markdown file containing:

- Title (prompt number)
- Statistics information about tokens
- Prompt
- AI-generated response

The section structure will be displayed in both JSON format and as a hierarchical list.

## Command-Line Options

```
uv run gp_summarize [-h] [-d OUTPUT_DIR] [-o OUTPUT] [-l {de,en,es,fr,ja,ko,zh}] [-m MODEL] [--suffix SUFFIX] [--ccache] [--version] paths [paths ...]
```

- `paths`: **Required** Path(s) to one or more files to summarize
  - Multiple files can be specified
    - Each file is processed separately
    - If you need to process them together, use an external tool to combine ([Repomix](https://repomix.com/) recommended)
  - Wildcards (`*`) are supported on Windows
    - On POSIX systems, wildcards are processed by the shell

- `-d, --output-dir`: Optional. Specify the output directory for intermediate files
  - Useful when processing multiple files

- `-o, --output`: Optional. Specify the output file for the summary
  - Can only be used with a single file

- `-l, --language`: Optional. Specify the output language
  - Supported languages: `de` (German), `en` (English), `es` (Spanish), `fr` (French), `ja` (Japanese), `ko` (Korean), `zh` (Chinese)
  - Default: Based on system language settings

- `-m, --model`: Optional. Specify the Gemini model to use
  - Default: gemini-2.5-flash-preview-05-20

- `--suffix`: Optional. Add custom suffix to the output filename
  - Useful for differentiating the output filename from the source filename

- `--ccache`: Optional. Enable context caching
  - Caches source file to reduce API usage costs
  - Currently disabled by default as uploaded files may sometimes fall below the minimum token count.

- `--version`: Display version information

### Examples

Summarize a single PDF:
```
uv run gp_summarize paper.pdf
```

Summarize multiple PDFs:
```
uv run gp_summarize paper1.pdf paper2.pdf
```

Specify an output directory:
```
uv run gp_summarize -d ./outputs paper.pdf
```

Summarize in a specific language:
```
uv run gp_summarize -l ja paper.pdf
```

## License

CC0 1.0 Universal
