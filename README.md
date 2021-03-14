## PAF to ADF conversion utility	
This antenna utility converts Planet Antenna File (PAF) XML files into TIA/EIA-804-B standard ADF files.

[ADF antenna standard](https://cloudrf.com/files/ADF_antenna_standard_wg16_99_050.pdf)

To use, take a PAFX zip file and extract the contents to a local folder eg. 'antennas', then call the script with two arguments: The folder and the .paf filename:

    python3 paf2adf.py {antennas} {antennas.paf}
    
The script output is a folder called adf containing ADF pattern files. Upload these at CloudRF to use them in the service.
![ADF polar plot from CloudRF.com](https://cloudrf.com/files/antenna_plot.jpg)


