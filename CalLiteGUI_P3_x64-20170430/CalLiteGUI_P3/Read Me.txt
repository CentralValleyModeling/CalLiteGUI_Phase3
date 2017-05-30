1. How to start the CalLiteGUI Application?
	In the project folder, we have a file name “CalLiteGUI” we recommend to use this file to open the application. This file has a "CL" icon on it.

2. Where can I find XML Configuration files?
	They are in the "config" folder. Each tab has its own xml file.

3. Where can I find Dynamic Files and why should we use it?
	They are in the "config" folder. The files are "TriggerForDynamicDisplay" and "TriggerForDynamicSelection".
	
	1. TriggerForDynamicSelection -> In this file we define the values that should be selected or deselected when a option is selected. This only works for the radio buttons and check boxes. For example when you selected A you can select B and deselect C.
		-> A on B on 
		-> A on C off.
	
	2. TriggerForDynamicDisplay -> In this file we define two things 1st one is enabling and disabling of the controls and the 2nd one is showing and hiding the controls.
		-> Enabling and Disabling : When one control is selected, we can enable or disable another control. For example when we select A we can enable B and disable C.
			-> A on B on 
			-> A on C off
		-> Showing and Hiding : When one control is selected, we can show or hide another control on the ui. For example, when we select A we can show B and hide C.
			-> A on B show
			-> A on C hide
