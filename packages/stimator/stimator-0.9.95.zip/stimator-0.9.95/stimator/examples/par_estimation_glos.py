
from stimator import read_model, readTCs
from stimator.deode import DeODEOptimizer

mdl = """
title Glyoxalase system in L. Infantum

glx1 : HTA -> SDLTSH, V1*HTA/(Km1 + HTA)
glx2 : SDLTSH ->,     V2*SDLTSH/(Km2 + SDLTSH)

find V1  in [0.00001, 0.0001]
find Km1 in [0.01, 1]
find V2  in [0.00001, 0.0001]
find Km2 in [0.01, 1]
init : (SDLTSH = 7.69231E-05, HTA = 0.1357)
"""
m1 = read_model(mdl)

print '================================================='
print 'Parameter estimation: glyoxalase system example'
print mdl
print '-------- an example with two time courses --------------'

optSettings={'genomesize':80, 'generations':200}
timecourses = readTCs(['TSH2a.txt', 'TSH2b.txt'], names = ['SDLTSH', 'HTA'], verbose=True)

## optimizer = DeODEOptimizer(m1,optSettings, timecourses, dump_generations=True,
##                            maxGenerations_noimprovement = 50)
optimizer = DeODEOptimizer(m1, optSettings, timecourses)
optimizer.run()

print optimizer.optimum.info()
optimizer.optimum.plot()
## #save predicted timecourses to files
## redsols = solver.optimum.optimum_tcs
## redsols.saveTimeCoursesTo(['TSH2a_pred.txt', 'TSH2b_pred.txt'], verbose=True)


print '-------- an example with unknown initial values --------------'

m2 = m1.copy()

# Now, assume init.HTA is uncertain
m2.init.HTA.set_bounds((0.05,0.25))
# do not estimate Km1 and Km2 to help the analysis
m2.parameters.Km1.reset_bounds()
m2.parameters.Km2.reset_bounds()
m2.parameters.Km1 = 0.252531
m2.parameters.Km2 = 0.0980973

optSettings={'genomesize':60, 'generations':200}

## VERY IMPORTANT:
## only one time course can be used: 
## cannot fit one uncertain initial value to several timecourses!!!
timecourses = readTCs(['TSH2a.txt'], '.', names = ['SDLTSH', 'HTA'], verbose=True)

optimizer = DeODEOptimizer(m2,optSettings, timecourses)
optimizer.run()

optimizer.optimum.print_info()
optimizer.optimum.plot(show=True)
