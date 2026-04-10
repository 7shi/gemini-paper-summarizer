import sys, os, time, re, mimetypes
from google import genai

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

TEXT_MIME_EXTENSIONS = {
    ".tex": "text/plain",
}

def generate_content(model, config, *contents):
    # Get the response
    rtext, chunk = generate_content_retry(model, config, contents)
    if not rtext.endswith("\n"):
        print(flush=True)
    rtext = rtext.rstrip() + "\n"

    # Get the statistics
    chunk_dict = chunk.to_json_dict()
    usage = {}
    if usage_metadata := chunk_dict.get("usage_metadata"):
        for k, v in usage_metadata.items():
            if isinstance(v, int):
                usage[k] = v

    return rtext, usage

def generate_content_with_config(model, generation_config, system_instruction, file, prompt, think):
    thinking_config = genai.types.ThinkingConfig(include_thoughts=think)
    config = genai.types.GenerateContentConfig(
        system_instruction=system_instruction,
        thinking_config=thinking_config,
        **generation_config
    )
    return generate_content(model, config, file, prompt)

def generate_content_retry(model, config, contents):
    for _ in range(5):
        try:
            response = client.models.generate_content_stream(
                model=model,
                config=config,
                contents=list(contents),
            )
            rtext = ""
            thoughts_shown = False
            answer_shown = False
            chunk = None
            for chunk in response:
                if (hasattr(chunk, "candidates") and chunk.candidates
                        and chunk.candidates[0].content
                        and chunk.candidates[0].content.parts):
                    for part in chunk.candidates[0].content.parts:
                        if not part.text:
                            continue
                        elif part.thought:
                            if not thoughts_shown:
                                print("\n[Thinking]", flush=True)
                                thoughts_shown = True
                            print(part.text, end="", flush=True)
                        else:
                            if thoughts_shown and not answer_shown:
                                print("\n[Answer]", flush=True)
                                answer_shown = True
                            print(part.text, end="", flush=True)
                            rtext += part.text
                elif chunk.text:
                    print(chunk.text, end="", flush=True)
                    rtext += chunk.text
            return rtext, chunk
        except genai.errors.APIError as e:
            if hasattr(e, "code") and e.code in [429, 500, 503]:
                print(e, file=sys.stderr)
                delay = 15
                if e.code == 429:
                    details = getattr(e, "details", {}).get("error", {}).get("details", [])
                    rd = None
                    for d in details:
                        if "retryDelay" in d:
                            rd = d["retryDelay"]
                            break
                    if rd and (m := re.match(r"^(\d+)s$", rd)):
                        delay = int(m.group(1)) or delay
                for i in range(delay, -1, -1):
                    print(f"\rRetrying... {i}s ", end="", file=sys.stderr, flush=True)
                    time.sleep(1)
                print(file=sys.stderr)
                continue
            else:
                raise
    raise RuntimeError("Max retries exceeded.")

def get_kv(line):
    if m := re.match(r"^([a-zA-Z_]+): (.*)$", line):
        k, v = m.group(1), m.group(2)
        if v.isdigit():
            return k, int(v)
        return k, v
    else:
        return None, None

def update_stats(st, k, v):
    if not k:
        return
    st.setdefault(k, 0)
    if not k.endswith("_rate"):
        st[k] += v

def iter_stats(st):
    keys = [
        "cached_content_token_count",
        "prompt_token_count",
        "thoughts_token_count",
        "candidates_token_count",
        "total_token_count",
    ]
    st_keys = list(st.keys())
    for k in keys:
        if k in st:
            yield k, st[k]
            st_keys.remove(k)
    for k in st_keys:
        yield k, st[k]

def show_stats(st, prefix=""):
    if not st:
        return
    maxlen = max(len(k) for k in st)
    for k, v in iter_stats(st):
        print(f"{prefix}{k.ljust(maxlen)}: {v}")

def get_upload_mime_type(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in TEXT_MIME_EXTENSIONS:
        return TEXT_MIME_EXTENSIONS[ext]
    return mimetypes.guess_type(path)[0] or "text/plain"

def upload_file(path):
    file = client.files.upload(
        file=path,
        config=genai.types.UploadFileConfig(
            display_name=os.path.basename(path),
            mime_type=get_upload_mime_type(path),
        ),
    )
    while file.state.name == "PROCESSING":
        print("Waiting for file to be processed.")
        time.sleep(2)
        file = client.files.get(name=file.name)
    return file

def delete_file(file):
    return client.files.delete(name=file.name)
