from pathlib import Path
import os
os.environ['MPLCONFIGDIR']='/tmp/flood-matplotlib'
import geopandas as g
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.colors import ListedColormap,BoundaryNorm
from shapely import union_all
p=Path(__file__).resolve().parents[1]/'results'
b=g.read_file(p/'September4_landcover_exposure.gpkg',layer='block_crop_overlap')
e=g.read_file(p/'September4_landcover_exposure.gpkg',layer='inundation_by_landcover')
w=g.read_file(p.parent/'inputs/September4_administrative_exposure.gpkg',layer='saharsa_mapped_inundation')
aoi=union_all(b.geometry)
unknown=union_all(w.geometry).difference(union_all(e.geometry))
crop=e[e.class_id.isin([2,3,4,5])]
other=e[~e.class_id.isin([2,3,4,5])]

def base(title,subtitle):
 fig,ax=plt.subplots(figsize=(11.7,11.7))
 fig.suptitle(title,x=.08,y=.97,ha='left',fontsize=19,fontweight='bold',color='#233947')
 fig.text(.08,.925,subtitle,fontsize=11,color='#465b67')
 g.GeoSeries([aoi],crs=b.crs).plot(ax=ax,color='#f1efe8',edgecolor='#4e5759',linewidth=.9)
 ax.set_aspect('equal');ax.set_axis_off()
 ax.annotate('Grid N',xy=(.94,.9),xytext=(.94,.81),xycoords='axes fraction',ha='center',arrowprops=dict(facecolor='#263a43',width=2,headwidth=8),fontsize=9)
 x0,y0,x1,y1=aoi.bounds
 x=x0+1000;y=y0-3000
 ax.plot([x,x+10000],[y,y],color='#263a43',linewidth=3)
 for delta,label in [(0,'0'),(5000,'5'),(10000,'10 km')]:
  ax.plot([x+delta,x+delta],[y-250,y+250],color='#263a43',linewidth=1)
  ax.text(x+delta,y-600,label,ha='center',va='top',fontsize=8)
 ax.set_ylim(y0-5000,y1+1200)
 fig.subplots_adjust(top=.89,bottom=.15,left=.06,right=.95)
 return fig,ax

def footer(fig):
 fig.text(.08,.09,'Sources: NRSC/ISRO inundation (4 September 2026, 1800 hrs product); NRSC LULC (2024–25);\nSurvey of India village boundaries, dissolved to blocks and district. Projection: WGS 84 / UTM zone 45N.',fontsize=9)
 fig.text(.08,.035,'LULC source mapping scale: 1:250,000. Historical cropland overlap is not standing-crop damage.\nNRSC inundation is preliminary. Unclassified coverage is retained as unknown. Prepared 24 September 2026.',fontsize=9,color='#555555')

fig,ax=base('Agricultural-land exposure in Saharsa','Official mapped inundation intersected with historical cropland | 4 September 2026')
b.boundary.plot(ax=ax,color='#b2afa5',linewidth=.45)
other.plot(ax=ax,color='#388db0')
g.GeoSeries([unknown],crs=b.crs).plot(ax=ax,color='#b93e79')
crop.plot(ax=ax,color='#d47922')
ax.legend(handles=[Patch(color='#d47922',label='Historical cropland overlap: 50.70 km²'),Patch(color='#388db0',label='Other classified land: 1.58 km²'),Patch(color='#b93e79',label='Unknown land cover: 1.29 km²')],loc='upper right',bbox_to_anchor=(1,.76),frameon=True,fontsize=9)
footer(fig);fig.savefig(p/'Final_district_map.png',dpi=230);plt.close(fig)

fig,ax=base('Proportional cropland exposure by block','Share of mapped 2024–25 cropland intersecting the 4 September 2026 inundation')
b['display_class']=b.baseline_crop_overlap_pct.map(lambda x:0 if x==0 else 1 if x<=5 else 2 if x<=10 else 3 if x<=15 else 4)
colors=['#eeeeea','#d4e7d8','#89c2a6','#369681','#096856']
b.plot(ax=ax,column='display_class',cmap=ListedColormap(colors),norm=BoundaryNorm([-.5,.5,1.5,2.5,3.5,4.5],5),edgecolor='#ffffff',linewidth=1)
for _,r in b.iterrows():
 pt=r.geometry.representative_point()
 name=r.Sub_dist.replace('Simri Bakhtiarpur','Simri\nBakhtiarpur').replace('Satar Kataiya','Satar\nKataiya').replace('Banma Itahri','Banma\nItahri')
 ax.text(pt.x,pt.y,f'{name}\n{r.baseline_crop_overlap_pct:.2f}%',ha='center',va='center',fontsize=8,color='white' if r.display_class>=3 else '#243c36')
ax.legend(handles=[Patch(color=c,label=l) for c,l in zip(colors,['0: no mapped overlap','>0–5%','>5–10%','>10–15%','>15%'])],loc='upper right',bbox_to_anchor=(1,.75),title='Baseline cropland intersected',fontsize=9,title_fontsize=9)
footer(fig);fig.savefig(p/'Final_block_map.png',dpi=230);plt.close(fig)

(p/'Methodology_and_findings.md').write_text((p.parent/'docs/Methodology_and_findings.md').read_text())
f=p/'Results.html';s=f.read_text();addition='<h2>Prepared maps</h2><p><a href="Final_district_map.png">District exposure map</a> · <a href="Final_block_map.png">Block exposure map</a> · <a href="Methodology_and_findings.md">Methodology and findings</a></p><img style="max-width:1000px" src="Final_district_map.png"><img style="max-width:1000px" src="Final_block_map.png">'
s=s.replace('</body>',addition+'</body>');f.write_text(s)
print('Created two maps and methodology; updated Results.html')
