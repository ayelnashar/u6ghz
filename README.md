# Upper 6 GHz Interference and Coexistence Simulator

Open-source simulator and notebook for the paper:

> A. Elnashar, M. A. El-saidny and S. Muhaidat, "Interference and Coexistence in the Upper 6 GHz Band: A Practical Framework for 5G-Advanced and 6G Giga-MIMO Deployment," *IEEE Open Journal of the Communications Society*, 2026. [IEEE Xplore](https://ieeexplore.ieee.org/document/11774859)

The framework evaluates the Upper 6 GHz band (6425–7125 MHz, 3GPP band n104, TDD) between a Giga-MIMO mobile network and three victim systems: Fixed Service links, geostationary FSS satellite uplinks and Wi-Fi. The 3.5 GHz comparison layer is 5G NR band n78.

**Interactive simulator:** https://etisalat-uae-lab.github.io/u6ghz/

> **Version 1.1 corrects the code published with the paper (v1.0).** The corrections cover the Fixed-Service dish pattern, the Wi-Fi channel raster, spectral coupling and clutter loss. Some results therefore differ from the values printed in the paper. [CHANGELOG.md](CHANGELOG.md) lists every change, the affected numbers, and the status of each finding from the external review. The v1.0 code is kept under the `v1.0` tag.

This is a research tool. A PASS or FAIL applies a study criterion to a synthetic hexagonal network. It is not a regulatory compliance result and not an assessment of any operator's network.

## Contents

| Path | What it is |
|---|---|
| `docs/index.html` | Interactive browser simulator: a single self-contained page with no installation |
| `notebook/U6GHz_Simulator.ipynb` | Full simulation framework, executed, with all outputs |
| `figures/` | Figures produced by the notebook |
| `tests/` | Regression tests: the notebook and the browser must give the same results |
| `CHANGELOG.md` | Corrections in v1.1 and their effect on the published results |

## Interactive simulator

Open `docs/index.html` in any modern browser. It runs offline (the fonts load from Google Fonts when online). To publish it, enable GitHub Pages with source **Deploy from a branch**, branch `main`, folder `/docs`.

The page covers:
- **Operator block:** the reference block (6525–6725 MHz) or the UAE assignment (6425–6775 MHz).
- **Wi-Fi channel:** any channel on the 802.11ax 6 GHz raster.
- **Fixed-Service victim:** co-channel or adjacent placement, distance, bearing, dish pointing and the clutter assumption.
- **Mitigations:** EIRP reduction and beam avoidance.
- **Monte Carlo:** snapshot count and random seed.
- **Terminal–Wi-Fi coupling:** device, distance and spectrum relation.

**Copy scenario link** stores the current settings in the URL.

## Running the notebook

```bash
pip install -r requirements.txt
jupyter notebook notebook/U6GHz_Simulator.ipynb
```

Select **Run All**. Only `numpy` and `matplotlib` are needed, and a full run takes under a minute on a laptop. `pycraf` is optional: it is used only to regenerate the tabulated ITU-R P.452-16 path loss (`generate_p452_table()`).

## Regression tests

```bash
python tests/check_notebook.py    # notebook models against tests/reference_values.json
node tests/check_browser.js       # browser models against the same values
```

Both compare 68 values: Fixed-Service cases (mitigations, bearings, clutter, pointing, distance, seed), the FSS result, the Wi-Fi trial matrix, coverage, cell-edge SNR, terminal coupling and the Resolution 220 check. v1.1 matches to 1e-13 dB.

## Models

| Component | Model |
|---|---|
| Mobile path loss | 3GPP TR 38.901 UMa NLOS, floored at free-space loss (ITU-R P.525) |
| Building entry loss | ITU-R P.2109 at the carrier frequency (median) |
| Indoor loss | ITU-R P.1238 |
| Fixed-Service path | ITU-R P.452-16, smooth earth, 20% time, Dubai radio climate (tabulated with pycraf 2.1.0) |
| Clutter at the base station | ITU-R P.2108-1 §3.2, with location variability and below-rooftop shares |
| IMT antenna | ITU-R M.2101 composite array, exact (64, 128 and 256 TRX) |
| Fixed-Service antenna | ITU-R F.1245-3 average pattern |
| Satellite | GSO at 50°E seen from 25°N, 55°E; free-space slant plus gaseous term; 20 dBi receive gain |
| Spectral coupling | Bandwidth-integrated: in-band share plus ACIR at the edge separation (3GPP TR 36.942 form) |
| Wi-Fi impact | Empirical airtime mapping calibrated to the BT/Nokia Adastral Park U6 GHz trial (2025), with a primary-channel fallback |
| Resolution 220 | Illustrative expected-EIRP check, zero mechanical tilt |

Two engines share these models:
- **Engine A:** Monte Carlo aggregate interference into Fixed Service and FSS receivers (400 snapshots, 80th percentile).
- **Engine B:** deterministic link budgets for mobile–Wi-Fi coexistence, terminal coupling and the U6 GHz versus 3.5 GHz coverage comparison.

The satellite I/N assumes uniform power spectral density across the operator block and a satellite receiver bandwidth fully inside it.

## Notebook structure

| Section | Content |
|---|---|
| 1–6 | Setup, propagation, antennas, geometry, configuration, spectral coupling and Wi-Fi raster |
| 7 | Engine B, with the measured-versus-predicted trial table |
| 8 | Engine A, and the Resolution 220 expected-EIRP function |
| 9–10 | Mitigation functions and component checks |
| 11 | Results behind paper Figs. 1 and 3–8, recomputed |
| 12 | Terminal–Wi-Fi coupling (paper Fig. 9) |
| 13 | Robustness: victim bearing, clutter, seeds, convergence, Resolution 220 |
| 14 | Sensitivity (paper Figs. 10 and 11) |
| 15 | Table of differences from the published values |

## Scope and limitations

- **Geometry:** results apply to the geometries, calibration cases and mitigation settings evaluated.
- **Fixed-Service margins:** these rest on clutter loss at the base stations. With no clutter, or with realistic below-rooftop shares, no evaluated mitigation protects a dish aimed at the cluster.
- **Victim bearing:** the margin also depends on where the victim sits relative to the sector orientation.
- **Wi-Fi model:** the model is empirical and calibrated to one trial; the primary-channel fallback is not calibrated. Of the 15 trial states, 11 are within 5%; 221/80 with an active UE is predicted at 41 against 336 Mbit/s measured.
- **Not modelled:** interference into the serving base-station receiver, FSS earth stations and radio astronomy.

See [CHANGELOG.md](CHANGELOG.md) for the full list.

## Citation

Please cite the paper (see `CITATION.cff`):

```bibtex
@article{elnashar2026u6ghz,
  author  = {Elnashar, Ayman and El-saidny, Mohamed A. and Muhaidat, Sami},
  title   = {Interference and Coexistence in the Upper 6 {GHz} Band: A Practical Framework for {5G}-Advanced and {6G} Giga-{MIMO} Deployment},
  journal = {IEEE Open Journal of the Communications Society},
  year    = {2026},
  url     = {https://ieeexplore.ieee.org/document/11774859}
}
```

## Repositories

- Paper link: https://github.com/ayelnashar/u6ghz
- Lab repository: https://github.com/etisalat-uae-lab/u6ghz

Both hold the same code.

## License

MIT. See `LICENSE`.

## Contact

Ayman Elnashar, ayman.elnashar@ku.ac.ae
