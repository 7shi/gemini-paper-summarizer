import sys, os, argparse, json

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai
model = genai.GenerativeModel(
    model_name="models/gemini-2.0-flash-exp",
    generation_config={
        "temperature": 0.5,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }
)

prompts = [
    "日本語で要約してください。箇条書きではなく文章で書いてください。",
    "Abstract を日本語に翻訳してください。",
    """章構成を JSON で出力してください。例:
```json
[
  {
    "title": "Introduction",
    "sub": [
      {
        "title": "Background"
      }
    ]
  }
]
```""",
]
sprompt = "セクション「%s」をサブセクションも含めて要約してください。箇条書きではなく文章で書いてください。"

def summarize_with_gemini(pdf_path):
    """
    Generate a summary using Gemini AI.
    
    Args:
        pdf_path (str): Path to the PDF file
    
    Returns:
        str: Generated summary
    """
    
    pdf_fn = os.path.splitext(pdf_path)[0]
    file = None
    chat_session = None
    result = ""
    i = 0
    sections = []
    try:
        while True:
            i += 1
            if i <= len(prompts):
                prompt = prompts[i - 1]
            elif (j := i - len(prompts) - 1) < len(sections):
                prompt = sprompt % sections[j]["title"]
            else:
                break
            md = f"{pdf_fn}-{i}.md"
            if os.path.exists(md):
                print(f"Skipping existing file: {md}")
                with open(md, "r", encoding="utf-8") as f:
                    text = f.read()
                if i == len(prompts):
                    json_data = text.split("```json")[2].split("```")[0]
                    sections = json.loads(json_data)
            else:
                if not file:
                    file = genai.upload_file(pdf_path, mime_type="application/pdf")
                    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
                plines = prompt.rstrip().split("\n")
                print(f"Prompt {i}: {plines[0]}")
                chat_session = model.start_chat(history=[
                    {"role": "user", "parts": [file]}
                ])
                response = chat_session.send_message(prompt)
                text = f"# Prompt {i}\n\n"
                for line in plines:
                    text += f"> {line}\n"
                text += f"\n{response.text.rstrip()}\n"
                if i == len(prompts):
                    json_data = response.text.split("```json")[1].split("```")[0]
                    sections = json.loads(json_data)
                    text += "\n"
                    def f(sections, indent=0):
                        nonlocal text
                        for section in sections:
                            text += ("  " * indent) + "- " + section["title"] + "\n"
                            if "sub" in section:
                                f(section["sub"], indent + 1)
                    f(sections)
                with open(md, "w", encoding="utf-8") as f:
                    f.write(text)
            if i > 1:
                result += "\n"
            result += text
    except Exception as e:
        print(f"Error generating summary at line {sys.exc_info()[2].tb_lineno}: {e}")
    finally:
        if file:
            genai.delete_file(file.name)
            print(f"Deleted file '{file.display_name}' from: {file.uri}")
    return result, pdf_fn + ".md"

def main():
    """
    Main CLI entry point for paper summarization.
    """
    parser = argparse.ArgumentParser(description='Summarize academic papers using Gemini AI')
    parser.add_argument('pdf_path', help='Path to the PDF file')
    parser.add_argument('-o', '--output', help='Output file for summary')
    args = parser.parse_args()

    summary, output = summarize_with_gemini(args.pdf_path)
    with open(args.output or output, "w", encoding="utf-8") as f:
        f.write(summary)
    print(f"Summary saved: {output}")

if __name__ == '__main__':
    main()
