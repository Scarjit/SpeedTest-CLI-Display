# Speedtest CLI Display

## Requirements
    - Python 3
    - tabulate (`pip install tabulate`)
    - humanize (`pip install humanize`)
    - dateutil (`pip install dateutil`)
    - [speedtest-cli](https://github.com/sivel/speedtest-cli)

## Gathering data
    - Run `speedtest-cli --json > locationName_networkName.json`
    - Once you gathered information for all locations and networks you want to test run
    - python result.py
