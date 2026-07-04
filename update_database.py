import json
import re
import urllib.request
import urllib.parse

SHEET_ID = "1DIlSqvPTcDX87VH5rIcynmBSbMqPBxNsAhSoe-65EbY"
SHEET_NAME = "List Lagu Raw"
API_KEY = "AIzaSyCd0o1M6jJjd4LZwYJ_Rl9LhEsJBFrrKtY"

encoded_sheet = urllib.parse.quote(SHEET_NAME)
sheet_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:json&tq&sheet={encoded_sheet}"
req = urllib.request.Request(sheet_url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as response:
    raw_sheet_text = response.read().decode("utf-8")

json_str = raw_sheet_text[raw_sheet_text.find("{") : raw_sheet_text.rfind("}") + 1]
sheet_data = json.loads(json_str)
database = []
visited_doc_ids = set()

for row_index, row in enumerate(sheet_data["table"]["rows"]):
    try:
        if not row or "c" not in row or len(row["c"]) <= 4 or row["c"][4] is None:
            continue

        doc_url = row["c"][4]["v"]
        if not doc_url:
            continue

        doc_id_match = re.search(r"/d/([a-zA-Z0-9-_]+)", doc_url)
        if not doc_id_match:
            continue
        doc_id = doc_id_match.group(1)

        if doc_id in visited_doc_ids:
            continue

        visited_doc_ids.add(doc_id)
        print(f"Processing row {row_index + 1}: Fetching Doc ID {doc_id}...")
        drive_url = f"https://www.googleapis.com/drive/v3/files/{doc_id}/export?mimeType=text/plain&key={API_KEY}"
        with urllib.request.urlopen(drive_url) as response:
            raw_doc_text = response.read().decode("utf-8")
        raw_doc_text = raw_doc_text.replace('\ufeff', '')

        song_blocks = re.split(r"\r?\n(?=\d+\.\s)", raw_doc_text)

        for block in song_blocks:
            if not block.strip():
                continue

            lines = block.strip().splitlines()
            if not lines:
                continue

            first_line = lines[0]

            titleKey = re.sub(r"^\s*\d+\.\s*", "", first_line).strip()
            title = re.sub(r"\s*\([A-G]#?m?\)\s*$", "", titleKey).strip()
            raw_sheet = "\n".join(lines[1:]).strip()
            sheet = re.sub(r"\n{3,}", "\n\n", raw_sheet)

            database.append({"title": title, "sheet": sheet})

    except Exception as e:
        print(f"error: processing row {row_index + 1}: {e}")
        continue

with open("database.json", "w", encoding="utf-8") as f:
    json.dump(database, f, ensure_ascii=False, indent=2)

print("Database updated")