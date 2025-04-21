import sys, os, time, re
from datetime import timedelta
from google import genai

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def generate_content(model, config, *contents):
    # Get the response
    time1, time2, time3, rtext, chunk = generate_content_retry(model, config, contents)
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
        usage["prompt_eval_duration"    ] = int((time2 - time1) * 1000)  # in ms
        usage["candidates_eval_duration"] = int((time3 - time2) * 1000)  # in ms
        set_stats(usage)

    return rtext, usage

def generate_content_retry(model, config, contents):
    for _ in range(5):
        try:
            time1 = time.monotonic()
            response = client.models.generate_content_stream(
                model=model,
                config=config,
                contents=contents,
            )
            time2 = None
            rtext = ""
            for chunk in response:
                if not time2:
                    time2 = time.monotonic()
                if chunk.text:
                    print(chunk.text, end="", flush=True)
                    rtext += chunk.text
            time3 = time.monotonic()
            return time1, time2, time3, rtext, chunk
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

def set_stats(st):
    dur1 = st.get("prompt_eval_duration"    , 0)
    dur2 = st.get("candidates_eval_duration", 0)
    if dur1 < 1 or dur2 < 1:
        return
    st["prompt_eval_rate"    ] = f'{st["prompt_token_count"    ] / (dur1 / 1000):.2f} tps'
    st["candidates_eval_rate"] = f'{st["candidates_token_count"] / (dur2 / 1000):.2f} tps'

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
        "prompt_eval_duration",
        "prompt_eval_rate",
        "candidates_token_count",
        "candidates_eval_duration",
        "candidates_eval_rate",
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
        w = timedelta(milliseconds=v) if k.endswith("_duration") else v
        print(f"{prefix}{k.ljust(maxlen)}: {w}")
