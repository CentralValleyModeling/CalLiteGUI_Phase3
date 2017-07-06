package gov.ca.water.calgui.pm;

import java.awt.BorderLayout;
import java.awt.Dimension;

import javax.swing.JPanel;

import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartPanel;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.renderer.category.BarRenderer;
import org.jfree.data.category.DefaultCategoryDataset;
import org.jfree.data.time.TimeSeries;

import gov.ca.water.calgui.constant.Constant;

public class BarChartPanel extends JPanel {
	/**
	 * 
	 */
	private static final long serialVersionUID = -1820330233114070810L;
	private JFreeChart chart;

	public BarChartPanel() {

		DefaultCategoryDataset dataset = new DefaultCategoryDataset();

		TimeSeries[][] series = PM_Data.getInstance().getSeries();

		// dimensions are bparts x cparts
		// For demo purposes, we will pick a year and show energy;
		// We assume first month is september ...

		int year = 2000;
		int offset = (year - 1922) * 12;
		int cPartI = 0;

		for (int bPartI = 0; bPartI < Constant.BPARTS.length; bPartI++)
			for (int m = 0; m < 12; m++)
				dataset.addValue(series[bPartI][cPartI].getValue(m + offset), Constant.BPARTS[bPartI],
						"OctNovDecJanFebMarAprMayJunJulAugSep".substring(m * 3, m * 3 + 3));

		chart = ChartFactory.createStackedBarChart(year + " " + Constant.CPARTS[cPartI], "Month",
				Constant.CPARTS[cPartI], dataset, true);

		BarRenderer renderer = (BarRenderer) chart.getCategoryPlot().getRenderer();
		renderer.setItemMargin(-2);

		ChartPanel panel = new ChartPanel(chart);
		panel.setMaximumDrawHeight(1200);
		panel.setMaximumDrawWidth(1920);
		panel.setMinimumDrawHeight(200);
		panel.setMinimumDrawWidth(300);
		panel.setPreferredSize(new Dimension(300, 200));

		this.setName("SWP");
		this.setLayout(new BorderLayout());
		this.add(panel);

	}

}
