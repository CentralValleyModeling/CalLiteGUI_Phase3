package gov.ca.water.calgui.pm;

import java.awt.Component;
import java.awt.Dimension;
import java.awt.GridLayout;

import javax.swing.JPanel;

import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartPanel;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.axis.NumberAxis;
import org.jfree.data.time.Month;
import org.jfree.data.time.TimeSeries;
import org.jfree.data.xy.XYSeries;
import org.jfree.data.xy.XYSeriesCollection;

import gov.ca.water.calgui.bus_service.impl.DSSGrabber1SvcImpl;
import hec.heclib.util.HecTime;
import hec.io.TimeSeriesContainer;

public class ChartPanel2 extends JPanel {

	private JFreeChart[] charts = new JFreeChart[12];
	private String[] bParts = { "CARRPP", "CVPSANLUISPP", "FOLSOMPP", "KESWICKPP", "NIMBUSPP", "ONEILPP", "SHASTAPP",
			"SPRINGCREEKPP", "TRINITYPP" };
	private String[] cParts = { "ENERGY", "FORGONE", "RELEASE", "SPILL" };

	private TimeSeries[][] series;
	private TimeSeries[][][] ex_series;
	private XYSeries[] dataSeries = new XYSeries[12];
	private XYSeriesCollection[] xydatasets = new XYSeriesCollection[12];
	private ChartPanel[] panels = new ChartPanel[12];

	/**
	 * Reads data in bulk
	 */
	private void readManyTimeSeries() {
		DSSGrabber1SvcImpl dg = (DSSGrabber1SvcImpl) DG_Handle.getInstance().getDG();
		series = new TimeSeries[bParts.length][cParts.length];
		ex_series = new TimeSeries[bParts.length][cParts.length][14];
		HecTime ht = new HecTime();
		for (int i = 0; i < bParts.length; i++) {
			for (int j = 0; j < cParts.length; j++) {

				dg.setBase(DG_Handle.getInstance().getBaseName());
				String seriesName = "/HYDROPOWER/" + bParts[i] + "/" + cParts[j]
						+ "/01JAN1930/1MON/POWERPLANT-GENERATION/";
				dg.setLocation("*" + seriesName);
				dg.setDateRange("FEB1924-feb2003");
				dg.setPrimaryDSSName(bParts[i] + "/" + cParts[j] + "/POWERPLANT-GENERATION");

				dg.checkReadiness();

				TimeSeriesContainer[] tscs = dg.getPrimarySeries(seriesName);
				series[i][j] = new TimeSeries(bParts[i] + "/" + cParts[j]);

				for (int k = 0; k < tscs[0].numberValues; k++) {
					ht.set(tscs[0].times[k]);
					series[i][j].addOrUpdate(new Month(ht.month(), ht.year()), tscs[0].values[k]);
				}

				TimeSeriesContainer[][] ex_tscs = dg.getExceedanceSeries(tscs);
				for (int l = 0; l < 14; l++) {
					ex_series[i][j][l] = new TimeSeries(bParts[i] + "/" + cParts[j] + " " + Integer.toString(l));
					for (int k = 0; k < ex_tscs[l][0].numberValues; k++) {
						ht.set(tscs[0].times[k]);
						ex_series[i][j][l].addOrUpdate(new Month(ht.month(), ht.year()), ex_tscs[l][0].values[k]);

					}
				}
			}
		}
	}

	public TimeSeries[][] getSeries() {
		return series;
	}

	private int getMonth(String month) {
		int i = "janfebmaraprmayjunjulaugsepoctnovdec".indexOf(month.toLowerCase()) / 3;
		return i;
	}

	private int getCPart(String cpart) {
		for (int i = 0; i < cParts.length; i++) {
			if (cpart.equals(cParts[i]))
				return i;
		}
		return -1;
	}

	private int getBPart(String bpart) {
		for (int i = 0; i < bParts.length; i++) {
			if (bpart.equals(bParts[i]))
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

		readManyTimeSeries();
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
		for (int i = 0; i < bParts.length; i++) {

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
			panels[i].getChart().setTitle(bParts[i]);
			this.add(panels[i]);
		}
		for (int i = 0; i < bParts.length; i++) {
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