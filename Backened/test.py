import json
import os

# paths
FAISS_IDS = "faiss_id_mapping.json"
SUMMARY = "id_to_summary.json"
FULLTEXT = "id_to_fulltext.json"

with open(FAISS_IDS, "r") as f:
    faiss_ids = json.load(f)

with open(SUMMARY, "r") as f:
    id_to_summary = json.load(f)

with open(FULLTEXT, "r") as f:
    id_to_fulltext = json.load(f)

print("len(faiss_ids) =", len(faiss_ids))
print("len(id_to_summary) =", len(id_to_summary))
print("len(id_to_fulltext) =", len(id_to_fulltext))

print("\nFirst 10 FAISS ids:", faiss_ids[:10])

# Check first 5 returned ids from your example (replace with actual)
for i, doc_id in enumerate(faiss_ids[:5], start=1):
    print(f"\n[{i}] id: {doc_id}")
    print("  in summary keys?:", doc_id in id_to_summary)
    if doc_id in id_to_summary:
        s = id_to_summary[doc_id]
        print("  len(summary):", len(s))
        print("  sample summary snippet:", repr(s[:200]))
    print("  in fulltext keys?:", doc_id in id_to_fulltext)
    if doc_id in id_to_fulltext:
        t = id_to_fulltext[doc_id]
        print("  len(fulltext):", len(t))
        print("  sample fulltext snippet:", repr(t[:200]))
