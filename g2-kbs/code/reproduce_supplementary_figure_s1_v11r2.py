from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import Rectangle
mpl.rcParams["pdf.fonttype"]=42
mpl.rcParams["ps.fonttype"]=42
OUT=Path(__file__).resolve().parents[1]
fig,ax=plt.subplots(figsize=(12.5,4.8))
ax.set_xlim(0,68); ax.set_ylim(0,1); ax.axis("off")
blocks=[(0,21,"21 independently incomplete tasks\n6 admissible rank-row types per task"),
(21,42,"21 fully known tasks"),(42,63,"21 fully known tasks"),(63,68,"5 fully\nknown tasks")]
for start,end,label in blocks:
    ax.add_patch(Rectangle((start,0.39),end-start,0.25,linewidth=1.2,fill=False))
    ax.text((start+end)/2,0.515,label,ha="center",va="center",fontsize=9.5 if end-start>6 else 8.8)
ax.annotate("",xy=(0,0.76),xytext=(21,0.76),arrowprops=dict(arrowstyle="<->",linewidth=1.1))
ax.text(10.5,0.81,"Uncertain block",ha="center",fontsize=10.5,fontweight="bold")
ax.annotate("",xy=(21,0.76),xytext=(68,0.76),arrowprops=dict(arrowstyle="<->",linewidth=1.1))
ax.text(44.5,0.81,"Known blocks",ha="center",fontsize=10.5,fontweight="bold")
ax.text(34,0.20,r"Permutation symmetry: $6^{21}$ assignments → $\binom{26}{5}=65{,}780$ canonical states → $65{,}780\times12=789{,}360$ ordered support checks.",ha="center",va="center",fontsize=10.7)
ax.text(34,0.07,"The completion domain allows heterogeneous uncertain-task assignments; synchronized completions are used only as obstruction witnesses.",ha="center",va="center",fontsize=9.2)
fig.tight_layout(pad=0.8)
fig.savefig(OUT/"FigureS1_68Task_Construction.png",dpi=240,bbox_inches="tight")
fig.savefig(OUT/"FigureS1_68Task_Construction.pdf",bbox_inches="tight")
plt.close(fig)
