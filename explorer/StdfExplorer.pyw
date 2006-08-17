#!/usr/bin/env python
#Boa:App:BoaApp

import wx

import MainFrame

modules ={'MainFrame': [1, 'Main frame of Application', u'MainFrame.py']}

class BoaApp(wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers()
        self.main = MainFrame.create(None)
        self.main.Show()
        self.SetTopWindow(self.main)
        return True

def main():
    application = BoaApp(0)
    application.MainLoop()

if __name__ == '__main__':
    main()
