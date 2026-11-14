"""Cross-validated comparison of small-lexicon wordlikeness scores (track 7a).
Deterministic (fixed seed). Reads canon-phonotactics.json and reuses the
segmentation of tools/analysis/phonotactics.py. Writes nothing."""
import importlib.util, json, math, random, sys, collections
ROOT = sys.argv[1]
spec = importlib.util.spec_from_file_location("ph", ROOT + "/tools/analysis/phonotactics.py")
ph = importlib.util.module_from_spec(spec); spec.loader.exec_module(ph)
d = json.load(open(ROOT + "/research/data/canon-phonotactics.json"))
allw = set(d["syllabification_of_lexicon"]); comp = set(d["mechanically_decomposable_words"])
words = sorted(allw - comp)
seg = {w: [u for u, _ in ph.units(w)] for w in words}
cls = {w: ph.units(w) for w in words}
INV = sorted({u for w in words for u in seg[w]}); V = len(INV) + 1
rng = random.Random(20261114)
order = words[:]; rng.shuffle(order)
K = 10
folds = [order[i::K] for i in range(K)]
B = "#"

def train(ws):
    uni = collections.Counter(); bi = collections.Counter(); tri = collections.Counter()
    ctx = collections.Counter(); ctx2 = collections.Counter()
    fol = collections.defaultdict(set); fol2 = collections.defaultdict(set)
    posu = collections.Counter(); posn = collections.Counter(); posb = collections.Counter(); posbn = collections.Counter()
    for w in ws:
        s = [B] + seg[w] + [B]
        for i in range(1, len(s)):
            uni[s[i]] += 1; bi[(s[i-1], s[i])] += 1; ctx[s[i-1]] += 1; fol[s[i-1]].add(s[i])
            if i >= 2:
                tri[(s[i-2], s[i-1], s[i])] += 1; ctx2[(s[i-2], s[i-1])] += 1; fol2[(s[i-2], s[i-1])].add(s[i])
        u = seg[w]
        for i, x in enumerate(u):
            posu[(i, x)] += 1; posn[i] += 1
            if i + 1 < len(u): posb[(i, x, u[i+1])] += 1; posbn[i] += 1
    return dict(uni=uni, bi=bi, tri=tri, ctx=ctx, ctx2=ctx2, fol=fol, fol2=fol2, N=sum(uni.values()),
                posu=posu, posn=posn, posb=posb, posbn=posbn, ws=set(ws),
                segs=[tuple(seg[w]) for w in ws])

def p_uni(m, x): return (m["uni"][x] + 1.0) / (m["N"] + V)
def p_addk(m, a, x, k): return (m["bi"][(a, x)] + k) / (m["ctx"][a] + k * V)
def p_jm(m, a, x, lam):
    c = m["ctx"][a]
    return p_uni(m, x) if c == 0 else lam * m["bi"][(a, x)] / c + (1 - lam) * p_uni(m, x)
def p_wb(m, a, x):
    c = m["ctx"][a]; t = len(m["fol"][a])
    if c == 0: return p_uni(m, x)
    lam = c / (c + t); return lam * m["bi"][(a, x)] / c + (1 - lam) * p_uni(m, x)
def p_wb3(m, a2, a, x):
    c = m["ctx2"][(a2, a)]; t = len(m["fol2"][(a2, a)])
    if c == 0: return p_wb(m, a, x)
    lam = c / (c + t); return lam * m["tri"][(a2, a, x)] / c + (1 - lam) * p_wb(m, a, x)

def edit1(a, b):
    la, lb = len(a), len(b)
    if abs(la - lb) > 1 or a == b: return False
    if la == lb: return sum(x != y for x, y in zip(a, b)) == 1
    if la > lb: a, b, la, lb = b, a, lb, la
    i = 0
    while i < la and a[i] == b[i]: i += 1
    return a[i:] == b[i+1:]

def scores(m, u):
    s = [B] + list(u) + [B]; n = len(s) - 1
    out = {}
    out["unigram"] = sum(math.log2(p_uni(m, x)) for x in s[1:]) / n
    for k in (0.01, 0.1, 0.5, 1.0):
        out["bigram add-%g" % k] = sum(math.log2(p_addk(m, s[i-1], s[i], k)) for i in range(1, len(s))) / n
    out["bigram add-0.5 SUM (not length-normalised)"] = out["bigram add-0.5"] * n
    for lam in (0.5, 0.7, 0.9):
        out["bigram JM lam=%g" % lam] = sum(math.log2(p_jm(m, s[i-1], s[i], lam)) for i in range(1, len(s))) / n
    out["bigram Witten-Bell"] = sum(math.log2(p_wb(m, s[i-1], s[i])) for i in range(1, len(s))) / n
    s3 = [B] + s
    out["trigram Witten-Bell"] = sum(math.log2(p_wb3(m, s3[i-2], s3[i-1], s3[i])) for i in range(2, len(s3))) / n
    out["min transition (WB bigram)"] = min(math.log2(p_wb(m, s[i-1], s[i])) for i in range(1, len(s)))
    pu = [m["posu"][(i, x)] / m["posn"][i] if m["posn"][i] else 0.0 for i, x in enumerate(u)]
    pb = [m["posb"][(i, u[i], u[i+1])] / m["posbn"][i] if m["posbn"][i] else 0.0 for i in range(len(u) - 1)]
    out["positional (Vitevitch-Luce style, mean)"] = sum(pu) / len(pu) + (sum(pb) / len(pb) if pb else 0.0)
    unseen = sum(1 for i in range(1, len(s)) if m["bi"][(s[i-1], s[i])] == 0)
    out["categorical: -(unseen bigrams)"] = -unseen
    tu = tuple(u)
    nd = sum(1 for t in m["segs"] if edit1(tu, t))
    out["neighbourhood density (edit-1 count)"] = nd
    out["WB bigram + 0.25*log2(1+density)"] = out["bigram Witten-Bell"] + 0.25 * math.log2(1 + nd)
    return out, unseen

def auc(pos, neg):
    g = 0.0
    for p in pos:
        for q in neg:
            g += 1.0 if p > q else 0.5 if p == q else 0.0
    return g / (len(pos) * len(neg))

def run(train_size=None, label="full"):
    P = collections.defaultdict(list); N1 = collections.defaultdict(list); N2 = collections.defaultdict(list)
    unseenP = []; unseenN1 = []
    hardP = hardN1 = hardN2 = 0; nP = nN1 = nN2 = 0
    r = random.Random(7)
    for f in range(K):
        test = folds[f]; tr = [w for g in range(K) if g != f for w in folds[g]]
        if train_size: tr = tr[:train_size]
        m = train(tr)
        on = {ph.edge_clusters(cls[w])[0] for w in tr}; co = {ph.edge_clusters(cls[w])[2] for w in tr}
        def hard(u):
            us = ph.units("".join(u)); a, _, c = ph.edge_clusters(us)
            return a in on and c in co and any(ph.is_vowel(k) for _, k in us)
        for w in test:
            u = seg[w]; sc, un = scores(m, u)
            for k, v in sc.items(): P[k].append(v)
            unseenP.append(un); nP += 1; hardP += hard(u)
            for _ in range(3):
                x = u[:]; r.shuffle(x)
                if x == u or "".join(x) in allw: continue
                sc2, un2 = scores(m, x)
                for k, v in sc2.items(): N1[k].append(v)
                unseenN1.append(un2); nN1 += 1; hardN1 += hard(x)
            x = [r.choice(INV) for _ in u]
            sc3, _ = scores(m, x)
            for k, v in sc3.items(): N2[k].append(v)
            nN2 += 1; hardN2 += hard(x)
    print("== %s: %d held-out canon roots, %d unit-shuffles, %d uniform-random strings" % (label, nP, nN1, nN2))
    for k in P:
        print("  %-46s AUC vs shuffle %.3f   vs random %.3f" % (k, auc(P[k], N1[k]), auc(P[k], N2[k])))
    print("  held-out canon with >=1 unseen bigram: %.3f ; shuffles with 0 unseen bigrams: %.3f" % (
        sum(1 for x in unseenP if x) / nP, sum(1 for x in unseenN1 if x == 0) / nN1))
    print("  hard edge filter (initial onset and final coda attested in training fold): pass canon %.3f, shuffle %.3f, random %.3f" % (
        hardP / nP, hardN1 / nN1, hardN2 / nN2))
    for key in ("bigram Witten-Bell", "bigram add-0.5"):
        sp = sorted(P[key]); thr = sp[int(0.05 * len(sp))]
        print("  %s: threshold at 5th pct of held-out canon (%.2f) lets through %.3f of shuffles, %.3f of random" % (
            key, thr, sum(1 for x in N1[key] if x >= thr) / len(N1[key]), sum(1 for x in N2[key] if x >= thr) / len(N2[key])))

print("training roots:", len(words), "| unit inventory:", len(INV))
run()
for n in (100, 200, 400):
    run(n, "train size %d" % n)
