# RTL-SDR ADS-B Decoder 

A Python-based, connects to an RTL-SDR USB dongle, manually decodes real-time ADS-B signals from aircraft, and streams the data to network ports in various formats. This project is intended as a low-level example of how ADS-B decoding works without relying on a pre-built library.

## Features

- **RTL-SDR Control:** Configures and controls the RTL-SDR dongle's frequency, sample rate, gain, and frequency correction.
- **Manual ADS-B Decoding:** Implements a simplified,scratch decoder for Mode S/ADS-B messages.
- **CRC Validation:** Includes a basic Cyclic Redundancy Check (CRC) function to validate message integrity.
- **Multi-Format Output:** Streams decoded data in Beast, SBS, and JSON formats to separate network ports.
- **Configurable:** Easily adjust settings via the `config.ini` file.

## Folder Structure

```
rtl_sdr_decoder/
├── main.py                     # Main script to run the program
├── decoder.py                   # Module containing the manual decoding logic
└── config.ini                   # Configuration file for settings
├── requirements.txt             # Python dependencies
```

## Getting Started

### Prerequisites

- **RTL-SDR Drivers:**
  - **Windows:** Use Zadig to install the libusb driver for RTL-SDR dongle.
  - **Linux:** Install librtlsdr via your package manager.
- **An RTL-SDR Dongle:** A low-cost dongle with an RTL2832U chip.

### Installation

1. Clone the repository or download the project files.
2. Navigate to the project directory.
3. Install the required Python libraries using pip:

```bash
pip install numpy pyrtlsdr
```

## Configuration

Before running, open the `config.ini` file and adjust the settings to match your hardware and needs.

**Example `config.ini`:**

```ini
[SDR_SETTINGS]
center_freq = 1090000000
sample_rate = 2400000
gain = auto
freq_correction = 0
read_size = 262144

[OUTPUT_PORTS]
beast = 30005
sbs = 30003
json = 30006

[GENERAL]
output_formats = beast, sbs, json
```

**Notes:**

- `gain`: The most important setting for signal quality. If reception is poor, try increasing this value (e.g., to 40) or leave it at `auto`.
- `freq_correction`: If your decoded messages are sparse, you may need to fine-tune this value. Adjust it by a few PPM at a time until you see a consistent stream of data.

## How to Run

Simply execute the `main.py` script from your terminal:

```bash
python main.py
```

The program will start, connect to RTL-SDR, and begin streaming decoded ADS-B data to the configured network ports. You can then use other applications (like Virtual Radar Server or dump1090) to connect to these ports and visualize the data.

## Limitations

- Decoder is simplified. A production-ready ADS-B decoder is being developed.
