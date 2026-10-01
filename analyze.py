"""Descriptive bike-rental analysis. No forecasting or causal claims."""
from pathlib import Path
import json, hashlib, io, zipfile, urllib.request
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=Path(__file__).resolve().parent
O=P/'outputs'; O.mkdir(exist_ok=True)
if not (P/'hour.csv').exists():
    url='https://archive.ics.uci.edu/static/public/275/bike+sharing+dataset.zip'
    with urllib.request.urlopen(url) as response:
        z=zipfile.ZipFile(io.BytesIO(response.read()))
    for name in ['hour.csv','day.csv','Readme.txt']:
        (P/name).write_bytes(z.read(name))
h=pd.read_csv(P/'hour.csv',parse_dates=['dteday'])
d=pd.read_csv(P/'day.csv',parse_dates=['dteday'])
assert len(h)==17379 and len(d)==731
assert h.instant.is_unique and d.dteday.is_unique
assert not h.isna().any().any() and not d.isna().any().any()
assert (h.casual+h.registered==h.cnt).all()
assert (d.casual+d.registered==d.cnt).all()
assert h.groupby('dteday').cnt.sum().equals(d.set_index('dteday').cnt)
g=h.groupby(['workingday','hr']).agg(mean_rentals=('cnt','mean'),observed_hours=('cnt','size'),rentals=('cnt','sum')).reset_index()
g.to_csv(O/'hourly-profile.csv',index=False)
w=h.groupby('weathersit').agg(mean_rentals=('cnt','mean'),observed_hours=('cnt','size')).reset_index()
w.to_csv(O/'weather-profile.csv',index=False)
m=d.groupby(d.dteday.dt.to_period('M').astype(str)).agg(total_rentals=('cnt','sum'),days=('cnt','size'),daily_mean=('cnt','mean')).reset_index()
m.to_csv(O/'monthly-rentals.csv',index=False)
y=d.groupby(d.dteday.dt.year).agg(total_rentals=('cnt','sum'),days=('cnt','size'),daily_mean=('cnt','mean')).reset_index()
y.to_csv(O/'year-comparison.csv',index=False)
peaks=g.loc[g.groupby('workingday').mean_rentals.idxmax()].to_dict('records')
# Calendar-hour gaps are absent records, not observed zero-rental hours.
full=pd.MultiIndex.from_product([pd.date_range(d.dteday.min(),d.dteday.max()),range(24)],names=['dteday','hr'])
present=pd.MultiIndex.from_frame(h[['dteday','hr']]);missing=full.difference(present)
pd.DataFrame(missing.tolist(),columns=['dteday','hr']).to_csv(O/'absent-calendar-hours.csv',index=False)
results={'rows_hour':len(h),'rows_day':len(d),'start':str(d.dteday.min().date()),'end':str(d.dteday.max().date()),'rentals':int(h.cnt.sum()),'registered_rentals':int(h.registered.sum()),'registered_share_pct':float(h.registered.sum()/h.cnt.sum()*100),'possible_calendar_hours':len(full),'absent_calendar_hours':len(missing),'missing_cells':int(h.isna().sum().sum()),'peak_by_daytype':peaks,'yearly':y.to_dict('records'),'weather':w.to_dict('records'),'raw_sha256':{n:hashlib.sha256((P/n).read_bytes()).hexdigest() for n in ['hour.csv','day.csv']}}
(O/'results.json').write_text(json.dumps(results,indent=2)+'\n')
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False,'axes.spines.left':False,'axes.spines.bottom':False,'axes.labelcolor':'#251f21','text.color':'#251f21','xtick.color':'#585254','ytick.color':'#585254'})
fig,ax=plt.subplots(figsize=(10,5.6));fig.subplots_adjust(left=.09,right=.97,top=.79,bottom=.2)
for typ,label,c in [(1,'Working day','#367d6b'),(0,'Weekend or holiday','#585254')]:
 a=g[g.workingday==typ]; ax.plot(a.hr,a.mean_rentals,label=label,color=c,lw=2.5)
ax.set(xlim=(0,23),ylim=(0,600),xticks=range(0,24,3),xlabel='Hour of day',ylabel='Rentals per observed hour')
ax.grid(axis='y',color='#eae9ea');ax.legend(frameon=False,loc='upper left')
fig.text(.09,.93,'Working days have two distinct rental peaks',fontsize=20,fontfamily='DejaVu Serif')
fig.text(.09,.85,'Capital Bikeshare, 2011-2012 | 17,379 observed hourly records',fontsize=11,color='#585254')
for typ in [0,1]:
 p=next(a for a in peaks if a['workingday']==typ)
 ax.annotate(f"{int(p['hr']):02d}:00 | {p['mean_rentals']:.1f}",(p['hr'],p['mean_rentals']),xytext=(0,13),textcoords='offset points',ha='center',fontsize=10)
fig.text(.09,.06,'Source: UCI Bike Sharing, H. Fanaee-T, CC BY 4.0. Means exclude 165 absent calendar hours.',fontsize=9,color='#585254')
fig.savefig(O/'hourly-demand.png',dpi=150);plt.close(fig)
print(json.dumps(results,indent=2))
