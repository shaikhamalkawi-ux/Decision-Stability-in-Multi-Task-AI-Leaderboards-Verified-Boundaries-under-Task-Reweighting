from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = Path(__file__).resolve().parents[1]
fig, ax = plt.subplots(figsize=(13.5,5.5))
ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis('off')

def box(x,y,w,h,title,body,fc='#f6f6f6',fs=9.2):
    p=FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.012,rounding_size=0.012',
                     linewidth=1.1,edgecolor='black',facecolor=fc)
    ax.add_patch(p)
    ax.text(x+w/2,y+h*0.67,title,ha='center',va='center',fontsize=11,weight='bold')
    ax.text(x+w/2,y+h*0.33,body,ha='center',va='center',fontsize=fs,wrap=True)

def arrow(x1,y1,x2,y2):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle='-|>',mutation_scale=14,
                                 linewidth=1.1,color='black'))

ax.text(0.5,0.95,'Decision diagnosis for incomplete machine-learning leaderboards',
        ha='center',va='center',fontsize=16,weight='bold')
box(0.02,0.58,0.18,0.22,'Partial evidence','Incomplete fold evidence\nand contestable task weights.',fc='#f0f0f0')
box(0.24,0.58,0.20,0.22,'Sound diagnostic','Opposite-answer witness?\nSemantic determination?\nDeclared certificate?')
arrow(0.20,0.69,0.24,0.69)

outcomes=[
    (0.49,0.75,'Information-limited','Opposite decisions are\ncompatible with the evidence.'),
    (0.49,0.55,'Certificate-limited','Decision is fixed, but the\ndeclared certificate fails.'),
    (0.49,0.35,'Certified / resolved','The declared certificate\nestablishes the fixed decision.'),
    (0.49,0.15,'Inconclusive','Neither ambiguity nor a\nfixed decision is proved.'),
]
for x,y,title,body in outcomes:
    box(x,y,0.19,0.14,title,body,fc='#f5f5f5',fs=8.7)
    arrow(0.44,0.69,x,y+0.07)

box(0.74,0.58,0.24,0.24,'Exact constructions','Certificate-limited state proved\n68 tasks; 65,780 states\n789,360 support comparisons',fc='#ececec',fs=9)
arrow(0.68,0.62,0.74,0.68)
box(0.74,0.22,0.24,0.25,'TabArena evidence','51 tasks; 14 methods; 816 folds\n47/80 information-limited\n33/80 inconclusive\n0 earlier stops / 480 checks',fc='#ececec',fs=8.8)
arrow(0.68,0.82,0.74,0.40)
arrow(0.68,0.22,0.74,0.33)

ax.text(0.5,0.03,'Different diagnoses require different actions: collect evidence, enrich reasoning, or remain explicitly uncertain.',
        ha='center',va='center',fontsize=10.5,weight='bold')
fig.tight_layout(pad=0.8)
fig.savefig(OUT/'Graphical_Abstract_KBS.png',dpi=300,bbox_inches='tight')
fig.savefig(OUT/'Graphical_Abstract_KBS.pdf',bbox_inches='tight')
plt.close(fig)
