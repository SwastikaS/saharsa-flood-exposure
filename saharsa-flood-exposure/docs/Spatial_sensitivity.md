# Spatial alignment sensitivity

Hypothetical translations of the entire LULC crop mask and valid-data mask relative to fixed NRSC inundation and SOI boundaries. Crop classes 2–5 were grouped on the native grid, polygonized without resampling, projected to UTM 45N and shifted before clipping to Saharsa. Block percentages use the shifted valid cropland denominator.

Offsets of 50 m and 100 m are illustrative stress tests of approximately one and two raster cells, not measured positional errors, source-accuracy specifications, statistical confidence bounds or classification validation. Only cardinal translations were tested. Seasonal land-cover change and class errors are not represented.

| Scenario | Cropland overlap km² | Change from baseline % | Unknown inundation km² |
|---|---:|---:|---:|
| Baseline | 50.699 | +0.00 | 1.292 |
| East 50 m | 50.644 | -0.11 | 1.446 |
| West 50 m | 50.225 | -0.93 | 1.162 |
| North 50 m | 50.307 | -0.77 | 1.647 |
| South 50 m | 50.596 | -0.20 | 1.054 |
| East 100 m | 50.040 | -1.30 | 1.630 |
| West 100 m | 49.566 | -2.23 | 1.073 |
| North 100 m | 49.447 | -2.47 | 2.075 |
| South 100 m | 50.310 | -0.77 | 0.895 |

## Block stability

| Block | Overlap range km² | Share range % | Area rank range | Share rank range |
|---|---:|---:|---:|---:|
| Nauhatta | 12.91–13.47 | 14.73–15.25 | 2–2 | 1–1 |
| Satar Kataiya | 0.00–0.00 | 0.00–0.00 | 7–7 | 7–7 |
| Mahishi | 17.15–17.71 | 12.66–13.16 | 1–1 | 2–2 |
| Kahara | 0.00–0.00 | 0.00–0.00 | 7–7 | 7–7 |
| Saur Bazar | 0.00–0.00 | 0.00–0.00 | 7–7 | 7–7 |
| Patarghat | 0.00–0.00 | 0.00–0.00 | 7–7 | 7–7 |
| Sonbarsa | 0.92–0.98 | 0.55–0.58 | 6–6 | 6–6 |
| Simri Bakhtiarpur | 1.64–1.73 | 1.12–1.18 | 5–5 | 5–5 |
| Salkhua | 9.87–10.33 | 7.92–8.24 | 3–3 | 4–4 |
| Banma Itahri | 6.52–6.72 | 10.22–10.48 | 4–4 | 3–3 |

Zero-overlap blocks have tied ranks. Stable rankings in these scenarios do not establish that the original classification is correct.