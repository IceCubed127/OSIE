# OSIE (Operating System Installation & Extraction)

OSIE is a terminal utility that helps you:

- Download operating system images (ISO/IMG and related formats)
- Detect removable USB targets
- Flash images to USB drives via Raspberry Pi Imager CLI

It supports Windows, macOS, and Linux host systems (with platform-specific behavior).

## Features

- Interactive menu-driven CLI
- Download with retry + resume support (`.osiedownload` temporary files)
- Operating system image selection for:
	- Windows (Windows 11, Windows 10, Windows XP SP3 language variants)
	- macOS recovery image workflow (OpenCore `macrecovery.py` flow)
	- Linux distributions (Ubuntu, Fedora, Arch, Kali, Debian, Linux Mint, Pop!_OS, Zorin)
- USB target detection:
	- Windows: PowerShell removable drive detection
	- macOS: `diskutil` external physical disks
	- Linux: `lsblk` removable/USB disks
- Safety confirmation before flashing (requires typing `ERASE`)

## Requirements

- Python 3.10+
- `requests`
- `tqdm`
- `colorama`

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running OSIE

```bash
python osie.py
```

Main menu options:

1. Install Operating System
2. Extract Operating System Image
3. Install and Extract Operating System Image
4. Exit

## Extraction/Flashing Notes

OSIE uses Raspberry Pi Imager CLI for writing images. You must have Raspberry Pi Imager installed (or provide its executable path when prompted).

- Windows expected default path:
	- `C:\Program Files\Raspberry Pi Imager\rpi-imager.exe`
- macOS expected default path:
	- `/Applications/Raspberry Pi Imager.app/Contents/MacOS/rpi-imager`
- Linux:
	- Uses `rpi-imager` from `PATH` (or asks you to install/provide path)

Supported image extensions include:

- `.iso`, `.img`, `.raw`, `.wic`, `.dmg`
- `.zip`, `.gz`, `.xz`, `.bz2`, `.zst`
- Combined image archives such as `.img.zip`, `.img.gz`, `.img.xz`, `.img.bz2`, `.img.zst`

## Platform-Specific Behavior

- **Windows host:**
	- Can download macOS recovery components via OpenCore `macrecovery.py`
	- Uses `py` launcher for some internal commands
- **macOS host:**
	- Uses `softwareupdate` for full macOS installers
- **Linux/other hosts:**
	- Uses OpenCore `macrecovery.py` via `python3` for macOS recovery download

## Important Warnings

- Flashing a USB target will erase all data on that target.
- Always verify that the selected removable drive is correct before continuing.
- Download links and version options are hardcoded in `osie.py` and may become outdated over time.

## Troubleshooting

- If a download fails, rerun OSIE to resume from the partial `.osiedownload` file.
- If removable drives are not detected:
	- Reconnect the USB device
	- Refresh scan from the prompt (`R`)
	- Retry with elevated privileges (Administrator/sudo) when required
- If flashing fails on Windows with privilege errors, rerun the program as Administrator.
