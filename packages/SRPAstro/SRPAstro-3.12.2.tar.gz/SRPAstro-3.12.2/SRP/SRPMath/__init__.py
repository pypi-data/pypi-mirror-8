""" Init file for SRPMath

Context : SRP
Module  : Math
Version : 1.1.2
Author  : Stefano Covino
Date    : 18/11/2014
E-mail  : stefano.covino@brera.inaf.it
URL     : http://www.me.oa-brera.inaf.it/utenti/covino


Usage   : to be imported

Remarks :

History : (29/09/2010) First named version.
        : (08/11/2010) Cartesian distance added.
        : (09/02/2012) Sidereal time, hour and parallactic angles computation added.
        : (11/02/2012) PointMatch added.
        : (18/02/2012) Sky functions moved to SRPSky.
        : (23/08/2012) New angular distance function.
        : (20/09/2012) Angular phasing function.
        : (18/11/2014) Doppler factor function.
"""


__all__ = ['AngularDistance', 'AstroAngleInput', 'AstroCoordInput', 'AstroMagInput',
           'CartesiamCoordAmpRotoTranslation','CartesianDistance', 'CartesianVectorClass',
           'DopplerFactor','FastAngularDistance', 'InverseCartesiamCoordAmpRotoTranslation',
           'LorentzFactor','MinDist', 'PhaseAngle', 'PointClass', 'PointMatch', 'TriangleClass',
           'TriangleMatch']


