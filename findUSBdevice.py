#!/usr/bin/python
import sys
import libusb_package

def listUSBdevices():
    # find USB devices
    for dev in libusb_package.find(find_all=True):
    # loop through devices, printing vendor and product ids in decimal and hex
        sys.stdout.write('Decimal VendorID=' + str(dev.idVendor) + ' & ProductID=' + str(dev.idProduct) + '\n')
        sys.stdout.write('Hexadecimal VendorID=' + hex(dev.idVendor) + ' & ProductID=' + hex(dev.idProduct) + '\n\n')

    
  
if __name__ == "__main__":
    print(libusb_package.get_library_path())
    listUSBdevices()