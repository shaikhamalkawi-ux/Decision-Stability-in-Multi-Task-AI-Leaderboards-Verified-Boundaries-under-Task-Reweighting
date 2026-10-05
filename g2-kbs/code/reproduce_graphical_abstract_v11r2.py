from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
mpl.rcParams["pdf.fonttype"]=42
mpl.rcParams["ps.fonttype"]=42
OUT=Path(__file__).resolve().parents[1]

fig,ax=plt.subplots(figsize=(16,6.4))
ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
def box(x,y,w,h,title,body="",title_fs=12,body_fs=9.3):
    p=FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.01,rounding_size=0.012",linewidth=1.2,fill=False)
    ax.add_patch(p)
    ax.text(x+w/2,y+h*0.68,title,ha="center",va="center",fontsize=title_fs,fontweight="bold")
    if body:
        ax.text(x+w/2,y+h*0.31,body,ha="center",va="center",fontsize=body_fs,wrap=True)
def arrow(x1,y1,x2,y2):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle="-|>",mutation_scale=13,linewidth=1.1))

ax.text(0.5,0.955,"Decision diagnosis for incomplete machine-learning leaderboards",ha="center",va="center",fontsize=19,fontweight="bold")
box(0.025,0.58,0.18,0.24,"Incomplete leaderboard","Partial fold evidence\nUncertain task importance\nDeclared decision rule",13,9.5)
box(0.255,0.54,0.22,0.32,"Decision diagnostic","1  Opposite-answer witness?\n2  Semantic determination?\n3  Certificate success?",13.5,10)
arrow(0.205,0.70,0.255,0.70)
arrow(0.475,0.70,0.515,0.70)
ax.plot([0.515,0.515],[0.35,0.81],linewidth=1.1)
outcomes=[
(0.555,0.74,"Information-limited","Opposite decisions remain compatible."),
(0.555,0.59,"Certificate-limited","Decision is fixed; the declared certificate fails."),
(0.555,0.44,"Certified / resolved","The declared certificate establishes the fixed decision."),
(0.555,0.29,"Inconclusive","Neither ambiguity nor a fixed decision is proved.")]
for x,y,t,b in outcomes:
    box(x,y,0.25,0.115,t,b,11.2,8.4); arrow(0.515,y+0.0575,x,y+0.0575)
box(0.835,0.63,0.15,0.18,"Exact theory","68 tasks\n65,780 states\n789,360 support checks",11.5,8.7)
box(0.835,0.34,0.15,0.22,"TabArena evidence","51 tasks • 14 methods\n816 fold vectors\n47/80 information-limited\n33/80 inconclusive\n0 earlier stops / 480 checks",11.5,8.1)
ax.text(0.5,0.115,"Exact theory establishes certificate limitation; real benchmark evidence establishes information limitation.",ha="center",va="center",fontsize=10.6)
ax.text(0.5,0.045,"Same unresolved status ≠ same remedy: collect evidence, strengthen assumptions, enrich the certificate, or remain explicitly uncertain.",ha="center",va="center",fontsize=11.3,fontweight="bold")
fig.tight_layout(pad=0.8)
fig.savefig(OUT/"Graphical_Abstract_KBS.png",dpi=240,bbox_inches="tight")
fig.savefig(OUT/"Graphical_Abstract_KBS.pdf",bbox_inches="tight")
fig.savefig(OUT/"Graphical_Abstract_KBS.tif",dpi=300,bbox_inches="tight")
plt.close(fig)
