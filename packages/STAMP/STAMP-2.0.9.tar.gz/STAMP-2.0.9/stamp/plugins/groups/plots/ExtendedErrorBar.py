#=======================================================================
# Author: Donovan Parks
#
# Extended error bar plot.
#
# Copyright 2011 Donovan Parks
#
# This file is part of STAMP.
#
# STAMP is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# STAMP is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with STAMP.  If not, see <http://www.gnu.org/licenses/>.
#=======================================================================

from PyQt4 import QtGui, QtCore

import sys
import math
import numpy as np
from mpl_toolkits.axes_grid import make_axes_locatable, Size

from stamp.plugins.groups.AbstractGroupPlotPlugin import AbstractGroupPlotPlugin, TestWindow, ConfigureDialog
from stamp.plugins.groups.plots.configGUI.extendedErrorBarUI import Ui_ExtendedErrorBarDialog
from stamp.metagenomics import TableHelper

from matplotlib.patches import Rectangle
		
class ExtendedErrorBar(AbstractGroupPlotPlugin):
	'''
	Extended error bar plot.
	'''	 
	def __init__(self, preferences, parent=None):
		AbstractGroupPlotPlugin.__init__(self, preferences, parent)
		
		self.name = 'Extended error bar'
		self.type = 'Statistical'
		
		self.bSupportsHighlight = True
		self.bPlotFeaturesIndividually = False
		
		self.settings = preferences['Settings']
		self.figWidth = self.settings.value('group: ' + self.name + '/width', 7.0).toDouble()[0]
		self.figHeightPerRow = self.settings.value('group: ' + self.name + '/row height', 0.2).toDouble()[0]
		self.sortingField = self.settings.value('group: ' + self.name + '/field', 'p-values').toString()
		self.bShowBarPlot = self.settings.value('group: ' + self.name + '/sequences subplot', True).toBool()
		self.bShowPValueLabels = self.settings.value('group: ' + self.name + '/p-value labels', True).toBool()
		self.bShowCorrectedPvalues = self.settings.value('group: ' + self.name + '/show corrected p-values', True).toBool()
		self.bCustomLimits = self.settings.value('group: ' + self.name + '/use custom limits', False).toBool()
		self.minX = self.settings.value('group: ' + self.name + '/minimum', 0.0).toDouble()[0]
		self.maxX = self.settings.value('group: ' + self.name + '/maximum', 1.0).toDouble()[0]
		self.markerSize = self.settings.value('group: ' + self.name + '/marker size', 30).toInt()[0]
		self.bShowStdDev = self.settings.value('group: ' + self.name + '/show std. dev.', False).toBool()
		self.endCapSize = self.settings.value('group: ' + self.name + '/end cap size', 0.0).toInt()[0]
		self.legendPos = self.settings.value('group: ' + self.name + '/legend position', -1).toInt()[0]

	def mirrorProperties(self, plotToCopy):
		self.name = plotToCopy.name
		
		self.figWidth = plotToCopy.figWidth
		self.figHeightPerRow = plotToCopy.figHeightPerRow
		
		self.sortingField = plotToCopy.sortingField
		
		self.bShowBarPlot = plotToCopy.bShowBarPlot
		self.bShowPValueLabels = plotToCopy.bShowPValueLabels
		
		self.bShowCorrectedPvalues = plotToCopy.bShowCorrectedPvalues
		
		self.bCustomLimits = plotToCopy.bCustomLimits
		self.minX = plotToCopy.minX
		self.maxX = plotToCopy.maxX
		
		self.markerSize = plotToCopy.markerSize
		self.bShowStdDev = plotToCopy.bShowStdDev
		self.endCapSize = plotToCopy.endCapSize
		
		self.legendPos = plotToCopy.legendPos
	
	def plot(self, profile, statsResults):
		# *** Check if there is sufficient data to generate the plot
		if len(statsResults.activeData) <= 0:
			self.emptyAxis()			
			return
		
		features = statsResults.getColumn('Features')
		if len(features) > 200:
			QtGui.QApplication.instance().setOverrideCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
			reply = QtGui.QMessageBox.question(self, 'Continue?', 'Profile contains ' + str(len(features)) + ' features. ' +
																		'It may take several seconds to generate this plot. We recommend filtering your profile first. ' + 
																		'Do you wish to continue?', QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
			QtGui.QApplication.instance().restoreOverrideCursor()
			if reply == QtGui.QMessageBox.No:
				self.emptyAxis()	
				return

		
		# *** Colour of plot elements
		axesColour = str(self.preferences['Axes colour'].name())
		group1Colour = str(self.preferences['Group colours'][profile.groupName1].name())
		group2Colour = str(self.preferences['Group colours'][profile.groupName2].name())
						
		# *** Colour of plot elements
		highlightColor = (0.9, 0.9, 0.9)
		
		# *** Sort data
		if self.sortingField == 'p-values':
			statsResults.activeData = TableHelper.SortTable(statsResults.activeData,\
																												[statsResults.dataHeadings['pValues']], False)
		elif self.sortingField == 'Effect sizes':
			statsResults.activeData = TableHelper.SortTable(statsResults.activeData,\
																												[statsResults.dataHeadings['EffectSize']], 
																												True, True, False)
			
		elif self.sortingField == 'Feature labels':
			statsResults.activeData = TableHelper.SortTableStrCol(statsResults.activeData,\
																												statsResults.dataHeadings['Features'], False)

		features = statsResults.getColumn('Features')	# get sorted feature labels
					
		# *** Create lists for each quantity of interest
		if statsResults.multCompCorrection.method == 'False discovery rate':
			pValueTitle = 'q-value'
		else:
			pValueTitle = 'p-value'

		if self.bShowCorrectedPvalues:
			pValueLabels = statsResults.getColumnAsStr('pValuesCorrected')
			pValueTitle += ' (corrected)'
		else:
			pValueLabels = statsResults.getColumnAsStr('pValues')
			
		effectSizes = statsResults.getColumn('EffectSize')
		
		lowerCIs = statsResults.getColumn('LowerCI')
		upperCIs = statsResults.getColumn('UpperCI')
		ciTitle = ('%.3g' % (statsResults.oneMinusAlpha()*100)) + '% confidence intervals'
			
		# *** Truncate feature labels
		highlightedFeatures = list(self.preferences['Highlighted group features'])
		if self.preferences['Truncate feature names']:
			length = self.preferences['Length of truncated feature names']
			
			for i in xrange(0, len(features)):
				if len(features[i]) > length+3:
					features[i] = features[i][0:length] + '...'
								
			for i in xrange(0, len(highlightedFeatures)):
				if len(highlightedFeatures[i]) > length+3:
					highlightedFeatures[i] = highlightedFeatures[i][0:length] + '...'
					
		# *** Check that there is at least one significant feature
		if len(features) <= 0:
			self.emptyAxis('No significant features')
			return
				
		# *** Adjust effect size for axis scale
		dominateInSample2 = []
		percentage1 = []
		percentage2 = []
		for i in xrange(0, len(effectSizes)):
			if statsResults.bConfIntervRatio:
				if effectSizes[i] < 1:
					# mirror CI across y-axis
					effectSizes[i] = 1.0 / effectSizes[i]
					lowerCI = effectSizes[i] - (1.0 / upperCIs[i])
					upperCI = (1.0 / lowerCIs[i]) - effectSizes[i]

					lowerCIs[i] = lowerCI
					upperCIs[i] = upperCI

					dominateInSample2.append(i)
				else:
					lowerCIs[i] = effectSizes[i] - lowerCIs[i]
					upperCIs[i] = upperCIs[i] - effectSizes[i] 
			else:
				lowerCIs[i] = effectSizes[i] - lowerCIs[i]
				upperCIs[i] = upperCIs[i] - effectSizes[i]
				if effectSizes[i] < 0.0:
					dominateInSample2.append(i)

		# *** Set figure size
		if self.legendPos == 3 or self.legendPos == 4 or self.legendPos == 8: # bottom legend
			heightBottomLabels = 0.56	# inches
		else:
			heightBottomLabels = 0.4	# inches
			
		heightTopLabels = 0.25
		plotHeight = self.figHeightPerRow*len(features) 
		self.imageWidth = self.figWidth
		self.imageHeight = plotHeight + heightBottomLabels + heightTopLabels
		if self.imageWidth > 256 or self.imageHeight > 256:
				QtGui.QApplication.instance().setOverrideCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
				self.emptyAxis()	
				reply = QtGui.QMessageBox.question(self, 'Excessively large plot', 'The resulting plot is too large to display.')
				QtGui.QApplication.instance().restoreOverrideCursor()
				return
		
		self.fig.set_size_inches(self.imageWidth, self.imageHeight)	
				
		# *** Determine width of y-axis labels
		yLabelBounds = self.yLabelExtents(features, 8)
		
		# *** Size plots which comprise the extended errorbar plot
		self.fig.clear()

		spacingBetweenPlots = 0.25	# inches
		widthNumSeqPlot = 1.25	# inches
		if self.bShowBarPlot == False:
			widthNumSeqPlot = 0.0
			spacingBetweenPlots = 0.0
		
		widthPvalueLabels = 0.75	# inches
		if self.bShowPValueLabels == False:
			widthPvalueLabels = 0.1
				 
		yPlotOffsetFigSpace = heightBottomLabels / self.imageHeight 
		heightPlotFigSpace = plotHeight / self.imageHeight
			 
		xPlotOffsetFigSpace = yLabelBounds.width + 0.1 / self.imageWidth
		pValueLabelWidthFigSpace =	widthPvalueLabels / self.imageWidth
		widthPlotFigSpace = 1.0 - pValueLabelWidthFigSpace - xPlotOffsetFigSpace
		
		widthErrorBarPlot = widthPlotFigSpace*self.imageWidth - widthNumSeqPlot - spacingBetweenPlots
				
		axInitAxis = self.fig.add_axes([xPlotOffsetFigSpace,yPlotOffsetFigSpace,widthPlotFigSpace,heightPlotFigSpace])		
		divider = make_axes_locatable(axInitAxis)	
		divider.get_vertical()[0] = Size.Fixed(len(features)*self.figHeightPerRow)
	 
		if self.bShowBarPlot == True:	 
			divider.get_horizontal()[0] = Size.Fixed(widthNumSeqPlot)
			axErrorbar = divider.new_horizontal(widthErrorBarPlot, pad=spacingBetweenPlots, sharey=axInitAxis)
			self.fig.add_axes(axErrorbar)
		else:
			divider.get_horizontal()[0] = Size.Fixed(widthErrorBarPlot)
			axErrorbar = axInitAxis
				
		# *** Plot of sequences for each subsystem
		if self.bShowBarPlot == True:
			axNumSeq = axInitAxis

			meanRelFreqSeqs1 = statsResults.getColumn('MeanRelFreq1')
			meanRelFreqSeqs2 = statsResults.getColumn('MeanRelFreq2')
			
			if self.bShowStdDev:
				stdDev1 = statsResults.getColumn('StdDevRelFreq1')
				stdDev2 = statsResults.getColumn('StdDevRelFreq2')
				endCapSize = self.endCapSize
			else:
				stdDev1 = [0] * len(meanRelFreqSeqs1)
				stdDev2 = [0] * len(meanRelFreqSeqs2)
				endCapSize = 0

			axNumSeq.barh(np.arange(len(features))+0.0, meanRelFreqSeqs1, height = 0.3, xerr=stdDev1, color=group1Colour, ecolor='black', capsize=endCapSize)
			axNumSeq.barh(np.arange(len(features))-0.3, meanRelFreqSeqs2, height = 0.3, xerr=stdDev2, color=group2Colour, ecolor='black', capsize=endCapSize)
			for value in np.arange(-0.5, len(features)-1, 2):
				axNumSeq.axhspan(value, value+1, facecolor=highlightColor,edgecolor='none',zorder=-1)
			
			axNumSeq.set_xlabel('Mean proportion (%)')
			maxPercentage = max(max(meanRelFreqSeqs1), max(meanRelFreqSeqs2))
			axNumSeq.set_xticks([0, maxPercentage])
			axNumSeq.set_xlim([0, maxPercentage*1.05])
			maxPercentageStr = '%.1f' % maxPercentage
			axNumSeq.set_xticklabels(['0.0', maxPercentageStr])
				
			axNumSeq.set_yticks(np.arange(len(features)))
			axNumSeq.set_yticklabels(features)
			axNumSeq.set_ylim([-1, len(features)])
			
			for label in axNumSeq.get_yticklabels():
				if label.get_text() in highlightedFeatures:
					label.set_color('red')
					
			for a in axNumSeq.yaxis.majorTicks:
				a.tick1On=False
				a.tick2On=False
					
			for a in axNumSeq.xaxis.majorTicks:
				a.tick1On=True
				a.tick2On=False
				
			for line in axNumSeq.yaxis.get_ticklines(): 
				line.set_color(axesColour)
				
			for line in axNumSeq.xaxis.get_ticklines(): 
				line.set_color(axesColour)
					
			for loc, spine in axNumSeq.spines.iteritems():
				if loc in ['left', 'right','top']:
					spine.set_color('none') 
				else:
					spine.set_color(axesColour)
						
		# *** Plot confidence intervals for each subsystem
		lastAxes = axErrorbar
		markerSize = math.sqrt(float(self.markerSize))
		axErrorbar.errorbar(effectSizes, np.arange(len(features)), xerr=[lowerCIs,upperCIs], fmt='o', ms=markerSize, mfc=group1Colour, mec='black', ecolor='black', zorder=10)
		effectSizesSample2 = [effectSizes[value] for value in dominateInSample2]
		axErrorbar.plot(effectSizesSample2, dominateInSample2, ls='', marker='o', ms=markerSize, mfc=group2Colour, mec='black', zorder=100)
		
		if statsResults.bConfIntervRatio:
			axErrorbar.vlines(1, -1, len(features), linestyle='dashed', color=axesColour)
		else:
			axErrorbar.vlines(0, -1, len(features), linestyle='dashed', color=axesColour)
		
		for value in np.arange(-0.5, len(features)-1, 2):
			axErrorbar.axhspan(value, value+1, facecolor=highlightColor,edgecolor='none',zorder=1)

		axErrorbar.set_title(ciTitle) 
		axErrorbar.set_xlabel('Difference in mean proportions (%)')
		
		if self.bCustomLimits:
			axErrorbar.set_xlim([self.minX, self.maxX])
		else:
			self.minX, self.maxX = axErrorbar.get_xlim()
 
		if self.bShowBarPlot == False:
			axErrorbar.set_yticks(np.arange(len(features)))
			axErrorbar.set_yticklabels(features)
			axErrorbar.set_ylim([-1, len(features)])
			
			for label in axErrorbar.get_yticklabels():
				if label.get_text() in self.preferences['Highlighted group features']:
					label.set_color('red')
		else:
			for label in axErrorbar.get_yticklabels():
				label.set_visible(False)
				
			for a in axErrorbar.yaxis.majorTicks:
				a.set_visible(False)
				
		for a in axErrorbar.xaxis.majorTicks:
			a.tick1On=True
			a.tick2On=False
				
		for a in axErrorbar.yaxis.majorTicks:
			a.tick1On=False
			a.tick2On=False
			
		for line in axErrorbar.yaxis.get_ticklines(): 
			line.set_visible(False)
				
		for line in axErrorbar.xaxis.get_ticklines(): 
			line.set_color(axesColour)

		for loc, spine in axErrorbar.spines.iteritems():
			if loc in ['left','right','top']:
				spine.set_color('none') 
			else:
				spine.set_color(axesColour)
						
		# *** Show p-values on right of last plot
		if self.bShowPValueLabels == True:
			axRight = lastAxes.twinx()
			axRight.set_yticks(np.arange(len(pValueLabels)))
			axRight.set_yticklabels(pValueLabels)
			axRight.set_ylim([-1, len(pValueLabels)])
			axRight.set_ylabel(pValueTitle)
			
			for a in axRight.yaxis.majorTicks:
				a.tick1On=False
				a.tick2On=False
				
		# *** Legend
		if self.legendPos != -1:
			legend1 = Rectangle((0, 0), 1, 1, fc=group1Colour)
			legend2 = Rectangle((0, 0), 1, 1, fc=group2Colour)
			legend = self.fig.legend([legend1, legend2], (profile.groupName1, profile.groupName2), loc=self.legendPos, ncol=2)
			legend.get_frame().set_linewidth(0)

		self.updateGeometry()
		self.draw()

	def configure(self, profile, statsResults):
		self.statsResults = statsResults
		
		self.configDlg = ConfigureDialog(Ui_ExtendedErrorBarDialog)
		
		# set enabled state of controls
		self.configDlg.ui.chkShowStdDev.setChecked(self.bShowBarPlot)
		self.configDlg.ui.spinEndCapSize.setValue(self.bShowBarPlot)
		self.configDlg.ui.spinMinimumX.setEnabled(self.bCustomLimits)
		self.configDlg.ui.spinMaximumX.setEnabled(self.bCustomLimits)

		# set current value of controls
		self.configDlg.ui.cboSortingField.setCurrentIndex(self.configDlg.ui.cboSortingField.findText(self.sortingField))
		
		self.configDlg.ui.spinFigWidth.setValue(self.figWidth)
		self.configDlg.ui.spinFigRowHeight.setValue(self.figHeightPerRow)
		
		self.configDlg.ui.chkShowBarPlot.setChecked(self.bShowBarPlot)
		self.configDlg.ui.chkPValueLabels.setChecked(self.bShowPValueLabels)
		
		self.configDlg.ui.chkCorrectedPvalues.setChecked(self.bShowCorrectedPvalues)
		
		self.configDlg.ui.chkCustomLimits.setChecked(self.bCustomLimits)
		self.configDlg.ui.spinMinimumX.setValue(self.minX)
		self.configDlg.ui.spinMaximumX.setValue(self.maxX)
		
		self.configDlg.ui.spinMarkerSize.setValue(self.markerSize)
		
		self.configDlg.ui.chkShowStdDev.setChecked(self.bShowStdDev)
		self.configDlg.ui.spinEndCapSize.setValue(self.endCapSize)
		
		if self.legendPos == 2:
			self.configDlg.ui.radioLegendPosUpperLeft.setChecked(True)
		elif self.legendPos == 3:
			self.configDlg.ui.radioLegendPosLowerLeft.setChecked(True)
		elif self.legendPos == 4:
			self.configDlg.ui.radioLegendPosLowerRight.setChecked(True)
		elif self.legendPos == 8:
			self.configDlg.ui.radioLegendPosLowerCentre.setChecked(True)
		else:
			self.configDlg.ui.radioLegendPosNone.setChecked(True)
				
		if self.configDlg.exec_() == QtGui.QDialog.Accepted:
			QtGui.QApplication.instance().setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
			
			self.sortingField = str(self.configDlg.ui.cboSortingField.currentText())
			
			self.figWidth = self.configDlg.ui.spinFigWidth.value()
			self.figHeightPerRow = self.configDlg.ui.spinFigRowHeight.value()
			
			self.bShowBarPlot = self.configDlg.ui.chkShowBarPlot.isChecked()
			self.bShowPValueLabels = self.configDlg.ui.chkPValueLabels.isChecked()			
			self.bShowCorrectedPvalues = self.configDlg.ui.chkCorrectedPvalues.isChecked()
			
			self.bCustomLimits = self.configDlg.ui.chkCustomLimits.isChecked()
			self.minX = self.configDlg.ui.spinMinimumX.value()
			self.maxX = self.configDlg.ui.spinMaximumX.value()
			
			self.markerSize = self.configDlg.ui.spinMarkerSize.value()
			
			self.bShowStdDev = self.configDlg.ui.chkShowStdDev.isChecked()
			self.endCapSize = self.configDlg.ui.spinEndCapSize.value()
			
			# legend position			
			if self.configDlg.ui.radioLegendPosUpperLeft.isChecked() == True:
				self.legendPos = 2
			elif self.configDlg.ui.radioLegendPosLowerLeft.isChecked() == True:
				self.legendPos = 3
			elif self.configDlg.ui.radioLegendPosLowerCentre.isChecked() == True:
				self.legendPos = 8
			elif self.configDlg.ui.radioLegendPosLowerRight.isChecked() == True:
				self.legendPos = 4
			else:
				self.legendPos = -1
			
			self.settings.setValue('group: ' + self.name + '/width', self.figWidth)
			self.settings.setValue('group: ' + self.name + '/row height', self.figHeightPerRow)
			self.settings.setValue('group: ' + self.name + '/field', self.sortingField)
			self.settings.setValue('group: ' + self.name + '/sequences subplot', self.bShowBarPlot)
			self.settings.setValue('group: ' + self.name + '/p-value labels', self.bShowPValueLabels)
			self.settings.setValue('group: ' + self.name + '/show corrected p-values', self.bShowCorrectedPvalues)
			self.settings.setValue('group: ' + self.name + '/use custom limits', self.bCustomLimits)
			self.settings.setValue('group: ' + self.name + '/minimum', self.minX)
			self.settings.setValue('group: ' + self.name + '/maximum', self.maxX)
			self.settings.setValue('group: ' + self.name + '/marker size', self.markerSize)
			self.settings.setValue('group: ' + self.name + '/show std. dev.', self.bShowStdDev)
			self.settings.setValue('group: ' + self.name + '/end cap size', self.endCapSize)
			self.settings.setValue('group: ' + self.name + '/legend position', self.legendPos)

			self.plot(profile, statsResults)
			
			QtGui.QApplication.instance().restoreOverrideCursor()	 

if __name__ == "__main__": 
	app = QtGui.QApplication(sys.argv)
	testWindow = TestWindow(ExtendedErrorBar)
	testWindow.show()
	sys.exit(app.exec_())
