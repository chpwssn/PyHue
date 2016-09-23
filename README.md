#PyHue
*A Python library for Philips Hue Gen 2 Systems*

##Getting Started

###Configuration
PyHue uses a [JSON](http://json.org/) format configuration file. By default the library attempts to open a file titled `config.json`. If no configuration is supplied and _autoConfig_ is not disabled. The library will prompt the user for information about their Hue setup. 

#### Automatically Generate Configuration File
To generate a configuration file automatically run `python3 example.py`, this will attempt to load the default configuration file and if one is not present, it will prompt the user for the information needed to generate `config.json`.


#### Manually Generate Configuration File
To get started with a manually generated configuration file, follow the setup instructions on your Hue station then get a username by following 

    http://www.developers.meethue.com/documentation/getting-started
    
Copy `config.example.json` to `config.json` and edit appropriately. You can then run `python3 example.py`.

##Debian/Ubuntu Quick Start
    sudo apt-get install python3 python3-pip git
    git clone https://github.com/chpwssn/PyHue.git PyHue
    cd PyHue/
    
	#Install Python3 Prerequisite Libraries
    pip3 install --user -r requirements.txt
    
    #Generate Config File and Run Example
    python3 example.py

##Requirements

This library does require `requests` which you can install by following the directions at http://docs.python-requests.org/en/master/ or by running `pip3 install -r requirements.txt`