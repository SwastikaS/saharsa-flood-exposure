# Agricultural land exposed to the 4 September 2026 inundation in Saharsa, Bihar

## Objective
Identify how much historical agricultural land intersects an official inundation product, and compare exposure by administrative block. This is an exposure assessment using official inundation, not a new flood-detection algorithm.

## Inputs
- NRSC inundation: ndem50d:brflood50dsc04092026_1800hrs; 4 September 2026, 1800 hrs product. Original polygons preserved in project downloads. Preliminary mapped wet/inundated areas may include rainwater accumulation; no independent field validation was conducted.
- NRSC annual LULC: lulc250k_2425_27776.tif, 2024–25, request 27776, supplied by the user in Swastika16 Request.zip. Source mapping scale 1:250,000. Class legend and supplied terms preserved with the raster.
- SOI Bihar village boundaries supplied by the user. Village polygons dissolved by district and subdistrict LGD code; supplied SOI metadata identifies edition 2025, Bihar harmonisation with ORGI in 2025, publication 8 May 2026, and source scale 1:50,000 (SOI/ABDB/VECTOR/50000/2025/VILLAGE/INDIA).

## Reproducible method
1. Use the previously unioned NRSC inundation clipped to the SOI-derived Saharsa district, preventing overlapping source polygons from being counted twice.
2. Read the LULC class legend. Group classes 2 (Kharif), 3 (Rabi), 4 (Zaid) and 5 (double/triple/annual crop) as historical cropland. Keep fallow (6), plantations/orchards (7) and other classes separate.
3. Polygonize valid native LULC pixels without resampling. Reproject class polygons to WGS 84 / UTM zone 45N (EPSG:32645), repair geometry and dissolve by class. Clip to district and intersect with inundation. Partial pixel intersections contribute their intersected area; this geometry does not improve the original mapping scale.
4. Sum cropland intersections by SOI village and block. Percentage exposure = intersected historical cropland area / all valid mapped historical cropland in the same block × 100. NoData is excluded from the denominator and separately reported within inundation.
5. Check summed class areas against covered inundation (difference <10 m²), and village/block sums against district cropland overlap (difference <0.001 km²). Verify percentages algebraically and verify no overlap exceeds its cropland denominator.
6. Visually review native LULC, SOI boundaries and NRSC outlines in Mahishi, Nauhatta and Salkhua. No gross coordinate displacement was apparent. This is not a measured registration test or independent accuracy assessment.

## Findings
- Mapped inundation within Saharsa: 53.571 km².
- Historical cropland intersection: 50.699 km² (about 5,070 hectares).
- Other classified land intersection: 1.580 km².
- Inundation without LULC coverage: 1.292 km².
- Mahishi leads by cropland overlap area (17.66 km²); Nauhatta leads by proportional exposure (15.25%).
- Banma Itahri ranks fourth by overlap area but third by percentage (10.41%).
- Four blocks have no overlap in this product. This does not prove absence of flooding.

## Interpretation and limitations
The LULC baseline predates the event. In particular, 25.98 km² of the cropland overlap is mapped as Rabi crop in 2024–25. Do not describe all intersections as standing September crops, damaged crops, yield loss, affected farmers or monetary loss. The result supports broad district/block screening. Village values are exploratory, and tiny intersections are sensitive to scale and boundary differences. The LULC valid boundary differs from SOI boundaries, especially near Nauhatta. The missing 1.292 km² remains unknown.

The earlier June/September SAR thresholds remain exploratory: differing acquisition geometry and threshold sensitivity prevent treating them as validated flood extents. They were not used to define the inundation for these exposure results.

## Sources and attribution
NRSC LULC 2024–25 and NRSC inundation product, National Remote Sensing Centre, ISRO, Government of India, Hyderabad, India. Administrative geometry: Survey of India, Bihar village dataset supplied by the user.
Official event report: https://ndem.nrsc.gov.in/documents/Disaster_Document/2026/BR/brflood50dsc04092026_1800hrs/brflood50dsc04092026_1800hrs_report.pdf

## Remaining submission checks
Confirm competition deliverable format, and redistribution compatibility of supplied datasets/derived layers before public packaging. The supplied LULC readme contains usage and redistribution conditions; it should not be presumed to grant an unrestricted open-data license. No data have been published or submitted by this workflow. The local workflow produces a styled QGIS project as Saharsa_exposure.qgz; that output is not bundled in this repository. Submission-form-specific formatting remains to be confirmed.

## SDG relevance
This screening assessment supports SDG 13 (Climate Action) through disaster-exposure information and SDG 2 (Zero Hunger) through identification of agricultural land intersecting mapped inundation. It does not quantify an SDG indicator or attribute the event to climate change.
