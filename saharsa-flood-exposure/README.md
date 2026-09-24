# Saharsa agricultural-land exposure

Working draft for GeoMapathon 2026. This project intersects official NRSC mapped inundation from 4 September 2026 with NRSC 2024–25 land cover and Survey of India administrative boundaries.

It is an exposure overlay, not an independently validated flood-detection model or crop-damage estimate. The current estimate is 50.70 km² of historical cropland intersecting mapped inundation. Mahishi has the largest overlap; Nauhatta the highest percentage of mapped baseline cropland.

## Status
Preliminary analysis with source-scale, temporal and spatial uncertainty. An initial spatial-alignment sensitivity check is complete; independent validation and other sources of uncertainty remain outstanding. Not a final competition submission.

## Reproduce locally
Use Python with the packages in requirements.txt. Obtain the source data under their applicable terms. Place the LULC ZIP as inputs/lulc_request.zip and the prepared administrative/inundation GeoPackage as inputs/September4_administrative_exposure.gpkg. The latter must contain saharsa_villages, saharsa_blocks and saharsa_mapped_inundation in EPSG:32645; it is a required preprocessing artifact, not bundled here.

Run scripts/analyse.py, then scripts/block_comparison.py, then scripts/final_maps.py. These write local outputs under results/. Run scripts/build_qgis.py using a QGIS Python environment to create a styled project. Rerun analyse.py before rebuilding the HTML report to avoid duplicate appended map sections.

## Data and attribution
NRSC/ISRO: 2024–25 annual LULC at 1:250,000 and the 4 September 2026 inundation product. Survey of India: ABDB village boundaries, edition 2025, Bihar harmonisation 2025, metadata publication 8 May 2026.

Source datasets and derived spatial layers are excluded while redistribution terms remain unresolved. No open license for third-party data is implied. See docs/Methodology_and_findings.md for the method and limitations.

## Spatial sensitivity
Eight hypothetical cardinal shifts (50 m and 100 m) of the land-cover layer produced 49.45–50.70 km² overlap including baseline, with a maximum decrease of 2.47%. Block rankings were unchanged. These are stress tests, not confidence intervals or measured positional errors. See [full findings](docs/Spatial_sensitivity.md). Run `python scripts/spatial_sensitivity.py` after the main analysis to reproduce them.
