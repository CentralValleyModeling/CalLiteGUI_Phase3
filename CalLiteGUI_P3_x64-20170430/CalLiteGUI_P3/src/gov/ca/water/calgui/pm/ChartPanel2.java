package gov.ca.water.calgui.pm;

import java.awt.Component;
import java.awt.Dimension;
import java.awt.GridLayout;

import javax.swing.JPanel;

import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartPanel;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.axis.NumberAxis;
import org.jfree.data.time.TimeSeries;
import org.jfree.data.xy.XYSeries;
import org.jfree.data.xy.XYSeriesCollection;

import gov.ca.water.calgui.constant.Constant;

public class ChartPanel2 extends JPanel {

	/**
	 * 
	 */
	private static final long serialVersionUID = -4268988706560498661L;

	private JFreeChart[] charts = new JFreeChart[12];

	private TimeSeries[][][] ex_series = PM_Data.getInstance().getExSeries();
	private XYSeries[] dataSeries = new XYSeries[12];
	private XYSeriesCollection[] xydatasets = new XYSeriesCollection[12];
	private ChartPanel[] panels = new ChartPanel[12];

	private int getMonth(String month) {
		int i = "janfebmaraprmayjunjulaugsepoctnovdec".indexOf(month.toLowerCase()) / 3;
		return i;
	}

	private int getCPart(String cpart) {
		for (int i = 0; i < Constant.CPARTS.length; i++) {
			if (cpart.equals(Constant.CPARTS[i]))
				return i;
		}
		return -1;
	}

	private int getBPart(String bpart) {
		for (int i = 0; i < Constant.BPARTS.length; i++) {
			if (bpart.equals(Constant.BPARTS[i]))
				return i;
		}
		return -1;
	}

	/**
	 * Provides access to array by month or by station of a parameter
	 * 
	 * @param bPart
	 * @param cPart
	 * @param month
	 */
	public ChartPanel2() {

		super();
		this.setLayout(new GridLayout(0, 4));
		// Set up time series charts
		for (int i = 0; i < 12; i++) {
			dataSeries[i] = new XYSeries("");
			xydatasets[i] = new XYSeriesCollection();

			charts[i] = ChartFactory.createXYLineChart("", "", "", null, false);
			panels[i] = new ChartPanel(charts[i]);
			panels[i].setMaximumDrawHeight(1200);
			panels[i].setMaximumDrawWidth(1920);
			panels[i].setMinimumDrawHeight(200);
			panels[i].setMinimumDrawWidth(300);
			panels[i].setPreferredSize(new Dimension(300, 200));

		}
	}

	/**
	 * Remove all chart subpanels from panel, then rebuild
	 * 
	 * @param bPart
	 * @param cPart
	 * @param month
	 * @param isExceedance
	 */
	public void resetCharts(String bPart, String cPart, String month, boolean isExceedance) {

		for (Component c : this.getComponents())
			if (c instanceof ChartPanel)
				this.remove(c);

		if (bPart.equals(""))
			buildStationCharts(month, cPart, isExceedance);
		else
			buildMonthCharts(bPart, cPart, isExceedance);

		this.invalidate();
	}

	/**
	 * Builds an array by station of charts for a given month
	 * 
	 * @param month
	 * @param isExceedance
	 */
	private void buildStationCharts(String month, String cPart, boolean isExceedance) {
		int m = getMonth(month);
		int c = getCPart(cPart);
		double max = 0.0;
		for (int i = 0; i < Constant.BPARTS.length; i++) {

			// Set series

			dataSeries[i].clear();
			Integer n = ex_series[i][c][m].getItemCount();

			for (int j = 0; j < n; j++) {
				dataSeries[i].add(100.0 - 100.0 * j / (n - 1), ex_series[i][c][m].getValue(j));
				max = Math.max(max, (double) ex_series[i][c][m].getValue(j));
			}

			// Build chart

			XYSeriesCollection sc = (XYSeriesCollection) charts[i].getXYPlot().getDataset();
			if (sc == null) {
				sc = new XYSeriesCollection();
				charts[i].getXYPlot().setDataset(sc);
			} else
				sc.removeAllSeries();

			sc.addSeries(dataSeries[i]);
			panels[i].getChart().getXYPlot().getRangeAxis().setLabel(cPart);
			panels[i].getChart().setTitle(Constant.BPARTS[i]);
			this.add(panels[i]);
		}
		for (int i = 0; i < Constant.BPARTS.length; i++) {
			NumberAxis axis = (NumberAxis) panels[i].getChart().getXYPlot().getRangeAxis();
			axis.setRange(0, max);
		}
	}

	private void buildMonthCharts(String bPart, String cPart, boolean isExceedance) {

		int c = getCPart(cPart);
		int b = getBPart(bPart);

		double max = 0.0;

		for (int m = 0; m < 12; m++) {

			// Set series

			dataSeries[m].clear();
			Integer n = ex_series[b][c][m].getItemCount();

			for (int j = 0; j < n; j++) {
				dataSeries[m].add(100.0 - 100.0 * j / (n - 1), ex_series[b][c][m].getValue(j));
				max = Math.max(max, (double) ex_series[b][c][m].getValue(j));
			}

			// Build chart

			XYSeriesCollection sc = (XYSeriesCollection) charts[m].getXYPlot().getDataset();
			if (sc == null) {
				sc = new XYSeriesCollection();
				charts[m].getXYPlot().setDataset(sc);
			} else
				sc.removeAllSeries();

			sc.addSeries(dataSeries[m]);
			panels[m].getChart().getXYPlot().getRangeAxis().setLabel(cPart);
			panels[m].getChart()
					.setTitle(bPart + " - " + "JanFebMarAprMayJunJulAugSepOctNovDec".substring(3 * m, 3 * m + 3));
			this.add(panels[m]);
		}
		for (int i = 0; i < 12; i++) {
			NumberAxis axis = (NumberAxis) panels[i].getChart().getXYPlot().getRangeAxis();
			axis.setRange(0, max);
		}

		this.invalidate();
	}

	public void setTitle(String s) {
		charts[0].getXYPlot().getRangeAxis().setLabel(s);
	}
}