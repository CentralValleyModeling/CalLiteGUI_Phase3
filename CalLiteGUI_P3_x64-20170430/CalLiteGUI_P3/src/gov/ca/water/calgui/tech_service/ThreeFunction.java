package gov.ca.water.calgui.tech_service;

import gov.ca.water.calgui.bo.CalLiteGUIException;

/**
 * This is a functional Interface which takes three parameters and one return
 * type. This interface is used for passing the lambda function
 *
 * @author Mohan
 *
 * @param <A>
 *            1st parameter
 * @param <B>
 *            2nd parameter
 * @param <C>
 *            3ed parameter
 * @param <R>
 *            return type
 */
@FunctionalInterface
public interface ThreeFunction<A, B, C, R> {
	public R apply(A a, B b, C c) throws CalLiteGUIException;
}
