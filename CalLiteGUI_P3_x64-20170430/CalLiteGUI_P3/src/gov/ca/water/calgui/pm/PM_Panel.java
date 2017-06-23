package gov.ca.water.calgui.pm;

import java.awt.BorderLayout;
import java.awt.Dimension;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.Box;
import javax.swing.ButtonGroup;
import javax.swing.JCheckBox;
import javax.swing.JComboBox;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JRadioButton;
import javax.swing.JSpinner;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;

import gov.ca.water.calgui.bo.ResultUtilsBO;

public class PM_Panel extends JPanel implements ActionListener, ChangeListener {

	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;

	private JRadioButton rb1 = new JRadioButton("By Month");
	private JSpinner sp;
	private JRadioButton rb2 = new JRadioButton("By Station");
	private JComboBox<String> sList;
	private JComboBox<String> cList;
	private ChartPanel2 cp;
	private JCheckBox cb1 = new JCheckBox("Exceedance");

	public PM_Panel() {

		super();

		this.setName("CVP");
		this.setLayout(new BorderLayout());

		Box h = Box.createHorizontalBox();
		ButtonGroup bg = new ButtonGroup();

		// By year radiobutton and spinner

		rb1.setSelected(false);
		bg.add(rb1);
		rb1.addActionListener(this);
		h.add(rb1);

		sp = new JSpinner();
		sp.setEnabled(false);
		ResultUtilsBO.SetMonthModelAndIndex(sp, 9, null, false);
		sp.addChangeListener(this);
		h.add(sp);
		h.add(Box.createRigidArea(new Dimension(20, 20)));

		// By station radiobutton and combo box

		rb2.setSelected(true);
		bg.add(rb2);
		rb2.addActionListener(this);
		h.add(rb2);

		String[] bParts = { "CARRPP", "CVPSANLUISPP", "FOLSOMPP", "KESWICKPP", "NIMBUSPP", "ONEILPP", "SHASTAPP",
				"SPRINGCREEKPP", "TRINITYPP" };

		sList = new JComboBox<String>(bParts);
		sList.setSelectedIndex(0);
		sList.setEnabled(true);
		sList.addActionListener(this);
		h.add(sList);
		h.add(Box.createRigidArea(new Dimension(20, 20)));

		// C-PART selection

		h.add(new JLabel("  C-PART: "));

		String[] cParts = { "ENERGY", "FORGONE", "RELEASE", "SPILL" };

		cList = new JComboBox<String>(cParts);
		cList.setSelectedIndex(0);
		cList.setEnabled(true);
		cList.addActionListener(this);
		h.add(cList);
		h.add(Box.createRigidArea(new Dimension(20, 20)));

		h.add(cb1);

		// Build panel

		this.add(h, BorderLayout.NORTH);
		cp = new ChartPanel2();
		this.add(cp, BorderLayout.CENTER);
		updateCharts();

	}

	public void actionPerformed(ActionEvent e) {
		if (e.getSource() instanceof JRadioButton) {
			JRadioButton rb = (JRadioButton) e.getSource();

			if (rb.isSelected()) {
				sp.setEnabled(rb.getText().equals("By Month"));
				sList.setEnabled(!sp.isEnabled());
				updateCharts();
			}
		} else if ((e.getSource() instanceof JComboBox) || (e.getSource() instanceof JSpinner)) {

			updateCharts();
		}

	}

	private void updateCharts() {
		if (sp.isEnabled())
			cp.resetCharts("", (String) cList.getSelectedItem(), (String) sp.getValue(), false);
		else
			cp.resetCharts((String) sList.getSelectedItem(), (String) cList.getSelectedItem(), "", false);

		invalidate();
		repaint();

	}

	public ChartPanel2 getCP() {
		return cp;
	}

	@Override
	public void stateChanged(ChangeEvent e) {
		if (e.getSource() instanceof JSpinner)
			updateCharts();

	}
}
