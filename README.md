# Upper 6 GHz Interference and Coexistence Simulator

Code and interactive simulator for the paper:

> A. Elnashar, M. A. El-saidny and S. Muhaidat, "Interference and Coexistence in the Upper 6 GHz Band: A Practical Framework for 5G-Advanced and 6G Giga-MIMO Deployment," *IEEE Open Journal of the Communications Society*, 2026. DOI: *to be added*.

The framework evaluates the Upper 6 GHz band (6425–7125 MHz, 3GPP band n104, TDD) between a Giga-MIMO mobile network and three victim systems: Fixed Service links, geostationary FSS satellite uplinks and Wi-Fi. The 3.5 GHz comparison layer is 5G NR band n78.

## Contents

| Path | What it is |
|---|---|
| `notebook/U6GHz_Simulator.ipynb` | Full simulation framework, with the outputs behind every result figure in the paper |
| `docs/index.html` | Interactive browser simulator: a single self-contained page, no installation needed |
| `figures/` | Figures produced by the notebook, named after the paper figures |

## Interactive simulator

Open `docs/index.html` in any modern browser. It runs offline and needs no server.

To publish it online, enable GitHub Pages for this repository with source **Deploy from a branch**, branch `main`, folder `/docs`. The simulator is then served at `https://<user>.github.io/u6ghz-coexistence-simulator/`.

## Running the notebook

```bash
pip install -r requirements.txt
jupyter notebook notebook/U6GHz_Simulator.ipynb
```

Then select **Run All**. The notebook needs only `numpy` and `matplotlib`; all propagation and antenna models are embedded. A full run takes about 3 minutes on a laptop and writes the figure files to the working directory.

`pycraf` is optional. It is used only to regenerate the tabulated ITU-R P.452-16 path loss (`generate_p452_table()`); the shipped table was produced with pycraf 2.1.0.

## Models

| Component | Model |
|---|---|
| Mobile path loss | 3GPP TR 38.901 UMa NLOS; free space (ITU-R P.525) |
| Building entry and indoor loss | ITU-R P.2109, ITU-R P.1238 |
| Clutter loss at the base station | ITU-R P.2108 |
| Fixed Service path | ITU-R P.452-16 (tabulated); protection criterion ITU-R F.758 |
| IMT antenna | ITU-R M.2101 composite array pattern (64, 128 and 256 TRX) |
| Fixed Service and FSS antennas | ITU-R F.1245, ITU-R S.672 |
| Spectral coupling | ACIR with emission-mask roll-off (3GPP TR 36.942, TS 38.104) |
| Wi-Fi impact | Empirical airtime-loss mapping, calibrated to the BT/Nokia Adastral Park U6 GHz trial (2025) |

Two engines share these models:

- **Engine A**: Monte Carlo aggregate interference into Fixed Service and FSS receivers.
- **Engine B**: deterministic link model for mobile–Wi-Fi coexistence and the U6 GHz versus 3.5 GHz coverage comparison.

## Notebook structure and paper figures

| Notebook section | Paper |
|---|---|
| 1–6. Setup, propagation, antennas, geometry, scenarios, ACIR | Section III, Tables 1–5, Eqs. (1)–(9) |
| 7. Engine B | Algorithm 2 |
| 8. Engine A | Algorithm 1 |
| 9. Mitigation techniques | Section V |
| 10. Validation checks | Model checks against ITU-R and pycraf reference values |
| 11. Results behind the paper figures | Figs. 1, 3, 4, 5, 6, 7, 8 |
| 12. Terminal–Wi-Fi coupling | Section VI.B, Fig. 9 |
| 13. Sensitivity analysis | Figs. 10 and 11 |
| 14. Summary | Key results |

## Validation

Section 10 runs automatic checks of the embedded models against reference values (for example, the ITU-R M.2101 256-TRX pattern against pycraf 2.1.0) and prints `All checks passed.` when the models are consistent.

## Scope

Results apply to the geometries, calibration cases and mitigation settings evaluated in the paper. The Wi-Fi model is empirical and calibrated to one field trial. Read the paper's limitations section before applying the results to other deployments.

## Citation

If you use this code, please cite the paper (see `CITATION.cff`):

```bibtex
@article{elnashar2026u6ghz,
  author  = {Elnashar, Ayman and El-saidny, Mohamed A. and Muhaidat, Sami},
  title   = {Interference and Coexistence in the Upper 6 {GHz} Band: A Practical Framework for {5G}-Advanced and {6G} Giga-{MIMO} Deployment},
  journal = {IEEE Open Journal of the Communications Society},
  year    = {2026},
  doi     = {TBD}
}
```

## License

MIT. See `LICENSE`.

## Contact

Ayman Elnashar, ayman.elnashar@ku.ac.ae
