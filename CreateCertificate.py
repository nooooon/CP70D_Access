#!C:/Python27/python.exe
# -*- coding:utf-8 -*-


import setting
import sys
import urllib2
    
class CreateCertificate(object):

    def __init__(self):
        pass

    def loadImage(self, filePath):
        try:
            ob = urllib2.urlopen(filePath)
            return ob
        except urllib2.URLError, e:
            print e,filePath
            sys.exit()


    def create(self, id, user_id, capture, signature0, signature1, update_at):
        #print("id:",id, user_id, capture, signature0, signature1, update_at)
        
        import io
        import os
        import datetime
        import modules.QR as QR

        path = setting.BASE_PATH + 'share/' + user_id + '/'

        qr = QR.QR()
        qrImg = qr.create(path)
        outQrData = io.BytesIO()
        qrImg.save(outQrData, format="png");
        #qrImg.show()
        
        from wand.image import Image
        from wand.drawing import Drawing
        from wand.color import Color


        with Image(filename=setting.MATERIALS_DIR + setting.BASE_IMAGE) as baseImg:

            # Capture
            with Image(file=self.loadImage(capture)) as cap:
                capWidth = 2106;
                cap.resize(capWidth, capWidth * cap.height / cap.width)
                baseImg.composite(cap, left=10, top=37)
            # Frame
            with Image(filename=setting.MATERIALS_DIR + setting.FRAME_IMAGE) as frame:
                baseImg.composite(frame, left=7, top=40)

            # QRcode
            with Image(blob=outQrData.getvalue()) as qr:
                qrWidth = 137
                qr.resize(qrWidth, qrWidth)
                baseImg.composite(qr, left=1911, top=1282)

            # Date
            with Drawing() as draw:

                d = datetime.datetime.today()
                dText = '%s.%s.%s' % (d.year, d.month, d.day)
                draw.font = setting.MATERIALS_DIR + setting.FONT_DATA
                draw.fill_color = Color("#FFFFFF")
                draw.font_size = 48
                draw.text_alignment = 'center'
                draw.text(x=1063, y=1470, body=dText)
                draw(baseImg)

            if not os.path.isdir(setting.CERTIFICATE_DIR):
                os.makedirs(setting.CERTIFICATE_DIR)
                            
            baseImg.save(filename = setting.CERTIFICATE_DIR + str(id) + '.png')
        return
