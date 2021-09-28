import sys
import re
import nltk
from transformers import BertTokenizer, BertForMaskedLM
import torch

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForMaskedLM.from_pretrained('bert-base-uncased')

def unmask(text, top_k=10):
    inputs = tokenizer(text, return_tensors='pt')
    predictions = model(**inputs)
    ismask = inputs['input_ids'][0] == tokenizer.mask_token_id
    predicted_indexes = torch.topk(predictions[0][0][ismask], k=top_k, dim=1).indices
    predicted_tokens = [tokenizer.convert_ids_to_tokens(i) for i in predicted_indexes]
    return predicted_tokens

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

def single_mask(s):
    fi = re.finditer(r"[\d_]+([A-Za-z_-]+)", s)
    sentences = []
    ans = []
    b = 0
    for ma in fi:
        sentences.append(s[b:ma.start()])
        ans.append(ma.groups()[0])
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
    fi = re.finditer(r"[\d_]+([A-Za-z_-]+)", s)
    sentences = []
    ans = []
    b = 0
    for ma in fi:
        sentences.append(s[b:ma.start()])
        ans.append(ma.groups()[0])
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
            print("="*20, i+1, "="*20, file=io)
            print(Q, file=io)
            um = unmask(Q, top_k=top_k)
            assert len(um) == len(A)
            for candi, ans in zip(um, A):
                aa = ans.lower()
                print("✔" if aa in candi else "✘", candi.index(aa)+1 if aa in candi else "", ans, file=io)
                print("●", ", ".join(candi), file=io)


def umaskall(text, split_stences=True, **kargs):
    if split_stences:
        sentences = nltk.tokenize.sent_tokenize(text)
    else:
        sentences = text.splitlines()
    sentences = [s.strip() for s in sentences if s]
    return umaskall_sentences(sentences, **kargs)