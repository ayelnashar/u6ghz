# Changelog

## 1.1.0 (11 November 2026)

Version 1.1 corrects the v1.0 code published with the paper. The corrections follow an external technical review of the browser simulator and the notebook. Several of them change numerical results printed in the paper; the table below lists every changed headline value. The v1.0 code remains available under the `v1.0` tag.

The notebook and the browser simulator implement the same models and random-number generator. For the 68 regression values in `tests/`, they agree to within 1e-6.

### Model corrections

1. **Fixed-Service dish pattern (ITU-R F.1245-3).** v1.0 held the gain flat at G1 between 1° and 5° and then used 29 − 25 log φ. Neither matches the Recommendation for this antenna: the 42 dBi dish has D/λ ≈ 52, so the D/λ ≤ 100 branch applies (39 − 5 log(D/λ) − 25 log φ from φm ≈ 1.46°, and −3 − 5 log(D/λ) ≈ −11.6 dBi beyond 48°). Both branches are now implemented and unit-tested at 2°, 10° and 60°.
2. **Wi-Fi channel raster.** v1.0 centred a 160 MHz channel on its primary 20 MHz channel. A configuration such as 193/160 means primary channel 193 inside the standard 160 MHz channel. 193/160 and 221/160 are therefore the same channel, 6905–7065 MHz, which overlaps the 7010–7090 MHz trial carrier by 34.4%, not 0% and 50%. The default Wi-Fi channel in v1.0 (6975–7135 MHz) extended beyond the band edge.
3. **Spectral coupling.** v1.0 gave 0 dB rejection for any overlap and for exactly touching edges. Coupling is now bandwidth-integrated: the in-band share of the interferer's power is the overlap divided by its bandwidth, and the remainder is rejected by the ACIR at the actual edge separation. A Fixed-Service channel inside the block now uses the same function (8.50 dB), replacing a separate bandwidth term.
4. **Wi-Fi airtime model.** The rule that imposed zero loss whenever channels do not overlap is removed, so adjacent-channel leakage now enters the airtime model. The loss slope is refitted from 0.07 to 0.077 per dB so the calibrated worst case still equals the measured 62 Mbit/s. A primary-channel fallback (802.11 dynamic bandwidth) is added: if the primary 20 MHz channel is clear, the access point may use the widest clear sub-channel that contains it.
5. **Handset carrier.** The active handset transmits on one NR carrier of at most 100 MHz, placed at the block edge nearest the Wi-Fi channel. In v1.0 it transmitted across the whole operator block.
6. **Clutter loss (ITU-R P.2108-1 §3.2).** v1.0 used a constant 31.4 dB, which matches the P.2108-0 expression, while the paper cites P.2108-1. The P.2108-1 model (same structure as the NTIA reference implementation) now gives a median of 32.5 dB at 6.625 GHz and 5 km, with location variability.
7. **Building entry loss (ITU-R P.2109).** Now evaluated at each carrier frequency. v1.0 applied the 7 GHz value at 3.5 GHz as well (30.9 dB rather than 32.6 dB for low-E glass).
8. **Short-range path loss.** UMa NLOS is floored at free-space loss. At 5 m the UMa fit was 5.6 dB below free space.
9. **Satellite direction.** v1.0 drew a new random satellite azimuth for every sector and snapshot. The satellite now has one azimuth and elevation per site (191.7° and 60.2° for 50°E seen from 25°N, 55°E).
10. **Terminal antennas.** In the terminal-coupling panel the handheld now uses the same antenna in both directions: −4 dBi, 4 dB body loss, 26 dBm conducted, 18 dBm EIRP. In v1.0 it had 26 dBm EIRP for transmit and a 17 dBi array for receive. The same-room handset in the Wi-Fi calibration keeps 26 dBm EIRP, the level the airtime model is fitted to. The 4×4 array (17.0 dBi) is kept for the coverage comparison and is labelled as a fixed-wireless CPE.

### Added

- **Fixed-Service placement and geometry:** an explicit co-channel or adjacent Fixed-Service channel, an edge-clearance control, the victim bearing, and the dish pointing offset.
- **Clutter options:** clutter at all sites (the paper's assumption), WP 5D below-rooftop shares (65% urban, 15% suburban), or no clutter.
- **Robustness sweeps (notebook Section 13):** bearing (0–180°), clutter mode over 25 clutter draws, 20 random seeds, and 4000-snapshot convergence.
- **Resolution 220 check:** an illustrative expected-EIRP check against the Resolution 220 (WRC-23) mask (zero mechanical tilt).
- **Trial comparison:** a measured-versus-predicted table for all 15 Hubble states of the BT/Nokia trial (Fig. 7), in the notebook and on the page.
- **UAE assignment preset:** 6425–6775 MHz, 350 MHz, treated as NR carriers of up to 100 MHz.
- **Wi-Fi channel selection:** the full 6 GHz raster, including the lower 6 GHz band.
- **Regression tests (`tests/`):** these confirm that the notebook and the browser give the same results.

### Browser interface

- **Mitigation controls:** the AFC toggle, which had no effect, is removed; AFC acts through the assigned channel and clearance. The beam-avoidance, separation and clutter cards are computed from matched runs for the current settings, where v1.0 showed fixed or point-path values. The power control is renamed "EIRP reduction" and now also affects coverage and cell-edge results.
- **Cell-edge card:** relabelled as SNR (no inter-cell interference is modelled).
- **Criteria labels:** study criteria are marked as such and illustrative thresholds as illustrative. The Wi-Fi loss is shown as a positive percentage.
- **Frequency controls:** blocks are kept inside 6425–7125 MHz, the bandwidth step is 10 MHz, and the Wi-Fi channel is chosen by number and width.
- **Trial rows:** the trial reference rows in the Wi-Fi matrix are fixed and shown next to the measurements.
- **Page usability:** a research-tool notice, version, paper and repository links, reset, a shareable scenario link, larger chart text and higher contrast.

### Changed results relative to the published paper

| Quantity | Published (v1.0) | v1.1 |
|---|---|---|
| Wi-Fi 221/160 overlap with the trial carrier | 50% | 34.4% |
| Wi-Fi 221/160, no UE (trial 1777 Mbit/s) | 1640 Mbit/s | 1832 Mbit/s |
| Wi-Fi 221/160, idle UE (trial 1481 Mbit/s) | 1295 Mbit/s | 1487 Mbit/s |
| Wi-Fi 221/160, active UE (trial 62 Mbit/s) | 62 Mbit/s | 62 Mbit/s |
| Wi-Fi 193/160, active UE (trial 407 Mbit/s) | ≈2300 Mbit/s | 666 Mbit/s |
| U6/3.5 GHz throughput ratio at 200 m (U6 at 7050 MHz) | 1.75 | 1.75 (1.81 at 6625 MHz) |
| FS co-channel I/N, 37 sites, 5 km | +26.3 dB | +23.3 dB |
| FS co-channel exceedance of −10 dB | 36.3 dB | 33.3 dB |
| FS, 60 MHz clearance | +0.6 dB | −2.4 dB |
| FS, 60 MHz clearance + beam avoidance | −10.7 dB | −11.3 dB |
| FS, 120 MHz clearance + beam avoidance | −16.7 dB | −17.3 dB |
| FS, 120 MHz + avoidance, victim bearings 0–180° that pass | not evaluated | 8 of 13 (worst −8.5 dB at 30°) |
| FS, 60 MHz + avoidance, victim bearings 0–180° that pass | not evaluated | 3 of 13 |
| FS, 120 MHz + avoidance + 10 dB EIRP reduction | −26.7 dB | −27.3 dB (13 of 13 bearings pass) |
| FS beam-avoidance relief (co-channel) | 11.4 dB | 8.8 dB |
| FS dish pointing: criterion met beyond | about 40° | about 42° |
| FS I/N floor, dish pointed away from the cluster | −12.2 dB | −11.8 dB |
| FS distance: criterion met from | about 69 km | about 69 km |
| FSS I/N, 37 sites | −49.0 dB | −56.4 dB |
| Edge clearance for 30 dB rejection (80 MHz into 160 MHz Wi-Fi) | about 10 MHz | 8 MHz |
| Terminal coupling, coordinated: handheld to AP at 5 m | −88.94 dBm | −103.88 dBm |
| Terminal coupling, coordinated: AP to handheld I/N at 5/10/20 m | +2.06 / −9.70 / −21.47 dB | −27.90 / −34.10 / −45.87 dB |
| Terminal coupling, coordinated: AP to rooftop CPE I/N at 5/10/20 m | +8.02 / −3.74 / −15.51 dB | +3.10 / −3.10 / −14.87 dB |

**What still holds:**
- **Fixed Service:** co-channel operation fails by more than 30 dB at 5 km. The 120 MHz clearance with beam avoidance meets the criterion in the reference geometry. The result rests on the clutter assumption: with no clutter, or with the WP 5D urban or suburban below-rooftop shares, no evaluated combination protects a dish aimed at the cluster.
- **Wi-Fi:** the same-room centre-overlap case still loses about 97% of its throughput.
- **Coverage:** the matched-bandwidth result (U6 below 3.5 GHz) is unchanged.

**What is new:**
- **Victim bearing:** the 120 MHz combination depends on where the victim sits. The paper's 45° reference bearing is one of the most favourable; at 0°, 30°, 90°, 120° and 150° the combination misses the criterion by 0.9 to 1.5 dB. A further 10 dB EIRP reduction restores it at every bearing tested.

### Known limitations (not addressed in 1.1)

- **Primary-channel fallback:** uncalibrated. It brings the 193/160 active-UE case from +465% to +64% error, but it is not fitted to that point. The 40 and 20 MHz baseline throughputs are scaled assumptions.
- **Wi-Fi trial points not reproduced:** 221/80 active UE 41 against 336 Mbit/s measured (−88%); 221/80 idle UE 970 against 1074 (−10%); 193/160 idle UE 1500 against 1621 (−7%); 193/160 active UE 666 against 407 (+64%). The other 11 states are within 5%.
- **ACLR and ACS values:** the generic values (30 dB, 33 dB, 20 dB roll-off per interferer bandwidth) are applied to every transmitter–victim pair. Pair-specific masks (for example the n104 base-station values in the WP 5D parameter set) are not yet parameterised.
- **Statistics:** the Monte Carlo 80th percentile and the 20%-time P.452 propagation are separate statistics and are reported as such.
- **Geometry:** victim distance is measured from the cluster centre, not from the nearest site.
- **Interference not evaluated:** interference into the serving base-station receiver, FSS space-to-Earth earth stations (6700–7075 MHz) and radio astronomy (6650–6675.2 MHz) are not modelled. The satellite result covers one cluster and one geometry, not a national footprint.
- **Resolution 220 check:** zero mechanical tilt and an idealised M.2101 pattern only.
- **Propagation:** smooth-earth P.452 without terrain; representative, not site-specific, deployment values.

### Review findings and status

| ID | Finding | Status in 1.1 |
|---|---|---|
| C01 | Zero rejection for any overlap and exact adjacency | Fixed (bandwidth-integrated coupling) |
| C02 | Bonded Wi-Fi channels centred on the primary channel | Fixed (802.11ax raster) |
| C03 | Wi-Fi calibration ignores the primary channel; zero-loss rule | Zero-loss rule removed; primary fallback added; measured-versus-predicted table for all 15 trial states published; 193/160 and 221/80 errors remain |
| C04 | Fixed-Service dish differs from F.1245-3 | Fixed |
| C05 | Constant clutter at every site | P.2108-1 with location variability; all-sites, urban, suburban and none options |
| C06 | Zero-guard Fixed-Service case drawn adjacent but computed co-channel | Fixed (explicit co-channel or adjacent placement) |
| C07 | Satellite bandwidth treatment | Not a defect; uniform-PSD assumption documented |
| C08 | Satellite PASS is not a footprint or Resolution 220 result | Fixed satellite direction; illustrative Resolution 220 check; footprint study out of scope |
| C09 | Generic ACLR/ACS for every pair | Documented; not yet parameterised |
| C10 | Fixed bearing, centroid distance, statistics | Bearing control and sweep, seeds, convergence; centroid distance kept and documented |
| C11 | Uplink panel omits the serving base-station receiver | Documented as out of scope; the terminal-coupling carrier is still placed on the Wi-Fi channel, not taken from the operator block |
| C12 | Handheld gain and geometry | Fixed in the terminal-coupling panel (consistent antenna, free-space floor, outdoor-to-indoor stated); the Wi-Fi calibration handset keeps 26 dBm EIRP |
| C13 | Coverage and cell-edge KPIs | Block-centre frequency, P.2109 per frequency, EIRP reduction applied, SNR label |
| C14 | Mixed criteria | Labelled as study or illustrative; sign fixed |
| C15 | Controls that do nothing or show fixed values | Fixed |
| C16 | Ranges outside n104; UAE assignment | Fixed (band limits, 350 MHz preset, full 6 GHz Wi-Fi raster) |
| C17 | Interface and traceability | Notice, version, links, reset, scenario link, contrast; CSV export not added |
| C18 | Out-of-scope services and directions | Documented |

## 1.0.0 (2 November 2026)

Initial release with the accepted paper.
