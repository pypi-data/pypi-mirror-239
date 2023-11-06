import pymel.core.uitypes as gui
import pymel.core as pm

from cwmaya.lib import reloader
import importlib

importlib.reload(reloader)

from cwmaya.lib import (
    export_tab,
    render_tab,
    comp_tab,
    slack_tab,
    tools_menu,
)


# from uprising import pov
WINDOW_TITLE = "Storm Tools"


class StormWindow(gui.Window):
    def __init__(self):

        others = pm.lsUI(windows=True)
        for win in others:
            if pm.window(win, q=True, title=True) == WINDOW_TITLE:
                pm.deleteUI(win)

        self.setTitle(WINDOW_TITLE)
        self.setIconName(WINDOW_TITLE)
        self.setWidthHeight([800, 600])

        self.menuBarLayout = pm.menuBarLayout()

        self.tabs = pm.tabLayout(changeCommand=pm.Callback(self.on_tab_changed))

        # TABS
        pm.setParent(self.tabs)
        self.export_tab = export_tab.ExportTab()
        self.tabs.setTabLabel((self.export_tab, "Export Task"))  


        pm.setParent(self.tabs)
        self.render_tab = render_tab.RenderTab()
        self.tabs.setTabLabel((self.render_tab, "Render Task"))

        pm.setParent(self.tabs)
        self.comp_tab = comp_tab.CompTab()
        self.tabs.setTabLabel((self.comp_tab, "Comp Task"))
        
        pm.setParent(self.tabs)
        self.slack_tab = slack_tab.SlackTab()
        self.tabs.setTabLabel((self.slack_tab, "Slack Task"))

        # MENUS
        pm.setParent(self.menuBarLayout)
        self.tools_menu = tools_menu.create()

        self.show()
        self.setResizeToFitChildren()

        self.populate()

    def on_tab_changed(self):
        self.save()

    def populate(self):
        var = ("storm_tab_index", 1)
        self.tabs.setSelectTabIndex(pm.optionVar.get(var[0], var[1]))

    def save(self):
        var = "storm_tab_index"
        pm.optionVar[var] = self.tabs.getSelectTabIndex()
