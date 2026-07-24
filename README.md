# Solar Eclipse Ionospheric Noise Logger (29 MHz HF)
29 MHz HF Noise Floor Logger for Solar Eclipse Ionospheric Monitoring using RTL-SDR Blog V4


A Python-based radiometric logging system to measure variations in solar/ionospheric background noise during solar eclipses using an RTL-SDR Blog V4 receiver.

## Overview

During a solar eclipse, the sudden drop in solar ultraviolet (UV) and X-ray radiation leads to rapid deionization in the upper ionosphere (D, E, and F layers). This repository provides a simple, high-resolution tool to continuously monitor, log, and plot relative RF noise floor levels around **29.0 MHz** (10-meter HF band).

The frequency centered at **29.0 MHz** (with 1 MHz bandwidth) was selected because it resides in a quiet segment of the HF spectrum, clear of HF digital modes (FT8/WSPR), CW, and FM repeaters.

## Hardware Requirements

- **SDR Receiver:** RTL-SDR Blog V4 (incorporating internal upconverter for HF reception).
- **Antenna:** Resonant 10m dipole, active HF whip, or long-wire antenna.
- **Host Machine:** macOS, Linux, or Raspberry Pi.

## Features

- **Automated Ctypes Patch:** Bypasses missing `librtlsdr` symbols under Python 3.14 / macOS environments.
- **Fixed Gain Control:** Disables Automatic Gain Control (AGC) and tuner auto-gain to preserve absolute relative power measurements.
- **Noise Power Integration:** Computes integrated power across 1 MHz bandwidth via sample-mean squared magnitude over $256 \times 1024$ samples per reading.
- **CSV Data Export:** Saves timestamped logarithmic power outputs (`dB`) for post-processing.
- **Visualization Script:** Generates publication-ready time-series plots with formatted UTC/local time axes.

## Installation & Dependencies

Ensure you have Python 3.x installed along with the required dependencies:

```bash
pip install numpy pandas matplotlib pyrtlsdr
