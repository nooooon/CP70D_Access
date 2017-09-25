#!C:/Python27/python.exe
# -*- coding:utf-8 -*-

import qrcode

class QR(object):
    
    def __init__(self):
        pass

    def create(self, url):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=5,
            border=1,
            )
        qr.add_data(url)
        qr.make(fit=True)
        return qr.make_image()
        
        
