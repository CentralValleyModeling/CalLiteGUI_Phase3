package gov.ca.water.calgui.pm;

import javax.swing.JList;

import gov.ca.water.calgui.bo.RBListItemBO;
import gov.ca.water.calgui.bus_service.IDSSGrabber1Svc;
import gov.ca.water.calgui.bus_service.impl.DSSGrabber1SvcImpl;

public class DG_Handle {

	private static DG_Handle instance;
	private static IDSSGrabber1Svc dg;
	private static RBListItemBO[] scens = {
			new RBListItemBO("Scenarios//CL_DCR2015_2020D09E_Corrob_DV_20150901_LtGen.dss", "Power") };

	private DG_Handle() {
	};

	public static DG_Handle getInstance() {
		if (instance == null) {
			instance = new DG_Handle();

			JList<RBListItemBO> list = new JList<RBListItemBO>(scens);
			dg = new DSSGrabber1SvcImpl(list);
		}
		return instance;
	}

	public IDSSGrabber1Svc getDG() {
		return dg;
	}

	public String getBaseName() {
		return scens[0].toString();
	}
}
