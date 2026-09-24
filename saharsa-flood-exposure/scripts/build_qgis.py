from pathlib import Path
from qgis.core import *
from qgis.PyQt.QtGui import QColor
p=Path(__file__).resolve().parents[1]/'results'
app=QgsApplication([],False);app.initQgis()
proj=QgsProject.instance();proj.setCrs(QgsCoordinateReferenceSystem('EPSG:32645'))
proj.setFilePathStorage(Qgis.FilePathType.Relative)
proj.setTitle('Saharsa agricultural-land exposure | 4 September 2026')

def layer(name,title):
 l=QgsVectorLayer(str(p/'September4_landcover_exposure.gpkg')+'|layername='+name,title,'ogr')
 assert l.isValid(),title
 proj.addMapLayer(l);return l
blocks=layer('block_crop_overlap','Blocks — share of historical cropland intersected (%)')
ranges=[]
for lo,hi,color,label in [(0,0,'#eeeeea','0: no mapped overlap'),(.000000001,5,'#d4e7d8','>0–5%'),(5,10,'#89c2a6','>5–10%'),(10,15,'#369681','>10–15%'),(15,100,'#096856','>15%')]:
 s=QgsFillSymbol.createSimple({'color':color,'outline_color':'#ffffff','outline_width':'0.3'})
 ranges.append(QgsRendererRange(lo,hi,s,label))
blocks.setRenderer(QgsGraduatedSymbolRenderer('baseline_crop_overlap_pct',ranges))
settings=QgsPalLayerSettings();settings.fieldName='"Sub_dist" || \'\\n\' || format_number("baseline_crop_overlap_pct", 2) || \'%\'';settings.isExpression=True
fmt=QgsTextFormat();fmt.setSize(9);buf=QgsTextBufferSettings();buf.setEnabled(True);buf.setSize(.8);buf.setColor(QColor('white'));fmt.setBuffer(buf);settings.setFormat(fmt)
blocks.setLabeling(QgsVectorLayerSimpleLabeling(settings));blocks.setLabelsEnabled(True)
v=layer('village_crop_overlap','Village screening — historical cropland overlap')
proj.layerTreeRoot().findLayer(v.id()).setItemVisibilityChecked(False)
e=layer('inundation_by_landcover','Inundation intersections by 2024–25 land-cover class')
colors={1:'#cc3030',2:'#d47922',3:'#d47922',4:'#d47922',5:'#d47922',6:'#c8b291',7:'#ae6fa9',9:'#449c55',16:'#388db0',17:'#1c6587'}
cats=[]
for f in e.getFeatures():
 n=int(f['class_id']);s=QgsFillSymbol.createSimple({'color':colors.get(n,'#999999'),'outline_style':'no'})
 cats.append(QgsRendererCategory(n,s,str(f['class_name'])))
e.setRenderer(QgsCategorizedSymbolRenderer('class_id',cats));proj.layerTreeRoot().findLayer(e.id()).setItemVisibilityChecked(False)
proj.viewSettings().setDefaultViewExtent(QgsReferencedRectangle(blocks.extent(),blocks.crs()))
proj.setFileName(str(p/'Saharsa_exposure.qgz'));assert proj.write()
proj.clear();assert proj.read(str(p/'Saharsa_exposure.qgz'))
assert all(l.isValid() for l in proj.mapLayers().values())
print('Saved and reopened project: all',len(proj.mapLayers()),'layers valid')
