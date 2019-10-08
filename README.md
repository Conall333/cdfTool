# cdf_tool
cdf command line tool


Coomand line tool that generates a sequence of pusedorandom numbers of a given distribution and plots their CDF(Cumulative distribution function)

Requirements to run:
you will need to be using linux
You will need to have python3 installed
you will need to have mathplotlib 3.03 package installed https://matplotlib.org/
you will need to have numpy package installed (this should automatically install with mathplotlib)

After unzipping the file, open a terminal and cd into the path where the file is stored, then input the commands in the same format as below
Example inputs:
python3 cdfTool.py 1500 442324 exp 6
python3 cdfTool.py 1750 32 geo 0.2
python3 cdfTool.py 1000 12312324 gum 1.5 3

This will give 3 outputs to present working directory:
a txt file containing the rng sequence
a txt file containing the lot ranges and counts
a pdf of the plot


Code Explanation:
method: exponential --> implements inverse function of exponential distribution
method: geometric --> implements inverse function of geometric distribution
method: gumbel --> implements inverse function of gumbel distribution
All of these methods use the method: uniformRng --> that takes a seed to return a random number between 0 and 1
The seed is incremented each time before it is passed to uniformRng
method: writeNumberSequence --> saves the generated number sequence to a txt file
method: plotCdf --> takes the number sequence, divides it into bins, and creates a plot
method: writeCdfData --> writes the cdf data to a file showing the bin ranges and counts
method: takeInputs --> takes cmd line inputs, does some validation before passing them to the required functions
