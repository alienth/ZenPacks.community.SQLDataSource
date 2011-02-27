
import Globals
import os.path
import sys

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

from Products.ZenModel.ZenPack import ZenPackBase
from Products.ZenModel.DataPointGraphPoint import DataPointGraphPoint

class ZenPack(ZenPackBase):
    """ SQLDataSource loader
    """

    _gdmap = (('Event Queue', 'eventQueueLength'),
            ('Data Point Rate', 'dataPoints'),
            ('Config Time', 'configTime'),
            ('Data Points', 'cyclePoints'))

    def install(self, app):
        if not hasattr(app.zport.dmd.Events.Status, 'PyDBAPI'):
            app.zport.dmd.Events.createOrganizer("/Status/PyDBAPI")
        pct = app.zport.dmd.Monitors.rrdTemplates.PerformanceConf
        if hasattr(pct.datasources, 'zenperfsql'):
            pct.manage_deleteRRDDataSources(['zenperfsql'])
        ds = pct.manage_addRRDDataSource('zenperfsql', 'BuiltInDS.Built-In')
        for gdn, dpn in self._gdmap:
            dp = ds.manage_addRRDDataPoint(dpn)
            if dpn in ['dataPoints']:
                dp.rrdtype = 'DERIVE'
                dp.rrdmin = 0
            gd = getattr(pct.graphDefs, gdn, None)
            if not gd: continue
            if hasattr(gd.graphPoints, 'zenperfsql'): continue
            gdp = gd.createGraphPoint(DataPointGraphPoint, 'zenperfsql')
            gdp.dpName = 'zenperfsql_%s'%dpn
        ZenPackBase.install(self, app)

    def upgrade(self, app):
        if not hasattr(app.zport.dmd.Events.Status, 'PyDBAPI'):
            app.zport.dmd.Events.createOrganizer("/Status/PyDBAPI")
        pct = app.zport.dmd.Monitors.rrdTemplates.PerformanceConf
        if hasattr(pct.datasources, 'zenperfsql'):
            pct.manage_deleteRRDDataSources(['zenperfsql'])
        ds = pct.manage_addRRDDataSource('zenperfsql', 'BuiltInDS.Built-In')
        for gdn, dpn in self._gdmap:
            dp = ds.manage_addRRDDataPoint(dpn)
            if dpn in ['dataPoints']:
                dp.rrdtype = 'DERIVE'
                dp.rrdmin = 0
            gd = getattr(pct.graphDefs, gdn, None)
            if not gd: continue
            if hasattr(gd.graphPoints, 'zenperfsql'): continue
            gdp = gd.createGraphPoint(DataPointGraphPoint, 'zenperfsql')
            gdp.dpName = 'zenperfsql_%s'%dpn
        ZenPackBase.upgrade(self, app)

    def remove(self, app, leaveObjects=False):
        pct = app.zport.dmd.Monitors.rrdTemplates.PerformanceConf
        for gdn, dpn in self._gdmap:
            gd = getattr(pct.graphDefs, gdn, None)
            if not gd: continue
            gd.manage_deleteGraphPoints(['zenperfsql'])
        if hasattr(pct.datasources, 'zenperfsql'):
            pct.manage_deleteRRDDataSources(['zenperfsql'])
        ZenPackBase.remove(self, app, leaveObjects)
