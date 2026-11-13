"""Build a section module page from src/template.html and src/sN/ content.

Usage: python3 src/build.py 4      -> writes section4.html
Each src/sN/ folder holds: meta.json (title, h1, lede, chips), concepts.html,
learn.html, method.html and data.js (defines T and Q).
"""
import json, os, sys

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(here)

def build(n):
    d = os.path.join(here, f"s{n}")
    meta = json.load(open(os.path.join(d, "meta.json")))
    read = lambda f: open(os.path.join(d, f)).read()
    chips = "\n".join(f'    <span class="chip">{c}</span>' for c in meta["chips"])
    header = (
        '<header class="top wrap">\n'
        f'  <h1>{meta["h1"]}</h1>\n'
        f'  <p class="lede">{meta["lede"]}</p>\n'
        f'  <div class="facts">\n{chips}\n  </div>\n</header>'
    )
    page = open(os.path.join(here, "template.html")).read()
    nq = read("data.js").count("{t:")
    for k, v in {
        "{{TITLE}}": meta["title"], "{{HEADER}}": header,
        "{{CONCEPTS}}": read("concepts.html"), "{{LEARN}}": read("learn.html"),
        "{{METHOD}}": read("method.html"), "{{DATA}}": read("data.js"),
        "{{KEY}}": f"s{n}-ans",
    }.items():
        page = page.replace(k, v)
    page = page.replace("{{NQ}}", str(nq)).replace("{{MIN}}", str(round(nq * 1.5)))
    out = os.path.join(root, f"section{n}.html")
    open(out, "w").write(page)
    print("wrote", out)

for n in sys.argv[1:]:
    build(n)
