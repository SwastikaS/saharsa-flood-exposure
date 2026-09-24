from pathlib import Path
import os
os.environ['MPLCONFIGDIR']='/tmp/flood-matplotlib'
import geopandas as g
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).resolve().parents[1]/'results'
d=g.read_file(p/'September4_landcover_exposure.gpkg',layer='block_crop_overlap')
assert np.allclose(d.baseline_crop_overlap_pct,100*d.crop_overlap_km2/d.baseline_crop_km2)
assert (d.crop_overlap_km2<=d.baseline_crop_km2).all()
d['area_rank']=d.crop_overlap_km2.rank(method='min',ascending=False).astype(int)
d['share_rank']=d.baseline_crop_overlap_pct.rank(method='min',ascending=False).astype(int)
t=d[['Sub_dist','baseline_crop_km2','crop_overlap_km2','baseline_crop_overlap_pct','lulc_uncovered_wet_km2']].sort_values('crop_overlap_km2',ascending=False).rename(columns={'Sub_dist':'Block','baseline_crop_km2':'Mapped baseline cropland (km²)','crop_overlap_km2':'Cropland overlap (km²)','baseline_crop_overlap_pct':'Baseline cropland intersected (%)','lulc_uncovered_wet_km2':'Inundation without LULC (km²)'})
fig,axs=plt.subplots(1,2,figsize=(13,6))
for ax,col,label,color in zip(axs,['crop_overlap_km2','baseline_crop_overlap_pct'],['Cropland overlap (km²)','Share of mapped baseline cropland (%)'],['#c87526','#25817b']):
 q=d.sort_values(col,ascending=True)
 ax.barh(q.Sub_dist,q[col],color=color)
 ax.set_xlim(0,q[col].max()*1.22)
 for i,val in enumerate(q[col]):ax.text(val+.15,i,f'{val:.2f}',va='center',fontsize=9)
 ax.set_xlabel(label);ax.spines[['top','right']].set_visible(False)
 ax.grid(axis='x',alpha=.15);ax.set_axisbelow(True)
fig.suptitle('Saharsa: block comparison of agricultural-land exposure',fontsize=15)
fig.text(.02,.015,'NRSC inundation: 4 September 2026 | LULC baseline: 2024–25, scale 1:250,000 | SOI-derived blocks\nPercentages use mapped baseline cropland only. Zero means no mapped overlap; not confirmed absence of flooding.',fontsize=9)
fig.tight_layout(rect=[0,.09,1,.94]);fig.savefig(p/'Block_comparison.png',dpi=160);plt.close(fig)
section='<h2 id="block-comparison">Block comparison: area and proportion</h2><p><b>Mahishi has the largest cropland overlap (17.66 km²), while Nauhatta has the highest proportional overlap (15.25% of mapped baseline cropland).</b> Banma Itahri ranks fourth by area but third by proportion.</p><img style="max-width:1100px" src="Block_comparison.png">'+t.to_html(index=False,float_format=lambda x:f'{x:.2f}')+'<p>Percentage = cropland intersecting mapped inundation ÷ all valid mapped 2024–25 cropland in the SOI block × 100. The denominator excludes LULC NoData. These are historical agricultural-land screening estimates, not percentages of standing crops damaged. Source coverage differs from SOI boundaries; the last column records unknown land cover within mapped inundation. Zero overlap does not establish dry conditions.</p>'
f=p/'Results.html';s=f.read_text();start=s.index('<h2>Block screening</h2>');end=s.index('<h2>Village screening</h2>',start);s=s[:start]+section+s[end:];f.write_text(s)
(p/'Block_comparison.json').write_text(t.to_json(orient='records',indent=2))
print(t.to_string(index=False))
