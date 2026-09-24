from pathlib import Path
import json
import geopandas as g
import rasterio
from rasterio.features import shapes
from shapely.geometry import shape
from shapely import union_all
from shapely.affinity import translate
root=Path(__file__).resolve().parents[1]
p=root/'results'
b=g.read_file(p/'September4_landcover_exposure.gpkg',layer='block_crop_overlap')
w=union_all(g.read_file(root/'inputs/September4_administrative_exposure.gpkg',layer='saharsa_mapped_inundation').geometry)
aoi=union_all(b.geometry)
with rasterio.open(root/'downloads/LULC_2024_25_request27776/lulc250k_2425_27776.tif') as r:
 a=r.read(1)
 import numpy as np
 binary=np.isin(a,[2,3,4,5]).astype('uint8')
 crop=g.GeoSeries([shape(x) for x,v in shapes(binary,mask=binary==1,transform=r.transform)],crs=r.crs).to_crs(b.crs).make_valid()
 valid=g.GeoSeries([shape(x) for x,v in shapes((a!=0).astype('uint8'),mask=a!=0,transform=r.transform)],crs=r.crs).to_crs(b.crs).make_valid()
crop=union_all(crop);valid=union_all(valid)
scenarios=[('Baseline',0,0)]+[(f'{direction} {distance} m',dx*distance,dy*distance) for distance in [50,100] for direction,dx,dy in [('East',1,0),('West',-1,0),('North',0,1),('South',0,-1)]]
results=[]
for name,dx,dy in scenarios:
 c=translate(crop,dx,dy).intersection(aoi)
 overlap=c.intersection(w)
 d=b[['Sub_dist','geometry']].copy()
 d['crop_overlap_km2']=d.geometry.intersection(overlap).area/1e6
 d['baseline_crop_km2']=d.geometry.intersection(c).area/1e6
 d['share_pct']=100*d.crop_overlap_km2/d.baseline_crop_km2
 d['area_rank']=d.crop_overlap_km2.rank(ascending=False,method='min').astype(int)
 d['share_rank']=d.share_pct.rank(ascending=False,method='min').astype(int)
 result={'scenario':name,'dx_m':dx,'dy_m':dy,'crop_overlap_km2':overlap.area/1e6,'unknown_wet_km2':w.difference(translate(valid,dx,dy)).area/1e6,'blocks':d.drop(columns='geometry').to_dict('records')}
 results.append(result)
 print(name,round(result['crop_overlap_km2'],3),flush=True)
base=results[0]['crop_overlap_km2']
assert abs(base-50.69851570489186)<.001
for r in results:r['change_pct']=100*(r['crop_overlap_km2']/base-1)
(p/'Spatial_sensitivity.json').write_text(json.dumps(results,indent=2))
lines=['# Spatial alignment sensitivity','', 'Hypothetical translations of the entire LULC crop mask and valid-data mask relative to fixed NRSC inundation and SOI boundaries. Crop classes 2–5 were grouped on the native grid, polygonized without resampling, projected to UTM 45N and shifted before clipping to Saharsa. Block percentages use the shifted valid cropland denominator.','', 'Offsets of 50 m and 100 m are illustrative stress tests of approximately one and two raster cells, not measured positional errors, source-accuracy specifications, statistical confidence bounds or classification validation. Only cardinal translations were tested. Seasonal land-cover change and class errors are not represented.','', '| Scenario | Cropland overlap km² | Change from baseline % | Unknown inundation km² |','|---|---:|---:|---:|']
for r in results:lines.append(f"| {r['scenario']} | {r['crop_overlap_km2']:.3f} | {r['change_pct']:+.2f} | {r['unknown_wet_km2']:.3f} |")
lines+=['','## Block stability','', '| Block | Overlap range km² | Share range % | Area rank range | Share rank range |','|---|---:|---:|---:|---:|']
for name in b.Sub_dist:
 q=[x for r in results for x in r['blocks'] if x['Sub_dist']==name]
 vals=lambda k:f"{min(x[k] for x in q):.2f}–{max(x[k] for x in q):.2f}"
 ranks=lambda k:f"{min(x[k] for x in q)}–{max(x[k] for x in q)}"
 lines.append(f"| {name} | {vals('crop_overlap_km2')} | {vals('share_pct')} | {ranks('area_rank')} | {ranks('share_rank')} |")
lines+=['','Zero-overlap blocks have tied ranks. Stable rankings in these scenarios do not establish that the original classification is correct.']
(p/'Spatial_sensitivity.md').write_text('\n'.join(lines))
print('\n'.join(lines))
