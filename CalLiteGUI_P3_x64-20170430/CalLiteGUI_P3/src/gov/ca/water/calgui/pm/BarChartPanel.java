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

public class BarChartPanel extends JPanel {
	private JFreeChart chart;
	private String[] bParts = { "CARRPP", "CVPSANLUISPP", "FOLSOMPP", "KESWICKPP", "NIMBUSPP", "ONEILPP", "SHASTAPP",
			"SPRINGCREEKPP", "TRINITYPP" };
	private String[] cParts = { "ENERGY", "FORGONE", "RELEASE", "SPILL" };

	public BarChartPanel(ChartPanel2 cp2) {

		DefaultCategoryDataset dataset = new DefaultCategoryDataset();

		TimeSeries[][] series = cp2.getSeries(); // TODO: Remove kludge by
													// moving data access out of
													// cp2
		// dimensions are bparts x cparts
		// For demo purposes, we will pick a year and show energy;
		// We assume first month is september ...

		int year = 2000;
		int offset = (year - 1922) * 12;
		int cPartI = 0;

		for (int bPartI = 0; bPartI < bParts.length; bPartI++)
			for (int m = 0; m < 12; m++)
				dataset.addValue(series[bPartI][cPartI].getValue(m + offset), bParts[bPartI],
						"OctNovDecJanFebMarAprMayJunJulAugSep".substring(m * 3, m * 3 + 3));

		chart = ChartFactory.createStackedBarChart(year + " " + cParts[cPartI], "Month", cParts[cPartI], dataset, true);

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
