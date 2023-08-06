# inverse2.py This file contains classes to solve inverse optimization problems 
# it only utilizes pulp, no dippy
# -----------------------------------------------------------------------------

'''
InvCollection:
    attributes:
        prob:        Original problem
                     type: LpProblem
        iter:        Iteration number
                     type: int
        x0:          point given
                     type: dict
        var:         dictionary of the variables of prob
                     type: dictionary
        dim:         dimension of the problem
                     type: int
        c:           objective function coefficients of the prob
                     type: dict
        invProb:     inverse of the prob
                     type: LpProblem
        currentXtremePoint:
                     current extreme point generated
                     type: dict
        dCurrent:    InvProblem variable d in current iteration
                     type: dict
        dPrevious:   InvProblem variable d in previous iteration
                     type: dict
    methods:
        __init__(self,prob,x0):
                     creates invProb, and sets some attributes, prob and x0
                     are as described above
        generate_inverse():
                     generates invProb from prob and point x0
        generate_xtreme_point():
                     generates extreme point for the current setting
        add_inequality():
                     creates inequality from current extreme point and adds
                     it the to InvProb
        solve():     uses other methods iteratively to solve the InvProb
'''

__version__    = '1.0.0'
__author__     = 'Aykut Bulut'
__license__    = None
__maintainer__ = 'Aykut Bulut'
__email__      = 'ayb211@lehigh.edu'
__url__     = None

import importlib as ilib
from copy import deepcopy
from pulp import LpProblem, LpVariable, LpMinimize, LpInteger
from pulp import LpContinuous, lpSum, LpConstraintVar, LpStatus
from src.grumpy.polyhedron2D import Polyhedron2D, Figure
import sys
sys.path.append('../instances')

EPS = 1e-6
class GenericSeparation(object):

    def __init__(self, origProb, x0):
        self.prob = origProb
        self.iter = 1
        self.x0 = x0
        self.var = origProb.variablesDict()
        self.dim = len(self.var)
        self.currentXtremePoint = {}
        self.solver = None
        self.c = dict(list((v.name,c) for v,c in origProb.objective.iteritems()))
        for v in self.var:
            if v in self.c:
                continue
            else:
                self.c[v] = 0.0
        self.generate_separation_problem()
        self.piCurrent = dict([(v.name, 0) for v in self.var.values()]) 
        self.piPrevious = dict([(v.name, 0) for v in self.var.values()]) 
        self.extremePoints = []
        self.f = Figure()
        
    def generate_separation_problem(self):
        self.sepProb = LpProblem (name='separation '+self.prob.name, sense=LpMinimize)
        self.pi = dict(list((v,LpVariable('pi'+v, None, None, LpContinuous,
                                         None))
                                         for v in self.var)) 
        self.sepProb += lpSum(self.pi[v]*self.x0[v] for v in self.var)

    def generate_xtreme_point(self):
        obj = LpConstraintVar()
        for v in self.prob.variables():
            obj.addVariable(v, self.piCurrent[v.name])
        self.prob.setObjective(obj)
        self.prob.solve()
        #solvers.COIN_CMD.solve(self.prob)
        for v in self.var:
            self.currentXtremePoint[v] = self.var[v].value()
        if self.output == 1:
            currentXtremePointList = self.currentXtremePoint.items()
            currentXtremePointList.sort()
            for v in currentXtremePointList:
                print v[0]+'\t', v[1]
        self.extremePoints.append(self.currentXtremePoint.values())
        return self.prob.objective.value()

    def add_inequality(self):
        # change this, you should not access sense directly call a method
        self.sepProb += lpSum (self.currentXtremePoint[v]*self.pi[v] for v in self.var) >= 1

    def separate(self, output = False, p = None):
        self.output = output
        while True:
            print 'Iteration ', self.iter
            if self.generate_xtreme_point() >= 1-EPS:
                break
            self.add_inequality()
            if self.output:
                print "Separation problem solution status:", LpStatus[self.sepProb.solve()]
                for v in self.sepProb.variables():
                    print v.name+'\t\t', v.value()
            self.piPrevious = deepcopy(self.piCurrent)
            for v in self.var:
                self.piCurrent[v] = self.pi[v].value()
            self.iter += 1
            if p is not None:
                self.f.initialize()
                self.f.add_polyhedron(p, label = 'Polyhedron P')
                xList = (self.x0.values()[0], self.x0.values()[1])
                if len(self.extremePoints) > 2:
                    pp = Polyhedron2D(points = self.extremePoints)
                    self.f.add_polyhedron(pp, color = 'red', linestyle = 'dashed',
                                          label = 'Convex Hull of Generated Points')
                elif len(self.extremePoints) == 1:
                    self.f.add_point(self.extremePoints[0], radius = 0.05, 
                                     color = 'green')
                    self.f.add_text(self.extremePoints[0][0]-0.5, 
                                    self.extremePoints[0][1]-0.08, '$x^0$')
                else:
                    self.f.add_line_segment(self.extremePoints[0], 
                                            self.extremePoints[1], 
                                            color = 'red',
                                            linestyle = 'dashed',
                                            label = 'Convex Hull of Generated Points')
                self.f.set_xlim(p.plot_min[0], p.plot_max[0])
                self.f.set_ylim(p.plot_min[1], p.plot_max[1])
                self.f.add_point(xList, radius = 0.05, color = 'red')
                self.f.add_text(xList[0]-0.5, xList[1]-0.08, '$x^*$')
                dList = (self.piCurrent.values()[0], self.piCurrent.values()[1])
                self.f.add_line(dList, 1, 
                                p.plot_max, p.plot_min, color = 'green', 
                                linestyle = 'dashed', label = 'Separating Hyperplane')
                self.f.show()
            if self.output:
                print self.sepProb.objective.value()            

def read_instance(module_name):
    '''
    creates problem defined in the documentation of this file
    ''' 
    mip = ilib.import_module(module_name)
            
    # create LpProblem instance
    prob = LpProblem("MIP", LpMinimize)
    # create variables
    x = []
    for i in range(len(mip.A[0])):
        x.append(LpVariable('x_'+str(i), 0, None, LpInteger))
    # add obj function
    prob +=  lpSum(mip.c[i]*x[i] for i in range(len(mip.A[0])))
    # add constraints to the prob
    for i in range(len(mip.A)):
        prob +=  mip.A[i][0]*x[0] + mip.A[i][1]*x[1] <= mip.b[i]
    return prob, x, mip

if __name__ == '__main__':
    
    display = True
    prob, vars, mip = read_instance('MIP8')

    if display:
        p = Polyhedron2D(A = mip.A, b = mip.b)
        f = Figure()
        f.add_polyhedron(p, show_int_points = True, label = 'Polyhedron P')
        f.set_xlim(p.plot_min[0], p.plot_max[0])
        f.set_ylim(p.plot_min[1], p.plot_max[1])
        f.add_point(mip.x, radius = 0.05, color = 'red')
        f.add_text(mip.x[0]-0.5, mip.x[1]-0.08, '$x^*$')
        f.show()
    # This is the point to be separated 
    x0 = {}
    for index, value in enumerate(mip.x):
        x0[vars[index].name] = value
    i = 0
    ic = GenericSeparation(prob, x0)
    ic.separate(output = True, p = p)
    print 'separation problem objective value', ic.sepProb.objective.value()


