import win32print
import win32ui,win32gui
import pywintypes
from PIL import Image, ImageWin

class PrinterAccess(object):

    # HORZRES / VERTRES = printable area
    HORZRES = 8
    VERTRES = 10
    # LOGPIXELS = dots per inch
    LOGPIXELSX = 300
    LOGPIXELSY = 600
    # PHYSICALWIDTH/HEIGHT = total area
    PHYSICALWIDTH = 110
    PHYSICALHEIGHT = 111
    # PHYSICALOFFSETX/Y = left / top margin
    PHYSICALOFFSETX = 112
    PHYSICALOFFSETY = 113
    
    def __init__(self):
        pass



    def printOut(self, file_name):

        # List available printers
        #print("Available printers")
        #print(win32print.EnumPrinters(0,"None",1))
        #print(win32print.EnumPrinters(1,"None",2))
        #print(win32print.EnumPrinters(3,"None",1)[4])
        #print(win32print.EnumPrinters(3,"None",5))

        # Use Default Printer
        #printer_name = win32print.GetDefaultPrinter ()
        printer_name = "MITSUBISHI CP70D Series(USB)"
        print("Printer: " + printer_name)

        hprinter = win32print.OpenPrinter(printer_name, {"DesiredAccess": win32print.PRINTER_ALL_ACCESS})
        devmode = win32print.GetPrinter(hprinter, 2)["pDevMode"]

        # DEVMODE
        devmodeSize=win32print.DocumentProperties(0, hprinter, printer_name, None, None, 0)
        devmode = pywintypes.DEVMODEType(devmodeSize - pywintypes.DEVMODEType().Size)
        #devmode.Fields = devmode.Fields|win32con.DM_ORIENTATION|win32con.DM_COPIES

        win32print.DocumentProperties(0, hprinter, printer_name, devmode, devmode, 0)

        '''
        try:
            win32print.SetPrinter(hprinter, 2, properties, 0)
        except pywintypes.error, err:
            print(err[2])
            #sys.exit()
        '''

        gDC = win32gui.CreateDC("WINSPOOL", printer_name, devmode)

        hDC = win32ui.CreateDCFromHandle(gDC)

        self.printable_area = hDC.GetDeviceCaps (self.HORZRES), hDC.GetDeviceCaps (self.VERTRES)
        print "printable_area",self.printable_area

        printer_size = hDC.GetDeviceCaps (self.PHYSICALWIDTH), hDC.GetDeviceCaps (self.PHYSICALHEIGHT)
        print "printer_size",printer_size

        printer_margins = hDC.GetDeviceCaps (self.PHYSICALOFFSETX), hDC.GetDeviceCaps (self.PHYSICALOFFSETY)
        print "printer_margins",printer_margins
        
        bmp = Image.open (file_name)

        print "bmp.size[0]",bmp.size[0]," bmp.size[1]",bmp.size[1]

        #if bmp.size[0] > bmp.size[1]:
          #bmp = bmp.rotate (90)

        ratios = [1.0 * self.printable_area[0] / bmp.size[0], 1.0 * self.printable_area[1] / bmp.size[1]]
        print "ratios",ratios

        scale = min (ratios)
        print "scale",scale
        
        hDC.StartDoc (file_name)
        hDC.StartPage () 

        dib = ImageWin.Dib (bmp)
        scaled_width, scaled_height = [int (scale * i) for i in bmp.size]

        print "scaled width",scaled_width," scaled height",scaled_height


        x1 = int ((printer_size[0] - scaled_width) / 2)
        y1 = int ((printer_size[1] - scaled_height) / 2)
        x2 = x1 + scaled_width
        y2 = y1 + scaled_height

        print "x1, y1, x2, y2",x1, y1, x2, y2

        #dib.draw (hDC.GetHandleOutput (), (x1-5, y1+38, x2-25, y2-24))
        #dib.draw (hDC.GetHandleOutput (), (x1-5, y1+38, x2, y2))
        dib.draw (hDC.GetHandleOutput (), (0, 0, scaled_width, scaled_height))

        hDC.EndPage ()
        hDC.EndDoc ()
        hDC.DeleteDC ()
        
