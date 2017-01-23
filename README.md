# XDSpider

A highly **customisable** website site mapper spider written in python,
- supporting link priority rating using user definable regex,
- supporting link exclusing using user definable regex,
- supporting link depth limiting,
- supporting multi-threading,
- supporting multiple site config

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

* [Python](https://www.python.org/)

## Deployment

Run on any platform (Windows, Linux, Other)
* Universal - All Python Supported Operating Systems
 * Python xdspider.py [commands]
* Windows Only
 * Python xdspider.py [commands]
* Linux
 * ./xdspider.py [commands]
   * mark xdspider.py as executable by executeing
     * chmod 755 xdspider.py
        
### Usage
```
usage: xdspider.py [commands]
Commands                        Commands Description
--out filename                # master output filename, will become filename_sha1-hash-of-url
--format format               # master output format {JSON, CSV, XML}
--import filename             # import configs from file (json only)
--export filename             # export the default config to file (json only)
--no-save                     # disables file output, prints output data to console
--debug                       # enables application debugging mode
-h                            # outputs help menu
-?                            # outputs help menu
-help                         # outputs help menu
```

## Built With

* [Python](https://www.python.org/)
* [Love](https://en.wikipedia.org/wiki/Love)
* Compasion and endurence of the world wide web

## Contributing

Please email [Dean Van Greunen](mailto:deanvg9000@gmail.com) for details on the process for submitting pull requests.

## Versioning & Downloads

* [XDSpider V2.0.0.0-stable](xdspider-v2.0.0.0-stable.zip). sha1-hash:  4b430a0b2e63a4d9d6b4152e039b82b37f1a6053
* * Supported: Python 2.6.7
* Coming Soon: Python 3
* Coming Soon: Python 4

## Author
* **Dean Van Greunen** - *Initial work* - [xX-MLG-Xx](https://github.com/xX-MLG-Xx)

## License

This project is licensed - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hozi Pty Ltd
