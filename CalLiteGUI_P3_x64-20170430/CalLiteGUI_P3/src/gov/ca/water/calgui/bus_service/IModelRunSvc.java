package gov.ca.water.calgui.bus_service;

import java.util.List;

import org.swixml.SwingEngine;

/**
 * This is the interface for Batch Run.
 * 
 * @author Mohan
 */
public interface IModelRunSvc {
	/**
	 * This method will generate the batch file and run it.
	 *
	 * @param scenarioNamesList
	 *            The list of scenario names to run batch on.
	 * @param swingEngine
	 *            The {@link SwingEngine} Object.
	 * @param isWsidi
	 *            The flag which says whether this run is WSIDI of not.
	 */
	public void doBatch(List<String> scenarioNamesList, SwingEngine swingEngine, boolean isWsidi);
}
