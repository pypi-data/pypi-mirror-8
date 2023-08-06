numVars = 2
numCons = 3

'''
A = [[-2, -3], 
     [-4, -2], 
     [-3, -4],
     ]

b = [-5, 
     -15, 
     -20,
      ]

x_u = [9,
       6,
       ]

'''

# For display, adding bounds explicitly is better
A = [[-2, -3], 
     [-4, -2], 
     [-3, -4], 
     [1, 0], 
     [0, 1], 
     [-1, 0], 
     [0, -1]]

b = [-5, 
     -15, 
     -20, 
     9, 
     6, 
     0, 
     0]

integerIndices = [0, 1]

c = [20,
     15,
     ]

obj_val = 100

sense = ('Min', '<=')

points = None
rays = []

cuts = [[-4.8, -4.4], 
        [-1, -1],
        [-2, -1],
        [-3, -2],
        [-2, -1],
        ]

rhs = [-26, 
       -6, 
       -8,
       -14,
       -10, 
       ]
