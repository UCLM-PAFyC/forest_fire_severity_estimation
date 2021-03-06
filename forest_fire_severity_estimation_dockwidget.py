# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ForestFireSeverityEstimationDockWidget
                                 A QGIS plugin
 Forest fire severity estimation using DNBR index from Sentinel-2
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2022-04-10
        git sha              : $Format:%H$
        copyright            : (C) 2022 by David Hernández López
        email                : david.hernandez@uclm.es
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from qgis.PyQt import QtGui, QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSignal, QSettings, QTranslator, qVersion, QCoreApplication, QFileInfo, QDir, QObject, QDate
from qgis.PyQt.QtWidgets import QMessageBox, QInputDialog, QLineEdit, QFileDialog
from qgis.core import QgsApplication, QgsDataSourceUri,QgsMapLayerProxyModel, QgsRectangle, QgsGeometry, \
    QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsProject, QgsVectorLayer

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'forest_fire_severity_estimation_dockwidget_base.ui'))

from .about_qdialog import AboutQDialog
from . import definitions

class ForestFireSeverityEstimationDockWidget(QtWidgets.QDockWidget, FORM_CLASS):

    closingPlugin = pyqtSignal()

    def __init__(self,
                 iface,
                 pluginPath,
                 currentPluginName,
                 settings,
                 parent=None):
        """Constructor."""
        super(ForestFireSeverityEstimationDockWidget, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://doc.qt.io/qt-5/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.windowTitle = definitions.CONST_PROGRAM_NAME
        self.iface = iface
        self.path_plugin = pluginPath
        self.current_plugin_name = currentPluginName
        self.settings = settings
        self.setupUi(self)
        self.initialize()

    def addNBR(self,image):
        """A function to compute NDVI."""
        ndvi = image.normalizedDifference(['B8', 'B12']).rename('nbr')
        return image.addBands([ndvi])

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()

    def initialize(self):
        self.about_qdialog = None
        self.ee_uninitialized = True

        path_file_qsettings = self.path_plugin + '/' + definitions.CONST_SETTINGS_FILE_NAME
        self.settings = QSettings(path_file_qsettings,QSettings.IniFormat)

        qs = QSettings()
        self.about_qdialog = None
        self.aboutPushButton.clicked.connect(self.showAboutDlg)
        self.googleDrivePathPushButton.clicked.connect(self.selectGoogleDrivePath)
        self.outputFileNamePushButton.clicked.connect(self.selectOutputFileName)
        self.processPushButton.clicked.connect(self.process)
        self.loadResultPushButton.clicked.connect(self.loadResult)

        pluginsPath = QFileInfo(QgsApplication.qgisUserDatabaseFilePath()).path()
        thisFilePath = os.path.dirname(os.path.realpath(__file__))
        thisFilePath = os.path.join(pluginsPath, thisFilePath)

        self.templatePath = thisFilePath + definitions.CONST_TEMPLATE_PATH
        self.qmlDNBRFileName = self.templatePath + definitions.CONST_DNBR_SYMBOLOGY_TEMPLATE

        self.path = self.settings.value(definitions.CONST_SETTINGS_LAST_PATH_TAG)
        if not self.path:
            self.path = QDir.currentPath()
            self.settings.setValue(definitions.CONST_SETTINGS_LAST_PATH_TAG,self.path)
            self.settings.sync()

        self.roiLayerComboBox.setFilters(QgsMapLayerProxyModel.VectorLayer)
        self.roiLayerComboBox.clear()
        existing_vector_layers = [l for l in QgsProject().instance().mapLayers().values() if isinstance(l, QgsVectorLayer)]
        self.roiLayerComboBox.setAdditionalLayers(existing_vector_layers)

        preFireInitialDateString = self.settings.value(definitions.CONST_SETTINGS_PREFIRE_INITIAL_DATE_TAG)
        if not preFireInitialDateString:
            preFireInitialDateString = definitions.CONST_PREFIRE_INITIAL_DATE_DEFAULT
        else:
            preFireInitialDate = QDate.fromString(preFireInitialDateString,
                                                  definitions.CONST_DATE_STRING_TEMPLATE)
            if not preFireInitialDate.isValid():
                preFireInitialDateString = definitions.CONST_PREFIRE_INITIAL_DATE_DEFAULT
        self.settings.setValue(definitions.CONST_SETTINGS_PREFIRE_INITIAL_DATE_TAG,
                               preFireInitialDateString)
        self.settings.sync()
        self.preFireInitialDateEdit.setDate(QDate.fromString(preFireInitialDateString,
                                                          definitions.CONST_DATE_STRING_TEMPLATE))

        preFireFinalDateString = self.settings.value(definitions.CONST_SETTINGS_PREFIRE_FINAL_DATE_TAG)
        if not preFireFinalDateString:
            preFireFinalDateString = definitions.CONST_PREFIRE_FINAL_DATE_DEFAULT
        else:
            preFireFinalDate = QDate.fromString(preFireFinalDateString,
                                                  definitions.CONST_DATE_STRING_TEMPLATE)
            if not preFireFinalDate.isValid():
                preFireFinalDateString = definitions.CONST_PREFIRE_FINAL_DATE_DEFAULT
        self.settings.setValue(definitions.CONST_SETTINGS_PREFIRE_FINAL_DATE_TAG,
                               preFireFinalDateString)
        self.settings.sync()
        self.preFireFinalDateEdit.setDate(QDate.fromString(preFireFinalDateString,
                                                          definitions.CONST_DATE_STRING_TEMPLATE))

        postFireInitialDateString = self.settings.value(definitions.CONST_SETTINGS_POSTFIRE_INITIAL_DATE_TAG)
        if not postFireInitialDateString:
            postFireInitialDateString = definitions.CONST_POSTFIRE_INITIAL_DATE_DEFAULT
        else:
            postFireInitialDate = QDate.fromString(postFireInitialDateString,
                                                  definitions.CONST_DATE_STRING_TEMPLATE)
            if not postFireInitialDate.isValid():
                postFireInitialDateString = definitions.CONST_POSTFIRE_INITIAL_DATE_DEFAULT
        self.settings.setValue(definitions.CONST_SETTINGS_POSTFIRE_INITIAL_DATE_TAG,
                               postFireInitialDateString)
        self.settings.sync()
        self.postFireInitialDateEdit.setDate(QDate.fromString(postFireInitialDateString,
                                                          definitions.CONST_DATE_STRING_TEMPLATE))

        postFireFinalDateString = self.settings.value(definitions.CONST_SETTINGS_POSTFIRE_FINAL_DATE_TAG)
        if not postFireFinalDateString:
            postFireFinalDateString = definitions.CONST_POSTFIRE_FINAL_DATE_DEFAULT
        else:
            postFireFinalDate = QDate.fromString(postFireFinalDateString,
                                                  definitions.CONST_DATE_STRING_TEMPLATE)
            if not postFireFinalDate.isValid():
                postFireFinalDateString = definitions.CONST_POSTFIRE_FINAL_DATE_DEFAULT
        self.settings.setValue(definitions.CONST_SETTINGS_POSTFIRE_FINAL_DATE_TAG,
                               postFireFinalDateString)
        self.settings.sync()
        self.postFireFinalDateEdit.setDate(QDate.fromString(postFireFinalDateString,
                                                          definitions.CONST_DATE_STRING_TEMPLATE))

        googleDrivePath = self.settings.value(definitions.CONST_SETTINGS_GOOGLE_DRIVE_PATH_TAG)
        if googleDrivePath:
            self.googleDrivePathLineEdit.setText(googleDrivePath)

        outputFileName = self.settings.value(definitions.CONST_SETTINGS_OUTPUT_FILE_NAME_TAG)
        if outputFileName:
            self.outputFileNameLineEdit.setText(outputFileName)

    def loadResult(self):
        filePath, _ = QFileDialog.getOpenFileName(self, 'Select downloaded GeoTIFF result',
                                            self.path, "GeoTIFF files (*.tif)")
        if filePath:
            fileInfo = QFileInfo(filePath)
            self.path = fileInfo.absolutePath()
            self.settings.setValue(definitions.CONST_SETTINGS_LAST_PATH_TAG, self.path)
            self.settings.sync()
            fileCompleteBaseName = fileInfo.completeBaseName()
            layerList = QgsProject.instance().mapLayersByName(fileCompleteBaseName)
            if not layerList:
                rlayer = self.iface.addRasterLayer(filePath, fileCompleteBaseName, "gdal")
                if rlayer.isValid():
                    # if vlayer.featureCount() == 0:
                    #     return
                    QgsProject.instance().addMapLayer(rlayer,False)
                    rlayer.loadNamedStyle(self.qmlDNBRFileName)
                    rlayer.triggerRepaint()
                    self.iface.setActiveLayer(rlayer)
                    self.iface.zoomToActiveLayer()
                else:
                    msgBox = QMessageBox(self)
                    msgBox.setIcon(QMessageBox.Information)
                    msgBox.setWindowTitle(self.windowTitle)
                    msgBox.setText("Error loading raster:\n" + filePath)
                    msgBox.exec_()

    def process(self):
        try:
            import ee
            MISSINGAPI = False
        except ImportError:
            MISSINGAPI = True
        if MISSINGAPI:
            text = 'Dependency error: earthengine-api must be installed'
            msgBox = QMessageBox(self.iface.mainWindow())
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setWindowTitle(definitions.CONST_PROGRAM_TITLE)
            msgBox.setText("Error:\n" + text)
            msgBox.exec_()
            return
        elif self.ee_uninitialized:
            try:
                ee.Initialize()
                self.ee_uninitialized = False
            except OSError:
                text = 'Fail to establish connection with the earthengine server'
                msgBox = QMessageBox(self.iface.mainWindow())
                msgBox.setIcon(QMessageBox.Information)
                msgBox.setWindowTitle(definitions.CONST_PROGRAM_TITLE)
                msgBox.setText("Error:\n" + text)
                msgBox.exec_()
                return
        from ee_plugin import Map
        from ee import batch
        roiLayer = self.roiLayerComboBox.currentLayer()
        if not roiLayer:
            text = "Load and select ROI layer"
            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setWindowTitle(self.windowTitle)
            msgBox.setText("Error:\n" + text)
            msgBox.exec_()
            return

        preFireInitialJulianDate = self.preFireInitialDateEdit.date().toJulianDay()
        preFireFinalJulianDate = self.preFireFinalDateEdit.date().toJulianDay()
        postFireInitialJulianDate = self.postFireInitialDateEdit.date().toJulianDay()
        postFireFinalJulianDate = self.postFireFinalDateEdit.date().toJulianDay()

        if preFireFinalJulianDate <= preFireInitialJulianDate:
            text = "Pre-fire final date must be later than pre-fire initial date"
            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setWindowTitle(self.windowTitle)
            msgBox.setText("Error:\n" + text)
            msgBox.exec_()
            return
        if (preFireFinalJulianDate-preFireInitialJulianDate)<definitions.CONST_MINIMAL_DATES_INTERVAL_PRE_AND_POST:
            text = "The pre-fire date interval must be greater than " + str(definitions.CONST_MINIMAL_DATES_INTERVAL_PRE_AND_POST-1)
            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setWindowTitle(self.windowTitle)
            msgBox.setText("Error:\n" + text)
            msgBox.exec_()
            return

        if postFireFinalJulianDate <= postFireInitialJulianDate:
            text = "Post-fire final date must be later than post-fire initial date"
            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setWindowTitle(self.windowTitle)
            msgBox.setText("Error:\n" + text)
            msgBox.exec_()
            return
        if (postFireFinalJulianDate-postFireInitialJulianDate)<definitions.CONST_MINIMAL_DATES_INTERVAL_PRE_AND_POST:
            text = "The post-fire date interval must be greater than " + str(definitions.CONST_MINIMAL_DATES_INTERVAL_PRE_AND_POST-1)
            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setWindowTitle(self.windowTitle)
            msgBox.setText("Error:\n" + text)
            msgBox.exec_()
            return

        googleDrivePath = self.googleDrivePathLineEdit.text()
        if not googleDrivePath:
            text = "Input Google Drive path for stores results"
            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setWindowTitle(self.windowTitle)
            msgBox.setText("Error:\n" + text)
            msgBox.exec_()
            return

        outputFileName = self.outputFileNameLineEdit.text()
        if not outputFileName:
            text = "Input a valid output GeoTIFF file name"
            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setWindowTitle(self.windowTitle)
            msgBox.setText("Error:\n" + text)
            msgBox.exec_()
            return

        roiLayerCrs = roiLayer.crs()
        roiExtentRectangle = roiLayer.extent()
        roiExtentWkt = roiExtentRectangle.asWktPolygon()
        roiExtentGeometry = QgsGeometry.fromWkt(roiExtentWkt)
        targetCrs = QgsCoordinateReferenceSystem(4326)
        crsOperation = QgsCoordinateTransform(roiLayerCrs, targetCrs, QgsProject.instance())
        roiExtentGeometry.transform(crsOperation)
        roiExtentWkt = roiExtentGeometry.asWkt()
        roiBoundigBox = roiExtentGeometry.boundingBox()
        westLongitude = roiBoundigBox.xMinimum()
        eastLongitude = roiBoundigBox.xMaximum()
        southLatitude = roiBoundigBox.yMinimum()
        northLatitude = roiBoundigBox.yMaximum()

        roi = ee.Geometry.Polygon([
            [[westLongitude, southLatitude], [westLongitude, northLatitude], [eastLongitude, northLatitude], [eastLongitude, southLatitude]]
        ])
        prefire_start = self.preFireInitialDateEdit.date().toString(definitions.CONST_DATE_STRING_TEMPLATE)
        prefire_end = self.preFireFinalDateEdit.date().toString(definitions.CONST_DATE_STRING_TEMPLATE)
        postfire_start = self.postFireInitialDateEdit.date().toString(definitions.CONST_DATE_STRING_TEMPLATE)
        postfire_end = self.postFireFinalDateEdit.date().toString(definitions.CONST_DATE_STRING_TEMPLATE)
        self.settings.setValue(definitions.CONST_SETTINGS_PREFIRE_INITIAL_DATE_TAG,
                               prefire_start)
        self.settings.setValue(definitions.CONST_SETTINGS_PREFIRE_FINAL_DATE_TAG,
                               prefire_end)
        self.settings.setValue(definitions.CONST_SETTINGS_POSTFIRE_INITIAL_DATE_TAG,
                               postfire_start)
        self.settings.setValue(definitions.CONST_SETTINGS_POSTFIRE_FINAL_DATE_TAG,
                               postfire_end)
        self.settings.sync()

        prefire_collection = ee.ImageCollection('COPERNICUS/S2') \
            .filterDate(prefire_start, prefire_end) \
            .filterMetadata('CLOUDY_PIXEL_PERCENTAGE', 'Less_Than', 10) \
            .map(self.addNBR).filterBounds(roi) \
            .max()
        prefire_nbr = prefire_collection.select('nbr')

        postfire_collection = ee.ImageCollection('COPERNICUS/S2') \
            .filterDate(postfire_start, postfire_end) \
            .filterMetadata('CLOUDY_PIXEL_PERCENTAGE', 'Less_Than', 10) \
            .map(self.addNBR) \
            .filterBounds(roi) \
            .min()
        postfire_nbr = postfire_collection.select('nbr')

        dNBR_unscaled = prefire_nbr.subtract(postfire_nbr)
        dNBR = dNBR_unscaled.multiply(1000)
        Map.addLayer(dNBR, {'min': -1000, 'max': 1000}, 'dNBR S2')

        task = ee.batch.Export.image.toDrive(image=dNBR,
                                             region=roi,
                                             folder=googleDrivePath,
                                             scale=10,
                                             # fileFormat: 'GeoTIFF',
                                             fileNamePrefix=outputFileName,
                                             crs='EPSG:25830')
        task.start()
        status = task.status()
        taskid, state = status['id'], status['state']
        if state == 'COMPLETED':
            self.iface.messageBar().pushMessage(f'Task id {taskid} is {state}. Please check GDrive')
        else:
            self.iface.messageBar().pushMessage(f'Task id {taskid} is {state}. Please wait and check GDrive')

        # msgBox = QMessageBox(self)
        # msgBox.setIcon(QMessageBox.Information)
        # msgBox.setWindowTitle(self.windowTitle)
        # msgBox.setText("ROI extent:\n" + roiExtentWkt)
        # msgBox.exec_()

    def selectGoogleDrivePath(self):
        oldText = self.googleDrivePathLineEdit.text()
        label = "Select Google Drive path for store results:"
        title = definitions.CONST_PROGRAM_TITLE
        [text, ok] = QInputDialog.getText(self, title, label, QLineEdit.Normal, oldText)
        if ok and text:
            text = text.strip()
            # text = text.replace(" ","")
            if not text == oldText:
                self.googleDrivePathLineEdit.setText(text)
                self.settings.setValue(definitions.CONST_SETTINGS_GOOGLE_DRIVE_PATH_TAG,
                                       text)
                self.settings.sync()
        return

    def selectOutputFileName(self):
        oldText = self.outputFileNameLineEdit.text()
        label = "Select a valid GeoTIFF output file name:"
        title = definitions.CONST_PROGRAM_TITLE
        [text, ok] = QInputDialog.getText(self, title, label, QLineEdit.Normal, oldText)
        if ok and text:
            text = text.strip()
            text = text.replace(" ","")
            if not text == oldText:
                self.outputFileNameLineEdit.setText(text)
                self.settings.setValue(definitions.CONST_SETTINGS_OUTPUT_FILE_NAME_TAG,
                                       text)
                self.settings.sync()
        return

    def showAboutDlg(self):
        if self.about_qdialog == None:
            self.about_qdialog = AboutQDialog()
        self.about_qdialog.show()
