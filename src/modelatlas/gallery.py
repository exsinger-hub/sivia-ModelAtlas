"""Portable, self-contained HTML preview built from actual render bundles."""
import base64
import html
from pathlib import Path


def gallery(runs, output):
    cards=[]
    for run in runs:
        directory=Path(run["directory"])
        picture=directory/"figure.png"
        if not picture.is_file():
            continue
        encoded=base64.b64encode(picture.read_bytes()).decode()
        title=html.escape(run["title"])
        links=" ".join(f'<a download="{html.escape(run["id"])}.{ext}" href="data:{mime};base64,{base64.b64encode((directory/("figure."+ext)).read_bytes()).decode()}">{ext.upper()}</a>' for ext,mime in [("svg","image/svg+xml"),("pdf","application/pdf")])
        cards.append(f'<article data-kind="{html.escape(run["kind"])}"><div class="meta">{html.escape(run["kind"])} · {html.escape(run["data_status"])}</div><h2>{title}</h2><img src="data:image/png;base64,{encoded}" alt="{title}"><footer>{links}<span>Mechanical audit: {"pass" if run["audit_passed"] else "review needed"}</span></footer></article>')
    document='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>SIVIA ModelAtlas</title><style>
*{box-sizing:border-box}body{margin:0;background:#f1f4f5;color:#18334b;font-family:system-ui,sans-serif}header{padding:48px 6vw 30px;background:#18334b;color:white}header p{color:#b7d7df;max-width:800px;line-height:1.7}h1{font-size:36px;letter-spacing:-1px;margin:10px 0}nav{padding:22px 6vw;display:flex;gap:12px;flex-wrap:wrap}input,select{font:inherit;padding:12px;border:1px solid #c7d5dc;border-radius:8px;background:white}input{flex:1;min-width:200px}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(380px,1fr));gap:24px;padding:0 6vw 50px}article{border:1px solid #d6e0e5;background:white;border-radius:12px;overflow:hidden}.meta{font-size:12px;text-transform:uppercase;letter-spacing:1.4px;color:#007c91;padding:22px 24px 0}h2{font-size:18px;padding:0 24px}img{width:100%;display:block}footer{padding:18px 24px;display:flex;gap:20px;align-items:center;border-top:1px solid #edf1f3}footer span{margin-left:auto;font-size:11px;color:#637985}a{color:#007c91;font-weight:600}article[hidden]{display:none}@media(max-width:480px){main{grid-template-columns:1fr}header{padding-top:28px}h1{font-size:28px}}
</style><header><small>SIVIA / MATHEMATICAL MODELING</small><h1>ModelAtlas · 美赛与数据建模作图</h1><p>来自实际运行的图表案例。每个案例对应完整配置、数据快照和审查记录。DEMO 表示演示数据；机械检查通过不代表论文结果已获验证。</p></header><nav><input id="q" aria-label="搜索案例" placeholder="搜索标题、图表类型…"><select id="kind" aria-label="图表类型"><option value="">全部类型</option>'''
    document+="".join(f'<option>{html.escape(k)}</option>' for k in sorted({r["kind"] for r in runs}))
    document+='</select></nav><main>'+"".join(cards)+'''</main><script>
const q=document.querySelector('#q'),k=document.querySelector('#kind');function filter(){for(const a of document.querySelectorAll('article'))a.hidden=!(a.textContent.toLowerCase().includes(q.value.toLowerCase())&&(!k.value||a.dataset.kind===k.value))}q.addEventListener('input',filter);k.addEventListener('change',filter);
</script></html>'''
    path=Path(output).resolve()
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(document,encoding="utf-8")
    return path
