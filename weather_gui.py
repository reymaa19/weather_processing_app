"""This is the main program use GUI """
import wx
import wx.xrc

from weather_processor import WeatherProcessor
from plot_operations import PlotOperations

class MyFrame1 (wx.Frame):
    """This class is to build the form"""

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"Weather App",
                          pos=wx.DefaultPosition, size=wx.Size(445, 415),
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.m_button1 = wx.Button(
            self, wx.ID_ANY, u"Download Full Database", wx.DefaultPosition,
            wx.DefaultSize, 0)
        bSizer1.Add(self.m_button1, 1, wx.ALL | wx.EXPAND, 5)

        self.m_button2 = wx.Button(
            self, wx.ID_ANY, u"Update Database", wx.DefaultPosition,
            wx.DefaultSize, 0)
        bSizer1.Add(self.m_button2, 1, wx.ALL | wx.EXPAND, 5)

        self.m_staticText3 = wx.StaticText(
            self, wx.ID_ANY, u"Please enter from year and end year :",
            wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText3.Wrap(-1)

        bSizer1.Add(self.m_staticText3, 0, wx.ALL | wx.EXPAND, 5)

        gSizer1 = wx.GridSizer(0, 2, 0, 0)

        self.m_textCtrl2 = wx.TextCtrl(
            self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
            wx.DefaultSize, 0)
        gSizer1.Add(self.m_textCtrl2, 1, wx.ALL | wx.EXPAND, 5)

        self.m_textCtrl1 = wx.TextCtrl(
            self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
            wx.DefaultSize, 0)
        gSizer1.Add(self.m_textCtrl1, 1, wx.ALL | wx.EXPAND, 5)

        bSizer1.Add(gSizer1, 1, wx.EXPAND, 5)

        self.m_button3 = wx.Button(
            self, wx.ID_ANY, u"Create Plot (yearly)", wx.DefaultPosition,
            wx.DefaultSize, 0)
        bSizer1.Add(self.m_button3, 1, wx.ALL | wx.EXPAND, 5)

        self.m_staticText4 = wx.StaticText(
            self, wx.ID_ANY, u"Please enter year and month:",
            wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText4.Wrap(-1)

        bSizer1.Add(self.m_staticText4, 0, wx.ALL | wx.EXPAND, 5)

        gSizer2 = wx.GridSizer(0, 2, 0, 0)

        self.m_textCtrl3 = wx.TextCtrl(
            self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
            wx.DefaultSize, 0)
        gSizer2.Add(self.m_textCtrl3, 1, wx.ALL | wx.EXPAND, 5)

        self.m_textCtrl4 = wx.TextCtrl(
            self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
            wx.DefaultSize, 0)
        gSizer2.Add(self.m_textCtrl4, 1, wx.ALL | wx.EXPAND, 5)

        bSizer1.Add(gSizer2, 1, wx.EXPAND, 5)

        self.m_button4 = wx.Button(
            self, wx.ID_ANY, u"Create Plot (Monthly)", wx.DefaultPosition,
            wx.DefaultSize, 0)
        bSizer1.Add(self.m_button4, 1, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.m_button1.Bind(wx.EVT_BUTTON, self.full_data)
        self.m_button2.Bind(wx.EVT_BUTTON, self.update_data)
        self.m_button3.Bind(wx.EVT_BUTTON, self.create_plot)
        self.m_button4.Bind(wx.EVT_BUTTON, self.monthly_plot)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def full_data(self, event):
        """This event will download the full set of data"""
        processor = WeatherProcessor()
        processor.download_full_set_data()

    def update_data(self, event):
        """This event will update the database"""
        processor = WeatherProcessor()
        processor.update_db()

    def create_plot(self, event):
        """This method create a plot with range of year"""
        from_year, to_year = eval(self.m_textCtrl2.GetValue()), eval(self.m_textCtrl1.GetValue())
        plot = PlotOperations(from_year, to_year)
        plot.create_weather_data()
        plot.create_plot(plot.weather_data)

    def monthly_plot(self, event):
        """This method create a monthly plot"""
        year, month = eval(self.m_textCtrl3.GetValue()), eval(self.m_textCtrl4.GetValue())
        plot = PlotOperations(int(year), int(year) + 1)
        plot.create_weather_data()
        plot.create_day_plot(int(year), int(month))

def main():
    app = wx.App()
    ex = MyFrame1(None)
    ex.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
