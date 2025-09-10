"""

This is a modified version of plot_3vars_savefig.py, which was originally
written by:

E. Wes Bethel, Copyright (C) 2022

Sept. 2025

Description: This code loads a .csv file and creates a 3-variable plot, with various arguments, saving it to the same filename with .png extension.

Inputs:
    filename        the name of the file we read from
    variable        the name of the variable we are plotting, displayed on the y-axis
    suppress_col_1  set this flag if you want to ignore data in column 1 and plot 2 variables instead of 3

Outputs: displays a chart with matplotlib

Dependencies: matplotlib, pandas modules, argparse

"""

import pandas as pd
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser(prog='summarize.py')
parser.add_argument('filename')
parser.add_argument('-v', '--variable', default='Runtime')
parser.add_argument('-o', '--suppress_col_1', action='store_true')
args = parser.parse_args()

fname = args.filename
plot_fname = fname.split('.')[0] + '.png'

df = pd.read_csv(fname, comment="#")
print(df)

var_names = list(df.columns)

print("var names =", var_names)

# split the df into individual vars
# assumption: column order - 0=problem size, 1=blas time, 2=basic time

problem_sizes = df[var_names[0]].values.tolist()
code1_time = df[var_names[1]].values.tolist()
code2_time = df[var_names[2]].values.tolist()
code3_time = df[var_names[3]].values.tolist()

plt.figure()

if args.suppress_col_1:
    plt.title("Comparison of 2 Codes")
else:
    plt.title("Comparison of 3 Codes")

xlocs = [i for i in range(len(problem_sizes))]

plt.xticks(xlocs, problem_sizes)

if not args.suppress_col_1:
    plt.plot(code1_time, "r-o")
plt.plot(code2_time, "b-x")
plt.plot(code3_time, "g-^")

#plt.xscale("log")
#plt.yscale("log")

plt.xlabel("Problem Sizes")
plt.ylabel(args.variable)

if not args.suppress_col_1:
    varNames = [var_names[1], var_names[2], var_names[3]]
else:
    varNames = [var_names[2], var_names[3]]
plt.legend(varNames, loc="best")

plt.grid(axis='both')

# save the figure before trying to show the plot
plt.savefig(plot_fname, dpi=300)


plt.show()

# EOF
