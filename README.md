# ADSBDawg Log ADSB messages from a DVT-T usb stick to Datadog.

* Requires a RTL-SDR (RTL2832U) dongle and dump1090 running and listening on port
30003.
* Datadog agent installed on your machine with valid API key.

## Usage

    adsb.py [-h] [--host HOST] [--port PORT]

    optional arguments:
      -h, --help   show this help message and exit
      --host HOST  Hostname of the ADSB server. Default: localhost
      --port PORT  Port of the ADSB server. Default is 30003