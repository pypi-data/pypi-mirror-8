================================================
titration: Computation and Plotting of pH-Values
================================================

This module provides object types which represents Solutes and Solutions
of acids and bases. A solute is representented by its pK-values (possibly
more than one value for di- (or tri-)protonic acids, similarly for bases) and its
concentration, measured in mol/L. The volume of the solute may be set later.
Each solution is represented by an instance of an arbitrary number of acids and bases.

This program is for teaching purposes only. The function plot_titration in
the class Titration allows easy plotting of titration curves. The volumes of
the solutes must be known.

This is no professional program. I tried to understand the titration curves
in 
Atkins, Jones: Chemie - Einfach alles
and did not find simple programs to plot such curves. So I wrote this program.
Dependence of the constants on the temperature is not implemented, the values
of the pK-values may be very inaccurate (I do not know any source of reliable
values). The values are from easily accessible literature. Salts must be
represented by mixtures of acids and bases. May be, this program is useful for
buffered solutions also. This has to be investigated.


Key features
------------

 * Plotting of titration curves
 * Arbitrary number of acids and bases
 * Acids and bases are represented by their pK-values and their concentration
   It is possible to have substances of the same kind, but different concentration.
 * Plotting of protionation
 * Computation of pH-values
 * Subclasses Acid and Base

Installation
------------

titration can be installed from source::

   $ tar xf titration-0.2.tar.gz
   $ cd titration-0.2 
   $ python setup.py install

or simply by copying
   titration.py
(english or german version) to PYTHONPATH

On Unix systems, the latter command may have to be executed with root
privileges.


Using the module
----------------

Plotting of a titration may be as simple as

   >>> from titration import *
   >>> acid = Substance('for')       # 'for' unique abbreviation of 'formic acid'
   >>> base = Substance('caustic p') # 'caustic p' abbreviation of 'caustic potash'
   >>> titration = Titration(base,acid)
   >>> titration.plot_titration(3,1) 

If we (and the program) know the chemical formula, we use (same substances)

   >>> from titration import *
   >>> acid = Substance('HCOOH')
   >>> base = Substance('KOH')
   >>> titration = Titration(base,acid)
   >>> titration.plot_titration(3,1) 

In both cases the program knows that HCOOH is an acid and KOH is a base.

If we want to use the known pk_values, we write

   >>> from titration import *
   >>> acid = Substance('[3.75,]',acid=True)
   >>> base = Substance('[-1.00,], acid=False)
   >>> titration = Titration(base,acid)
   >>> titration.plot_titration(3,1) 

Here we must tell the program that acid is an acid and base a base.

It is possible to plot protianation curves of a solute.

   >>> from titration import *
   >>> acid = Substance('H_3PO_4') # 'phosphoric acid'
   >>> acid.plot_protionation()

References
----------

Michael Luthardt: Die Berechnung von pH-Werten in Wasser.
http://dr-luthardt.de/chemie.htm?tip=ph

Valuable information can be found in
http://chemistry.stackexchange.com/questions/8057/the-reason-behind-the-steep-rise-in-
ph-in-the-acid-base-titration-curve

A little theory:
Peter W. Atkins, Loretta Jones: Chemie - einfach alles. 2-te Aufl.
Wiley-VCH Verlag, Weinheim (2006), Ch. 10 and 11

Algorithms are explained in titration.pdf
D. Kadelka. Titration - Berechnung von pH-Werten in Wasser (2014).
(In german, in folder german)

Version
-------

titration-0.1
  This is german/titration.py in folder german
(In this version, substances are identified by their german names).
