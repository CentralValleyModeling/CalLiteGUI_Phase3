package gov.ca.water.calgui.bo;

//! Utilities for display of results
import java.awt.Component;
import java.awt.GridBagConstraints;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.PrintStream;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Vector;

import javax.swing.JFileChooser;
import javax.swing.JList;
import javax.swing.JMenuBar;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JSpinner;
import javax.swing.JTabbedPane;
import javax.swing.SpinnerListModel;
import javax.swing.SpinnerModel;
import javax.swing.SpinnerNumberModel;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;

import org.apache.log4j.Logger;
import org.swixml.SwingEngine;

import calsim.app.AppUtils;
import calsim.app.DerivedTimeSeries;
import calsim.app.MultipleTimeSeries;
import calsim.app.Project;
import calsim.gui.GuiUtils;
import gov.ca.water.calgui.constant.Constant;
import gov.ca.water.calgui.presentation.ControlFrame;
import gov.ca.water.calgui.tech_service.IDialogSvc;
import gov.ca.water.calgui.tech_service.impl.DialogSvcImpl;

/**
 * Supporting utilities for display of results
 * 
 * @author tslawecki
 *
 */
public class ResultUtilsBO implements ChangeListener {
	private static final Logger LOG = Logger.getLogger(ResultUtilsBO.class.getName());
	private IDialogSvc dialogSvc = DialogSvcImpl.getDialogSvcInstance();

	private static ResultUtilsBO resultUtilsBO;
	private HashMap<String, Integer> monthMap;
	private SwingEngine swingEngine;
	private Project project;
	private ControlFrame _controlFrame = null;
	// private Cursor hourglassCursor = new Cursor(Cursor.WAIT_CURSOR);
	// private Cursor normalCursor = new Cursor(Cursor.DEFAULT_CURSOR);
	private FileDialogBO fdDSSFiles;

	/**
	 * This method is for implementing the singleton.
	 *
	 * @return
	 */
	public static ResultUtilsBO getResultUtilsInstance(SwingEngine swingEngine) {
		if (resultUtilsBO == null) {
			resultUtilsBO = new ResultUtilsBO(swingEngine);
		}
		return resultUtilsBO;
	}

	/**
	 * Constructor stores SwiXml instance, builds month-to-integer map, and sets
	 * up a WRIMS GUI Project object for use in Custom Results
	 * 
	 * @param swingEngine
	 */
	private ResultUtilsBO(SwingEngine swingEngine) {
		this.swingEngine = swingEngine;

		// Build map for mmm -> m mapping

		monthMap = new HashMap<String, Integer>();
		monthMap.put("jan", 1);
		monthMap.put("feb", 2);
		monthMap.put("mar", 3);
		monthMap.put("apr", 4);
		monthMap.put("may", 5);
		monthMap.put("jun", 6);
		monthMap.put("jul", 7);
		monthMap.put("aug", 8);
		monthMap.put("sep", 9);
		monthMap.put("oct", 10);
		monthMap.put("nov", 11);
		monthMap.put("dec", 12);

		// Create a WRIMS GUI project for WRIMS GUI to work off of

		project = new Project();
		AppUtils.setCurrentProject(project);
		AppUtils.baseOn = false;
	}

	/**
	 * Reads QuickResults output list, Custom Results Dts Tree
	 */
	public void readCGR() {
		String aLine;
		Vector<String> data = new Vector<String>();
		JFileChooser fc = new JFileChooser();
		fc.setFileFilter(new SimpleFileFilter("cgr", "CalLite GUI Report File (*.cgr)"));
		fc.setCurrentDirectory(new File(".//Config"));
		File file = null;
		String filename = null;
		int retval = fc.showOpenDialog(swingEngine.find(Constant.MAIN_FRAME_NAME));
		if (retval == JFileChooser.APPROVE_OPTION) {
			// ... The user selected a file, get it, use it.
			file = fc.getSelectedFile();
			filename = file.toString();
			try {
				FileInputStream fin = new FileInputStream(filename);
				BufferedReader br = new BufferedReader(new InputStreamReader(fin));
				aLine = br.readLine();
				while ((aLine != null) && !aLine.startsWith("===== Dts Tree =====")) {
					data.add(aLine);
					aLine = br.readLine();
				}
				if (aLine != null) {
					GuiUtils.getCLGPanel().getDtsTreePanel().getCurrentModel().readData(filename + ".tree.xml", "");
					Vector<MultipleTimeSeries> mts = GuiUtils.getCLGPanel().getDtsTreePanel().getCurrentModel()
							.getPrjMts();
					Vector<DerivedTimeSeries> dts = GuiUtils.getCLGPanel().getDtsTreePanel().getCurrentModel()
							.getPrjDts();
					Project p = getProject();
					p.clearMTSList();
					for (int i = 0; i < mts.size(); i++)
						p.add(mts.get(i));
					p.clearDTSList();
					for (int i = 0; i < dts.size(); i++)
						p.add(dts.get(i));
				}
				br.close();
			} catch (Exception e1) {
				LOG.debug(e1.getMessage());
			}
			JList lstReports = (JList) (getSwix()).find("lstReports");
			lstReports.setListData(data);
		}
	}

	/**
	 * Writes Quick Results display list, Custom Result DTS tree
	 */
	public void writeCGR() {
		JFileChooser fc = new JFileChooser();
		fc.setFileFilter(new SimpleFileFilter("cgr", "CalLite Report File (*.cgr)"));
		fc.setCurrentDirectory(new File(".//Config"));
		File file = null;
		String filename = null;
		int retval = fc.showSaveDialog(swingEngine.find(Constant.MAIN_FRAME_NAME));
		if (retval == JFileChooser.APPROVE_OPTION) {
			// ... The user selected a file, get it, use it.
			file = fc.getSelectedFile();
			filename = file.toString();
			if (!filename.toUpperCase().endsWith(".CGR") && !filename.endsWith("."))
				filename = filename + ".cgr";
			boolean saveFlag = true;
			if (new File(filename).exists()) {
				// saveFlag =
				// (JOptionPane.showConfirmDialog(swingEngine.find(Constant.MAIN_FRAME_NAME),
				// "The display list file '" + filename + "' already exists.
				// Press OK to overwrite.",
				// "CalLite GUI", JOptionPane.OK_CANCEL_OPTION) ==
				// JOptionPane.OK_OPTION);

				// ImageIcon icon = new
				// ImageIcon(getClass().getResource("/images/CalLiteIcon.png"));
				// Object[] options = { "OK", "Cancel" };
				// JOptionPane optionPane = new JOptionPane("The display list
				// file '" + filename + "' already exists. Press OK to
				// overwrite.",
				// JOptionPane.QUESTION_MESSAGE, JOptionPane.OK_CANCEL_OPTION,
				// null, options, options[0]);
				// JDialog dialog =
				// optionPane.createDialog(swingEngine.find(Constant.MAIN_FRAME_NAME),"CalLite");
				// dialog.setIconImage(icon.getImage());
				// dialog.setResizable(false);
				// dialog.setVisible(true);
				// switch (optionPane.getValue().toString()) {
				// case "Cancel":
				// saveFlag = false;
				// break;
				// case "OK":
				// saveFlag = true;
				// break;
				// default:
				// saveFlag = false;
				// break;
				// }
				saveFlag = (dialogSvc
						.getOKCancel("The display list file '" + filename + "' already exists. Press OK to overwrite.",
								JOptionPane.QUESTION_MESSAGE)
						.equals("OK"));
			}
			if (saveFlag) {
				OutputStream outputStream;
				try {
					outputStream = new FileOutputStream(filename);
				} catch (FileNotFoundException e2) {
					LOG.debug(e2.getMessage());
					return;
				}
				// Store previous list items
				JList lstReports = (JList) (swingEngine).find("lstReports");
				int size = lstReports.getModel().getSize(); // 4
				int n;
				n = 0;
				String[] lstArray = new String[size];
				for (int i = 0; i < size; i++) {
					Object item = lstReports.getModel().getElementAt(i);
					if (item.toString() != " ") {
						lstArray[n] = item.toString();
						n = n + 1;
					}
				}
				// Store contents of Project
				List<String> pList = new ArrayList<String>();
				pList.add("===== Dts Tree =====");
				Project p = getProject();
				pList.add(String.valueOf(p.getNumberOfMTS()));
				for (int i = 0; i < p.getNumberOfMTS(); i++) {
					MultipleTimeSeries mts = p.getMTSList()[i];
					pList.add(mts.getName());
					pList.add(String.valueOf(mts.getNumberOfDataReferences()));
					for (int j = 0; j < mts.getNumberOfDataReferences(); j++) {
						pList.add(mts.getBPartAt(j) + ";" + mts.getCPartAt(j) + ";" + mts.getVarTypeAt(j) + ";"
								+ mts.getDTSNameAt(i));
					}
				}
				pList.add(String.valueOf(p.getNumberOfDTS()));
				for (int i = 0; i < p.getNumberOfDTS(); i++) {
					DerivedTimeSeries dts = p.getDTSList()[i];
					pList.add(dts.getName());
					pList.add(String.valueOf(dts.getNumberOfDataReferences()));
					for (int j = 0; j < dts.getNumberOfDataReferences(); j++) {
						pList.add(dts.getBPartAt(j) + ";" + dts.getCPartAt(j) + ";" + dts.getVarTypeAt(j) + ";"
								+ String.valueOf(dts.getOperationIdAt(j)) + ";" + dts.getDTSNameAt(j));
					}
				}
				try {
					PrintStream output = new PrintStream(outputStream);
					for (int i = 0; i < n; i++) {
						output.println(lstArray[i]);
					}
					for (int i = 0; i < pList.size(); i++) {
						output.println(pList.get(i));
					}
					output.close();
					outputStream.close();
					GuiUtils.getCLGPanel().getDtsTreePanel().getCurrentModel().saveFile(filename + ".tree.xml");
				} catch (IOException ex) {
					LOG.debug(ex.getMessage());
				}
			}
		}
	}

	/**
	 * Creates a singleton ControlFrame to receive undocked Quick Results
	 * controls for use with Map View and Custom Results dashboards
	 * 
	 * @return
	 */
	public ControlFrame getControlFrame() {

		if (_controlFrame == null)
			_controlFrame = new ControlFrame();
		return _controlFrame;
	}

	/**
	 * Disposes of ControlFrame
	 */
	public void closeControlFrame() {
		if (_controlFrame != null) {
			_controlFrame.dispose();
			_controlFrame = null;
		}
		return;
	}

	/**
	 * Getter for access to application-wide SwiXml engine
	 *
	 * @return swix
	 */
	public SwingEngine getSwix() {
		return swingEngine;
	}

	/**
	 * Getter access to WRIMS GUI project for Custom Results
	 * 
	 * @return
	 */
	public Project getProject() {
		return project;
	}

	/**
	 * Convert three-letter month abbreviation to integer 1-12
	 */
	public int monthToInt(String month) {
		month = month.toLowerCase();
		Integer monthCode = null;
		try {
			monthCode = monthMap.get(month);
		} catch (Exception e) {
			LOG.debug(e.getMessage());
		}
		if (monthCode == null) {
			LOG.debug("Invalid Key at UnitsUtils.monthToInt");
			return -1;
		}
		return monthCode.intValue();
	}

	/**
	 * Sets up a spinner for a numeric range
	 *
	 * @param jspn
	 *            - Swing spinner component
	 * @param val
	 *            - Initial value
	 * @param min
	 *            - Minimum value
	 * @param max
	 *            - Maximum value
	 * @param step
	 *            - Increment between values
	 * @param format
	 *            - Format for display
	 * @param obj
	 *            - ChangeListener
	 * @param changelistener
	 *            - True is a ChangeListener is to be assigned
	 */
	public static void SetNumberModelAndIndex(JSpinner jspn, int val, int min, int max, int step, String format,
			Object obj, boolean changelistener) {

		SpinnerModel spnmod = new SpinnerNumberModel(val, min, max, step);
		jspn.setModel(spnmod);
		jspn.setEditor(new JSpinner.NumberEditor(jspn, format));
		if (changelistener == true) {
			jspn.addChangeListener((ChangeListener) obj);
		}
	}

	/**
	 * Sets up a spinner for months Jan - Dec
	 * 
	 * @param jspn
	 *            - Swing spinner component
	 * @param idx
	 * @param obj
	 *            - ChangeListener
	 * @param changelistener
	 *            - True is a ChangeListener is to be assigned
	 *
	 */
	public static void SetMonthModelAndIndex(JSpinner jspn, int idx, Object obj, boolean changelistener) {
		String[] monthNames = { "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec" };

		try {
			SpinnerListModel monthModel = new SpinnerListModel(monthNames);
			jspn.setModel(monthModel);
			jspn.setValue(monthNames[idx]);
			if (changelistener == true) {
				jspn.addChangeListener((ChangeListener) obj);
			}
		}

		catch (Exception e) {
			LOG.debug("Problem reading table files. " + e);
		}
	}

	@Override
	/**
	 * Custom ChangeListener constrains time spinners to WY 1922 - WY 2003
	 */
	public void stateChanged(ChangeEvent changeEvent) {
		Component c = (Component) changeEvent.getSource();
		String lcName = c.getName().toLowerCase();
		if (lcName.substring(0, 3).equals("spn")) {
			// Constrain run times to [10/1921,9/2003]
			int syr = (Integer) ((JSpinner) swingEngine.find("spnRunStartYear")).getValue();
			int eyr = (Integer) ((JSpinner) swingEngine.find("spnRunEndYear")).getValue();
			int smo = monthToInt(((String) ((JSpinner) swingEngine.find("spnRunStartMonth")).getValue()).trim());
			int emo = monthToInt(((String) ((JSpinner) swingEngine.find("spnRunEndMonth")).getValue()).trim());
			if ((syr == 1921) && (smo < 10))
				((JSpinner) swingEngine.find("spnRunStartMonth")).setValue("Oct");
			if ((eyr == 2003) && (emo > 9))
				((JSpinner) swingEngine.find("spnRunEndMonth")).setValue("Sep");
			// Constrain display times the same way [inefficient?]
			syr = (Integer) ((JSpinner) swingEngine.find("spnStartYear")).getValue();
			eyr = (Integer) ((JSpinner) swingEngine.find("spnEndYear")).getValue();
			smo = monthToInt(((String) ((JSpinner) swingEngine.find("spnStartMonth")).getValue()).trim());
			emo = monthToInt(((String) ((JSpinner) swingEngine.find("spnEndMonth")).getValue()).trim());
			if ((syr == 1921) && (smo < 10))
				((JSpinner) swingEngine.find("spnStartMonth")).setValue("Oct");
			if ((eyr == 2003) && (emo > 9))
				((JSpinner) swingEngine.find("spnEndMonth")).setValue("Sep");
		} else if (lcName.equals("tabbedpane1")) {
			JMenuBar menuBar = (JMenuBar) this.swingEngine.find("menu");
			menuBar.setSize(150, 20);
			if (((JTabbedPane) c).getSelectedIndex() == 6) { // Quick Results
				ControlFrame cf = getControlFrame();
				if (cf != null) {

					JPanel p = (JPanel) swingEngine.find("controls");
					GridBagConstraints gbc = new GridBagConstraints();

					gbc.gridx = 0;
					gbc.gridy = 0;
					gbc.gridheight = 1;
					gbc.anchor = GridBagConstraints.NORTHWEST;
					p.add(swingEngine.find("ss"), gbc);

					gbc.gridy = 1;
					p.add(swingEngine.find("Display"), gbc);

					((JPanel) swingEngine.find("Reporting")).invalidate();

					closeControlFrame();

				}
			}
		}
	}

	/**
	 * Return the custom file dialog containing the scenario list
	 * 
	 * @return
	 */
	public FileDialogBO getFdDSSFiles() {
		return fdDSSFiles;
	}

	/**
	 * Store the custom file dialog containing the Quick Results scenario list
	 * 
	 * @param fdDSSFiles
	 */
	public void setFdDSSFiles(FileDialogBO fdDSSFiles) {
		this.fdDSSFiles = fdDSSFiles;
	}
}
