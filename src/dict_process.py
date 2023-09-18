import re
import json
def dump_dict(d, fn):
    with open(fn, "w", encoding="utf-8") as f:
        for k, v in d.items():
            f.write(json.dumps({k:v}, ensure_ascii=False) + "\n")

def load_dict(f):
    d = {}
    with open(f, "r", encoding="utf-8") as f:
        for line in f:
            d.update(json.loads(line))
    return d

def get_rev_dicts(Dictionary):
    RevDicts = {}
    for k,v in Dictionary.items():
        for l in v:
            nt = tuple(l[3].split("    "))
            nt = tuple(i.strip() for i in nt)
            RevDicts.setdefault(normalize_name(nt), set()).add(k)
    return RevDicts

def get_series_list(RevDicts):
    Books = set((i[0] for i in RevDicts))
    Series = set((extract_series_name(b) for b in Books))
    return Series

def normalize_name(n):
    n = list(n)
    while len(n) < 4:
        n.append("")
    assert len(n) == 4
    n2 = n[2].lower()
    for term in ["lesson", "topic", "unit", "module", ]:
        if term + "s" in n2:
            term = term + "s"
        n2 = n2.replace(term, term + " ")
    n2 = n2.replace("  ", " ").strip()
    n[2] = n2
    return tuple(n)
    
def reorder(nm):
    for t in ["lesson", "topic", "unit", "module", ]:
        if t in nm:
            i = nm.find(t)
            nm = " ".join([nm[i:].strip(), nm[:i].strip()]).strip()
    return nm

def extract_series_name(b):
    b = re.sub(r"[(（].*[)）]", "", b)
    b = re.sub(r"第.*版", "", b)
    b = re.sub(r"[\d\-]+年*[.*月]*版*", "", b)
    return b.strip().strip("版")

def sort_key(n):
    od = {"小":0, "初":1, "高":2, "选":3}
    n = [i.strip() for i in n]
    n = [i if i else "Z"*7 for i in n]
    n[1] = n[1].replace("starter", "0") 
    n[2] = reorder(n[2])
    n[2] = n[2].replace("units", "unit") 
    n[2] = re.sub("unit.*[-/]", "unit ", n[2]).strip()
    n[2] = n[2].replace("welcome", "0") 
    n[2] = n[2].replace("starter", "0") 
    n[2] = n[2].replace("learning to learn", "0")
    n[2] = n[2].replace("review of", "T"*7)
    n[2] = n[2].replace("topic", "R"*7)
    n[2] = n[2].replace("reading", "Q"*7)
    n[2] = n[2].replace("writing", "P"*7)
    ln2 = len(n[2])
    for t in ["lesson", "topic", "unit", "module", ]:
        n[2] = n[2].replace(t, "")
    n[2] = n[2].replace("  ", " ").strip()
    n1sp = n[1].split("-")
    while len(n1sp) < 2:
        n1sp.append("999")
    n2sp = n[2].split()
    while len(n2sp) < 4:
        n2sp.append("S"*7)
    return (od.get(n[1][0] if n[1] else "", 100), [(len(i),i) for i in n1sp], [(len(i),i) for i in n2sp],-ln2, n[3],  n)

def get_sorted_kept_names(RevDicts, kept_series):
    kept_names = [n for n in RevDicts if extract_series_name(n[0]) in kept_series]
    sorted_names = sorted(kept_names, key=sort_key)
    return sorted_names

def get_levels(sorted_names):
    seen = set()
    levels = []
    for n in sorted_names:
        nl = n[1:3]
        if nl not in seen:
            seen.add(nl)
            levels.append(nl)
    L1 = []
    L2s = {}
    for l1, l2 in levels:
        if (not L1) or l1 != L1[-1]:
            L1.append(l1)
        L2 = L2s.setdefault(l1, [])
        if (not L2) or l2 != L2[-1]:
            L2.append(l2)
    return L1, L2s

def find_level_index(sorted_names, level_begin, level_end):
    begin_index = None
    end_index = None
    for i, n in enumerate(sorted_names):
        if begin_index is None and n[1:3] == level_begin:
            begin_index = i
        if n[1:3] == level_end:
            end_index = i
    return begin_index, end_index

def get_filtered_names(sorted_names, level_begin, level_end):
    begin_index, end_index = find_level_index(sorted_names, level_begin, level_end)
    return sorted_names[begin_index:end_index]

def get_filtered_vocabulary(RevDicts, sorted_names, level_begin, level_end):
    filtered_names = get_filtered_names(sorted_names, level_begin, level_end)
    if filtered_names:
        return set.union(*[RevDicts[n] for n in filtered_names])
    else:
        return set()

