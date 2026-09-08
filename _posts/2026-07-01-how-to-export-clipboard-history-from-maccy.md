---
title: "How to export clipboard history from Maccy on macOS"
date: 2026-07-01T09:00:00+0200
lastmod: 2026-07-01T09:00:00+0200
draft: false
description: "A robust bash script that exports text and image entries from Maccy's SQLite clipboard database on macOS, converting TIFF images to PNG for a compact archive."
image: "https://images.unsplash.com/photo-1587620962725-abab7fe55159?w=800&h=420&fit=crop"
author: "Jan Toth"
tags: ["macos", "maccy", "clipboard", "sqlite", "bash"]
categories: ["macOS"]
---

[Maccy](https://maccy.app/) is a lightweight open-source clipboard manager for macOS that keeps a searchable history of everything you copy. Under the hood it persists that history in a Core Data SQLite database, which means you can query it directly with `sqlite3` and pull out both text snippets and screenshots you've captured over the day.

The script below reads the last **N** entries from Maccy's database, writes text entries to a single file, extracts image entries as TIFFs, and then re-encodes them as PNGs with `sips` so the resulting archive is small enough to attach to a ticket, a blog post, or your own notes.

> The database sits inside Maccy's sandboxed container. It is only readable while Maccy is not actively writing to it — if you hit a `database is locked` error, quit Maccy briefly and re-run the script.
{: .prompt-info }

## The script

Save this as `maccy-export.sh` and `chmod +x maccy-export.sh`:

```bash
#!/bin/bash
# maccy-export.sh — Export clipboard history from Maccy (text + images)
# Usage: maccy-export.sh [entries] [output_dir]
#   entries    — number of recent clipboard entries to export (default: 30)
#   output_dir — where to save files (default: /tmp/maccy_export_YYYY-MM-DD)

set -euo pipefail

ENTRIES="${1:-30}"
TODAY=$(date +%Y-%m-%d)
OUTPUT_DIR="${2:-/tmp/maccy_export_${TODAY}}"
DB="$HOME/Library/Containers/org.p0deje.Maccy/Data/Library/Application Support/Maccy/Storage.sqlite"

if [ ! -f "$DB" ]; then
  echo "❌ Maccy database not found at: $DB"
  exit 1
fi

mkdir -p "$OUTPUT_DIR"

echo "📋 Exporting last $ENTRIES clipboard entries to: $OUTPUT_DIR"
echo "---"

# Export text entries
TEXT_COUNT=$(sqlite3 "$DB" \
"SELECT COUNT(*) FROM (
  SELECT i.Z_PK FROM ZHISTORYITEM i
  JOIN ZHISTORYITEMCONTENT c ON c.ZITEM = i.Z_PK
  WHERE c.ZTYPE = 'public.utf8-plain-text'
  ORDER BY i.ZLASTCOPIEDAT DESC LIMIT $ENTRIES
);")

sqlite3 "$DB" \
"SELECT '--- Entry ' || i.Z_PK || ' ---' || CHAR(10) || c.ZVALUE || CHAR(10)
FROM ZHISTORYITEM i
JOIN ZHISTORYITEMCONTENT c ON c.ZITEM = i.Z_PK
WHERE c.ZTYPE = 'public.utf8-plain-text'
ORDER BY i.ZLASTCOPIEDAT DESC LIMIT $ENTRIES;" > "$OUTPUT_DIR/clipboard_text.txt"

echo "📝 Exported $TEXT_COUNT text entries → clipboard_text.txt"

# Export images (TIFF from clipboard → convert to PNG)
IMG_COUNT=$(sqlite3 "$DB" \
"SELECT COUNT(*) FROM (
  SELECT i.Z_PK FROM ZHISTORYITEM i
  JOIN ZHISTORYITEMCONTENT c ON c.ZITEM = i.Z_PK
  WHERE c.ZTYPE = 'public.tiff'
  ORDER BY i.ZLASTCOPIEDAT DESC LIMIT $ENTRIES
);")

if [ "$IMG_COUNT" -gt 0 ]; then
  sqlite3 "$DB" \
  "SELECT writefile('$OUTPUT_DIR/img_' || i.Z_PK || '.tiff', c.ZVALUE)
  FROM ZHISTORYITEM i
  JOIN ZHISTORYITEMCONTENT c ON c.ZITEM = i.Z_PK
  WHERE c.ZTYPE = 'public.tiff'
  ORDER BY i.ZLASTCOPIEDAT DESC LIMIT $ENTRIES;"

  # Convert TIFF to PNG (much smaller) and remove TIFFs
  for f in "$OUTPUT_DIR"/img_*.tiff; do
    sips -s format png "$f" --out "${f%.tiff}.png" >/dev/null 2>&1
    rm "$f"
  done

  echo "🖼️  Exported $IMG_COUNT images → img_*.png"
else
  echo "🖼️  No images found in last $ENTRIES entries"
fi

echo "---"
echo "✅ Done! Output: $OUTPUT_DIR"
du -sh "$OUTPUT_DIR"
```

## How it works, step by step

### 1. Strict mode and CLI arguments

```bash
set -euo pipefail
ENTRIES="${1:-30}"
OUTPUT_DIR="${2:-/tmp/maccy_export_${TODAY}}"
```

- `set -e` aborts on the first failing command, `-u` treats unset variables as errors, and `-o pipefail` propagates failures through pipelines. Together they turn silent bugs into loud, early exits.
- Both arguments are optional and use the `${var:-default}` idiom, so `./maccy-export.sh` with no arguments still works — it exports the last 30 entries to `/tmp/maccy_export_2026-07-01/`.

### 2. Locating the Maccy database

```bash
DB="$HOME/Library/Containers/org.p0deje.Maccy/Data/Library/Application Support/Maccy/Storage.sqlite"
```

Maccy is a sandboxed app, so its data lives under `~/Library/Containers/org.p0deje.Maccy/…` rather than the standard `~/Library/Application Support/` path. The `if [ ! -f "$DB" ]` guard prints a friendly error if the file is missing (Maccy uninstalled, moved, or renamed) instead of blowing up mid-query.

### 3. The Core Data schema

Maccy's Core Data model produces two tables the script cares about:

- **`ZHISTORYITEM`** — one row per clipboard event, with `ZLASTCOPIEDAT` (a Core Data timestamp) as the recency signal and `Z_PK` as the primary key.
- **`ZHISTORYITEMCONTENT`** — the actual payload, keyed by `ZITEM` back to `ZHISTORYITEM.Z_PK`. `ZTYPE` holds the UTI (Uniform Type Identifier), and `ZVALUE` is the raw bytes.

The two UTIs the script filters on are:

| UTI | What it is |
| --- | --- |
| `public.utf8-plain-text` | Plain text copied from any app |
| `public.tiff` | Bitmap screenshots and images |

### 4. Exporting text entries

```sql
SELECT '--- Entry ' || i.Z_PK || ' ---' || CHAR(10) || c.ZVALUE || CHAR(10)
FROM ZHISTORYITEM i
JOIN ZHISTORYITEMCONTENT c ON c.ZITEM = i.Z_PK
WHERE c.ZTYPE = 'public.utf8-plain-text'
ORDER BY i.ZLASTCOPIEDAT DESC LIMIT $ENTRIES;
```

The `||` operator is SQLite's string concatenation. `CHAR(10)` is a newline, so each entry is printed as:

```text
--- Entry 4711 ---
<the copied text>
```

The output is redirected to `clipboard_text.txt` in the output directory. A separate `COUNT(*)` query populates `TEXT_COUNT` so the summary line is accurate even when the query returns no rows.

### 5. Exporting images with `writefile`

SQLite ships with a [`writefile(path, blob)`](https://sqlite.org/cli.html#file_i_o_functions) function that writes a BLOB column straight to disk. The script uses it to dump each TIFF payload:

```sql
SELECT writefile('$OUTPUT_DIR/img_' || i.Z_PK || '.tiff', c.ZVALUE)
FROM ZHISTORYITEM i
JOIN ZHISTORYITEMCONTENT c ON c.ZITEM = i.Z_PK
WHERE c.ZTYPE = 'public.tiff'
ORDER BY i.ZLASTCOPIEDAT DESC LIMIT $ENTRIES;
```

The filename embeds `Z_PK` so entries never collide. The `if [ "$IMG_COUNT" -gt 0 ]` guard skips the whole TIFF branch when there are no images — otherwise the `for f in *.tiff` loop below would iterate over the literal glob string and fail.

### 6. Shrinking TIFFs to PNGs with `sips`

macOS ships [`sips`](https://ss64.com/mac/sips.html) (Scriptable Image Processing System), so no extra dependency is needed:

```bash
for f in "$OUTPUT_DIR"/img_*.tiff; do
  sips -s format png "$f" --out "${f%.tiff}.png" >/dev/null 2>&1
  rm "$f"
done
```

TIFFs from the clipboard are uncompressed and can easily hit tens of megabytes each. Re-encoding to PNG shrinks a typical Retina screenshot by roughly 10× while staying lossless. The `${f%.tiff}.png` pattern is bash parameter expansion — it strips the `.tiff` suffix so `img_4711.tiff` becomes `img_4711.png`.

### 7. Summary line

`du -sh "$OUTPUT_DIR"` at the end prints the total size of the export, which is a handy sanity check before you attach the folder to an email or upload it somewhere.

## Usage examples

```bash
# Defaults: last 30 entries to /tmp/maccy_export_2026-07-01/
./maccy-export.sh

# Grab the last 100 entries
./maccy-export.sh 100

# Send everything to a custom directory
./maccy-export.sh 50 ~/Desktop/clipboard-dump
```

Sample output:

```text
📋 Exporting last 30 clipboard entries to: /tmp/maccy_export_2026-07-01
---
📝 Exported 24 text entries → clipboard_text.txt
🖼️  Exported 6 images → img_*.png
---
✅ Done! Output: /tmp/maccy_export_2026-07-01
1.8M	/tmp/maccy_export_2026-07-01
```

## Why this is useful

- **Daily journal** — pipe the text file into your notes app to reconstruct what you were working on.
- **Screenshot archive** — quickly extract every screenshot you took today without hunting through `~/Desktop`.
- **Debugging** — when a colleague asks "what did you actually copy into that form?", you can hand them the exact bytes.
- **Backups** — Maccy has an internal retention limit; this script lets you snapshot the history before it rotates out.

> The exported files are readable by anyone with access to your filesystem. If your clipboard history contains passwords, tokens or personal data, move the output directory into an encrypted volume or delete it as soon as you're done.
{: .prompt-warning }
