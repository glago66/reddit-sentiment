import json
import zstandard as zstd

# -------------------------------------------------------
# WHAT THIS DOES:
# Opens the .zst file, reads just the first 5 lines,
# and prints them so we can see what fields exist
# before we write any filtering logic.
# This is like doing df.head() in pandas.
# -------------------------------------------------------

FILE = "data/raw/RC_2025-12.zst"
LINES_TO_PREVIEW = 5

def peek(filepath, n):
    with open(filepath, "rb") as f:
        # Create a decompressor — think of this as a zip opener
        dctx = zstd.ZstdDecompressor(max_window_size=2**31)
        stream = dctx.stream_reader(f)
        buffer = ""
        count = 0
        while count < n:
            chunk = stream.read(65536).decode("utf-8", errors="ignore")
            if not chunk:
                break
            buffer += chunk
            lines = buffer.split("\n")
            buffer = lines[-1]
            for line in lines[:-1]:
                if line.strip():
                    data = json.loads(line)
                    print(f"\n--- Record {count + 1} ---")
                    # Print every field name and its value
                    for key, value in data.items():
                        print(f"  {key}: {value}")
                    count += 1
                    if count >= n:
                        break

peek(FILE, LINES_TO_PREVIEW)