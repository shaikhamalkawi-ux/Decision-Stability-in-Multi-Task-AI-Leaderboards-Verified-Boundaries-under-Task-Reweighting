from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon

# Embed TrueType fonts in PDF outputs (avoid Type-3 fonts).
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42

OUT = Path(__file__).resolve().parents[1]

# ---------- Figure 1: sound diagnostic workflow ----------
fig, ax = plt.subplots(figsize=(11, 7.6))
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')

def box(x,y,w,h,text,fontsize=10,weight='normal',fc='#f7f7f7'):
    p = FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.012,rounding_size=0.012',
                       linewidth=1.2, edgecolor='black', facecolor=fc)
    ax.add_patch(p)
    ax.text(x+w/2,y+h/2,text,ha='center',va='center',fontsize=fontsize,weight=weight,wrap=True)
    return p

def diamond(cx,cy,w,h,text,fontsize=9.5):
    pts = [(cx,cy+h/2),(cx+w/2,cy),(cx,cy-h/2),(cx-w/2,cy)]
    p=Polygon(pts,closed=True,facecolor='#fbfbfb',edgecolor='black',linewidth=1.2)
    ax.add_patch(p)
    ax.text(cx,cy,text,ha='center',va='center',fontsize=fontsize,wrap=True)
    return p

def arrow(x1,y1,x2,y2,label=None,lx=None,ly=None):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle='-|>',mutation_scale=12,
                                 linewidth=1.1,color='black',shrinkA=2,shrinkB=2))
    if label:
        ax.text(lx if lx is not None else (x1+x2)/2,
                ly if ly is not None else (y1+y2)/2,
                label,fontsize=9.5,ha='center',va='center')

box(0.33,0.89,0.34,0.075,'Partial benchmark evidence and a declared decision rule',10,weight='bold',fc='#eeeeee')
diamond(0.50,0.75,0.38,0.12,'Can two compatible completions\nbe proved to yield opposite decisions?')
arrow(0.50,0.89,0.50,0.815)
box(0.04,0.60,0.28,0.095,'Information-limited\nEvidence permits opposite decisions.',10,weight='bold',fc='#f3f3f3')
arrow(0.31,0.75,0.18,0.695,'Yes',0.27,0.735)
box(0.04,0.46,0.28,0.085,'Action: collect more evidence\nor strengthen assumptions.',9.5,fc='white')
arrow(0.18,0.60,0.18,0.545)
diamond(0.69,0.57,0.40,0.12,'Is semantic determination proved\nover all compatible completions?')
arrow(0.64,0.71,0.69,0.63,'No',0.66,0.685)
box(0.69,0.37,0.26,0.085,'Inconclusive\nDo not infer agreement.',10,weight='bold',fc='#f3f3f3')
arrow(0.69,0.51,0.80,0.455,'No',0.73,0.49)
diamond(0.50,0.34,0.38,0.12,'Does the declared certificate\ncertify the fixed decision?')
arrow(0.60,0.53,0.52,0.40,'Yes',0.57,0.47)
box(0.08,0.17,0.31,0.095,'Certificate-limited\nDecision is fixed, but the declared\ncertificate cannot establish it.',9.5,weight='bold',fc='#f3f3f3')
arrow(0.37,0.34,0.235,0.265,'No',0.33,0.315)
box(0.08,0.035,0.31,0.085,'Action: use richer reasoning\nor a richer certificate.',9.5,fc='white')
arrow(0.235,0.17,0.235,0.12)
box(0.61,0.17,0.27,0.095,'Certified / resolved\nThe declared certificate establishes\nthe fixed decision.',9.5,weight='bold',fc='#f3f3f3')
arrow(0.63,0.34,0.745,0.265,'Yes',0.67,0.315)
ax.text(0.5,0.005,'Sound labels require explicit witnesses or proofs; failed searches remain inconclusive.',
        ha='center',va='bottom',fontsize=9)
fig.tight_layout(pad=0.8)
fig.savefig(OUT/'Figure1_Diagnostic_Framework.png',dpi=300,bbox_inches='tight')
fig.savefig(OUT/'Figure1_Diagnostic_Framework.pdf',bbox_inches='tight')
plt.close(fig)

# ---------- Figure 2 ----------
labels = [r'$\varepsilon=2/51$', r'$\varepsilon=4/51$']
amb = [39, 8]; inc = [1, 32]
fig, ax = plt.subplots(figsize=(7.5,5.4)); x=[0,1]
ax.bar(x,amb,label='Proven ambiguous')
ax.bar(x,inc,bottom=amb,label='Inconclusive',color='0.80')
ax.set_ylabel('Number of traces'); ax.set_xlabel('Total-variation radius')
ax.set_xticks(x,labels); ax.set_ylim(0,42)
ax.legend(frameon=False,loc='upper center',ncol=2,bbox_to_anchor=(0.5,1.03))
for i,(a,b) in enumerate(zip(amb,inc)):
    ax.text(i,a/2,f'{a}\n({a/40*100:g}%)',ha='center',va='center',fontsize=10,
            color='white' if a>12 else 'black')
    ax.text(i,a+b/2,f'{b}\n({b/40*100:g}%)',ha='center',va='center',fontsize=10)
ax.text(0.5,-0.19,'Descriptive counts for fixed, overlapping traces; not population estimates.',
        transform=ax.transAxes,ha='center',va='top',fontsize=9)
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
fig.tight_layout()
fig.savefig(OUT/'Figure2_Witnesses_By_TV_Radius.png',dpi=300,bbox_inches='tight')
fig.savefig(OUT/'Figure2_Witnesses_By_TV_Radius.pdf',bbox_inches='tight')
plt.close(fig)

# ---------- Graphical abstract ----------
fig, ax = plt.subplots(figsize=(13.5,5.5))
ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis('off')
def gabox(x,y,w,h,title,body,fc='#f6f6f6',fs=9.2):
    p=FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.012,rounding_size=0.012',
                     linewidth=1.1,edgecolor='black',facecolor=fc)
    ax.add_patch(p)
    ax.text(x+w/2,y+h*0.67,title,ha='center',va='center',fontsize=11,weight='bold')
    ax.text(x+w/2,y+h*0.33,body,ha='center',va='center',fontsize=fs,wrap=True)
def gaarr(x1,y1,x2,y2):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle='-|>',mutation_scale=14,
                                 linewidth=1.1,color='black'))
ax.text(0.5,0.95,'Decision diagnosis for incomplete machine-learning leaderboards',
        ha='center',va='center',fontsize=16,weight='bold')
gabox(0.02,0.58,0.18,0.22,'Partial evidence','Incomplete fold evidence\nand contestable task weights.',fc='#f0f0f0')
gabox(0.24,0.58,0.20,0.22,'Sound diagnostic','Opposite-answer witness?\nSemantic determination?\nDeclared certificate?')
gaarr(0.20,0.69,0.24,0.69)
outcomes=[
    (0.49,0.75,'Information-limited','Opposite decisions are\ncompatible with the evidence.'),
    (0.49,0.55,'Certificate-limited','Decision is fixed, but the\ndeclared certificate fails.'),
    (0.49,0.35,'Certified / resolved','The declared certificate\nestablishes the fixed decision.'),
    (0.49,0.15,'Inconclusive','Neither ambiguity nor a\nfixed decision is proved.'),
]
for x,y,title,body in outcomes:
    gabox(x,y,0.19,0.14,title,body,fc='#f5f5f5',fs=8.7); gaarr(0.44,0.69,x,y+0.07)
gabox(0.74,0.58,0.24,0.24,'Exact constructions','Certificate-limited state proved\n68 tasks; 65,780 states\n789,360 support comparisons',fc='#ececec',fs=9)
gaarr(0.68,0.62,0.74,0.68)
gabox(0.74,0.22,0.24,0.25,'TabArena evidence','51 tasks; 14 methods; 816 folds\n47/80 information-limited\n33/80 inconclusive\n0 earlier stops / 480 checks',fc='#ececec',fs=8.8)
gaarr(0.68,0.82,0.74,0.40); gaarr(0.68,0.22,0.74,0.33)
ax.text(0.5,0.03,'Different diagnoses require different actions: collect evidence, enrich reasoning, or remain explicitly uncertain.',
        ha='center',va='center',fontsize=10.5,weight='bold')
fig.tight_layout(pad=0.8)
fig.savefig(OUT/'Graphical_Abstract_KBS.png',dpi=300,bbox_inches='tight')
fig.savefig(OUT/'Graphical_Abstract_KBS.pdf',bbox_inches='tight')
plt.close(fig)
