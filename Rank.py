# pylint: disable=no-member
import regex
import wx

"""
Rankingräknare för att träna GUI Python programmering.
https://docs.wxpython.org/
"""


class CalcPanel(wx.Panel):
    # This Panel does some custom thing
    def __init__(self, *args, **kwargs):

        # Create panel to enter times.
        wx.Panel.__init__(self, *args, **kwargs)
    
        # Buttons
        self.BtnDam = wx.RadioButton(self,-1, label = 'Dam:', pos = (10,10), style = wx.RB_GROUP) 
        self.BtnHerr = wx.RadioButton(self,-1, label = 'Herr:', pos = (60,10)) 
        self.BtnHerr.SetValue(True)
        # BtnJunior = wx.CheckBox(self,-1, label="Junior", pos=(130,10))


class TimePanel(wx.Panel):
    # This Panel does some custom thing
    def __init__(self, *args, **kwargs):

        # Create panel to enter times.
        wx.Panel.__init__(self, *args, **kwargs)

        # Rubrik
        TmHdr = wx.StaticText(self, label="Tid", pos=(20,5))
        font = TmHdr.GetFont()
        font.PointSize += 8
        font = font.Bold()
        TmHdr.SetFont(font)

        # Fält 1
        _stTm1 = wx.StaticText(self, label="1: ", pos=(5,45))
        self.txtTm1 = wx.TextCtrl(self, -1, value="", pos=(20,45), size = (60,20))

        # Fält 2
        _stTm2 = wx.StaticText(self, label="2: ", pos=(5,75))
        self.txtTm2 = wx.TextCtrl(self, -1, value="", pos=(20,75), size = (60,20))

        # Fält 3
        _stTm3 = wx.StaticText(self, label="3: ", pos=(5,105))
        self.txtTm3 = wx.TextCtrl(self, -1, value="", pos=(20,105), size = (60,20))

        # Fält 4
        _stTm4 = wx.StaticText(self, label="Min tid: ", pos=(20,135))
        self.txtTm4 = wx.TextCtrl(self, -1, value="", pos=(20,155), size = (60,20))

    def getSec(self, tid):
        # Beräkna antal sekunder från min.sek.
        (m, s) = tid.split('.')
        return int(m)*60 + int(s)

    def egenTid(self):
        # Returnera  min tid (min.sek) som antal sekunder.
        return self.getSec(self.txtTm4.GetValue())

    def avgTime(self):
        # Beräkna medeltiden.
        total = 0
        for tid in CalcFrame.txtList[0:3]:
            total += self.getSec(tid.GetValue())
        avg = total/3
       
        # Medeltiden tillåts ligga högst 10 %  efter segrartiden.
        maxTid = self.getSec(self.txtTm1.GetValue()) * 1.1
        if avg > maxTid:
            avg = maxTid
        return avg


class RankPanel(wx.Panel):
    # This Panel does some custom thing
    def __init__(self, *args, **kwargs):

        # Create panel to enter rank points.
        wx.Panel.__init__(self, *args, **kwargs)

        # Rubrik
        RnkHdr = wx.StaticText(self, label="Ranking", pos=(5,5))
        font = RnkHdr.GetFont()
        font.PointSize += 8
        font = font.Bold()
        RnkHdr.SetFont(font)

        # Fält 1
        _stRnk1 = wx.StaticText(self, label="1: ", pos=(5,45))
        self.txtRnk1 = wx.TextCtrl(self, -1, value="", pos=(20,45), size = (60,20))

        # Fält 2
        _stRnk2 = wx.StaticText(self, label="2: ", pos=(5,75))
        self.txtRnk2 = wx.TextCtrl(self, -1, value="", pos=(20,75), size = (60,20))

        # Fält 3
        _stRnk3 = wx.StaticText(self, label="3: ", pos=(5,105))
        self.txtRnk3 = wx.TextCtrl(self, -1, value="", pos=(20,105), size = (60,20))

        # Knapp för att läsa rankingpoäng från sverigelistan.
        BtnGet = wx.Button(self, -1, label="Hämta", pos=(20,135), size = (60,40))
        BtnGet.Bind(wx.EVT_BUTTON, self.OnBtnGet)

    def avgPoints(self):
        # Beräkna medelpoängen.
        total=0.0
        for point in CalcFrame.txtList[4:]:
            total += float(point.GetValue())
        return total/3

    def OnBtnGet(self, event):
        # Sverigelistan.
        href = "https://eventor.orientering.se/sverigelistan/ol"
        wx.BeginBusyCursor()
        import webbrowser
        webbrowser.open(href)
        wx.EndBusyCursor()


class CalcFrame(wx.Frame):
    """
    A Frame that calculates your ranking point.
    """
    txtList = []

    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super().__init__(*args, **kw)
        self.SetSize(260,400)

        # Create panels in the frame.
        self.pnl = wx.Panel(self, style = wx.BORDER_STATIC)

        self.CalcPnl = CalcPanel(self.pnl, -1, pos=(10,220), size=(230,90), style=wx.BORDER_NONE)    
        self.TmPnl = TimePanel(self.pnl, -1, pos=(10,10), size=(100,190), style=wx.BORDER_SIMPLE)    
        self.RnkPnl = RankPanel(self.pnl, -1, pos=(130,10), size=(100,190), style=wx.BORDER_SIMPLE)
                
        # create a menu bar
        self.makeMenuBar()

        # and a status bar
        self.CreateStatusBar()
        self.SetStatusText("Fyll i bästa tider och rankingpoäng!")

        # Beräkna och rensa knappar på CalcPnl.
        BtnCalc = wx.Button(self.CalcPnl, -1, label="Beräkna", pos=(5,40), size = (90,40))
        BtnCalc.Bind(wx.EVT_BUTTON, self.OnBtnCalc)

        BtnClear = wx.Button(self.CalcPnl, -1, label="Rensa", pos=(130,40), size = (90,40))
        BtnClear.Bind(wx.EVT_BUTTON, self.OnBtnClear)

        # All text fields
        CalcFrame.txtList = [self.TmPnl.txtTm1, self.TmPnl.txtTm2, self.TmPnl.txtTm3, self.TmPnl.txtTm4, 
                             self.RnkPnl.txtRnk1, self.RnkPnl.txtRnk2, self.RnkPnl.txtRnk3]

        # Start entering first time field
        self.TmPnl.txtTm1.SetFocus()

    def OnBtnCalc(self, event):
        # Kontrollera fältens format.
        if self.parseFld() == False:
            return

        # Beräkna och presentera min poäng.
        Tm = self.TmPnl.avgTime()
        Pm = self.RnkPnl.avgPoints()

        if self.CalcPnl.BtnHerr.GetValue() :
            # Beräkna herrpoäng
            Kk = (75 + Pm)/Tm
            P = self.TmPnl.egenTid() * Kk - 75
        else:
            # Beräkna dampoäng
            Kk = (60 + Pm)/Tm
            P = self.TmPnl.egenTid() * Kk - 60

        minPoäng = round(P, 2)
        dialog = wx.MessageDialog(self, str(minPoäng), "Din poäng:")
        dialog.ShowModal()

    def OnBtnClear(self, event):
        # Rensa alla textfält.
        for fld in CalcFrame.txtList:
            fld.SetValue("")

    def parseFld(self):
        # Kontrollera rätt format i textfälten.
        pTime = regex.compile(r"\d{1,3}[,.:][0-5]\d") # Time ex. 23:34
        pPoint = regex.compile(r"\d{1,3}[,.:]\d\d")   # Point ex. 23,99
        for fld in CalcFrame.txtList:
            if fld in CalcFrame.txtList[0:3]:
                check = pTime.match(fld.GetValue())
            else:
                check = pPoint.match(fld.GetValue())
            
            val = fld.GetValue()
            if check == None:
                fel = wx.MessageDialog(self, val, "Felaktigt format:")
                fel.ShowModal()
                return False
            else:
                # Ersätt (:) och (,) med (.)
                for note in [':',',']:
                    if val.find(note) > 0:
                        val = val.replace(note,'.')
                fld.SetValue(val)
        return True

    def makeMenuBar(self):
        """
        A menu bar is composed of menus, which are composed of menu items.
        This method builds a set of menus and binds handlers to be called
        when the menu item is selected.
        """

        # Make a file menu with Hello and Exit items
        fileMenu = wx.Menu()
        # The "\t..." syntax defines an accelerator key that also triggers
        # the same event
        helloItem = fileMenu.Append(-1, "&Hello...\tCtrl-H",
                "Help string shown in status bar for this menu item")
        fileMenu.AppendSeparator()
        # When using a stock ID we don't need to specify the menu item's
        # label
        exitItem = fileMenu.Append(wx.ID_EXIT)

        # Now a help menu for the about item
        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        # Make the menu bar and add the two menus to it. The '&' defines
        # that the next letter is the "mnemonic" for the menu item. On the
        # platforms that support it those letters are underlined and can be
        # triggered from the keyboard.
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")

        # Give the menu bar to the frame
        self.SetMenuBar(menuBar)

        # Finally, associate a handler function with the EVT_MENU event for
        # each of the menu items. That means that when that menu item is
        # activated then the associated handler function will be called.
        self.Bind(wx.EVT_MENU, self.OnHello, helloItem)
        self.Bind(wx.EVT_MENU, self.OnExit,  exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)

    def OnExit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)

    def OnHello(self, event):
        """Say hello to the user."""
        wx.MessageBox("Hello again from wxPython")

    def OnAbout(self, event):
        """Display an About Dialog"""
        wx.MessageBox("This is a wxPython Hello World sample",
                      "About Hello World 2",
                      wx.OK|wx.ICON_INFORMATION)


if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    frm = CalcFrame(None, title='Min Rankingräknare')
    frm.Show()

    # Start the event loop.
    app.MainLoop()

