# py3status-fbox

Python module to monitor freebox activity in py3status bars

## Prerequisites

This is an i3/py3status module and it uses requests.

## Installation

```console
pip install py3status-fbox
```

## Configuration

Available parameters:
- `refresh_delay` (default: 60s)
- `format` (default: `freebox: ↑ {fmt_rate_up} ↓ {fmt_rate_down}`)

Available format variables:
- `rate_up`: raw upload rate
- `rate_down`: raw download rate
- `fmt_rate_up`: human readable upload rate
- `fmt_rate_down`: human readable download rate
- `bw_up`: raw upload bandwidth
- `bw_down`: raw download bandwidth
- `fmt_bw_up`: human readable upload bandwidth
- `fmtbw_down`: human readable download bandwidth
- `percent_up`: upload bandwidth usage
- `percent_down`: download bandwidth usage
- `time`: time of last update

Example configuration:

```
fbox {
  color="#dcedc1"
  refresh_delay=10
  format = " ↑[\?color=lightgreen {fmt_rate_up}]↓[\?color=lightblue {fmt_rate_down}]"
}
```
