"""K-DART synthetic methodological stress test. NOT evidence about actual firms."""
import json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import wilcoxon
from sklearn.model_selection import train_test_split
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, average_precision_score, brier_score_loss
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.calibration import calibration_curve

OUT=Path(__file__).parent/'outputs';OUT.mkdir(exist_ok=True)
SEEDS=range(20)
FEATURES=['digital_infrastructure','workforce_skills','innovation_investment','leadership_support','process_integration','financial_slack']

def generate(seed,n=2400,shift=False):
    rng=np.random.default_rng(seed)
    latent=rng.normal(size=(n,3))
    x=np.zeros((n,6));x[:,0]=latent[:,0]+rng.normal(0,.65,n);x[:,1]=.6*latent[:,0]+.5*latent[:,1]+rng.normal(0,.7,n)
    x[:,2]=latent[:,1]+rng.normal(0,.7,n);x[:,3]=latent[:,2]+rng.normal(0,.7,n)
    x[:,4]=.65*latent[:,0]+.55*latent[:,2]+rng.normal(0,.65,n)
    x[:,5]=.45*latent[:,1]+rng.normal(0,.9,n)
    if shift:x[:,0]-=.8;x[:,5]-=.9
    z= -.55+ .65*latent[:,0]+.55*latent[:,1]+.6*latent[:,2]+.65*(latent[:,0]>.1)*(latent[:,2]>.1)-.75*(latent[:,0]<-.4)
    if shift:z-=.3
    p=1/(1+np.exp(-z));y=rng.binomial(1,p)
    return pd.DataFrame(x,columns=FEATURES),y

def rules(x):
    # Hypothetical predeclared rules; NOT independently expert validated.
    a=x.to_numpy();return np.column_stack(((a[:,0]<-.4).astype(float),((a[:,0]>.1)&(a[:,3]>.1)).astype(float),np.minimum(a[:,0],a[:,4]),(a[:,1]<-.5).astype(float)))

def fit_predict(xtr,ytr,xt,method):
    if method=='Logistic':a,b=xtr,xt;model=make_pipeline(StandardScaler(),LogisticRegression(max_iter=1000))
    elif method=='GradientBoosting':a,b=xtr,xt;model=HistGradientBoostingClassifier(max_iter=100,learning_rate=.06,l2_regularization=1.0,random_state=1)
    else:
        a=np.column_stack((xtr.to_numpy(),rules(xtr)));b=np.column_stack((xt.to_numpy(),rules(xt)))
        model=make_pipeline(StandardScaler(),LogisticRegression(max_iter=1000))
    model.fit(a,ytr);return model.predict_proba(b)[:,1]

records=[];calibrations={}
for seed in SEEDS:
    x,y=generate(seed);xtr,xt,ytr,yt=train_test_split(x,y,test_size=.3,stratify=y,random_state=seed)
    xs,ys=generate(seed+10000,n=750,shift=True)
    for model in ('Logistic','GradientBoosting','K-DART'):
        for split,xte,yte in [('ID',xt,yt),('SHIFT',xs,ys)]:
            p=fit_predict(xtr,ytr,xte,model)
            records.append(dict(seed=seed,model=model,split=split,auc=roc_auc_score(yte,p),ap=average_precision_score(yte,p),brier=brier_score_loss(yte,p)))
            if seed==0 and split=='ID':calibrations[model]=(yte,p)

df=pd.DataFrame(records);df.to_csv(OUT/'run_level_metrics.csv',index=False)
g=df.groupby(['split','model'])[['auc','ap','brier']].agg(['mean','std'])
g.to_csv(OUT/'table_1_metrics.csv')
abl=[]
for seed in SEEDS:
 x,y=generate(seed);xtr,xt,ytr,yt=train_test_split(x,y,test_size=.3,stratify=y,random_state=seed)
 for label,chosen in [('All rules',[0,1,2,3]),('No rule features',[]),('Threshold only',[0,3]),('Interactions only',[1,2])]:
  if chosen:
   a=np.column_stack((xtr.to_numpy(),rules(xtr)[:,chosen]));b=np.column_stack((xt.to_numpy(),rules(xt)[:,chosen]))
  else:a=xtr.to_numpy();b=xt.to_numpy()
  mdl=make_pipeline(StandardScaler(),LogisticRegression(max_iter=1000));mdl.fit(a,ytr)
  pr=mdl.predict_proba(b)[:,1];abl.append(dict(seed=seed,variant=label,auc=roc_auc_score(yt,pr),brier=brier_score_loss(yt,pr)))
adf=pd.DataFrame(abl);adf.to_csv(OUT/'ablation_runs.csv',index=False)
adf.groupby('variant')[['auc','brier']].agg(['mean','std']).to_csv(OUT/'table_2_ablation.csv')

fig,ax=plt.subplots(figsize=(8,4.6))
for i,method in enumerate(['Logistic','GradientBoosting','K-DART']):
 for j,split in enumerate(['ID','SHIFT']):
  a=df[(df.model==method)&(df.split==split)].auc
  ax.errorbar(i+(-.16 if j==0 else .16),a.mean(),yerr=1.96*a.std(ddof=1)/np.sqrt(len(a)),fmt='o',capsize=5,label=split if i==0 else None)
ax.set_xticks(range(3),['Logistic','Gradient boosting','K-DART']);ax.set_ylim(.45,1);ax.set_ylabel('AUROC (mean ± 95% run-level CI)');ax.set_title('Repeated synthetic experiments: predictive discrimination');ax.legend(frameon=False);ax.grid(axis='y',alpha=.2);fig.tight_layout();fig.savefig(OUT/'Figure_1.pdf');fig.savefig(OUT/'Figure_1.png',dpi=320);plt.close(fig)
fig,ax=plt.subplots(figsize=(7.2,4.5))
for method,(y,p) in calibrations.items():
 frac,mean=calibration_curve(y,p,n_bins=10,strategy='quantile');ax.plot(mean,frac,marker='o',label=method)
ax.plot([0,1],[0,1],'k--',linewidth=1,label='Perfect calibration');ax.set(xlabel='Mean predicted probability',ylabel='Observed simulated-readiness frequency',title='Calibration in one held-out synthetic run');ax.legend(fontsize=9);ax.grid(alpha=.2);fig.tight_layout();fig.savefig(OUT/'Figure_2.pdf');fig.savefig(OUT/'Figure_2.png',dpi=320);plt.close(fig)
paired=df[df.split=='ID'].pivot(index='seed',columns='model',values='auc')
stat=wilcoxon(paired['K-DART']-paired['Logistic'],zero_method='wilcox')
summary={'synthetic_only':True,'n_seeds':len(SEEDS),'n_per_seed':2400,'mean_auroc':{str(k):float(v) for k,v in df.groupby(['split','model']).auc.mean().to_dict().items()},'p_kdart_vs_logistic_ID_auroc_wilcoxon':float(stat.pvalue)}
(OUT/'summary.json').write_text(json.dumps(summary,indent=2));print(g.round(4));print('ablation');print(adf.groupby('variant')[['auc','brier']].mean().round(4));print('paired p',stat.pvalue)
