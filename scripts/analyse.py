from pathlib import Path
import zipfile,json
import numpy as np
import rasterio
from rasterio.features import shapes
import geopandas as gpd
from shapely.geometry import shape
from shapely import union_all,make_valid
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'results'
OUT.mkdir(exist_ok=True)
SRC=ROOT/'downloads'/'LULC_2024_25_request27776'
SRC.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(ROOT/'inputs'/'lulc_request.zip') as z:
 for n in ['lulc250k_2425_27776.tif','LULC_Classes.txt','readme.txt','lulc_classes.JPG']:
  (SRC/n).write_bytes(z.read(n))
labels={1:'Built-up',2:'Kharif crop',3:'Rabi crop',4:'Zaid crop',5:'Double/triple/annual crop',6:'Current fallow',7:'Plantation/orchard',8:'Evergreen/semi-evergreen woodland',9:'Deciduous woodland',10:'Degraded woodland',11:'Littoral/swamp/mangroves',12:'Grassland',13:'Shifting cultivation',14:'Wasteland',15:'Rann',16:'Waterbodies max spread',17:'Waterbodies min spread',18:'Snow/glacial areas'}
p=ROOT/'inputs/September4_administrative_exposure.gpkg'
v=gpd.read_file(p,layer='saharsa_villages')
b=gpd.read_file(p,layer='saharsa_blocks')
wet=make_valid(union_all(gpd.read_file(p,layer='saharsa_mapped_inundation').geometry))
aoi=make_valid(union_all(v.geometry))
with rasterio.open(SRC/'lulc250k_2425_27776.tif') as r:
 a=r.read(1)
 records=[{'class_id':int(val),'geometry':shape(geom)} for geom,val in shapes(a,mask=a!=0,transform=r.transform)]
 lc=gpd.GeoDataFrame(records,crs=r.crs).to_crs(v.crs)
print('Polygonized regions',len(lc),flush=True)
lc.geometry=lc.geometry.make_valid()
lc=lc.dissolve(by='class_id').reset_index()
lc.geometry=lc.geometry.intersection(aoi)
lc=lc[~lc.is_empty].copy()
lc['class_name']=lc.class_id.map(labels)
valid=union_all(lc.geometry)
covered=wet.intersection(valid)
ex=lc.copy();ex.geometry=ex.geometry.intersection(wet)
ex['overlap_km2']=ex.area/1e6
ex=ex[ex.overlap_km2>0].copy()
rows=[{'class_id':int(r.class_id),'class_name':r.class_name,'overlap_km2':float(r.overlap_km2)} for _,r in ex.iterrows()]
crop=union_all(lc[lc.class_id.isin([2,3,4,5])].geometry)
cropwet=wet.intersection(crop)
for d in [v,b]:
 d['crop_overlap_km2']=d.geometry.intersection(cropwet).area/1e6
 d['lulc_covered_wet_km2']=d.geometry.intersection(covered).area/1e6
 d['lulc_uncovered_wet_km2']=d.geometry.intersection(wet.difference(valid)).area/1e6
 d['baseline_crop_km2']=d.geometry.intersection(crop).area/1e6
 d['baseline_crop_overlap_pct']=np.where(d.baseline_crop_km2>0,100*d.crop_overlap_km2/d.baseline_crop_km2,np.nan)
check=abs(ex.overlap_km2.sum()-covered.area/1e6)
assert check<1e-5,check
assert abs(v.crop_overlap_km2.sum()-cropwet.area/1e6)<1e-3
assert abs(b.crop_overlap_km2.sum()-cropwet.area/1e6)<1e-3
out=OUT/'September4_landcover_exposure.gpkg'
if out.exists():out.unlink()
for d,name in [(ex,'inundation_by_landcover'),(v,'village_crop_overlap'),(b,'block_crop_overlap')]:
 d.to_file(out,layer=name,driver='GPKG')
summary={'event':'2026-09-04 NRSC 1800hrs product','baseline':'NRSC LULC 2024-25, 1:250,000','mapped_inundation_km2':wet.area/1e6,'lulc_covered_inundation_km2':covered.area/1e6,'lulc_uncovered_inundation_km2':wet.difference(valid).area/1e6,'baseline_cropland_overlap_km2':cropwet.area/1e6,'crop_classes':[2,3,4,5],'classes':rows,'blocks':b[['Sub_dist','crop_overlap_km2']].sort_values('crop_overlap_km2',ascending=False).to_dict('records'),'villages_positive_crop_overlap':int((v.crop_overlap_km2>0).sum())}
(OUT/'summary.json').write_text(json.dumps(summary,indent=2))
fig,ax=plt.subplots(figsize=(9,10))
gpd.GeoSeries([aoi],crs=v.crs).plot(ax=ax,color='#f3f1e9',edgecolor='#666666',linewidth=.7)
gpd.GeoSeries([wet],crs=v.crs).plot(ax=ax,color='#55a8d8')
gpd.GeoSeries([cropwet],crs=v.crs).plot(ax=ax,color='#d77720')
ax.set_aspect('equal');ax.set_axis_off()
ax.set_title('Saharsa | Mapped inundation over baseline cropland\n4 September 2026 inundation × 2024–25 land cover',fontsize=13,pad=14)
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color='#d77720',label='Inundation intersecting baseline cropland'),Patch(color='#55a8d8',label='Other mapped inundation')],loc='upper right',fontsize=9)
fig.text(.06,.025,'Sources: NRSC/ISRO and Survey of India. Areas in UTM 45N.\nLULC mapping scale 1:250,000. Screening estimate; not observed crop damage.',fontsize=9)
fig.savefig(OUT/'Cropland_overlap.png',dpi=170,bbox_inches='tight');plt.close(fig)
html='<html><head><meta charset="utf-8"><title>Saharsa cropland overlap</title><style>body{font:16px system-ui;max-width:1100px;margin:40px auto;color:#24313b}table{border-collapse:collapse;width:100%;margin:20px 0}td,th{padding:8px;border-bottom:1px solid #ddd;text-align:left}img{max-width:700px;width:100%}</style></head><body><h1>Saharsa: land-cover exposure to mapped inundation</h1>'
html+=f'<p>NRSC mapped inundation, 4 September 2026, intersects <b>{cropwet.area/1e6:.2f} km² of baseline cropland</b> classified in 2024–25. This is not a measurement of standing crops, crop damage or yield loss.</p>'
html+=f'<p>Mapped inundation: {wet.area/1e6:.3f} km². LULC coverage within it: {covered.area/1e6:.3f} km². Unclassified/NoData overlap: {wet.difference(valid).area/1e6:.3f} km².</p>'
html+='<img src="Cropland_overlap.png"><h2>Land-cover intersections</h2>'+ex[['class_id','class_name','overlap_km2']].to_html(index=False,float_format=lambda x:f'{x:.4f}')
html+='<h2>Block screening</h2>'+b[['Sub_dist','crop_overlap_km2']].sort_values('crop_overlap_km2',ascending=False).to_html(index=False,float_format=lambda x:f'{x:.4f}')
html+='<h2>Village screening</h2><p>Small intersections should not be interpreted as precise field-level estimates at this mapping scale.</p>'+v.loc[v.crop_overlap_km2>0,['Vill_name','Vill_LGD','Sub_dist','crop_overlap_km2']].sort_values('crop_overlap_km2',ascending=False).to_html(index=False,float_format=lambda x:f'{x:.4f}')
html+='<h2>Method and limitations</h2><p>Native raster class regions were polygonized without resampling, projected to EPSG:32645 and intersected with unioned NRSC inundation clipped to SOI-derived Saharsa. Partial pixels are represented by geometric intersections. Crop classes 2–5 are grouped; fallow and plantations/orchards remain separate. Class sums and village/block totals were checked against district totals.</p><p>The 2024–25 baseline predates the September 2026 event. NRSC inundation is preliminary and can include wet areas/rainwater accumulation. This analysis uses the official inundation product, not the experimental SAR thresholds. Fine output geometry does not improve the source mapping scale of 1:250,000. NoData is not assumed to be non-cropland. Raw LULC data retain the supplied NRSC terms; this local analysis does not establish redistribution permission.</p></body></html>'
(OUT/'Results.html').write_text(html)
print(json.dumps(summary,indent=2))
