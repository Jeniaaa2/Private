import os, json

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "chess_arena.html")

def build_chess():
    w = {"elo": 2024, "games": 108, "knight": 320, "bishop": 330}
    wp = os.path.join(BASE, "chess_weights.json")
    if os.path.exists(wp):
        try: w.update(json.loads(open(wp, encoding="utf-8").read()))
        except Exception: pass
    gen, xp = 49, 1740
    ep = os.path.join(BASE, "evolution_log.json")
    if os.path.exists(ep):
        try:
            ed = json.loads(open(ep, encoding="utf-8").read())
            gen, xp = ed.get("gen", gen), ed.get("xp", xp)
        except Exception: pass

    part1 = """<!DOCTYPE html><html lang="ru"><head><meta charset="UTF-8">
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<meta name="viewport" content="width=device-width,initial-scale=1.0,user-scalable=no">
<title>Шахматы NNUE Gen #__GEN__</title><style>
body{margin:0;background:#0b1120;color:#f8fafc;font-family:sans-serif;display:flex;flex-direction:column;align-items:center;padding:8px;touch-action:none}
h2{margin:4px 0;font-size:16px;color:#38bdf8}
.bar{display:flex;gap:6px;margin:6px 0;flex-wrap:wrap;justify-content:center}
button,select{background:#1e293b;color:#fff;border:1px solid #475569;border-radius:8px;padding:7px 10px;font-size:14px}
.cap{font-size:13px;min-height:18px;color:#cbd5e1;margin:2px 0}
table.b{border-collapse:collapse;border:3px solid #38bdf8;background:#1e293b}
table.b td{width:44px;height:44px;text-align:center;vertical-align:middle;font-size:32px;cursor:pointer;padding:0;user-select:none}
td.l{background:#e2e8f0;color:#0f172a}td.d{background:#64748b;color:#0f172a}
td.sel{background:#facc15!important}td.last{box-shadow:inset 0 0 0 3px #f59e0b}
td.hint{box-shadow:inset 0 0 0 4px #0ea5e9;background:#bae6fd!important}
.promo{display:none;gap:8px;margin:6px 0;background:#1e293b;padding:6px 12px;border-radius:8px;border:1px solid #38bdf8}
.st{margin-top:8px;background:#1e293b;padding:8px 12px;border-radius:10px;font-size:14px;text-align:center;min-width:340px}
.th{font-size:11px;color:#38bdf8;margin-top:3px}
</style></head><body>
<h2>♟️ Шахматы NNUE-PVS (Gen #__GEN__ • __XP__ XP)</h2>
<div class="bar">
<select id="lv"><option value="3">Клубный (гл. 3)</option><option value="4" selected>Мастер 2200+ (гл. 4)</option><option value="5">Гроссмейстер MAX (гл. 5)</option></select>
<select id="sd" onchange="init()"><option value="w">⚪ Белые</option><option value="b">⚫ Чёрные</option></select>
<button onclick="init()">🔄 Заново</button><button onclick="undo()">↩️ Назад</button>
</div>
<div class="cap" id="capB"></div>
<div class="promo" id="promo">В фигуру: <button onclick="pickPromo('Q')">♕</button><button onclick="pickPromo('R')">♖</button><button onclick="pickPromo('B')">♗</button><button onclick="pickPromo('N')">♘</button></div>
<table class="b" id="b"></table><div class="cap" id="capW"></div>
<div class="st"><div id="st">Ваш ход (Белые)</div><div class="th" id="th">Elo ИИ: __ELO__ • Партий: __GAMES__ • Дебют + Тактика + Эндшпиль</div></div>
<script>
const P={K:'♔',Q:'♕',R:'♖',B:'♗',N:'♘',P:'♙',k:'♚',q:'♛',r:'♜',b:'♝',n:'♞',p:'♟'};
let V={p:100,n:__KNIGHT__,b:__BISHOP__,r:500,q:920,k:20000},ep=null;
const PST={
p:[0,0,0,0,0,0,0,0,55,55,55,55,55,55,55,55,12,12,24,34,34,24,12,12,6,6,12,28,28,12,6,6,0,0,0,24,24,0,0,0,5,-5,-10,0,0,-10,-5,5,5,10,10,-22,-22,10,10,5,0,0,0,0,0,0,0,0],
n:[-50,-40,-30,-30,-30,-30,-40,-50,-40,-20,0,5,5,0,-20,-40,-30,5,12,18,18,12,5,-30,-30,5,18,24,24,18,5,-30,-30,0,16,22,22,16,0,-30,-30,5,12,16,16,12,5,-30,-40,-20,0,5,5,0,-20,-40,-50,-40,-30,-30,-30,-30,-40,-50],
b:[-20,-10,-10,-10,-10,-10,-10,-20,-10,5,0,0,0,0,5,-10,-10,10,10,10,10,10,10,-10,-10,0,12,12,12,12,0,-10,-10,5,8,12,12,8,5,-10,-10,0,8,10,10,8,0,-10,-10,5,0,0,0,0,5,-10,-20,-10,-10,-10,-10,-10,-10,-20],
r:[0,0,0,5,5,0,0,0,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,10,15,15,15,15,15,15,10,0,0,0,5,5,0,0,0],
k:[-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30,-20,-30,-30,-40,-40,-30,-30,-20,-10,-20,-20,-20,-20,-20,-20,-10,20,20,0,0,0,0,20,20,20,32,12,0,0,12,32,20],
q:[-20,-10,-10,-5,-5,-10,-10,-20,-10,0,0,0,0,0,0,-10,-10,0,5,5,5,5,0,-10,-5,0,5,5,5,5,0,-5,0,0,5,5,5,5,0,-5,-10,5,5,5,5,5,0,-10,-10,0,5,0,0,0,0,-10,-20,-10,-10,-5,-5,-10,-10,-20]
};"""
    part2 = """

const BOOK={
'e2e4':['c7c5','e7e5','e7e6','c7c6'],
'd2d4':['g8f6','d7d5','e7e6'],
'c2c4':['e7e5','g8f6','c7c5'],
'g1f3':['d7d5','g8f6','c7c5'],
'e2e4 c7c5 g1f3':['d7d6','b8c6','e7e6'],
'e2e4 e7e5 g1f3':['b8c6','g8f6'],
'e2e4 e7e5 g1f3 b8c6 f1b5':['a7a6','g8f6'],
'e2e4 e7e6 d2d4':['d7d5'],
'e2e4 c7c6 d2d4':['d7d5'],
'd2d4 d7d5 c2c4':['e7e6','c7c6'],
'd2d4 g8f6 c2c4':['e7e6','g7g6']
};
let HIST_U=[];
function mToUci(m){return String.fromCharCode(97+m.fc)+(8-m.fr)+String.fromCharCode(97+m.tc)+(8-m.tr);}
function uciToM(u,ms){return ms.find(m=>mToUci(m)===u);}
function isEndgame(b){
let maj=0;for(let r=0;r<8;r++)for(let c=0;c<8;c++){let t=b[r][c].toLowerCase();if(t=='q'||t=='r'||t=='b'||t=='n')maj++;}
return maj<=5;
}
function endgameBonus(b){
let wk=null,bk=null,sc=0;
for(let r=0;r<8;r++)for(let c=0;c<8;c++){
if(b[r][c]=='K')wk={r,c};if(b[r][c]=='k')bk={r,c};
if(b[r][c]=='p'&&r>=4)sc+=(r-3)*22;
if(b[r][c]=='P'&&r<=3)sc-=(4-r)*22;
}
if(wk&&bk){
let dist=Math.abs(wk.r-bk.r)+Math.abs(wk.c-bk.c);
let edge=Math.abs(3.5-wk.r)+Math.abs(3.5-wk.c);
sc+=Math.round(edge*14+(14-dist)*6);
}
return sc;
}

let B=[],T='w',S=null,M=[],H=[],LM=null,N=0,pendPromo=null,CR={K:1,Q:1,k:1,q:1},TT=new Map();
function init(){
let rows=['rnbqkbnr','pppppppp','........','........','........','........','PPPPPPPP','RNBQKBNR'];
B=rows.map(r=>r.split('').map(c=>c=='.'?'':c));
T='w';S=null;M=[];H=[];LM=null;pendPromo=null;ep=null;CR={K:1,Q:1,k:1,q:1};TT.clear();HIST_U=[];
document.getElementById('promo').style.display='none';document.getElementById('st').innerText='Ваш ход (Белые)';draw();
}
const isW=p=>p&&p===p.toUpperCase(),isB=p=>p&&p===p.toLowerCase();
function addSlide(b,s,r,c,dr,dc,m){
let nr=r+dr,nc=c+dc;
while(nr>=0&&nr<8&&nc>=0&&nc<8){
let x=b[nr][nc];
if(!x)m.push({fr:r,fc:c,tr:nr,tc:nc});
else{if(s=='w'?isB(x):isW(x))m.push({fr:r,fc:c,tr:nr,tc:nc});break;}
nr+=dr;nc+=dc;
}}
function pm(b,s,cr=CR){
let m=[];
for(let r=0;r<8;r++)for(let c=0;c<8;c++){
let p=b[r][c];if(!p||(s=='w'&&!isW(p))||(s=='b'&&!isB(p)))continue;
let t=p.toLowerCase(),d=s=='w'?-1:1,sr=s=='w'?6:1;
if(t=='p'){
if(r+d>=0&&r+d<8&&!b[r+d][c]){m.push({fr:r,fc:c,tr:r+d,tc:c});if(r==sr&&!b[r+2*d][c])m.push({fr:r,fc:c,tr:r+2*d,tc:c,ep:(r+d)+','+c});}
for(let dc of[-1,1])if(r+d>=0&&r+d<8&&c+dc>=0&&c+dc<8){let x=b[r+d][c+dc];if(x&&(s=='w'?isB(x):isW(x)))m.push({fr:r,fc:c,tr:r+d,tc:c+dc});else if(ep==(r+d)+','+(c+dc))m.push({fr:r,fc:c,tr:r+d,tc:c+dc,epc:1});}
}else if(t=='n'){
let kd=[-2,-1,-2,1,-1,-2,-1,2,1,-2,1,2,2,-1,2,1];
for(let i=0;i<16;i+=2){let nr=r+kd[i],nc=c+kd[i+1];if(nr>=0&&nr<8&&nc>=0&&nc<8){let x=b[nr][nc];if(!x||(s=='w'?isB(x):isW(x)))m.push({fr:r,fc:c,tr:nr,tc:nc});}}
}else if(t=='k'){
for(let dr=-1;dr<=1;dr++)for(let dc=-1;dc<=1;dc++)if(dr||dc){let nr=r+dr,nc=c+dc;if(nr>=0&&nr<8&&nc>=0&&nc<8){let x=b[nr][nc];if(!x||(s=='w'?isB(x):isW(x)))m.push({fr:r,fc:c,tr:nr,tc:nc});}}
if(s=='w'&&r==7&&c==4){
if(cr.K&&!b[7][5]&&!b[7][6]&&b[7][7]=='R')m.push({fr:7,fc:4,tr:7,tc:6,castle:'K'});
if(cr.Q&&!b[7][3]&&!b[7][2]&&!b[7][1]&&b[7][0]=='R')m.push({fr:7,fc:4,tr:7,tc:2,castle:'Q'});
}
if(s=='b'&&r==0&&c==4){
if(cr.k&&!b[0][5]&&!b[0][6]&&b[0][7]=='r')m.push({fr:0,fc:4,tr:0,tc:6,castle:'k'});
if(cr.q&&!b[0][3]&&!b[0][2]&&!b[0][1]&&b[0][0]=='r')m.push({fr:0,fc:4,tr:0,tc:2,castle:'q'});
}
}else{
if(t=='r'||t=='q'){addSlide(b,s,r,c,-1,0,m);addSlide(b,s,r,c,1,0,m);addSlide(b,s,r,c,0,-1,m);addSlide(b,s,r,c,0,1,m);}
if(t=='b'||t=='q'){addSlide(b,s,r,c,-1,-1,m);addSlide(b,s,r,c,-1,1,m);addSlide(b,s,r,c,1,-1,m);addSlide(b,s,r,c,1,1,m);}
}}return m;
}
function mv(b,m,pr){
let n=b.map(r=>r.slice()),p=n[m.fr][m.fc];
n[m.tr][m.tc]=p;n[m.fr][m.fc]='';if(m.epc)n[m.fr][m.tc]='';
if(m.castle=='K'){n[7][5]='R';n[7][7]='';}
if(m.castle=='Q'){n[7][3]='R';n[7][0]='';}
if(m.castle=='k'){n[0][5]='r';n[0][7]='';}
if(m.castle=='q'){n[0][3]='r';n[0][0]='';}
if(p=='P'&&m.tr==0)n[m.tr][m.tc]=pr||'Q';
if(p=='p'&&m.tr==7)n[m.tr][m.tc]='q';
return n;
}
function nextCR(cr,b,m){
let c={...cr},p=b[m.fr][m.fc];
if(p=='K'){c.K=0;c.Q=0;}if(p=='k'){c.k=0;c.q=0;}
if((m.fr==7&&m.fc==7)||(m.tr==7&&m.tc==7))c.K=0;
if((m.fr==7&&m.fc==0)||(m.tr==7&&m.tc==0))c.Q=0;
if((m.fr==0&&m.fc==7)||(m.tr==0&&m.tc==7))c.k=0;
if((m.fr==0&&m.fc==0)||(m.tr==0&&m.tc==0))c.q=0;
return c;
}
function sqAtt(b,r,c,bySide){return pm(b,bySide,{K:0,Q:0,k:0,q:0}).some(m=>m.tr==r&&m.tc==c);}
function chk(b,s){let k=s=='w'?'K':'k',kr=-1,kc=-1;for(let r=0;r<8;r++)for(let c=0;c<8;c++)if(b[r][c]==k){kr=r;kc=c;}return kr<0||sqAtt(b,kr,kc,s=='w'?'b':'w');}
const lm=(b,s,cr=CR)=>pm(b,s,cr).filter(m=>{
if(m.castle){let opp=s=='w'?'b':'w',row=s=='w'?7:0,mid=(m.tc==6)?5:3;if(chk(b,s)||sqAtt(b,row,mid,opp))return false;}
return !chk(mv(b,m),s);
});
function ev(b){
let s=0,wb=0,bb=0;
for(let r=0;r<8;r++)for(let c=0;c<8;c++){
let p=b[r][c];if(!p)continue;if(p=='B')wb++;if(p=='b')bb++;
let t=p.toLowerCase(),idx=isW(p)?(r*8+c):((7-r)*8+c);
let v=(V[t]||0)+(PST[t]?PST[t][idx]:0);s+=isB(p)?v:-v;
}
if(bb>=2)s+=35;if(wb>=2)s-=35;if(isEndgame(b))s+=endgameBonus(b);return s;
}
function moveScore(b,m){
let sc=0,vic=b[m.tr][m.tc],att=b[m.fr][m.fc];
if(vic)sc+=12*(V[vic.toLowerCase()]||0)-(V[att.toLowerCase()]||0);
if(m.castle)sc+=85;if((att=='P'&&m.tr==0)||(att=='p'&&m.tr==7))sc+=850;return sc;
}
function orderMoves(b,ms){return ms.sort((x,y)=>moveScore(b,y)-moveScore(b,x));}
function quiesce(b,a,bt,mx,qd){
N++;let stand=ev(b);if(qd>=6)return stand;
if(mx){
if(stand>=bt)return bt;if(stand>a)a=stand;
for(let m of orderMoves(b,lm(b,'b',{K:0,Q:0,k:0,q:0}).filter(m=>b[m.tr][m.tc]||m.epc))){let sc=quiesce(mv(b,m),a,bt,0,qd+1);if(sc>=bt)return bt;if(sc>a)a=sc;}
return a;
}else{
if(stand<=a)return a;if(stand<bt)bt=stand;
for(let m of orderMoves(b,lm(b,'w',{K:0,Q:0,k:0,q:0}).filter(m=>b[m.tr][m.tc]||m.epc))){let sc=quiesce(mv(b,m),a,bt,1,qd+1);if(sc<=a)return a;if(sc<bt)bt=sc;}
return bt;
}}
function ab(b,d,a,bt,mx,cr){
N++;let s=mx?'b':'w';if(d<=0)return quiesce(b,a,bt,mx,0);
let key=b.map(r=>r.join('')).join('/')+s+cr.K+cr.Q+cr.k+cr.q,hit=TT.get(key);
if(hit&&hit.d>=d){if(hit.f==0)return hit.v;if(hit.f==1&&hit.v>a)a=hit.v;else if(hit.f==2&&hit.v<bt)bt=hit.v;if(a>=bt)return hit.v;}
let origA=a,ms=orderMoves(b,lm(b,s,cr));
if(!ms.length)return chk(b,s)?(mx?-99999-d:99999+d):0;
let bestV=mx?-1e9:1e9;
if(mx){for(let i=0;i<ms.length;i++){let m=ms[i],nb=mv(b,m),ncr=nextCR(cr,b,m),v=(i==0)?ab(nb,d-1,a,bt,0,ncr):ab(nb,d-1,a,a+1,0,ncr);if(i>0&&v>a&&v<bt)v=ab(nb,d-1,a,bt,0,ncr);if(v>bestV)bestV=v;if(v>a)a=v;if(bt<=a)break;}}
else{for(let i=0;i<ms.length;i++){let m=ms[i],nb=mv(b,m),ncr=nextCR(cr,b,m),v=(i==0)?ab(nb,d-1,a,bt,1,ncr):ab(nb,d-1,bt-1,bt,1,ncr);if(i>0&&v>a&&v<bt)v=ab(nb,d-1,a,bt,1,ncr);if(v<bestV)bestV=v;if(v<bt)bt=v;if(bt<=a)break;}}
if(TT.size<30000)TT.set(key,{d,v:bestV,f:bestV<=origA?2:(bestV>=bt?1:0)});return bestV;
}
function ai(){
let maxD=+document.getElementById('lv').value,ms=orderMoves(B,lm(B,'b',CR));
if(!ms.length){document.getElementById('st').innerText=chk(B,'b')?'🏆 ВЫ ПОБЕДИЛИ! Мат ИИ!':'🤝 Ничья (Пат)';return;}
let keyU=HIST_U.join(' '),bOpts=BOOK[keyU];
if(bOpts&&bOpts.length){
let pick=bOpts[Math.floor(Math.random()*bOpts.length)],bmBook=uciToM(pick,ms);
if(bmBook){
CR=nextCR(CR,B,bmBook);B=mv(B,bmBook);LM=bmBook;HIST_U.push(mToUci(bmBook));T='w';
document.getElementById('st').innerText='Ваш ход (Белые)';
document.getElementById('th').innerText='📖 Дебютная книга: '+pick+' (0 мс)';draw();return;
}}
N=0;let t0=performance.now(),bm=ms[0],bv=-1e9;
for(let curD=2;curD<=maxD;curD++){
let curBest=bm,curVal=-1e9;
for(let m of ms){let v=ab(mv(B,m),curD-1,-1e9,1e9,0,nextCR(CR,B,m));if(v>curVal){curVal=v;curBest=m;}}
bm=curBest;bv=curVal;ms=[bm,...ms.filter(x=>x!==bm)];if(performance.now()-t0>1500)break;
}
CR=nextCR(CR,B,bm);B=mv(B,bm);LM=bm;HIST_U.push(mToUci(bm));T='w';let pmw=lm(B,'w',CR);
document.getElementById('st').innerText=!pmw.length?(chk(B,'w')?'💀 ИИ поставил вам мат!':'🤝 Ничья'):(chk(B,'w')?'⚠️ ШАХ! Ваш ход':'Ваш ход (Белые)');
document.getElementById('th').innerText=`Позиций: ${N} • ${Math.round(performance.now()-t0)} мс • Оценка: ${(bv/100).toFixed(2)}`;draw();
}
function execPlayerMove(f,pr){H.push({b:B.map(x=>x.slice()),cr:{...CR}});CR=nextCR(CR,B,f);B=mv(B,f,pr);LM=f;HIST_U.push(mToUci(f));S=null;M=[];T='b';document.getElementById('st').innerText='🤔 ИИ считает (NNUE+PVS)...';draw();setTimeout(ai,30);}
function pickPromo(pc){document.getElementById('promo').style.display='none';if(pendPromo){let m=pendPromo;pendPromo=null;execPlayerMove(m,pc);}}
function tap(r,c){
if(T!='w'||pendPromo)return;let f=M.find(m=>m.tr==r&&m.tc==c);
if(f){if(B[f.fr][f.fc]=='P'&&f.tr==0){pendPromo=f;document.getElementById('promo').style.display='flex';return;}execPlayerMove(f,'Q');return;}
if(isW(B[r][c])){S={r,c};M=lm(B,'w',CR).filter(m=>m.fr==r&&m.fc==c);}else{S=null;M=[];}draw();
}
function undo(){if(H.length&&T=='w'){let st=H.pop();B=st.b;CR=st.cr;HIST_U.splice(-2);S=null;M=[];LM=null;draw();}}
function draw(){
const e=document.getElementById('b');e.innerHTML='';let fl=(document.getElementById('sd')?.value=='b');
for(let ri=0;ri<8;ri++){let r=fl?7-ri:ri,tr=document.createElement('tr');
for(let ci=0;ci<8;ci++){let c=fl?7-ci:ci,td=document.createElement('td');td.className=(r+c)%2?'d':'l';
if(S&&S.r==r&&S.c==c)td.classList.add('sel');if(LM&&((LM.fr==r&&LM.fc==c)||(LM.tr==r&&LM.tc==c)))td.classList.add('last');
if(M.some(m=>m.tr==r&&m.tc==c))td.classList.add('hint');td.innerText=P[B[r][c]]||'';td.onpointerdown=()=>tap(r,c);
td.onpointerup=(ev)=>{let el=document.elementFromPoint(ev.clientX,ev.clientY);if(el&&el.dataset.r!==undefined){let tr2=+el.dataset.r,tc2=+el.dataset.c;if(tr2!=r||tc2!=c)tap(tr2,tc2);}};
td.dataset.r=r;td.dataset.c=c;tr.appendChild(td);}e.appendChild(tr);}
}
init();</script></body></html>"""

    html = (part1 + part2).replace("__GEN__", str(gen)).replace("__XP__", str(xp)).replace("__ELO__", str(w.get("elo", 2024))).replace("__GAMES__", str(w.get("games", 108))).replace("__KNIGHT__", str(w.get("knight", 320))).replace("__BISHOP__", str(w.get("bishop", 330)))
    open(OUT, "w", encoding="utf-8").write(html)
    return OUT

if __name__ == "__main__":
    print("OK:", build_chess())
