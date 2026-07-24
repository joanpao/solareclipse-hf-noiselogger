# 🛰️ eclipse-sdr-radiometer

> **29 MHz HF Noise Floor Logger for Solar Eclipse Ionospheric Monitoring using RTL-SDR Blog V4**

`eclipse-sdr-radiometer` is a Python-based radiometric logging and visualization tool designed to measure variations in solar RF noise flux and ionospheric noise floor levels during solar eclipses using an RTL-SDR Blog V4 receiver.

---

## ☀️ Scientific Background & Methodology

This project was specifically developed for the **Total Solar Eclipse of August 12, 2026**, visible across major regions of Spain.

The software implementation is based on the observational proposal by **Ricardo Lamarca Belanche**, who proposed monitoring background solar RF noise in the **25 to 30 MHz** frequency range using a Software Defined Radio (SDR).

### Key Scientific Principles

* **Solar RF Emissions as Background Noise:** In the 25–30 MHz spectrum (high HF / low VHF), quiet-Sun and active-Sun radiation manifest as a baseline increase in broadband background noise rather than discrete modulated signals.
* **The Eclipse Effect:** As the Moon partially and then totally occults the solar disk, direct solar RF flux decreases. Simultaneously, the sudden drop in solar ionizing radiation (UV and X-rays) alters ionospheric absorption. This results in a measurable drop in total noise power—typically on the order of **2 to 6 dB**, depending on real-time solar activity and effective integrated bandwidth.
* **Statistical PSD Measurement:** Rather than relying on instantaneous or single-point readings, the experiment performs continuous statistical integration of the Power Spectral Density (PSD) over time, quantifying average relative noise levels in dB.

---

## 🛠️ Experimental Setup & Prerequisites

* **Bandwidth Selection:** A bandwidth between **200 kHz and 1 MHz** (1 MHz default) is used to integrate total noise power cleanly.
* **Fixed Gain Control (Mandatory):** Automatic Gain Control (AGC) and tuner auto-gain **must be strictly disabled**. Fixed manual gain is enforced to ensure power variations reflect true physical phenomena rather than internal receiver compensation.
* **Antenna Requirements:** The receiving antenna is **not a critical element**; a standard resonant 10m dipole, active whip, or long-wire antenna is sufficient as long as it provides adequate sensitivity above the receiver's thermal floor.
* **Spectrum Verification & RFI Mitigation:** Prior to the eclipse, the target RF spectrum must be thoroughly surveyed to avoid local Radio Frequency Interference (RFI), digital modes (FT8/WSPR), or active transmissions that could skew statistical calculations. Operating in a low-noise RF environment is highly recommended.

---

## 💻 Repository Structure

```text
eclipse-sdr-radiometer/
├── noise_logger.py    # Main SDR capture script (29 MHz logging)
├── plot_noise.py      # Data processing & visualization script
└── README.md          # Project documentation
