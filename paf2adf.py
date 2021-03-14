#!/usr/bin/python3
#
# PAF to ADF antenna pattern conversion utility
#
# Copyright 2021 Farrant Consulting Ltd
# CloudRF.com
import sys
import os
import xml.etree.ElementTree as ET


if len(sys.argv) < 3:
    print("Usage: python3 paf2adf.py {in directory} {antennas.paf}")
    quit()

indir=sys.argv[1]
outdir="adf"
try:
    os.mkdir(outdir)
except:
    pass

tree = ET.parse(indir+"/"+sys.argv[2])
root = tree.getroot()

polarisation = "V"

def plane(gains,patcut):
    startA=0
    endA=0
    step=1
    gainArray = []
    text = "PATCUT:,%s\n" % (patcut)
    text += "POLARI:,%s/%s\n" % (polarisation,polarisation)
    for child in gains:
        if child.tag == "StartAngle":
            startA = int(child.text)
        if child.tag == "EndAngle":
            endA = int(child.text)
        if child.tag == "Gains":
            gainArray = child.text.split(";")
            if len(gainArray) != (endA-startA)+1:
            	print("Number of values (%d) does not match start/end angles (%d)!" % (len(gainArray),(endA-startA)+1))
    text += "NUPOIN:,%d\n" % ((endA-startA)+1)
    text += "FSTLST:,%d,%d\n" % (startA,endA)
    a=0
    while a <= endA-startA:
        text += "%d,%s\n" % (startA+a,gainArray[a])
        a+=1
    return text

for child in root:
    if child.tag == "Version":
        version = child.text
    if child.tag == "Type":
        type = child.text
    if child.tag == "Name":
        name = child.text
    if child.tag == "Manufacturer":
        oem = child.text
    if child.tag == "Patterns":
        print(version,type,name,oem)
        for patob in child:
            if patob.tag == "Pattern":
                for pat in patob:
                    if pat.tag == "Name":
                        name = pat.text
                    if pat.tag == "MinimumFrequencyMHz":
                        lower = pat.text
                    if pat.tag == "MaximumFrequencyMHz":
                        upper = pat.text
                    if pat.tag == "MeasurementFrequencyMHz":
                        freq = pat.text
                    if pat.tag == "Polarization":
                        pol = pat.text
                    if pat.tag == "ElectricalTiltDegrees":
                        etilt = pat.text
                    if pat.tag == "ElectricalAzimuthDegrees":
                        etilt = pat.text
                    if pat.tag == "ElectricalBeamwidthDegrees":
                        bwi = pat.text
                    if pat.tag == "BoresightGain":
                        gain = pat.text
                    if pat.tag == "BoresightGainUnit":
                        gainUnit = pat.text
                    if pat.tag == "HorizontalBeamwidthDegrees":
                        hbw = pat.text
                    if pat.tag == "VerticalBeamwidthDegrees":
                        vbw = pat.text
                    if pat.tag == "FrontToBackRatioDB":
                        fbr = pat.text
                    if pat.tag == "AntennaPatternsEntryName":
                        filename = pat.text
                        print(filename)
                        tree = ET.parse(indir+"/"+filename)
                        patroot = tree.getroot()
                        adf = open(outdir+"/"+filename.replace(" ","").replace(",","")+".adf","a")
                        adf.write("REVNUM:,TIA/EIA-804-B\n")
                        adf.write("COMNT1:,Standard TIA/EIA Antenna Pattern Data\n")
                        adf.write("ANTMAN:,"+oem+"\n")
                        adf.write("MODNUM:,"+name+"\n")
                        adf.write("DESCR1:,"+name+"\n")
                        adf.write("DESCR2:,Made with love at CloudRF.com\n")
                        adf.write("DTDATA:,20210311\n")
                        adf.write("LOWFRQ:,"+lower+"\n")
                        adf.write("HGHFRQ:,"+upper+"\n")
                        adf.write("GUNITS:,"+gainUnit+"\n")
                        adf.write("MDGAIN:,"+gain+"\n")
                        adf.write("AZWIDT:,"+hbw+"\n")
                        adf.write("ELWIDT:,"+vbw+"\n")
                        adf.write("CONTYP:,N/A\n")
                        adf.write("ATVSWR:,1.5\n")
                        adf.write("FRTOBA:,"+fbr+"\n")
                        adf.write("ELTILT:,"+etilt+"\n")
                        adf.write("MAXPOW:,0\n")
                        adf.write("ANTLEN:,0\n")
                        adf.write("ANTWID:,0\n")
                        adf.write("ANTWGT:,0\n")
                        adf.write("PATTYP:,Typical\n")
                        adf.write("NOFREQ:,1\n")
                        adf.write("PATFRE:,"+freq+"\n")
                        adf.write("NUMCUT:,2\n")

                        for child in patroot:
                            if child.tag == "HorizontalPatterns":
                                data = plane(child[0],"H")
                            if child.tag == "VerticalPatterns":
                                data = plane(child[0],"V")
                            adf.write(data)
                        adf.write("ENDFIL:,EOF")
                        adf.close()
