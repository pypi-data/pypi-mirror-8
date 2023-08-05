"""Contains basic astronomical constants and functions"""
import numpy
import math
import datetime
from math import pi

day = 86400.
julian_year = 365.25*day
julian_century = 100*julian_year

"""Frequencies (angular speeds) at which the following astronomical quantities change:
   
    Cm: longitude (hour angle) of a point on earth with respect to the moon
    s:  geocentric mean longitude of the moon
    h:  geocentric mean longitude of the sun
    p:  longitude of the lunar perigee
    N:  longitude of the lunar ascending node
    pp: p', longitude of the perihelion

    All angles/arguments are in radians, times in seconds
    Source: D.T.Pugh, "Tides, Surges and Mean Sea-Level", Wiley 1996 - table 3:2 """

astronomical_omegas = [
        2*pi/(1.03505*day),    # omega_1, cm:  mean lunar day (this is one more significant figure than in Pugh obtained from 1.0/0.9661369, necessary to match Schwiderski's frequencies)
        2*pi/(27.3217*day),     # omega_2, s:   sidereal month
        2*pi/(365.2422*day),     # omega_3, h:   tropical year
        2*pi*3.0937e-4/day      # omega_4, p:   moon's perigee (8.85 julian years)
        #-2*pi*1.471e-4/day,       # omega_5, N:   regression of moon's nodes
        #2*pi/(20942*julian_year) # omega_6, pp:  perihelion
       ]

"""longterm variation matrix, encoding formulae by 
  E.W. Schwiderski - Rev. Geophys. Space Phys. Vol. 18
  No. 1 pp. 243--268, 1980
such that:
       (s, h, p, N, p')=A * (1,T,T**2,T**3)
where T is T=(27392.500528+1.0000000356*D)/36525, where D is number of days since 1 jan 1975,
which roughly means T is n/o julian centuries since 1 Jan 1899, 12 noon (!) (with day length corection?)
phases here are in degrees, not radians!
Supplemented by formulas for N and p' from Kowalik and Luick"""
Schwiderski_matrix = numpy.array([
       # These are (s,h,p) at 1 Jan 1899 12 noon(!) in degrees
       [270.434358, 279.69668, 334.329653, 259.18344, 281.22084],
       # phase speeds degree/julian_century - should be equal to omega above
       [481267.88314137, 36000.768930485, 4069.0340329575, -1934.14212, 1.7189999999999999],
       # quadratic coefficients
       [-0.001133, 3.03e-4, -0.01325, 0.00216, 0.00036],
       # cubic coefficients
       [1.9e-6, 0.0, -1.2e-5, 0.0, 0.0 ]]).T

deg2rad = pi/180
rad2deg = 180/pi

"""The first lunar doodson number indicates the angle Cm of Greenwich wrt 
 the moon (i.e. minus the longitude of the moon, and Cm increases as
 Greenwich turns away from the moon). This can be calculated as Cm = H+h-s, 
 where H is the angle of the sun wrt to Greenwich which we
 can compute from the number of hours since noon times 360deg/24hr (although
 we actually use the time since midnight below which gives a 180 shift which
 is compensated in the tidal_phase_origin table below.)"""
lunar_doodson_numbers = {
  'Z0': [ 0.0, 0.0, 0.0, 0.0],
  # Diurnal components:
  'K1': [ 1.0, 1.0, 0.0, 0.0],
  'O1': [ 1.0, -1.0, 0.0, 0.0],
  'Q1': [ 1.0, -2.0, 0.0, 1.0],
  'P1': [ 1.0, 1.0, -2.0, 0.0],
  'S1': [ 1.0, 1.0, -1.0, 0.0],
  # Semi-diurnal components:
  'M2': [ 2.0, 0.0, 0.0, 0.0],
  'S2': [ 2.0, 2.0, -2.0, 0.0],
  'N2': [ 2.0, -1.0, 0.0, 1.0],
  'K2': [ 2.0, 2.0, 0.0, 0.0],
  'L2': [ 2.0, 1.0, 0.0, -1.0],
  # Higher-order (nonlinear) components, these are simply combinations of the above:
  '2N2': [ 2.0, -2.0, 0.0, 2.0],
  'MU2': [ 2.0, -2.0, 2.0, 0.0],
  'NU2': [ 2.0, -1.0, 2.0, -1.0],
  'T2':  [ 2.0, 2.0, -3.0, 0.0], # what about its p' component?
  'M4':  [ 4.0, 0.0, 0.0, 0.0],
  'MS4': [ 4.0, 2.0, -2.0, 0.0],
  'MN4': [ 4.0, -1.0, 0.0, 1.0],
  # long period species:
  'Mf': [ 0.0, 2.0, 0.0, 0.0],
  'Mm': [ 0.0, 1.0, 0.0, -1.0],
  'Ssa': [ 0.0, 0.0, 2.0, 0.0],
  'Sa': [ 0.0, 0.0, 1.0, 0.0]}

# now we can compute the frequencies of the tidal constituents
omega={}
for constituent,doodson_numbers in lunar_doodson_numbers.items():
  omega[constituent] = numpy.dot(doodson_numbers, astronomical_omegas)

# sanity check that solar S2 is exactly 12 hours
assert(abs(omega['S2']-2*pi/day*2)<1e-10)

# the solar doodson numbers indicate a linear combination of (H,s,h,p) instead 
# of the lunar doodson numbers which refer to (Cm,s,h,p)
solar_doodson_numbers = {}
for constituent,doodson_numbers in lunar_doodson_numbers.items():
  solar_doodson_numbers[constituent] = doodson_numbers[:]
  # Cm=H-s+h, so for lunar doodson (alpha,0,0,0) we get (alpha,-alpha,alpha,0) solar
  solar_doodson_numbers[constituent][1] -= doodson_numbers[0] # -s
  solar_doodson_numbers[constituent][2] += doodson_numbers[0] # +h

tidal_phase_origin={
    'Z0':0., 
    'K1':90., 'O1':-90., 'Q1':-90., 'P1':-90., 'S1':90.,
    'M2':0., 'S2':0., 'N2':0., 'K2':0., 'L2':180., 
    'Mf':0., 'Mm':0., 'Ssa':0., 'Sa':0.,
    '2N2':0., 'MU2':0., 'NU2':0., 'T2':0.,
    'M4':0., 'MS4':0., 'MN4':0.}

# compute the astronomical arguments H, s, h, p'
def astronomical_argument(time):
    # time should be specified as a datetime object
    # compute the timedelta since 1975-1-1
    td = time-datetime.datetime(1975,1,1,0,0)
    # don't use total_seconds() as that's python2.7
    D = td.days + td.seconds/day + 1.0 # days since 1975-1-1 counting from 1
    # Note that in TABLE 1 of Schwiderski there is no H
    # This is because there D is assumed integer (i.e. it computes \chi for
    # midnight universal time), to add in the contribution for H keeping
    # tidal_phase_origin above the same as in the table,
    # we have to start H=0 at midnight instead of H=-180 which is the longitude 
    # of the sun at midnight Greenwich time
    H = float(td.seconds)/day*360. # fraction of the day since last noon time 360

    T = (27392.500528+1.0000000356*D)/36525 # big T in Schwiderski
    s,h,p,N,pp = numpy.dot(Schwiderski_matrix, [1.0, T, T**2, T**3])
    return H,s,h,p,N,pp

nodal_correction_f0 = {
  'Mf': 1.043, 
  'O1': 1.009,
  'Q1': 1.009,
  'K1': 1.006,
  'K2': 1.024}
nodal_correction_f1 = {
  'Mm': -0.130,
  'Mf': +0.414,
  'O1': +0.187,
  'Q1': +0.187,
  'K1': +0.115,
  'M2': -0.037,
  'N2': -0.037,
  'K2': +0.286}
nodal_correction_u1 = {
  'Mf': -0.41364303,
  'O1':  0.18849556,
  'Q1':  0.18849556,
  'K1': -0.1553343,
  'M2': -0.03665191,
  'N2': -0.03665191,
  'K2': -0.30892328}
nodal_correction_f2={}
# nodal corrections for M4, MN4, MS4
for comp in ('M2','N2','S2'):
  if comp[0]=='M':
    name='M4'
  else:
    name='M'+comp[0]+'4'
  nodal_correction_f0[name] = nodal_correction_f0.get('M2',1.0) * nodal_correction_f0.get(comp, 1.0)
  nodal_correction_f1[name] = (nodal_correction_f0.get('M2',1.0) * nodal_correction_f1.get(comp, 0.0) +
            nodal_correction_f1.get('M2',0.0) * nodal_correction_f0.get(comp, 1.0))
  nodal_correction_f2[name] = nodal_correction_f1.get('M2',0.0) * nodal_correction_f1.get(comp, 0.0)
  nodal_correction_u1[name] = nodal_correction_u1.get('M2',0.0) + nodal_correction_u1.get(comp, 0.0)
# nodal corrections that are the same as M2 and N2 (see Pugh table 4.3):
for comp in ('2N2', 'MU2', 'NU2', 'T2'):
  nodal_correction_f0[comp] = nodal_correction_f0.get('M2', 1.0)
  nodal_correction_f1[comp] = nodal_correction_f1.get('M2', 0.0)
  nodal_correction_f2[comp] = nodal_correction_f2.get('M2', 0.0)
  nodal_correction_u1[comp] = nodal_correction_u1.get('M2', 0.0)

def nodal_corrections(constituents, N, pp):
  # compute the 18.6 year variations (pp is currently not used)
  # the numbers come from Kowalik and Luick, table 1.6
  f=[]; u=[]
  cosN = math.cos(N*deg2rad)
  cosNsq = cosN**2
  sinN = math.sin(N*deg2rad)
  for constituent in constituents:
    # amplitude corrections:
    f0 = nodal_correction_f0.get(constituent, 1.0)
    f1 = nodal_correction_f1.get(constituent, 0.0)
    f2 = nodal_correction_f2.get(constituent, 0.0)
    f.append(f0 + f1*cosN + f2*cosNsq)
    # phase corrections:
    u.append(nodal_correction_u1.get(constituent, 0.0)*sinN)

  return numpy.array(f), numpy.array(u)

def tidal_arguments(constituents, time):
    H,s,h,p,N,pp = astronomical_argument(time)
    arguments = []
    for constituent in constituents:
      arguments.append( (numpy.dot(solar_doodson_numbers[constituent], [H,s,h,p]) 
        + tidal_phase_origin[constituent]) * deg2rad )
    return numpy.array(arguments)
