package gov.ca.water.calgui.pm;

import java.awt.BorderLayout;
import java.awt.Component;

import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTabbedPane;

public class PM_Demo {

	public static void main(String[] args) {

		JFrame f = new JFrame("PM_Demo");
		f.setLayout(new BorderLayout());

		JTabbedPane tp = new JTabbedPane();

		// First panel

		PM_Panel p1 = new PM_Panel();

		// Second panel

		JPanel p2 = new BarChartPanel(p1.getCP());

		JScrollPane scrollPane = new JScrollPane((Component) p1, JScrollPane.VERTICAL_SCROLLBAR_AS_NEEDED,
				JScrollPane.HORIZONTAL_SCROLLBAR_AS_NEEDED);

		tp.add("Multiple Bar Charts", scrollPane);
		tp.add("Stacked Bar Chart", p2);

		f.add(tp);
		f.pack();
		f.setVisible(true);

	}

}
