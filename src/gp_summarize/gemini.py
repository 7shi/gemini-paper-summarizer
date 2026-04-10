import os, re, mimetypes
from google import genai
from llm7shi import gemini as _gemini

TEXT_MIME_EXTENSIONS = {
    ".tex": "text/plain",
}

def generate_content_with_config(model, generation_config, system_instruction, file, prompt, think):
    config = genai.types.GenerateContentConfig(
        system_instruction=system_instruction,
        **generation_config
    )
    response = _gemini.generate_content_retry(
        [file, prompt],
        model=model,
        config=config,
        include_thoughts=think,
        show_params=False,
    )
    rtext = response.text.rstrip() + "\n"

    usage = {}
    if response.chunks:
        chunk_dict = response.chunks[-1].to_json_dict()
        if usage_metadata := chunk_dict.get("usage_metadata"):
            for k, v in usage_metadata.items():
                if isinstance(v, int):
                    usage[k] = v

    return rtext, usage

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
    return _gemini.upload_file(path, get_upload_mime_type(path))

def delete_file(file):
    return _gemini.delete_file(file)
