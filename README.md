Prokject structure:
- requirements.txt
	contains requirements for source code to run succesfully
	navigate to folder in shell (e.g. windows cmd promt) and run "pip install -r requirements.txt" to install
- src/
	binning.py
		binning and plotting of binned data
	main.py
		run this file.
		params are listed and described at the top
	plot_settings.py
		changes global plotting options
	rock_abundance.py
		plot RA for given window - file path adjustment requiered
	save_and_load.py
		helper for runtime purposes
	subsetting.py
		corrections and sample reduction helpers
- CE-2 MRM Data/
	biggerMean=False/
		contains fully evaluated data for whole planet with biggerMean=False
	biggerMean=True/
		contains fully evaluated data for whole planet with biggerMean=True 
		CE2_data.mat
			original Chang'e 2 CELMS data
		CE2_data.xlsx
			description for CE2_data.mat data product