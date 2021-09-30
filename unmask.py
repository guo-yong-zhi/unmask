import sys
import os
import re
import nltk
from transformers import BertTokenizer, BertForMaskedLM
import torch

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForMaskedLM.from_pretrained('bert-base-uncased')

def topk_pos(string, words, i, tag, top_k=5):
    tag = [t.upper() for t in tag.split("|")]
    string = string.copy()
    ret = []
    for word in words:
        string[i] = word
        w,t = nltk.pos_tag(string)[i]
        if t in tag:
            ret.append(w)
            top_k -= 1
        if top_k == 0:
            break
    return ret

def unmask(text, ans, top_k=10):
    inputs = tokenizer(text, return_tensors='pt')
    predictions = model(**inputs)[0][0]
    ismask = inputs['input_ids'][0] == tokenizer.mask_token_id
    maskinds = torch.arange(len(predictions))[ismask]
    rts = []
    assert len(ans) == len(maskinds)
    for ind,aa in zip(maskinds, ans):
        if len(aa)>=2 and aa[0]=="[" and aa[-1]=="]":
            sinds = predictions[ind].argsort(descending=True)
            words = (tokenizer.convert_ids_to_tokens(i.item()) for i in sinds)
            string = tokenizer.convert_ids_to_tokens(inputs['input_ids'][0])
            rt = topk_pos(string[1:-1], words, ind-1, aa[1:-1], top_k)
        else:
            rt = tokenizer.convert_ids_to_tokens(predictions[ind].topk(top_k).indices)
        rts.append(rt)
    return rts

import requests
import shutil
def wget(url, filename):
    chunk_size = 1024*1024
    res = requests.get(url, stream=True)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    print("Downloading:", filename)
    with open(filename, "wb") as f:
        for chunk in res.iter_content(chunk_size=chunk_size):
            if chunk:
                f.write(chunk)
    return filename

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    print("nltk.download('punkt')")
    nltk.download('punkt')
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    datapath = nltk.data.path[0]
    url = "https://github.com/guo-yong-zhi/unmask/releases/download/punkt/punkt.zip"
    zipfile = wget(url, os.path.join(datapath, "tokenizers/punkt.zip"))
    shutil.unpack_archive(zipfile, os.path.join(datapath, "tokenizers"))
try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    print("nltk.download('averaged_perceptron_tagger')")
    nltk.download('averaged_perceptron_tagger')
    
def single_mask(s):
    fi = re.finditer(r"[\d_]+([A-Za-z_-]+)|(\[[\w\|\$]+\])", s)
    sentences = []
    ans = []
    b = 0
    for ma in fi:
        sentences.append(s[b:ma.start()])
        g = ma.groups()[0]
        g = ma.groups()[1] if not g else g
        ans.append(g)
        b = ma.end()
    sentences.append(s[b:])
    for i in range(len(ans)):
        r = [sentences[0]]
        for j in range(len(ans)):
            a = "[MASK]" if i == j else ans[j]
            r.append(a)
            r.append(sentences[j+1])
        yield ''.join(r), (ans[i],)
        
def multi_masks(s):
    fi = re.finditer(r"[\d_]+([A-Za-z_-]+)|(\[[\w\|\$]+\])", s)
    sentences = []
    ans = []
    b = 0
    for ma in fi:
        sentences.append(s[b:ma.start()])
        g = ma.groups()[0]
        g = ma.groups()[1] if not g else g
        ans.append(g)
        b = ma.end()
    sentences.append(s[b:])
    r = [sentences[0]]
    if ans:
        for j in range(len(ans)):
            r.append("[MASK]")
            r.append(sentences[j+1])
        yield ''.join(r), ans

def gen_mask_sentences(s, single=False):
    if single:
        yield from single_mask(s)
    else:
        yield from multi_masks(s)

def umaskall_sentences(sentences, top_k=50, single_mask=False, io=sys.stdout):
    for i,s in enumerate(sentences):
        for Q, A in gen_mask_sentences(s, single=single_mask):
            if len(Q) and (Q[-1].isalpha() or Q[-1] == "]"):
                Q = Q + "."
            print("="*20, i+1, "="*20, file=io)
            print(Q, file=io)
            um = unmask(Q, A, top_k=top_k)
            assert len(um) == len(A)
            for candi, ans in zip(um, A):
                ans = ans.strip("_")
                aa = ans.lower()
                if aa.isalpha():
                    sign = "✔" if aa in candi else "✘"
                else:
                    sign = "☐"
                print(sign, candi.index(aa)+1 if aa in candi else "", ans, file=io)
                print("●", ", ".join(candi), file=io)


def umaskall(text, split_stences=True, **kargs):
    if split_stences:
        sentences = nltk.tokenize.sent_tokenize(text)
    else:
        sentences = text.splitlines()
    sentences = [s.strip() for s in sentences if s]
    return umaskall_sentences(sentences, **kargs)