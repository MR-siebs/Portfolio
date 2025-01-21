#MIT License

#Copyright (c) 2025 Siebren Groenendijk

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

import math
import numpy as np
import cmath
import csv
import matplotlib.pyplot as plt

#parameters of the planets
ganymede = { "v":10875.3 + 0j, "m":0.148*10**24, "pos":1070000000j, "Fres":0 }
europa = { "v":-13739.6 + 0j, "m":4.8*10**22, "pos":-670900000j, "Fres":0 }
io = { "v":17339.83 + 0j, "m":8.9*10**22, "pos":421800000j, "Fres":0 }
jupiter = { "m":1.900*10**27, "pos":0 }

#overige parameters
t = 0
dt = 60*60
regels = 16*48

#Berekent Gravitatiekracht (N) om Fres en versnelling te kunnen berekenen
#PosSubj is de positie van de andere maan/planeet die de gravitatie uitoefent
#PosObj is de positie van de huidige maan die de kracht ondergaat
def calcFg( M, m, PosSubj, PosObj ):
    z = PosSubj - PosObj
    r = abs( PosSubj - PosObj )
    G = 6.67430*10**(-11)
    Fg = z*G*M*m/(r**3)
    return Fg

def calcFres( maan, *other ):
    Fres = 0
    for arg in other:
        Fg = calcFg( arg["m"], maan["m"], arg["pos"], maan["pos"] )
        Fres += Fg
    return Fres

with open( "natuurkunde_model.csv", "w", newline="" ) as f:
    fieldnames = ['index', 't', 
                  'ganymede_x', 'ganymede_y', 'ganymede_v', 
                  'europa_x', 'europa_y', 'europa_v', 
                  'io_x', 'io_y', 'io_v']
    lijst = csv.DictWriter( f, fieldnames=fieldnames )

    lijst.writeheader()
    lijst.writerow({ 'index':'0', 't':t, 
                   'ganymede_x':ganymede["pos"].real, 'ganymede_y':ganymede["pos"].imag, 'ganymede_v':abs(ganymede["v"]), 
                   'europa_x':europa["pos"].real, 'europa_y':europa["pos"].imag, 'europa_v':abs(europa["v"]), 
                   'io_x':io["pos"].real, 'io_y':io["pos"].imag, 'io_v':abs(io["v"]) })
    
    plot = { 'ganymede':np.array( [[ganymede["pos"].real], [ganymede["pos"].imag]] ),
            'europa':np.array( [[europa["pos"].real], [europa["pos"].imag]] ),
            'io':np.array( [[io["pos"].real], [io["pos"].imag]] ),
             }

    for i in range( 1, regels+1 ):
        t += dt
        
        ganymede["Fres"] = calcFres( ganymede, europa, io, jupiter )
        europa["Fres"] = calcFres( europa, io, jupiter, ganymede )
        io["Fres"] = calcFres( io, jupiter, ganymede, europa )

        for arg in ( ganymede, europa, io ):
            a = arg["Fres"] / arg["m"]
            dv = a * dt
            arg["v"] += dv
            dPos = arg["v"] * dt
            print(f"i={i}  a: {a} dv: {dv} dPos: {dPos}")
            arg["pos"] += dPos
        lijst.writerow({ 'index':i, 't':t, 
                   'ganymede_x':ganymede["pos"].real, 'ganymede_y':ganymede["pos"].imag, 'ganymede_v':abs(ganymede["v"]), 
                   'europa_x':europa["pos"].real, 'europa_y':europa["pos"].imag, 'europa_v':abs(europa["v"]), 
                   'io_x':io["pos"].real, 'io_y':io["pos"].imag, 'io_v':abs(io["v"]) })
        
        plot['ganymede'] = np.append(plot['ganymede'], [[ganymede["pos"].real],[ganymede["pos"].imag]], axis = 1)
        plot['europa'] = np.append(plot['europa'], [[europa["pos"].real],[europa["pos"].imag]], axis = 1)
        plot['io'] = np.append(plot['io'], [[io["pos"].real],[io["pos"].imag]], axis = 1)
    

plt.plot(plot["ganymede"][0], plot["ganymede"][1], color='green', linewidth = '1')
plt.plot(plot["europa"][0], plot["europa"][1], color='blue', linewidth = '1')
plt.plot(plot["io"][0], plot["io"][1], color='purple', linewidth = '1')
plt.plot(0,0, marker='*', color='orange')
plt.show()
