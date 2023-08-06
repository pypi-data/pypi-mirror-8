# Slightly more advanced sample illustrating the usage of CEFWindow class
# __author__ = "Greg Kacy <grkacy@gmail.com>"

# --WARNING--
# TODO: There is something wrong with this example. On Linux
#       CPU usage for the python process is 100% all the time.
#       The other examples sample1.py / sample2.py do not
#       show such behavior. It must have something to do
#       with the wx controls used in this example.

import wx
import wx.lib.agw.flatnotebook as fnb
import cefpython3.wx.chromectrl as chrome

ROOT_NAME = "My Locations"

URLS = ["http://gmail.com",
        "http://maps.google.com",
        "http://youtube.com",
        "http://yahoo.com",
        "http://wikipedia.com",
        "http://cyaninc.com",
        "http://tavmjong.free.fr/INKSCAPE/MANUAL/web/svg_tests.php"
        ]


class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, id=wx.ID_ANY,
                          title='cefwx example2', size=(1024, 768))

        self.initComponents()
        self.layoutComponents()
        self.initEventHandlers()

    def initComponents(self):
        self.tree = wx.TreeCtrl(self, id=-1, size=(200, -1))
        self.root = self.tree.AddRoot(ROOT_NAME)
        for url in URLS:
            self.tree.AppendItem(self.root, url)
        self.tree.Expand(self.root)

        self.tabs = fnb.FlatNotebook(self, wx.ID_ANY,
                agwStyle=fnb.FNB_NODRAG | fnb.FNB_X_ON_TAB)
        # You also have to set the wx.WANTS_CHARS style for
        # all parent panels/controls, if it's deeply embedded.
        self.tabs.SetWindowStyleFlag(wx.WANTS_CHARS)

    def layoutComponents(self):
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.tree, 0, wx.EXPAND)
        sizer.Add(self.tabs, 1, wx.EXPAND)
        self.SetSizer(sizer)

    def initEventHandlers(self):
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, self.tree)
        self.Bind(fnb.EVT_FLATNOTEBOOK_PAGE_CLOSING, self.OnPageClosing)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def OnSelChanged(self, event):
        self.item = event.GetItem()
        url = self.tree.GetItemText(self.item)
        if url and url != ROOT_NAME:
            cefPanel = chrome.ChromeCtrl(self.tabs, useTimer=True, url=str(url))
            self.tabs.AddPage(cefPanel, url)
            self.tabs.SetSelection(self.tabs.GetPageCount()-1)
        event.Skip()

    def OnPageClosing(self, event):
        print("sample2.py: One could place some extra closing stuff here")
        event.Skip()

    def OnClose(self, event):
        self.Destroy()

if __name__ == '__main__':
    chrome.Initialize()
    print('sample2.py: wx.version=%s' % wx.version())
    app = wx.PySimpleApp()
    MainFrame().Show()
    app.MainLoop()
    # Important: do the wx cleanup before calling Shutdown.
    del app
    chrome.Shutdown()

