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

---

## ⚙️ Features

* **Automated Ctypes Patch:** Bypasses missing `librtlsdr` symbols under Python 3.14 / macOS environments.
* **Strict AGC Disabling:** Enforces `set_agc_mode(False)` and `set_manual_gain_enabled(True)` for stable gain dynamics.
* **Optimized for RTL-SDR Blog V4:** Operates natively in HF without forcing obsolete direct sampling flags.
* **Noise Power Integration:** Computes integrated power across 1 MHz bandwidth via sample-mean squared magnitude over $256 \times 1024$ samples per reading.
* **CSV Data Export:** Saves timestamped logarithmic power outputs (`dB`) for post-processing.
* **Publication-Ready Plotting:** Generates high-resolution time-series plots with formatted local time axes.

---

## 🚀 Installation & Dependencies

Ensure you have Python 3.x installed along with the required libraries:

```bash
pip install numpy pandas matplotlib pyrtlsdr

---

💻 Usage
1. Data Collection (noise_logger.py)
Connect your RTL-SDR Blog V4 receiver and run the logger:

Bash

python3 noise_logger.py

The script will:
- Initialize the tuner at 29.0 MHz with a fixed gain of 25.4 dB.
- Disable hardware and software AGC.
- Record average noise levels every 2 seconds.
- Export data continuously to eclipse_ruido_29MHz.csv.

2. Data Visualization (plot_noise.py)
To render the noise curve during or after the event:

Bash

python3 plot_noise.py

This generates a plot (grafica_eclipse_29MHz.png) displaying the noise floor evolution over time.

---

📄 Data Output Format
The generated CSV file contains timestamped power entries:

timestamp,power_dB
2026-07-24 18:18:05,-44.670
2026-07-24 18:18:07,-44.680

👥 Credits & Acknowledgments
Methodology & Proposal: Ricardo Lamarca Belanche.

Hardware Support: RTL-SDR Blog team for V4 architecture.

📜 License
MIT License - Open for educational, radio astronomy, and scientific research purposes.
