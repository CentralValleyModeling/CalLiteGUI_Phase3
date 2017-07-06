package gov.ca.water.calgui.pm;

import org.jfree.data.time.Month;
import org.jfree.data.time.TimeSeries;

import gov.ca.water.calgui.bus_service.impl.DSSGrabber1SvcImpl;
import gov.ca.water.calgui.constant.Constant;
import hec.heclib.util.HecTime;
import hec.io.TimeSeriesContainer;

public class PM_Data {

	private static PM_Data instance;

	private PM_Data() {
	};

	public static PM_Data getInstance() {
		if (instance == null) {
			instance = new PM_Data();
			readManyTimeSeries();
		}
		return instance;
	}

	private static TimeSeries[][] series;
	private static TimeSeries[][][] ex_series;

	/**
	 * Reads data in bulk
	 */
	private static void readManyTimeSeries() {
		DSSGrabber1SvcImpl dg = (DSSGrabber1SvcImpl) DG_Handle.getInstance().getDG();
		series = new TimeSeries[Constant.BPARTS.length][Constant.CPARTS.length];
		ex_series = new TimeSeries[Constant.BPARTS.length][Constant.CPARTS.length][14];
		HecTime ht = new HecTime();
		for (int i = 0; i < Constant.BPARTS.length; i++) {
			for (int j = 0; j < Constant.CPARTS.length; j++) {

				dg.setBase(DG_Handle.getInstance().getBaseName());
				String seriesName = "/HYDROPOWER/" + Constant.BPARTS[i] + "/" + Constant.CPARTS[j]
						+ "/01JAN1930/1MON/POWERPLANT-GENERATION/";
				dg.setLocation("*" + seriesName);
				dg.setDateRange("FEB1924-feb2003");
				dg.setPrimaryDSSName(Constant.BPARTS[i] + "/" + Constant.CPARTS[j] + "/POWERPLANT-GENERATION");

				dg.checkReadiness();

				TimeSeriesContainer[] tscs = dg.getPrimarySeries(seriesName);
				series[i][j] = new TimeSeries(Constant.BPARTS[i] + "/" + Constant.CPARTS[j]);

				for (int k = 0; k < tscs[0].numberValues; k++) {
					ht.set(tscs[0].times[k]);
					series[i][j].addOrUpdate(new Month(ht.month(), ht.year()), tscs[0].values[k]);
				}

				TimeSeriesContainer[][] ex_tscs = dg.getExceedanceSeries(tscs);
				for (int l = 0; l < 14; l++) {
					ex_series[i][j][l] = new TimeSeries(
							Constant.BPARTS[i] + "/" + Constant.CPARTS[j] + " " + Integer.toString(l));
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

	public TimeSeries[][][] getExSeries() {
		return ex_series;
	}

}
