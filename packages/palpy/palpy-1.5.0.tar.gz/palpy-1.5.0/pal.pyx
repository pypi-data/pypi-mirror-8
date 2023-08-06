
# Copyright (C) 2012 Tim Jenness and Science and Technology
# Facilities Council.
# Copyright (C) 2014 Tim Jenness

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of
# the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

cimport cpal

from libc.stdlib cimport malloc, free

cimport numpy as np
import numpy as np

D2PI = cpal.PAL__D2PI
DAS2R = cpal.PAL__DAS2R
DD2R = cpal.PAL__DD2R
DH2R = cpal.PAL__DH2R
DPI = cpal.PAL__DPI
DPIBY2 = cpal.PAL__DPIBY2
DR2AS = cpal.PAL__DR2AS
DR2D = cpal.PAL__DR2D
DR2H = cpal.PAL__DR2H
DR2S = cpal.PAL__DR2S
DS2R = cpal.PAL__DS2R

def palvers():
    """
    versiondict = palvers()

    Returns the version information from the underlying PAL C
    library used to build palpy. Version information is returned in
    a dict with keys:

    verstring : Version in string form, e.g "1.6.2"
    major : Major version number as integer, e.g. 1
    minor : Minor version number as integer, e.g. 6
    patchlevel : Patch level as integer, e.g. 2
    """
    return dict( { "verstring": "0.9.0",
                    "major": 0,
                    "minor": 9,
                    "patchlevel": 0 } )

def addet( double rm, double dm, double eq ):
     """
     (rc, dc) = addet( rm, dm, eq)

Add the E-terms to a pre IAU 1976 mean place

Arguments
---------
rm = double (Given)
   RA without E-terms (radians)
dm = double (Given)
   Dec without E-terms (radians)
eq = double (Given)
   Besselian epoch of mean equator and equinox
rc = double * (Returned)
   RA with E-terms included (radians)
dc = double * (Returned)
   Dec with E-terms included (radians)


Notes
-----
Most star positions from pre-1984 optical catalogues (or
derived from astrometry using such stars) embody the
E-terms.  If it is necessary to convert a formal mean
place (for example a pulsar timing position) to one
consistent with such a star catalogue, then the RA,Dec
should be adjusted using this routine.
     """
     cdef double rc
     cdef double dc
     cpal.palAddet( rm, dm, eq, &rc, &dc )
     return ( rc, dc )

def airmas( double zd ):
     """
     airmass = airmas( zd )

Air mass at given zenith distance

Arguments
---------
zd = double (Given)
   Observed zenith distance (radians)


Notes
-----
- The "observed" zenith distance referred to above means "as
  affected by refraction".
- Uses Hardie's (1962) polynomial fit to Bemporad's data for
  the relative air mass, X, in units of thickness at the zenith
  as tabulated by Schoenberg (1929). This is adequate for all
  normal needs as it is accurate to better than 0.1% up to X =
  6.8 and better than 1% up to X = 10. Bemporad's tabulated
  values are unlikely to be trustworthy to such accuracy
  because of variations in density, pressure and other
  conditions in the atmosphere from those assumed in his work.
- The sign of the ZD is ignored.
- At zenith distances greater than about ZD = 87 degrees the
  air mass is held constant to avoid arithmetic overflows.
     """
     return cpal.palAirmas( zd )

def altaz(double ha, double dec, double phi):
     """
     (az, azd, azdd, el, eld, eldd, pa, pad, padd) = altaz( ha, dec, phi )

Positions, velocities and accelerations for an altazimuth telescope mount

Arguments
---------
ha = double (Given)
   Hour angle (radians)
dec = double (Given)
   Declination (radians)
phi = double (Given)
   Observatory latitude (radians)
az = double * (Returned)
   Azimuth (radians)
azd = double * (Returned)
   Azimuth velocity (radians per radian of HA)
azdd = double * (Returned)
   Azimuth acceleration (radians per radian of HA squared)
el = double * (Returned)
   Elevation (radians)
eld = double * (Returned)
   Elevation velocity (radians per radian of HA)
eldd = double * (Returned)
   Elevation acceleration (radians per radian of HA squared)
pa = double * (Returned)
   Parallactic angle (radians)
pad = double * (Returned)
   Parallactic angle velocity (radians per radian of HA)
padd = double * (Returned)
   Parallactic angle acceleration (radians per radian of HA squared)


Notes
-----
- Natural units are used throughout.  HA, DEC, PHI, AZ, EL
  and ZD are in radians.  The velocities and accelerations
  assume constant declination and constant rate of change of
  hour angle (as for tracking a star);  the units of AZD, ELD
  and PAD are radians per radian of HA, while the units of AZDD,
  ELDD and PADD are radians per radian of HA squared.  To
  convert into practical degree- and second-based units:

    angles * 360/2pi -> degrees
    velocities * (2pi/86400)*(360/2pi) -> degree/sec
    accelerations * ((2pi/86400)**2)*(360/2pi) -> degree/sec/sec

  Note that the seconds here are sidereal rather than SI.  One
  sidereal second is about 0.99727 SI seconds.

  The velocity and acceleration factors assume the sidereal
  tracking case.  Their respective numerical values are (exactly)
  1/240 and (approximately) 1/3300236.9.

- Azimuth is returned in the range 0-2pi;  north is zero,
  and east is +pi/2.  Elevation and parallactic angle are
  returned in the range +/-pi.  Parallactic angle is +ve for
  a star west of the meridian and is the angle NP-star-zenith.

- The latitude is geodetic as opposed to geocentric.  The
  hour angle and declination are topocentric.  Refraction and
  deficiencies in the telescope mounting are ignored.  The
  purpose of the routine is to give the general form of the
  quantities.  The details of a real telescope could profoundly
  change the results, especially close to the zenith.

- No range checking of arguments is carried out.

- In applications which involve many such calculations, rather
  than calling the present routine it will be more efficient to
  use inline code, having previously computed fixed terms such
  as sine and cosine of latitude, and (for tracking a star)
  sine and cosine of declination.
     """
     cdef double az
     cdef double azd
     cdef double azdd
     cdef double el
     cdef double eld
     cdef double eldd
     cdef double pa
     cdef double pad
     cdef double padd
     cpal.palAltaz (ha, dec, phi, &az, &azd, &azdd, &el, &eld, &eldd, &pa, &pad, &padd )
     return (az, azd, azdd, el, eld, eldd, pa, pad, padd )

def amp( double ra, double da, double date, double eq):
     """
     (rm, dm) = amp( ra, da, date, eq )

Convert star RA,Dec from geocentric apparaent to mean place.

Arguments
---------
ra = double (Given)
   Apparent RA (radians)
dec = double (Given)
   Apparent Dec (radians)
date = double (Given)
   TDB for apparent place (JD-2400000.5)
eq = double (Given)
   Equinox: Julian epoch of mean place.
rm = double * (Returned)
   Mean RA (radians)
dm = double * (Returned)
   Mean Dec (radians)


Notes
-----
- See palMappa and palAmpqk for details.
     """
     cdef double rm
     cdef double dm
     cpal.palAmp( ra, da, date, eq, &rm, &dm )
     return ( rm, dm )

def ampqk( double ra, double da, np.ndarray[double, ndim=1] amprms not None ):
     """
     (rm, dm) = ampqk( ra, da, amprms )

Convert star RA,Dec from geocentric apparent to mean place.

Arguments
---------
ra = double (Given)
   Apparent RA (radians).
da = double (Given)
   Apparent Dec (radians).
amprms = double[21] (Given)
   Star-independent mean-to-apparent parameters (see palMappa):
   (0)      time interval for proper motion (Julian years)
   (1-3)    barycentric position of the Earth (AU)
   (4-6)    not used
   (7)      not used
   (8-10)   abv: barycentric Earth velocity in units of c
   (11)     sqrt(1-v*v) where v=modulus(abv)
   (12-20)  precession/nutation (3,3) matrix
rm = double (Returned)
   Mean RA (radians).
dm = double (Returned)
   Mean Dec (radians).
     """
     cdef double rm
     cdef double dm
     cdef double camprms[21]
     for i in range(21):
          camprms[i] = amprms[i]
     cpal.palAmpqk( ra, da, camprms, &rm, &dm )
     return (rm, dm)

def aop( double rap, double dap, double date, double dut,
         double elongm, double phim, double hm, double xp,
         double yp, double tdk, double pmb, double rh,
         double wl, double tlr ):
     """
     (aob, zob, hob, dob, rob) = aop( rap, dap, date, dut,
                                      elongm, phim, hm, xp,
                                      yp, tdk, pmb, rh,
                                      wl, tlr )

Apparent to observed place

Arguments
---------
rap = double (Given)
   Geocentric apparent right ascension
dap = double (Given)
   Geocentirc apparent declination
date = double (Given)
   UTC date/time (Modified Julian Date, JD-2400000.5)
dut = double (Given)
   delta UT: UT1-UTC (UTC seconds)
elongm = double (Given)
   Mean longitude of the observer (radians, east +ve)
phim = double (Given)
   Mean geodetic latitude of the observer (radians)
hm = double (Given)
   Observer's height above sea level (metres)
xp = double (Given)
   Polar motion x-coordinates (radians)
yp = double (Given)
   Polar motion y-coordinates (radians)
tdk = double (Given)
   Local ambient temperature (K; std=273.15)
pmb = double (Given)
   Local atmospheric pressure (mb; std=1013.25)
rh = double (Given)
   Local relative humidity (in the range 0.0-1.0)
wl = double (Given)
   Effective wavelength (micron, e.g. 0.55)
tlr = double (Given)
   Tropospheric laps rate (K/metre, e.g. 0.0065)
aob = double * (Returned)
   Observed azimuth (radians: N=0; E=90)
zob = double * (Returned)
   Observed zenith distance (radians)
hob = double * (Returned)
   Observed Hour Angle (radians)
dob = double * (Returned)
   Observed Declination (radians)
rob = double * (Returned)
   Observed Right Ascension (radians)


Notes
-----
- This routine returns zenith distance rather than elevation
  in order to reflect the fact that no allowance is made for
  depression of the horizon.

- The accuracy of the result is limited by the corrections for
  refraction.  Providing the meteorological parameters are
  known accurately and there are no gross local effects, the
  predicted apparent RA,Dec should be within about 0.1 arcsec
  for a zenith distance of less than 70 degrees.  Even at a
  topocentric zenith distance of 90 degrees, the accuracy in
  elevation should be better than 1 arcmin;  useful results
  are available for a further 3 degrees, beyond which the
  palRefro routine returns a fixed value of the refraction.
  The complementary routines palAop (or palAopqk) and palOap
  (or palOapqk) are self-consistent to better than 1 micro-
  arcsecond all over the celestial sphere.

- It is advisable to take great care with units, as even
  unlikely values of the input parameters are accepted and
  processed in accordance with the models used.

- "Apparent" place means the geocentric apparent right ascension
  and declination, which is obtained from a catalogue mean place
  by allowing for space motion, parallax, precession, nutation,
  annual aberration, and the Sun's gravitational lens effect.  For
  star positions in the FK5 system (i.e. J2000), these effects can
  be applied by means of the palMap etc routines.  Starting from
  other mean place systems, additional transformations will be
  needed;  for example, FK4 (i.e. B1950) mean places would first
  have to be converted to FK5, which can be done with the
  palFk425 etc routines.

- "Observed" Az,El means the position that would be seen by a
  perfect theodolite located at the observer.  This is obtained
  from the geocentric apparent RA,Dec by allowing for Earth
  orientation and diurnal aberration, rotating from equator
  to horizon coordinates, and then adjusting for refraction.
  The HA,Dec is obtained by rotating back into equatorial
  coordinates, using the geodetic latitude corrected for polar
  motion, and is the position that would be seen by a perfect
  equatorial located at the observer and with its polar axis
  aligned to the Earth's axis of rotation (n.b. not to the
  refracted pole).  Finally, the RA is obtained by subtracting
  the HA from the local apparent ST.

- To predict the required setting of a real telescope, the
  observed place produced by this routine would have to be
  adjusted for the tilt of the azimuth or polar axis of the
  mounting (with appropriate corrections for mount flexures),
  for non-perpendicularity between the mounting axes, for the
  position of the rotator axis and the pointing axis relative
  to it, for tube flexure, for gear and encoder errors, and
  finally for encoder zero points.  Some telescopes would, of
  course, exhibit other properties which would need to be
  accounted for at the appropriate point in the sequence.

- This routine takes time to execute, due mainly to the
  rigorous integration used to evaluate the refraction.
  For processing multiple stars for one location and time,
  call palAoppa once followed by one call per star to palAopqk.
  Where a range of times within a limited period of a few hours
  is involved, and the highest precision is not required, call
  palAoppa once, followed by a call to palAoppat each time the
  time changes, followed by one call per star to palAopqk.

- The DATE argument is UTC expressed as an MJD.  This is,
  strictly speaking, wrong, because of leap seconds.  However,
  as long as the delta UT and the UTC are consistent there
  are no difficulties, except during a leap second.  In this
  case, the start of the 61st second of the final minute should
  begin a new MJD day and the old pre-leap delta UT should
  continue to be used.  As the 61st second completes, the MJD
  should revert to the start of the day as, simultaneously,
  the delta UTC changes by one second to its post-leap new value.

- The delta UT (UT1-UTC) is tabulated in IERS circulars and
  elsewhere.  It increases by exactly one second at the end of
  each UTC leap second, introduced in order to keep delta UT
  within +/- 0.9 seconds.

- IMPORTANT -- TAKE CARE WITH THE LONGITUDE SIGN CONVENTION.
  The longitude required by the present routine is east-positive,
  in accordance with geographical convention (and right-handed).
  In particular, note that the longitudes returned by the
  palObs routine are west-positive, following astronomical
  usage, and must be reversed in sign before use in the present
  routine.

- The polar coordinates XP,YP can be obtained from IERS
  circulars and equivalent publications.  The maximum amplitude
  is about 0.3 arcseconds.  If XP,YP values are unavailable,
  use XP=YP=0.0.  See page B60 of the 1988 Astronomical Almanac
  for a definition of the two angles.

- The height above sea level of the observing station, HM,
  can be obtained from the Astronomical Almanac (Section J
  in the 1988 edition), or via the routine palObs.  If P,
  the pressure in millibars, is available, an adequate
  estimate of HM can be obtained from the expression

        HM ~ -29.3*TSL*LOG(P/1013.25).

  where TSL is the approximate sea-level air temperature in K
  (see Astrophysical Quantities, C.W.Allen, 3rd edition,
  section 52).  Similarly, if the pressure P is not known,
  it can be estimated from the height of the observing
  station, HM, as follows:

        P ~ 1013.25*EXP(-HM/(29.3*TSL)).

  Note, however, that the refraction is nearly proportional to the
  pressure and that an accurate P value is important for precise
  work.

- The azimuths etc produced by the present routine are with
  respect to the celestial pole.  Corrections to the terrestrial
  pole can be computed using palPolmo.
     """
     cdef double aob
     cdef double zob
     cdef double hob
     cdef double dob
     cdef double rob
     cpal.palAop( rap, dap, date, dut, elongm, phim, hm,
                  xp, yp, tdk, pmb, rh, wl, tlr,
                  &aob, &zob, &hob, &dob, &rob)
     return (aob, zob, hob, dob, rob )

def aoppa(double date, double dut, double elongm, double phim,
          double hm, double xp, double yp, double tdk, double pmb,
          double rh, double wl, double tlr ):
     """
     aoprms = aoppa( date, dut, elongm, phim, hm, xp, yp,
                     tdk, pmb, rh, wl, tlr )

Precompute apparent to observed place parameters

Arguments
---------
date = double (Given)
   UTC date/time (modified Julian Date, JD-2400000.5)
dut = double (Given)
   delta UT:  UT1-UTC (UTC seconds)
elongm = double (Given)
   mean longitude of the observer (radians, east +ve)
phim = double (Given)
   mean geodetic latitude of the observer (radians)
hm = double (Given)
   observer's height above sea level (metres)
xp = double (Given)
   polar motion x-coordinate (radians)
yp = double (Given)
   polar motion y-coordinate (radians)
tdk = double (Given)
   local ambient temperature (K; std=273.15)
pmb = double (Given)
   local atmospheric pressure (mb; std=1013.25)
rh = double (Given)
   local relative humidity (in the range 0.0-1.0)
wl = double (Given)
   effective wavelength (micron, e.g. 0.55)
tlr = double (Given)
   tropospheric lapse rate (K/metre, e.g. 0.0065)
aoprms = double [14] (Returned)
   Star-independent apparent-to-observed parameters

    (0)      geodetic latitude (radians)
    (1,2)    sine and cosine of geodetic latitude
    (3)      magnitude of diurnal aberration vector
    (4)      height (hm)
    (5)      ambient temperature (tdk)
    (6)      pressure (pmb)
    (7)      relative humidity (rh)
    (8)      wavelength (wl)
    (9)     lapse rate (tlr)
    (10,11)  refraction constants A and B (radians)
    (12)     longitude + eqn of equinoxes + sidereal DUT (radians)
    (13)     local apparent sidereal time (radians)


Notes
-----
- It is advisable to take great care with units, as even
  unlikely values of the input parameters are accepted and
  processed in accordance with the models used.

- The DATE argument is UTC expressed as an MJD.  This is,
  strictly speaking, improper, because of leap seconds.  However,
  as long as the delta UT and the UTC are consistent there
  are no difficulties, except during a leap second.  In this
  case, the start of the 61st second of the final minute should
  begin a new MJD day and the old pre-leap delta UT should
  continue to be used.  As the 61st second completes, the MJD
  should revert to the start of the day as, simultaneously,
  the delta UTC changes by one second to its post-leap new value.

- The delta UT (UT1-UTC) is tabulated in IERS circulars and
  elsewhere.  It increases by exactly one second at the end of
  each UTC leap second, introduced in order to keep delta UT
  within +/- 0.9 seconds.

- IMPORTANT -- TAKE CARE WITH THE LONGITUDE SIGN CONVENTION.
  The longitude required by the present routine is east-positive,
  in accordance with geographical convention (and right-handed).
  In particular, note that the longitudes returned by the
  palObs routine are west-positive, following astronomical
  usage, and must be reversed in sign before use in the present
  routine.

- The polar coordinates XP,YP can be obtained from IERS
  circulars and equivalent publications.  The maximum amplitude
  is about 0.3 arcseconds.  If XP,YP values are unavailable,
  use XP=YP=0.0.  See page B60 of the 1988 Astronomical Almanac
  for a definition of the two angles.

- The height above sea level of the observing station, HM,
  can be obtained from the Astronomical Almanac (Section J
  in the 1988 edition), or via the routine palObs.  If P,
  the pressure in millibars, is available, an adequate
  estimate of HM can be obtained from the expression

        HM ~ -29.3*TSL*log(P/1013.25).

  where TSL is the approximate sea-level air temperature in K
  (see Astrophysical Quantities, C.W.Allen, 3rd edition,
  section 52).  Similarly, if the pressure P is not known,
  it can be estimated from the height of the observing
  station, HM, as follows:

        P ~ 1013.25*exp(-HM/(29.3*TSL)).

  Note, however, that the refraction is nearly proportional to the
  pressure and that an accurate P value is important for precise
  work.

- Repeated, computationally-expensive, calls to palAoppa for
  times that are very close together can be avoided by calling
  palAoppa just once and then using palAoppat for the subsequent
  times.  Fresh calls to palAoppa will be needed only when
  changes in the precession have grown to unacceptable levels or
  when anything affecting the refraction has changed.
     """
     cdef double caoprms[14]
     cdef np.ndarray aoprms = np.zeros( [14], dtype=np.float64 )
     cpal.palAoppa( date, dut, elongm, phim, hm, xp, yp, tdk, pmb,
                    rh, wl, tlr, caoprms )
     for i in range(14):
          aoprms[i] = caoprms[i]
     return aoprms

def aoppat( double date, np.ndarray[double, ndim=1] aoprms not None ):
     """
     aoprms_updated = aoppat( date, aoprms )

Recompute sidereal time to support apparent to observed place

Arguments
---------
date = double (Given)
    UTC date/time (modified Julian Date, JD-2400000.5)
    (see palAoppa description for comments on leap seconds)
aoprms = double[14] (Given & Returned)
    Star-independent apparent-to-observed parameters. Updated
    by this routine. Requires element 12 to be the longitude +
    eqn of equinoxes + sidereal DUT and fills in element 13
    with the local apparent sidereal time (in radians).


Notes
-----
- See palAoppa for more information.
- The star-independent parameters are not treated as an opaque
  struct in order to retain compatibility with SLA.
     """
     # We can either copy the array or modify in place.
     # For now we return a new copy
     cdef double caoprms[14]
     for i in range(14):
          caoprms[i] = aoprms[i]
     cpal.palAoppat( date, caoprms )
     cdef np.ndarray result = np.zeros( [14], dtype=np.float64 )
     for i in range(14):
          result[i] = caoprms[i]
     return result

def aopqk(double rap, double dap, np.ndarray[double, ndim=1] aoprms not None):
    """
    (aob, zob, hob, dob, rob) = aopqk( rap, dap, aoprms )

Quick apparent to observed place

Arguments
---------
rap = double (Given)
   Geocentric apparent right ascension
dap = double (Given)
   Geocentric apparent declination
aoprms = const double [14] (Given)
   Star-independent apparent-to-observed parameters.

    [0]      geodetic latitude (radians)
    [1,2]    sine and cosine of geodetic latitude
    [3]      magnitude of diurnal aberration vector
    [4]      height (HM)
    [5]      ambient temperature (T)
    [6]      pressure (P)
    [7]      relative humidity (RH)
    [8]      wavelength (WL)
    [9]      lapse rate (TLR)
    [10,11]  refraction constants A and B (radians)
    [12]     longitude + eqn of equinoxes + sidereal DUT (radians)
    [13]     local apparent sidereal time (radians)
aob = double * (Returned)
   Observed azimuth (radians: N=0,E=90)
zob = double * (Returned)
   Observed zenith distance (radians)
hob = double * (Returned)
   Observed Hour Angle (radians)
dob = double * (Returned)
   Observed Declination (radians)
rob = double * (Returned)
   Observed Right Ascension (radians)


Notes
-----
- This routine returns zenith distance rather than elevation
  in order to reflect the fact that no allowance is made for
  depression of the horizon.

- The accuracy of the result is limited by the corrections for
  refraction.  Providing the meteorological parameters are
  known accurately and there are no gross local effects, the
  observed RA,Dec predicted by this routine should be within
  about 0.1 arcsec for a zenith distance of less than 70 degrees.
  Even at a topocentric zenith distance of 90 degrees, the
  accuracy in elevation should be better than 1 arcmin;  useful
  results are available for a further 3 degrees, beyond which
  the palRefro routine returns a fixed value of the refraction.
  The complementary routines palAop (or palAopqk) and palOap
  (or palOapqk) are self-consistent to better than 1 micro-
  arcsecond all over the celestial sphere.

- It is advisable to take great care with units, as even
  unlikely values of the input parameters are accepted and
  processed in accordance with the models used.

- "Apparent" place means the geocentric apparent right ascension
  and declination, which is obtained from a catalogue mean place
  by allowing for space motion, parallax, precession, nutation,
  annual aberration, and the Sun's gravitational lens effect.  For
  star positions in the FK5 system (i.e. J2000), these effects can
  be applied by means of the palMap etc routines.  Starting from
  other mean place systems, additional transformations will be
  needed;  for example, FK4 (i.e. B1950) mean places would first
  have to be converted to FK5, which can be done with the
  palFk425 etc routines.

- "Observed" Az,El means the position that would be seen by a
  perfect theodolite located at the observer.  This is obtained
  from the geocentric apparent RA,Dec by allowing for Earth
  orientation and diurnal aberration, rotating from equator
  to horizon coordinates, and then adjusting for refraction.
  The HA,Dec is obtained by rotating back into equatorial
  coordinates, using the geodetic latitude corrected for polar
  motion, and is the position that would be seen by a perfect
  equatorial located at the observer and with its polar axis
  aligned to the Earth's axis of rotation (n.b. not to the
  refracted pole).  Finally, the RA is obtained by subtracting
  the HA from the local apparent ST.

- To predict the required setting of a real telescope, the
  observed place produced by this routine would have to be
  adjusted for the tilt of the azimuth or polar axis of the
  mounting (with appropriate corrections for mount flexures),
  for non-perpendicularity between the mounting axes, for the
  position of the rotator axis and the pointing axis relative
  to it, for tube flexure, for gear and encoder errors, and
  finally for encoder zero points.  Some telescopes would, of
  course, exhibit other properties which would need to be
  accounted for at the appropriate point in the sequence.

- The star-independent apparent-to-observed-place parameters
  in AOPRMS may be computed by means of the palAoppa routine.
  If nothing has changed significantly except the time, the
  palAoppat routine may be used to perform the requisite
  partial recomputation of AOPRMS.

- At zenith distances beyond about 76 degrees, the need for
  special care with the corrections for refraction causes a
  marked increase in execution time.  Moreover, the effect
  gets worse with increasing zenith distance.  Adroit
  programming in the calling application may allow the
  problem to be reduced.  Prepare an alternative AOPRMS array,
  computed for zero air-pressure;  this will disable the
  refraction corrections and cause rapid execution.  Using
  this AOPRMS array, a preliminary call to the present routine
  will, depending on the application, produce a rough position
  which may be enough to establish whether the full, slow
  calculation (using the real AOPRMS array) is worthwhile.
  For example, there would be no need for the full calculation
  if the preliminary call had already established that the
  source was well below the elevation limits for a particular
  telescope.

- The azimuths etc produced by the present routine are with
  respect to the celestial pole.  Corrections to the terrestrial
  pole can be computed using palPolmo.
    """
    cdef double aob
    cdef double zob
    cdef double hob
    cdef double dob
    cdef double rob

    cdef double caoprms[14]
    for i in range(14):
        caoprms[i]=aoprms[i]

    cpal.palAopqk(rap,dap,caoprms,&aob,&zob,&hob,&dob,&rob)

    return (aob,zob,hob,dob,rob)

def aopqkVector(np.ndarray rap, np.ndarray dap, np.ndarray[double, ndim=1] aoprms not None):
    """
    This is just aopqk, except that it accepts a vector of inputs and
    returns a vector of outputs.
    """
    cdef int i
    cdef int length=len(rap)
    cdef np.ndarray aobout = np.zeros(length,dtype=np.float64)
    cdef np.ndarray zobout = np.zeros(length,dtype=np.float64)
    cdef np.ndarray hobout = np.zeros(length,dtype=np.float64)
    cdef np.ndarray dobout = np.zeros(length,dtype=np.float64)
    cdef np.ndarray robout = np.zeros(length,dtype=np.float64)
    cdef double aob
    cdef double zob
    cdef double hob
    cdef double dob
    cdef double rob

    cdef double caoprms[14]
    for i in range(14):
         caoprms[i]=aoprms[i]
    for i in range(length):
         cpal.palAopqk(rap[i],dap[i],caoprms,&aob,&zob,&hob,&dob,&rob)
         aobout[i]=aob
         zobout[i]=zob
         hobout[i]=hob
         dobout[i]=dob
         robout[i]=rob
    return (aobout,zobout,hobout,dobout,robout)

def atmdsp(double tdk, double pmb, double rh, double wl1,
                 double a1, double b1, double wl2):
    """
    (a2, b2) = atmdsp( tdk, pmb, rh, wl1, a1, b1, wl2 )

Apply atmospheric-dispersion adjustments to refraction coefficients

Arguments
---------
tdk = double (Given)
   Ambient temperature, K
pmb = double (Given)
   Ambient pressure, millibars
rh = double (Given)
   Ambient relative humidity, 0-1
wl1 = double (Given)
   Reference wavelength, micrometre (0.4 recommended)
a1 = double (Given)
   Refraction coefficient A for wavelength wl1 (radians)
b1 = double (Given)
   Refraction coefficient B for wavelength wl1 (radians)
wl2 = double (Given)
   Wavelength for which adjusted A,B required
a2 = double * (Returned)
   Refraction coefficient A for wavelength WL2 (radians)
b2 = double * (Returned)
   Refraction coefficient B for wavelength WL2 (radians)


Notes
-----
- To use this routine, first call palRefco specifying WL1 as the
wavelength.  This yields refraction coefficients A1,B1, correct
for that wavelength.  Subsequently, calls to palAtmdsp specifying
different wavelengths will produce new, slightly adjusted
refraction coefficients which apply to the specified wavelength.

- Most of the atmospheric dispersion happens between 0.7 micrometre
and the UV atmospheric cutoff, and the effect increases strongly
towards the UV end.  For this reason a blue reference wavelength
is recommended, for example 0.4 micrometres.

- The accuracy, for this set of conditions:

   height above sea level    2000 m
                 latitude    29 deg
                 pressure    793 mb
              temperature    17 degC
                 humidity    50%
               lapse rate    0.0065 degC/m
     reference wavelength    0.4 micrometre
           star elevation    15 deg

is about 2.5 mas RMS between 0.3 and 1.0 micrometres, and stays
within 4 mas for the whole range longward of 0.3 micrometres
(compared with a total dispersion from 0.3 to 20.0 micrometres
of about 11 arcsec).  These errors are typical for ordinary
conditions and the given elevation;  in extreme conditions values
a few times this size may occur, while at higher elevations the
errors become much smaller.

- If either wavelength exceeds 100 micrometres, the radio case
is assumed and the returned refraction coefficients are the
same as the given ones.  Note that radio refraction coefficients
cannot be turned into optical values using this routine, nor
vice versa.

- The algorithm consists of calculation of the refractivity of the
air at the observer for the two wavelengths, using the methods
of the palRefro routine, and then scaling of the two refraction
coefficients according to classical refraction theory.  This
amounts to scaling the A coefficient in proportion to (n-1) and
the B coefficient almost in the same ratio (see R.M.Green,
"Spherical Astronomy", Cambridge University Press, 1985).
    """
    cdef double a2
    cdef double b2
    cpal.palAtmdsp(tdk, pmb, rh, wl1, a1, b1, wl2, &a2, &b2)
    return (a2, b2)

def caldj( int iy, int im, int id ):
     """
     djm = caldj( iy, im, id )

Gregorian Calendar to Modified Julian Date

Arguments
---------
iy = int (Given)
   Year in the Gregorian calendar
im = int (Given)
   Month in the Gergorian calendar
id = int (Given)
   Day in the Gregorian calendar
djm = double * (Returned)
   Modified Julian Date (JD-2400000.5) for 0 hrs
j = status (Returned)
  0 = OK. See eraCal2jd for other values.


Notes
-----
- Uses eraCal2jd
- Unlike eraCal2jd this routine treats the years 0-100 as
  referring to the end of the 20th Century and beginning of
  the 21st Century. If this behaviour is not acceptable
  use the SOFA/ERFA routine directly or palCldj.
  Acceptable years are 00-49, interpreted as 2000-2049,
                       50-99,     "       "  1950-1999,
                       all others, interpreted literally.
- Unlike SLA this routine will work with negative years.

     Raises
     ------
     ValueError if arguments are out of range.
     """
     cdef double djm
     cdef int j
     cpal.palCaldj( iy, im, id, &djm, &j )
     if j==0:
          return djm
     else:
          bad = ""
          if j==-1:
               bad = "year"
          elif j==-2:
               bad = "month"
          else:
               bad = "day"
          raise ValueError( "Julian date not computed. Bad {}".format(bad) )

def cldj( int iy, int im, int id ):
     """
     djm = cldj( iy, im, id )

Gregorian Calendar to Modified Julian Date

Arguments
---------
iy = int (Given)
   Year in Gregorian calendar
im = int (Given)
   Month in Gregorian calendar
id = int (Given)
   Day in Gregorian calendar
djm = double * (Returned)
   Modified Julian Date (JD-2400000.5) for 0 hrs
j = int * (Returned)
   status: 0 = OK, 1 = bad year (MJD not computed),
   2 = bad month (MJD not computed), 3 = bad day (MJD computed).


Notes
-----
- Uses eraCal2jd(). See SOFA/ERFA documentation for details.

     Raises
     ------
     ValueError if arguments are out of range.
     """
     cdef int j
     cdef double djm
     cpal.palCldj( iy, im, id, &djm, &j )
     if j==0:
          return djm
     else:
          bad = ""
          if j==-1:
               bad = "year"
          elif j==-2:
               bad = "month"
          else:
               bad = "day"
          raise ValueError( "Bad {} argument".format(bad) )

def dafin( string, int ipos ):
     """
     Decode a sexagesimal string into an angle.

       (angle, endpos) = pal.dafin( string, startpos )

     where string is the string to be analyzed, startpos
     is the position in the string to start looking
     (starts at 1), endpos is the position in the string
     after the search and angle is the decoded angle in
     radians.

     A ValueError exception is thrown if no angle can
     be found.

     A ValueError exception is thrown if an angle can
     be located but is numerically out of range.

     The interface for this routine is experimental. In
     particular the startpos and endpos variables need
     some thought. startpos could simply be ignored
     as a python slice would work just as well. endpos
     is useful in that you know where to slice the string
     to continue searching for angles. Zero- versus one-
     based indexing is an issue.
     """
     byte_string = string.encode('ascii')
     cdef char * cstring = byte_string
     cdef int cipos = ipos
     cdef double a
     cdef int j
     cpal.palDafin( cstring, &cipos, &a, &j )
     if j==0:
          return ( a, cipos )
     elif j==1:
          raise ValueError( "No angle could be located in string '{}'".format(string) )
     else:
          bad = "unknown"
          if j==-1:
               bad = "degrees"
          elif j==-2:
               bad = "arcminutes"
          elif j==-3:
               bad = "arcseconds"
          raise ValueError( "Bad {} in input string".format(bad) )

def dat( double dju ):
     """
     deltat = dat( dju )

Return offset between UTC and TAI

Arguments
---------
utc = double (Given)
   UTC date as a modified JD (JD-2400000.5)


Returned Value
--------------
dat = double
   TAI-UTC in seconds


Notes
-----
- This routine converts the MJD argument to calendar date before calling
  the SOFA/ERFA eraDat function.
- This routine matches the slaDat interface which differs from the eraDat
  interface. Consider coding directly to the SOFA/ERFA interface.
- See eraDat for a description of error conditions when calling this function
  with a time outside of the UTC range.
- The status argument from eraDat is ignored. This is reasonable since the
  error codes are mainly related to incorrect calendar dates when calculating
  the JD internally.
     """
     return cpal.palDat( dju )

def dav2m( np.ndarray[double, ndim=1] axvec not None ):
     """
     rmat = dav2m( axvec )

Form the rotation matrix corresponding to a given axial vector.

Arguments
---------
axvec = double [3] (Given)
  Axial vector (radians)
rmat = double [3][3] (Returned)
  Rotation matrix.


Notes
-----
- Uses eraRv2m(). See SOFA/ERFA documentation for details.
     """
     cdef double c_rmat[3][3]
     cdef double c_axvec[3]
     for i in range(3):
         c_axvec[i] = axvec[i]
     cpal.palDav2m( c_axvec, c_rmat )

     cdef np.ndarray rmat = np.zeros([3,3], dtype=np.float64)
     for i in range(3):
         for j in range(3):
             rmat[i][j] = c_rmat[i][j]
     return rmat

def dbear( double a1, double b1, double a2, double b2 ):
     """
     b = dbear( a1, b1, a2, b2 )

Bearing (position angle) of one point on a sphere relative to another

Arguments
---------
a1 = double (Given)
   Longitude of point A (e.g. RA) in radians.
a2 = double (Given)
   Latitude of point A (e.g. Dec) in radians.
b1 = double (Given)
   Longitude of point B in radians.
b2 = double (Given)
   Latitude of point B in radians.


Returned Value
--------------
The result is the bearing (position angle), in radians, of point
A2,B2 as seen from point A1,B1.  It is in the range +/- pi.  If
A2,B2 is due east of A1,B1 the bearing is +pi/2.  Zero is returned
if the two points are coincident.


Notes
-----
- Uses eraPas(). See SOFA/ERFA documentation for details.
     """
     return cpal.palDbear( a1, b1, a2, b2 )

def daf2r( int ideg, int iamin, double asec ):
     """
     ang = daf2r( ideg, iamin, asec )

Convert degrees, arcminutes, arcseconds to radians

Arguments
---------
ideg = int (Given)
   Degrees.
iamin = int (Given)
   Arcminutes.
iasec = double (Given)
   Arcseconds.
rad = double * (Returned)
   Angle in radians.
j = int * (Returned)
   Status: 0 = OK, 1 = "ideg" out of range 0-359,
           2 = "iamin" outside of range 0-59,
           2 = "asec" outside range 0-59.99999


Notes
-----
- Uses eraAf2a(). See SOFA/ERFA documentation for details.

     Raises
     ------
     ValueError if the input arguments are out of range.
     """
     cdef double rad
     cdef int j
     cpal.palDaf2r( ideg, iamin, asec, &rad, &j )
     if j==0:
          return rad
     else:
          bad = ""
          if j==1:
               bad = "Degree argument outside range 0-369"
          elif j==2:
               bad = "Minute argument outside range 0-59"
          else:
               bad = "Arcsec argument outside range 0-59.9999..."
          raise ValueError( bad )

def dcc2s( np.ndarray[double, ndim=1] v not None ):
     """
     (a, b) = dcc2s( v )

Cartesian to spherical coordinates

Arguments
---------
v = double [3] (Given)
   x, y, z vector.
a = double * (Returned)
   Spherical coordinate (radians)
b = double * (Returned)
   Spherical coordinate (radians)


Notes
-----
- Uses eraC2s(). See SOFA/ERFA documentation for details.
     """
     cdef double cv[3]
     for i in range(3):
          cv[i] = v[i]
     cdef double a
     cdef double b
     cpal.palDcc2s( cv, &a, &b )
     return (a, b)

def dcs2c( double a, double b ):
     """
     v = dcs2c( a, b )

Spherical coordinates to direction cosines

Arguments
---------
a = double (Given)
   Spherical coordinate in radians (ra, long etc).
b = double (Given)
   Spherical coordinate in radians (dec, lat etc).
v = double [3] (Returned)
   x, y, z vector


Notes
-----
- Uses eraS2c(). See SOFA/ERFA documentation for details.
     """
     cdef double cv[3]
     cpal.palDcs2c( a, b, cv )
     cdef np.ndarray v = np.zeros( [3], dtype=np.float64 )
     for i in range(3):
          v[i] = cv[i]
     return v

def dd2tf( int ndp, double days ):
     """
     (sign, ih, im, is, frac) = dd2tf( ndp, days )

Convert an interval in days into hours, minutes, seconds

Arguments
---------
ndp = int (Given)
   Number of decimal places of seconds
days = double (Given)
   Interval in days
sign = char * (Returned)
   '+' or '-' (single character, not string)
ihmsf = int [4] (Returned)
   Hours, minutes, seconds, fraction


Notes
-----
- Uses eraD2tf(). See SOFA/ERFA documentation for details.
     """
     cdef char * csign = " "
     cdef int ihmsf[4]
     cpal.palDd2tf( ndp, days, csign, ihmsf )
     sign = csign.decode('UTF-8')
     return ( sign, ihmsf[0], ihmsf[1], ihmsf[2], ihmsf[3] )

def de2h( double ha, double dec, double phi ):
     """
     (az, el) = de2h( ha, dec, phi )

Equatorial to horizon coordinates: HA,Dec to Az,E

Arguments
---------
ha = double * (Given)
   Hour angle (radians)
dec = double * (Given)
   Declination (radians)
phi = double (Given)
   Observatory latitude (radians)
az = double * (Returned)
   Azimuth (radians)
el = double * (Returned)
   Elevation (radians)


Notes
-----
- All the arguments are angles in radians.
- Azimuth is returned in the range 0-2pi;  north is zero,
  and east is +pi/2.  Elevation is returned in the range
  +/-pi/2.
- The latitude must be geodetic.  In critical applications,
  corrections for polar motion should be applied.
- In some applications it will be important to specify the
  correct type of hour angle and declination in order to
  produce the required type of azimuth and elevation.  In
  particular, it may be important to distinguish between
  elevation as affected by refraction, which would
  require the "observed" HA,Dec, and the elevation
  in vacuo, which would require the "topocentric" HA,Dec.
  If the effects of diurnal aberration can be neglected, the
  "apparent" HA,Dec may be used instead of the topocentric
  HA,Dec.
- No range checking of arguments is carried out.
- In applications which involve many such calculations, rather
  than calling the present routine it will be more efficient to
  use inline code, having previously computed fixed terms such
  as sine and cosine of latitude, and (for tracking a star)
  sine and cosine of declination.
     """
     cdef double az
     cdef double el
     cpal.palDe2h( ha, dec, phi, &az, &el )
     return (az, el)

def de2hVector( np.ndarray ha, np.ndarray dec, double phi ):
     """
     This isjust de2h, except that it accepts a vector of inputs
     and returns a vector of outputs
     """
     cdef int i
     cdef int length=len(ha)
     cdef np.ndarray azout = np.zeros(length,dtype=np.float64)
     cdef np.ndarray elout = np.zeros(length,dtype=np.float64)
     cdef double az
     cdef double el
     for i in range(length):
          cpal.palDe2h( ha[i], dec[i], phi, &az, &el )
          azout[i]=az
          elout[i]=el
     return (azout, elout)



def deuler( order, double phi, double theta, double psi ):
    """
    rmat = deuler( order, phi, theta, psi )

Form a rotation matrix from the Euler angles

Arguments
---------
order = const char[] (Given)
   Specifies about which axes the rotation occurs
phi = double (Given)
   1st rotation (radians)
theta = double (Given)
   2nd rotation (radians)
psi = double (Given)
   3rd rotation (radians)
rmat = double[3][3] (Given & Returned)
   Rotation matrix
    """
    cdef double c_rmat[3][3]
    byte_order = order.encode('ascii')
    cdef char * c_order = byte_order
    cpal.palDeuler( c_order, phi, theta, psi, c_rmat )
    cdef np.ndarray rmat = np.zeros([3,3], dtype=np.float64)
    for i in range(3):
        for j in range(3):
            rmat[i][j] = c_rmat[i][j]
    return rmat

# dfltin() not implemented -- not necessary for python

def dh2e( double az, double el, double phi ):
     """
     (ha, dec) = dh2e( az, el, phi )

Horizon to equatorial coordinates: Az,El to HA,Dec

Arguments
---------
az = double (Given)
   Azimuth (radians)
el = double (Given)
   Elevation (radians)
phi = double (Given)
   Observatory latitude (radians)
ha = double * (Returned)
   Hour angle (radians)
dec = double * (Returned)
   Declination (radians)


Notes
-----
- All the arguments are angles in radians.
- The sign convention for azimuth is north zero, east +pi/2.
- HA is returned in the range +/-pi.  Declination is returned
  in the range +/-pi/2.
- The latitude is (in principle) geodetic.  In critical
  applications, corrections for polar motion should be applied.
- In some applications it will be important to specify the
  correct type of elevation in order to produce the required
  type of HA,Dec.  In particular, it may be important to
  distinguish between the elevation as affected by refraction,
  which will yield the "observed" HA,Dec, and the elevation
  in vacuo, which will yield the "topocentric" HA,Dec.  If the
  effects of diurnal aberration can be neglected, the
  topocentric HA,Dec may be used as an approximation to the
  "apparent" HA,Dec.
- No range checking of arguments is done.
- In applications which involve many such calculations, rather
  than calling the present routine it will be more efficient to
  use inline code, having previously computed fixed terms such
  as sine and cosine of latitude.
     """
     cdef double ha
     cdef double dec
     cpal.palDh2e( az, el, phi, &ha, &dec )
     return (ha, dec)

def dimxv( np.ndarray[double, ndim=2] dm not None, np.ndarray[double, ndim=1] va not None):
     """
     vb = dimxv( dm, va )

Perform the 3-D backward unitary transformation

Arguments
---------
dm = double [3][3] (Given)
   Matrix
va = double [3] (Given)
   vector
vb = double [3] (Returned)
   Result vector


Notes
-----
- Uses eraTrxp(). See SOFA/ERFA documentation for details.
     """
     cdef double c_dm[3][3]
     cdef double c_va[3]
     cdef double c_vb[3]
     for i in range(3):
          for j in range(3):
                c_dm[i][j] = dm[i][j]
          c_va[i] = va[i]
     cpal.palDimxv(c_dm, c_va, c_vb)

     cdef np.ndarray vb = np.zeros([3], dtype=np.float64)
     for i in range(3):
          vb[i] = c_vb[i]
     return vb

def djcal( int ndp, double djm ):
     """
     (iy, im, id, frac) = djcal( ndp, djm )

Modified Julian Date to Gregorian Calendar

Arguments
---------
ndp = int (Given)
   Number of decimal places of days in fraction.
djm = double (Given)
   Modified Julian Date (JD-2400000.5)
iymdf[4] = int[] (Returned)
  Year, month, day, fraction in Gregorian calendar.
j = status (Returned)
  0 = OK. See eraJd2cal for other values.


Notes
-----
- Uses eraJd2cal

     Raises
     ------
     ValueError for unacceptable dates.
     """
     cdef int iymdf[4]
     cdef int j
     cpal.palDjcal( ndp, djm, iymdf, &j )
     if j==0:
          return ( iymdf[0], iymdf[1], iymdf[2], iymdf[3] )
     else:
          raise ValueError( "Unacceptable date" )

def djcl( double djm ):
     """
     (iy, im, id, frac) = djcl( djm )

Modified Julian Date to Gregorian year, month, day and fraction of day

Arguments
---------
djm = double (Given)
   modified Julian Date (JD-2400000.5)
iy = int * (Returned)
   year
im = int * (Returned)
   month
id = int * (Returned)
   day
fd = double * (Returned)
   Fraction of day.


Notes
-----
- Uses eraJd2cal(). See SOFA/ERFA documentation for details.

     Raises
     ------
     ValueError for unacceptable date.
     """
     cdef int iy
     cdef int im
     cdef int id
     cdef double fd
     cdef int j
     cpal.palDjcl( djm, &iy, &im, &id, &fd, &j )
     if j==0:
          return ( iy, im, id, fd )
     else:
          raise ValueError( "Unacceptable date" )

def dmat( np.ndarray[double, ndim=2] a not None,
          np.ndarray[double, ndim=1] y not None ):
     """
     (na, ny, d) = dmat( a, y )

Matrix inversion & solution of simultaneous equations

Arguments
---------
n = int (Given)
   Number of simultaneous equations and number of unknowns.
a = double[] (Given & Returned)
   A non-singular NxN matrix (implemented as a contiguous block
   of memory). After calling this routine "a" contains the
   inverse of the matrix.
y = double[] (Given & Returned)
   On input the vector of N knowns. On exit this vector contains the
   N solutions.
d = double * (Returned)
   The determinant.
jf = int * (Returned)
   The singularity flag.  If the matrix is non-singular, jf=0
   is returned.  If the matrix is singular, jf=-1 & d=0.0 are
   returned.  In the latter case, the contents of array "a" on
   return are undefined.
iw = int[] (Given)
   Integer workspace of size N.


Notes
-----
- Implemented using Gaussian elimination with partial pivoting.
- Optimized for speed rather than accuracy with errors 1 to 4
  times those of routines optimized for accuracy.

     Raises
     ------
     MemoryError: Unable to get workspace

     ArithmeticError: Singular matrix

     ValueError: Shapes of input matrices incompatible
     """
     # validate the arguments and get the dimension
     ashape = a.shape
     yshape = y.shape
     if ashape[0] != ashape[1]:
          raise ValueError( "Matrix must be square" )
     if yshape[0] != ashape[0]:
          raise ValueError( "Matrix must match number of elements in supplied vector" )

     cdef int n = y.size
     cdef int j
     cdef double d
     cdef int *iw = <int *>malloc( n * sizeof(int) )
     cdef double *ca = <double *>malloc( n * n * sizeof(double))
     cdef double *cy = <double *>malloc( n * sizeof(double))

     if not ca or not iw or not cy:
          if ca:
               free(ca)
          if iw:
               free(iw)
          if cy:
               free(cy)
          raise MemoryError( "Could not get dynamic memory for matrix" )

     # Need to flatten the input 2d matrix
     k = 0;
     for i in range(n):
          cy[i] = y[i]
          for j in range(n):
               ca[k] = a[ i, j ]
               k = k + 1

     cpal.palDmat( n, ca, cy, &d, &j, iw )
     free(iw)

     cdef np.ndarray na = np.zeros( [n,n], dtype=np.float64 )
     cdef np.ndarray ny = np.zeros( [n], dtype=np.float64 )

     if j==0:
          k = 0
          for i in range(n):
               ny[i] = cy[i]
               for j in range(n):
                    na[i,j] = ca[k]
                    k = k + 1
          free(ca)
          free(cy)
          return ( na, ny, d )
     else:
          free(ca)
          free(cy)
          raise ArithmeticError( "Matrix is singular" )

def dmoon( double date ):
     """
     pv = dmoon( date )

Approximate geocentric position and velocity of the Moon

Arguments
---------
date = double (Given)
   TDB as a Modified Julian Date (JD-2400000.5)
pv = double [6] (Returned)
   Moon x,y,z,xdot,ydot,zdot, mean equator and
   equinox of date (AU, AU/s)


Notes
-----
- Meeus quotes accuracies of 10 arcsec in longitude, 3 arcsec in
  latitude and 0.2 arcsec in HP (equivalent to about 20 km in
  distance).  Comparison with JPL DE200 over the interval
  1960-2025 gives RMS errors of 3.7 arcsec and 83 mas/hour in
  longitude, 2.3 arcsec and 48 mas/hour in latitude, 11 km
  and 81 mm/s in distance.  The maximum errors over the same
  interval are 18 arcsec and 0.50 arcsec/hour in longitude,
  11 arcsec and 0.24 arcsec/hour in latitude, 40 km and 0.29 m/s
  in distance.
- The original algorithm is expressed in terms of the obsolete
  timescale Ephemeris Time.  Either TDB or TT can be used, but
  not UT without incurring significant errors (30 arcsec at
  the present time) due to the Moon's 0.5 arcsec/sec movement.
- The algorithm is based on pre IAU 1976 standards.  However,
  the result has been moved onto the new (FK5) equinox, an
  adjustment which is in any case much smaller than the
  intrinsic accuracy of the procedure.
- Velocity is obtained by a complete analytical differentiation
  of the Meeus model.
     """
     cdef double cpv[6]
     cpal.palDmoon( date, cpv )
     cdef np.ndarray pv = np.zeros( [6], dtype=np.float64 )
     for i in range(6):
          pv[i] = cpv[i]
     return pv

def dmxm(np.ndarray[double, ndim=2] a not None, np.ndarray[double, ndim=2] b not None):
    """
    c = dmxm( a, b )

Product of two 3x3 matrices

Arguments
---------
a = double [3][3] (Given)
   Matrix
b = double [3][3] (Given)
   Matrix
c = double [3][3] (Returned)
   Matrix result


Notes
-----
- Uses eraRxr(). See SOFA/ERFA documentation for details.
    """
    cdef double c_a[3][3]
    cdef double c_b[3][3]
    cdef double c_c[3][3]
    for i in range(3):
        for j in range(3):
            c_a[i][j] = a[i][j]
            c_b[i][j] = b[i][j]
    cpal.palDmxm(c_a, c_b, c_c)

    cdef np.ndarray c = np.zeros([3,3], dtype=np.float64)
    for i in range(3):
        for j in range(3):
            c[i][j] = c_c[i][j]
    return c

def dmxv(np.ndarray[double, ndim=2] dm not None, np.ndarray[double, ndim=1] va not None):
     """
     vb = dmxv( dm, va )

Performs the 3-D forward unitary transformation

Arguments
---------
dm = double [3][3] (Given)
   matrix
va = double [3] (Given)
   vector
dp = double [3] (Returned)
   result vector


Notes
-----
- Uses eraRxp(). See SOFA/ERFA documentation for details.
     """
     cdef double c_dm[3][3]
     cdef double c_va[3]
     cdef double c_vb[3]
     for i in range(3):
          for j in range(3):
                c_dm[i][j] = dm[i][j]
          c_va[i] = va[i]
     cpal.palDmxv(c_dm, c_va, c_vb)

     cdef np.ndarray vb = np.zeros([3], dtype=np.float64)
     for i in range(3):
          vb[i] = c_vb[i]
     return vb

def dm2av(np.ndarray[double, ndim=2] rmat not None):
    """
    axvec = dm2av( rmat )

From a rotation matrix, determine the corresponding axial vector

Arguments
---------
rmat = double [3][3] (Given)
   Rotation matrix
axvec = double [3] (Returned)
   Axial vector (radians)


Notes
-----
- Uses eraRm2v(). See SOFA/ERFA documentation for details.
    """
    cdef double c_rmat[3][3]
    cdef double c_axvec[3]
    for i in range(3):
        for j in range(3):
            c_rmat[i][j] = rmat[i][j]
    cpal.palDm2av( c_rmat, c_axvec )

    cdef np.ndarray axvec = np.zeros([3], dtype=np.float64)
    for i in range(3):
        axvec[i] = c_axvec[i]
    return axvec

def dpav( np.ndarray[double, ndim=1] v1 not None, np.ndarray[double, ndim=1] v2 not None ):
     """
     pa = dpav( v1, v2 )

Position angle of one celestial direction with respect to another

Arguments
---------
v1 = double [3] (Given)
   direction cosines of one point.
v2 = double [3] (Given)
   direction cosines of the other point.


Returned Value
--------------
The result is the bearing (position angle), in radians, of point
V2 with respect to point V1.  It is in the range +/- pi.  The
sense is such that if V2 is a small distance east of V1, the
bearing is about +pi/2.  Zero is returned if the two points
are coincident.


Notes
-----
- The coordinate frames correspond to RA,Dec, Long,Lat etc.
- Uses eraPap(). See SOFA/ERFA documentation for details.
     """
     cdef double cv1[3]
     cdef double cv2[3]
     cdef double result
     for i in range(3):
          cv1[i] = v1[i]
          cv2[i] = v2[i]
     result = cpal.palDpav( cv1, cv2 )
     return result

def dr2af( int ndp, double days ):
     """
     (sign, id, im, is, frac) = dr2af( ndp, days )
Convert an angle in radians to degrees, arcminutes, arcseconds

Arguments
---------
ndp = int (Given)
   number of decimal places of arcseconds
angle = double (Given)
   angle in radians
sign = char * (Returned)
   '+' or '-' (single character)
idmsf = int [4] (Returned)
   Degrees, arcminutes, arcseconds, fraction


Notes
-----
- Uses eraA2af(). See SOFA/ERFA documentation for details.
     """
     cdef char * csign = " "
     cdef int idmsf[4]
     cpal.palDr2af( ndp, days, csign, idmsf )
     sign = csign.decode('UTF-8')
     return ( sign, idmsf[0], idmsf[1], idmsf[2], idmsf[3] )

def drange( double angle ):
     """
     a = drange( angle )

Normalize angle into range +/- pi

Arguments
---------
angle = double (Given)
   The angle in radians.
     """
     return cpal.palDrange( angle )

def dranrm( double angle ):
     """
     a = dranrm( angle )

Normalize angle into range 0-2 pi

Arguments
---------
angle = double (Given)
   angle in radians


Returned Value
--------------
Angle expressed in the range 0-2 pi


Notes
-----
- Uses eraAnp(). See SOFA/ERFA documentation for details.
     """
     return cpal.palDranrm( angle )

def ds2tp( double ra, double dec, double raz, double decz ):
     """
     (xi, eta) = ds2tp( ra, dec, raz, decz )

Spherical to tangent plane projection

Arguments
---------
ra = double (Given)
   RA spherical coordinate of point to be projected (radians)
dec = double (Given)
   Dec spherical coordinate of point to be projected (radians)
raz = double (Given)
   RA spherical coordinate of tangent point (radians)
decz = double (Given)
   Dec spherical coordinate of tangent point (radians)
xi = double * (Returned)
   First rectangular coordinate on tangent plane (radians)
eta = double * (Returned)
   Second rectangular coordinate on tangent plane (radians)
j = int * (Returned)
   status: 0 = OK, star on tangent plane
           1 = error, star too far from axis
           2 = error, antistar on tangent plane
           3 = error, antistar too far from axis

     Raises
     ------
     ValueError: Bad input arguments
     """
     cdef double xi
     cdef double eta
     cdef int j
     cpal.palDs2tp( ra, dec, raz, decz, &xi, &eta, &j )
     if j==0:
          return (xi, eta)
     elif j==1:
          raise ValueError( "Star too far from axis" )
     elif j==2:
          raise ValueError( "Antistar on tangent plane" )
     else:
          raise ValueError( "Antistart too far from axis" )

def ds2tpVector( np.ndarray ra, np.ndarray dec, double raz, double decz ):
     """
     This is just ds2tp, except that it takes an array of ra and array
     of dec and calculates xi and eta for each relative to the scalar
     raz and decz
     """
     cdef int i
     cdef int j
     cdef int length=len(ra)
     cdef double xi
     cdef double eta
     cdef np.ndarray xiout=np.zeros(length,dtype=np.float64)
     cdef np.ndarray etaout=np.zeros(length,dtype=np.float64)

     for i in range(length):
          cpal.palDs2tp( ra[i], dec[i], raz, decz, &xi, &eta, &j )
          if j==0:
               xiout[i] = xi
               etaout[i] = eta
          elif j==1:
               raise ValueError( "Star too far from axis" )
          elif j==2:
               raise ValueError( "Antistar on tangent plane" )
          else:
               raise ValueError( "Antistart too far from axis" )

     return xiout, etaout

def dsep( double a1, double b1, double a2, double b2 ):
     """
     s = dsep( a1, b1, a2, b2 )

Angle between two points on a sphere

Arguments
---------
a1 = double (Given)
   Spherical coordinate of one point (radians)
b1 = double (Given)
   Spherical coordinate of one point (radians)
a2 = double (Given)
   Spherical coordinate of other point (radians)
b2 = double (Given)
   Spherical coordinate of other point (radians)


Returned Value
--------------
Angle, in radians, between the two points. Always positive.


Notes
-----
- The spherical coordinates are [RA,Dec], [Long,Lat] etc, in radians.
- Uses eraSeps(). See SOFA/ERFA documentation for details.
     """
     return cpal.palDsep( a1, b1, a2, b2 )

def dsepv( np.ndarray[double, ndim=1] v1 not None, np.ndarray[double, ndim=1] v2 not None ):
     """
     s = dsepv( v1, v2 )

Angle between two vectors

Arguments
---------
v1 = double [3] (Given)
   First vector
v2 = double [3] (Given)
   Second vector


Returned Value
--------------
Angle, in radians, between the two points. Always positive.


Notes
-----
- Uses eraSepp(). See SOFA/ERFA documentation for details.
     """
     cdef double cv1[3]
     cdef double cv2[3]
     cdef double result
     for i in range(3):
          cv1[i] = v1[i]
          cv2[i] = v2[i]
     result = cpal.palDsepv( cv1, cv2 )
     return result

def dt( double epoch ):
     """
     d = dt( epoch )

Estimate the offset between dynamical time and UT

Arguments
---------
epoch = double (Given)
   Julian epoch (e.g. 1850.0)


Returned Value
--------------
palDt = double
   Rough estimate of ET-UT (after 1984, TT-UT) at the
   given epoch, in seconds.


Notes
-----
- Depending on the epoch, one of three parabolic approximations
  is used:

    before 979    Stephenson & Morrison's 390 BC to AD 948 model
    979 to 1708   Stephenson & Morrison's 948 to 1600 model
    after 1708    McCarthy & Babcock's post-1650 model

  The breakpoints are chosen to ensure continuity:  they occur
  at places where the adjacent models give the same answer as
  each other.
- The accuracy is modest, with errors of up to 20 sec during
  the interval since 1650, rising to perhaps 30 min by 1000 BC.
  Comparatively accurate values from AD 1600 are tabulated in
  the Astronomical Almanac (see section K8 of the 1995 AA).
- The use of double-precision for both argument and result is
  purely for compatibility with other SLALIB time routines.
- The models used are based on a lunar tidal acceleration value
  of -26.00 arcsec per century.

     """
     return cpal.palDt( epoch )

def dtf2d( int ihour, int imin, double sec ):
     """
     days = dtf2d( ihour, imin, sec )

Convert hours, minutes, seconds to days

Arguments
---------
ihour = int (Given)
   Hours
imin = int (Given)
   Minutes
sec = double (Given)
   Seconds
days = double * (Returned)
   Interval in days
j = int * (Returned)
   status: 0 = ok, 1 = ihour outside range 0-23,
   2 = imin outside range 0-59, 3 = sec outside range 0-59.999...


Notes
-----
- Uses eraTf2d(). See SOFA/ERFA documentation for details.

     Raises
     ------
     ValueError: Arguments out of range.
     """
     cdef double days
     cdef int j
     cpal.palDtf2d( ihour, imin, sec, &days, &j )
     if j==0:
          return days
     else:
          bad = ""
          if j==1:
               bad = "Degree argument outside range 0-369"
          elif j==2:
               bad = "Minute argument outside range 0-59"
          else:
               bad = "Arcsec argument outside range 0-59.9999..."
          raise ValueError( bad )

def dtf2r( int ihour, int imin, double sec ):
     """
     rad = dtf2r( ihour, imin, sec )

Convert hours, minutes, seconds to radians

Arguments
---------
ihour = int (Given)
   Hours
imin = int (Given)
   Minutes
sec = double (Given)
   Seconds
days = double * (Returned)
   Angle in radians
j = int * (Returned)
   status: 0 = ok, 1 = ihour outside range 0-23,
   2 = imin outside range 0-59, 3 = sec outside range 0-59.999...


Notes
-----
- Uses eraTf2a(). See SOFA/ERFA documentation for details.

     Raises
     ------
     ValueError: Arguments out of range.
     """
     cdef double rad
     cdef int j
     cpal.palDtf2r( ihour, imin, sec, &rad, &j )
     if j==0:
          return rad
     else:
          bad = ""
          if j==1:
               bad = "Degree argument outside range 0-369"
          elif j==2:
               bad = "Minute argument outside range 0-59"
          else:
               bad = "Arcsec argument outside range 0-59.9999..."
          raise ValueError( bad )

def dtp2s( double xi, double eta, double raz, double decz):
     """
     (ra,dec) = dtp2s( xi, eta, raz, decz )

Tangent plane to spherical coordinates

Arguments
---------
xi = double (Given)
   First rectangular coordinate on tangent plane (radians)
eta = double (Given)
   Second rectangular coordinate on tangent plane (radians)
raz = double (Given)
   RA spherical coordinate of tangent point (radians)
decz = double (Given)
   Dec spherical coordinate of tangent point (radians)
ra = double * (Returned)
   RA spherical coordinate of point to be projected (radians)
dec = double * (Returned)
   Dec spherical coordinate of point to be projected (radians)
     """
     cdef double ra
     cdef double dec
     cpal.palDtp2s( xi, eta, raz, decz, &ra, &dec )
     return (ra,dec)

def dtps2c( double xi, double eta, double ra, double dec ):
     """
     (raz1, decz1, raz2, decz2) = dtps2c( xi, eta, ra, dec )

Determine RA,Dec of tangent point from coordinates

Arguments
---------
xi = double (Given)
   First rectangular coordinate on tangent plane (radians)
eta = double (Given)
   Second rectangular coordinate on tangent plane (radians)
ra = double (Given)
   RA spherical coordinate of star (radians)
dec = double (Given)
   Dec spherical coordinate of star (radians)
raz1 = double * (Returned)
   RA spherical coordinate of tangent point, solution 1 (radians)
decz1 = double * (Returned)
   Dec spherical coordinate of tangent point, solution 1 (radians)
raz2 = double * (Returned)
   RA spherical coordinate of tangent point, solution 2 (radians)
decz2 = double * (Returned)
   Dec spherical coordinate of tangent point, solution 2 (radians)
n = int * (Returned)
   number of solutions: 0 = no solutions returned (note 2)
                        1 = only the first solution is useful (note 3)
                        2 = both solutions are useful (note 3)


Notes
-----
- The RAZ1 and RAZ2 values are returned in the range 0-2pi.
- Cases where there is no solution can only arise near the poles.
  For example, it is clearly impossible for a star at the pole
  itself to have a non-zero XI value, and hence it is
  meaningless to ask where the tangent point would have to be
  to bring about this combination of XI and DEC.
- Also near the poles, cases can arise where there are two useful
  solutions.  The argument N indicates whether the second of the
  two solutions returned is useful.  N=1 indicates only one useful
  solution, the usual case;  under these circumstances, the second
  solution corresponds to the "over-the-pole" case, and this is
  reflected in the values of RAZ2 and DECZ2 which are returned.
- The DECZ1 and DECZ2 values are returned in the range +/-pi, but
  in the usual, non-pole-crossing, case, the range is +/-pi/2.
- This routine is the spherical equivalent of the routine sla_DTPV2C.

     Python notes
     ------------
     If some solutions are missing None is returned for each value.
     """
     cdef double raz1
     cdef double decz1
     cdef double raz2
     cdef double decz2
     cdef int n
     cpal.palDtps2c( xi, eta, ra, dec, &raz1, &decz1, &raz2, &decz2, &n )
     if n==0:
          return (None, None, None, None)
     elif n==1:
          return (raz1, decz1, None, None)
     else:
          return (raz1, decz1, raz2, decz2 )

def dtt( double dju ):
     """
     d = dtt( dju )

Return offset between UTC and TT

Arguments
---------
utc = double (Given)
   UTC date as a modified JD (JD-2400000.5)


Returned Value
--------------
dtt = double
   TT-UTC in seconds


Notes
-----
- Consider a comprehensive upgrade to use the time transformations in SOFA's time
  cookbook:  http://www.iausofa.org/sofa_ts_c.pdf.
- See eraDat for a description of error conditions when calling this function
  with a time outside of the UTC range. This behaviour differs from slaDtt.
     """
     return cpal.palDtt( dju )

def dvn( np.ndarray[double, ndim=1] v not None):
    """
    (uv, vm) = dvn( v )

Normalizes a 3-vector also giving the modulus

Arguments
---------
v = double [3] (Given)
   vector
uv = double [3] (Returned)
   unit vector in direction of "v"
vm = double * (Returned)
   modulus of "v"


Notes
-----
- Uses eraPn(). See SOFA/ERFA documentation for details.
    """
    cdef double c_v[3]
    cdef double c_uv[3]
    cdef double vm
    for i in range(3):
        c_v[i] = v[i]
    cpal.palDvn( c_v, c_uv, &vm )

    cdef np.ndarray uv = np.zeros([3], dtype=np.float64)
    for i in range(3):
        uv[i] = c_uv[i]
    return (uv, vm)

def dvxv( np.ndarray[double, ndim=1] va not None, np.ndarray[double, ndim=1] vb not None):
    """
    vc = dvxv( va, vb )

Vector product of two 3-vectors

Arguments
---------
va = double [3] (Given)
   First vector
vb = double [3] (Given)
   Second vector
vc = double [3] (Returned)
   Result vector


Notes
-----
- Uses eraPxp(). See SOFA/ERFA documentation for details.
    """
    cdef double c_va[3]
    cdef double c_vb[3]
    cdef double c_vc[3]
    for i in range(3):
        c_va[i] = va[i]
        c_vb[i] = vb[i]
    cpal.palDvxv( c_va, c_vb, c_vc )

    cdef np.ndarray vc = np.zeros([3], dtype=np.float64)
    for i in range(3):
        vc[i] = c_vc[i]
    return vc

def ecleq( double dl, double db, double date ):
     """
     (dr, dd) = eqecl( dl, db, date )

Transform from ecliptic coordinates to J2000.0 equatorial coordinates

Arguments
---------
dl = double (Given)
   Ecliptic longitude (mean of date, IAU 1980 theory, radians)
db = double (Given)
   Ecliptic latitude (mean of date, IAU 1980 theory, radians)
date = double (Given)
   TT as Modified Julian Date (JD-2400000.5). The difference
   between TT and TDB is of the order of a millisecond or two
   (i.e. about 0.02 arc-seconds).
dr = double * (Returned)
   J2000.0 mean RA (radians)
dd = double * (Returned)
   J2000.0 mean Dec (Radians)
     """
     cdef double dr
     cdef double dd
     cpal.palEcleq( dl, db, date, &dr, &dd )
     return (dr, dd)

def ecmat( double date ):
     """
     rmat = ecmat( date )

Form the equatorial to ecliptic rotation matrix - IAU 2006
precession model.

Arguments
---------
date = double (Given)
   TT as Modified Julian Date (JD-2400000.5). The difference
   between TT and TDB is of the order of a millisecond or two
   (i.e. about 0.02 arc-seconds).
rmat = double[3][3] (Returned)
   Rotation matrix
     """
     cdef double crmat[3][3]
     cpal.palEcmat( date, crmat )
     cdef np.ndarray rmat = np.zeros( [3,3], dtype=np.float64 )
     for i in range(3):
          for j in range(3):
               rmat[i,j] = crmat[i][j]
     return rmat

def el2ue( double date, int jform, double epoch, double orbinc,
            double anode, double perih, double aorq,  double e,
            double aorl, double dm ):
    """
    u = el2ue( date, jform, epoch, orbinc, anode, perih, aorq, e, aorl, dm )

Transform conventional elements into "universal" form

Arguments
---------
date = double (Given)
   Epoch (TT MJD) of osculation (Note 3)
jform = int (Given)
   Element set actually returned (1-3; Note 6)
epoch = double (Given)
   Epoch of elements (TT MJD)
orbinc = double (Given)
   inclination (radians)
anode = double (Given)
   longitude of the ascending node (radians)
perih = double (Given)
   longitude or argument of perihelion (radians)
aorq = double (Given)
   mean distance or perihelion distance (AU)
e = double (Given)
   eccentricity
aorl = double (Given)
   mean anomaly or longitude (radians, JFORM=1,2 only)
dm = double (Given)
   daily motion (radians, JFORM=1 only)
u = double [13] (Returned)
   Universal orbital elements (Note 1)
     -   (0)  combined mass (M+m)
     -   (1)  total energy of the orbit (alpha)
     -   (2)  reference (osculating) epoch (t0)
     - (3-5)  position at reference epoch (r0)
     - (6-8)  velocity at reference epoch (v0)
     -   (9)  heliocentric distance at reference epoch
     -  (10)  r0.v0
     -  (11)  date (t)
     -  (12)  universal eccentric anomaly (psi) of date, approx
jstat = int * (Returned)
   status:  0 = OK
         - -1 = illegal JFORM
         - -2 = illegal E
         - -3 = illegal AORQ
         - -4 = illegal DM
         - -5 = numerical error


Notes
-----
- The "universal" elements are those which define the orbit for the
  purposes of the method of universal variables (see reference).
  They consist of the combined mass of the two bodies, an epoch,
  and the position and velocity vectors (arbitrary reference frame)
  at that epoch.  The parameter set used here includes also various
  quantities that can, in fact, be derived from the other
  information.  This approach is taken to avoiding unnecessary
  computation and loss of accuracy.  The supplementary quantities
  are (i) alpha, which is proportional to the total energy of the
  orbit, (ii) the heliocentric distance at epoch, (iii) the
  outwards component of the velocity at the given epoch, (iv) an
  estimate of psi, the "universal eccentric anomaly" at a given
  date and (v) that date.
- The companion routine is palUe2pv.  This takes the set of numbers
  that the present routine outputs and uses them to derive the
  object's position and velocity.  A single prediction requires one
  call to the present routine followed by one call to palUe2pv;
  for convenience, the two calls are packaged as the routine
  palPlanel.  Multiple predictions may be made by again calling the
  present routine once, but then calling palUe2pv multiple times,
  which is faster than multiple calls to palPlanel.
- DATE is the epoch of osculation.  It is in the TT timescale
  (formerly Ephemeris Time, ET) and is a Modified Julian Date
  (JD-2400000.5).
- The supplied orbital elements are with respect to the J2000
  ecliptic and equinox.  The position and velocity parameters
  returned in the array U are with respect to the mean equator and
  equinox of epoch J2000, and are for the perihelion prior to the
  specified epoch.
- The universal elements returned in the array U are in canonical
  units (solar masses, AU and canonical days).
- Three different element-format options are available:

  Option JFORM=1, suitable for the major planets:

  EPOCH  = epoch of elements (TT MJD)
  ORBINC = inclination i (radians)
  ANODE  = longitude of the ascending node, big omega (radians)
  PERIH  = longitude of perihelion, curly pi (radians)
  AORQ   = mean distance, a (AU)
  E      = eccentricity, e (range 0 to <1)
  AORL   = mean longitude L (radians)
  DM     = daily motion (radians)

  Option JFORM=2, suitable for minor planets:

  EPOCH  = epoch of elements (TT MJD)
  ORBINC = inclination i (radians)
  ANODE  = longitude of the ascending node, big omega (radians)
  PERIH  = argument of perihelion, little omega (radians)
  AORQ   = mean distance, a (AU)
  E      = eccentricity, e (range 0 to <1)
  AORL   = mean anomaly M (radians)

  Option JFORM=3, suitable for comets:

  EPOCH  = epoch of perihelion (TT MJD)
  ORBINC = inclination i (radians)
  ANODE  = longitude of the ascending node, big omega (radians)
  PERIH  = argument of perihelion, little omega (radians)
  AORQ   = perihelion distance, q (AU)
  E      = eccentricity, e (range 0 to 10)

- Unused elements (DM for JFORM=2, AORL and DM for JFORM=3) are
  not accessed.
- The algorithm was originally adapted from the EPHSLA program of
  D.H.P.Jones (private communication, 1996).  The method is based
  on Stumpff's Universal Variables.


    Raises
    ------
    ValueError: Illegal input arguments
    ArithmeticError: Numerical error
    """
    cdef int jstat
    cdef double cu[13]
    cpal.palEl2ue( date, jform, epoch, orbinc, anode, perih, aorq,
                    e, aorl, dm, cu, &jstat )
    if jstat == -1:
        raise ValueError( "Illegal jform" )
    elif jstat == -2:
        raise ValueError( "Illegal e" )
    elif jstat == -3:
        raise ValueError( "Illegal aorq" )
    elif jstat == -4:
        raise ValueError( "Illegal dm" )
    elif jstat == -5:
        raise ArithmeticError( "Numerical error" )

    cdef np.ndarray u = np.zeros( [13], dtype=np.float64 )
    for i in range(13):
        u[i] = cu[i]
    return u

def epb( double date ):
     """
     e = epb( date )

Conversion of modified Julian Data to Besselian Epoch

Arguments
---------
date = double (Given)
   Modified Julian Date (JD - 2400000.5)


Returned Value
--------------
 Besselian epoch.


Notes
-----
- Uses eraEpb(). See SOFA/ERFA documentation for details.
     """
     return cpal.palEpb(date)

def epb2d( double epb ):
     """
     d = epb2d( epb )

Conversion of Besselian Epoch to Modified Julian Date

Arguments
---------
epb = double (Given)
   Besselian Epoch


Returned Value
--------------
Modified Julian Date (JD - 2400000.5)


Notes
-----
- Uses eraEpb2jd(). See SOFA/ERFA documentation for details.
     """
     return cpal.palEpb2d(epb)

def epco( k0, k, double e ):
     """
     e = epco( k0, k, e )

Convert an epoch into the appropriate form - 'B' or 'J'

Arguments
---------
k0 = char (Given)
  Form of result: 'B'=Besselian, 'J'=Julian
k = char (Given)
  Form of given epoch: 'B' or 'J'.


Notes
-----
- The result is always either equal to or very close to
  the given epoch E.  The routine is required only in
  applications where punctilious treatment of heterogeneous
  mixtures of star positions is necessary.
- k and k0 are case insensitive. This differes slightly from the
  Fortran SLA implementation.
- k and k0 are not validated. They are interpreted as follows:
  o If k0 and k are the same the result is e
  o If k0 is 'b' or 'B' and k isn't the conversion is J to B.
  o In all other cases, the conversion is B to J.
     """
     k0_bytes = k0.encode('ascii')
     k_bytes = k.encode('ascii')
     cdef char * ck0 = k0_bytes
     cdef char * ck = k_bytes
     return cpal.palEpco( ck0[0], ck[0], e )

def epj( double date ):
     """
     e = epj( date )

Conversion of Modified Julian Date to Julian Epoch

Arguments
---------
date = double (Given)
   Modified Julian Date (JD - 2400000.5)


Returned Value
--------------
The Julian Epoch.


Notes
-----
- Uses eraEpj(). See SOFA/ERFA documentation for details.
     """
     return cpal.palEpj(date)

def epj2d( double epj ):
     """
     d = epj2d( epj )

Conversion of Julian Epoch to Modified Julian Date

Arguments
---------
epj = double (Given)
   Julian Epoch.


Returned Value
--------------
Modified Julian Date (JD - 2400000.5)


Notes
-----
- Uses eraEpj2d(). See SOFA/ERFA documentation for details.
     """
     return cpal.palEpj2d(epj)

# epv goes here
def epv( double date ):
    """
    (ph, vh, pb, vb) = epv( date )

Earth position and velocity with respect to the BCRS

Arguments
---------
date = double (Given)
   Date, TDB Modified Julian Date (JD-2400000.5)
ph = double [3] (Returned)
   Heliocentric Earth position (AU)
vh = double [3] (Returned)
   Heliocentric Earth velocity (AU/day)
pb = double [3] (Returned)
   Barycentric Earth position (AU)
vb = double [3] (Returned)
   Barycentric Earth velocity (AU/day)


Notes
-----
- See eraEpv00 for details on accuracy
- Note that the status argument from eraEpv00 is ignored
    """
    cdef double cph[3]
    cdef double cvh[3]
    cdef double cpb[3]
    cdef double cvb[3]
    cpal.palEpv( date, cph, cvh, cpb, cvb )

    cdef np.ndarray ph = np.zeros( [3], dtype=np.float64 )
    cdef np.ndarray vh = np.zeros( [3], dtype=np.float64 )
    cdef np.ndarray pb = np.zeros( [3], dtype=np.float64 )
    cdef np.ndarray vb = np.zeros( [3], dtype=np.float64 )
    for i in range(3):
        ph[i] = cph[i]
        vh[i] = cvh[i]
        pb[i] = cpb[i]
        vb[i] = cvb[i]
    return (ph, vh, pb, vb)

def eqecl( double dr, double dd, double date ):
     """
     (dl, db) = eqecl( dr, dd, date )

Transform from J2000.0 equatorial coordinates to ecliptic coordinates

Arguments
---------
dr = double (Given)
   J2000.0 mean RA (radians)
dd = double (Given)
   J2000.0 mean Dec (Radians)
date = double (Given)
   TT as Modified Julian Date (JD-2400000.5). The difference
   between TT and TDB is of the order of a millisecond or two
   (i.e. about 0.02 arc-seconds).
dl = double * (Returned)
   Ecliptic longitude (mean of date, IAU 1980 theory, radians)
db = double * (Returned)
   Ecliptic latitude (mean of date, IAU 1980 theory, radians)
     """
     cdef double dl
     cdef double db
     cpal.palEqecl( dr, dd, date, &dl, &db )
     return (dl, db)

def eqeqx( double date ):
     """
     eq = eqeqx( date )

Equation of the equinoxes (IAU 2000/2006)

Arguments
---------
date = double (Given)
   TT as Modified Julian Date (JD-400000.5)


Notes
-----
- Uses eraEe06a(). See SOFA/ERFA documentation for details.
     """
     return cpal.palEqeqx( date )

def eqgal( double dr, double dd ):
     """
     (dl, dd) = eqgal( dr, dd )

Convert from J2000.0 equatorial coordinates to Galactic

Arguments
---------
dr = double (Given)
  J2000.0 RA (radians)
dd = double (Given)
  J2000.0 Dec (radians
dl = double * (Returned)
  Galactic longitude (radians).
db = double * (Returned)
  Galactic latitude (radians).


Notes
-----
The equatorial coordinates are J2000.0.  Use the routine
palGe50 if conversion to B1950.0 'FK4' coordinates is
required.
     """
     cdef double dl
     cdef double db
     cpal.palEqgal( dr, dd, &dl, &dd )
     return (dl, dd)

def etrms( double ep ):
     """
     ev = etrms( ep )

Compute the E-terms vector

Arguments
---------
ep = double (Given)
   Besselian epoch
ev = double [3] (Returned)
   E-terms as (dx,dy,dz)
     """
     cdef double cev[3]
     cpal.palEtrms( ep, cev )
     cdef np.ndarray ev = np.zeros( [3], dtype=np.float64 )
     for i in range(3):
          ev[i] = cev[i]
     return ev

def evp(double date, double deqx):
    """
    (dvb, dpb, dvh, dph) = evp( date, deqx )

Returns the barycentric and heliocentric velocity and position of the
Earth.

Arguments
---------
date = double (Given)
   TDB (loosely ET) as a Modified Julian Date (JD-2400000.5)
deqx = double (Given)
   Julian epoch (e.g. 2000.0) of mean equator and equinox of the
   vectors returned.  If deqx <= 0.0, all vectors are referred to the
   mean equator and equinox (FK5) of epoch date.
dvb = double[3] (Returned)
   Barycentric velocity (AU/s, AU)
dpb = double[3] (Returned)
   Barycentric position (AU/s, AU)
dvh = double[3] (Returned)
   heliocentric velocity (AU/s, AU)
dph = double[3] (Returned)
   Heliocentric position (AU/s, AU)
    """
    cdef double cdvb[3]
    cdef double cdpb[3]
    cdef double cdvh[3]
    cdef double cdph[3]
    cpal.palEvp( date, deqx, cdvb, cdpb, cdvh, cdph )

    cdef np.ndarray dvb = np.zeros( [3], dtype=np.float64 )
    cdef np.ndarray dpb = np.zeros( [3], dtype=np.float64 )
    cdef np.ndarray dvh = np.zeros( [3], dtype=np.float64 )
    cdef np.ndarray dph = np.zeros( [3], dtype=np.float64 )
    for i in range(3):
        dvb[i] = cdvb[i]
        dpb[i] = cdpb[i]
        dvh[i] = cdvh[i]
        dph[i] = cdph[i]
    return (dvb, dpb, dvh, dph)

def fk45z( double r1950, double d1950, double bepoch ):
     """
     (r2000, d2000) = fk45z( r1950, d1950, bepoch )

Convert B1950.0 FK4 star data to J2000.0 FK5 assuming zero
proper motion in the FK5 frame

Arguments
---------
r1950 = double (Given)
   B1950.0 FK4 RA at epoch (radians).
d1950 = double (Given)
   B1950.0 FK4 Dec at epoch (radians).
bepoch = double (Given)
   Besselian epoch (e.g. 1979.3)
r2000 = double (Returned)
   J2000.0 FK5 RA (Radians).
d2000 = double (Returned)
   J2000.0 FK5 Dec(Radians).


Notes
-----
- The epoch BEPOCH is strictly speaking Besselian, but if a
Julian epoch is supplied the result will be affected only to
a negligible extent.

- Conversion from Besselian epoch 1950.0 to Julian epoch 2000.0
only is provided for.  Conversions involving other epochs will
require use of the appropriate precession, proper motion, and
E-terms routines before and/or after palFk45z is called.

- In the FK4 catalogue the proper motions of stars within 10
degrees of the poles do not embody the differential E-term effect
and should, strictly speaking, be handled in a different manner
from stars outside these regions. However, given the general lack
of homogeneity of the star data available for routine astrometry,
the difficulties of handling positions that may have been
determined from astrometric fields spanning the polar and non-polar
regions, the likelihood that the differential E-terms effect was not
taken into account when allowing for proper motion in past
astrometry, and the undesirability of a discontinuity in the
algorithm, the decision has been made in this routine to include the
effect of differential E-terms on the proper motions for all stars,
whether polar or not.  At epoch 2000, and measuring on the sky rather
than in terms of dRA, the errors resulting from this simplification
are less than 1 milliarcsecond in position and 1 milliarcsecond per
century in proper motion.

     """
     cdef double r2000
     cdef double d2000
     cpal.palFk45z( r1950, d1950, bepoch, &r2000, &d2000 )
     return (r2000, d2000)

def fk524( double r2000, double d2000, double dr2000,
           double dd2000, double p2000, double v2000 ):
     """
     (r1950, d1950, dr1950, dd1950, p1950, v1950) = fk524( r2000, d2000, dr2000, dd2000, p2000, v2000 )

Convert J2000.0 FK5 star data to B1950.0 FK4.

Arguments
---------
r2000 = double (Given)
   J2000.0 FK5 RA (radians).
d2000 = double (Given)
   J2000.0 FK5 Dec (radians).
dr2000 = double (Given)
   J2000.0 FK5 RA proper motion (rad/Jul.yr)
dd2000 = double (Given)
   J2000.0 FK5 Dec proper motion (rad/Jul.yr)
p2000 = double (Given)
   J2000.0 FK5 parallax (arcsec)
v2000 = double (Given)
    J2000.0 FK5 radial velocity (km/s, +ve = moving away)
r1950 = double * (Returned)
   B1950.0 FK4 RA (radians).
d1950 = double * (Returned)
   B1950.0 FK4 Dec (radians).
dr1950 = double * (Returned)
   B1950.0 FK4 RA proper motion (rad/Jul.yr)
dd1950 = double * (Returned)
   B1950.0 FK4 Dec proper motion (rad/Jul.yr)
p1950 = double * (Returned)
   B1950.0 FK4 parallax (arcsec)
v1950 = double * (Returned)
    B1950.0 FK4 radial velocity (km/s, +ve = moving away)


Notes
-----
- The proper motions in RA are dRA/dt rather than
cos(Dec)*dRA/dt, and are per year rather than per century.
- Note that conversion from Julian epoch 2000.0 to Besselian
epoch 1950.0 only is provided for.  Conversions involving
other epochs will require use of the appropriate precession,
proper motion, and E-terms routines before and/or after
FK524 is called.
- In the FK4 catalogue the proper motions of stars within
10 degrees of the poles do not embody the differential
E-term effect and should, strictly speaking, be handled
in a different manner from stars outside these regions.
However, given the general lack of homogeneity of the star
data available for routine astrometry, the difficulties of
handling positions that may have been determined from
astrometric fields spanning the polar and non-polar regions,
the likelihood that the differential E-terms effect was not
taken into account when allowing for proper motion in past
astrometry, and the undesirability of a discontinuity in
the algorithm, the decision has been made in this routine to
include the effect of differential E-terms on the proper
motions for all stars, whether polar or not.  At epoch 2000,
and measuring on the sky rather than in terms of dRA, the
errors resulting from this simplification are less than
1 milliarcsecond in position and 1 milliarcsecond per
century in proper motion.

     """
     cdef double r1950
     cdef double d1950
     cdef double dr1950
     cdef double dd1950
     cdef double p1950
     cdef double v1950
     cpal.palFk524( r2000, d2000, dr2000, dd2000, p2000, v2000,
                    &r1950, &d1950, &dr1950, &dd1950,
                    &p1950, &v1950 )
     return (r1950, d1950, dr1950, dd1950, p1950, v1950 )

def fk54z(double r2000, double d2000, double bepoch):
     """
     (r1950, d1950, dr1950, dd1950) = fk54z( r2000, d2000, bepoch )

Convert a J2000.0 FK5 star position to B1950.0 FK4 assuming
zero proper motion and parallax.

Arguments
---------
r2000 = double (Given)
   J2000.0 FK5 RA (radians).
d2000 = double (Given)
   J2000.0 FK5 Dec (radians).
bepoch = double (Given)
    Besselian epoch (e.g. 1950.0).
r1950 = double * (Returned)
   B1950 FK4 RA (radians) at epoch "bepoch".
d1950 = double * (Returned)
   B1950 FK4 Dec (radians) at epoch "bepoch".
dr1950 = double * (Returned)
   B1950 FK4 proper motion (RA) (radians/trop.yr)).
dr1950 = double * (Returned)
   B1950 FK4 proper motion (Dec) (radians/trop.yr)).


Notes
-----
- The proper motion in RA is dRA/dt rather than cos(Dec)*dRA/dt.
- Conversion from Julian epoch 2000.0 to Besselian epoch 1950.0
only is provided for.  Conversions involving other epochs will
require use of the appropriate precession functions before and
after this function is called.
- The FK5 proper motions, the parallax and the radial velocity
 are presumed zero.
- It is the intention that FK5 should be a close approximation
to an inertial frame, so that distant objects have zero proper
motion;  such objects have (in general) non-zero proper motion
in FK4, and this function returns those fictitious proper
motions.
- The position returned by this function is in the B1950
reference frame but at Besselian epoch BEPOCH.  For comparison
with catalogues the "bepoch" argument will frequently be 1950.0.
     """
     cdef double r1950
     cdef double d1950
     cdef double dr1950
     cdef double dd1950
     cpal.palFk54z( r2000, d2000, bepoch, &r1950, &d1950,
                    &dr1950, &dd1950 )
     return (r1950, d1950, dr1950, dd1950 )

def fk5hz( double r5, double d5, double epoch):
     """
     (rh, dh) = fk5hz( r5, d5, epoch )

Transform an FK5 (J2000) star position into the frame of the
Hipparcos catalogue.

Arguments
---------
r5 = double (Given)
   FK5 RA (radians), equinox J2000, epoch "epoch"
d5 = double (Given)
   FK5 dec (radians), equinox J2000, epoch "epoch"
epoch = double (Given)
   Julian epoch
rh = double * (Returned)
   RA (radians)
dh = double * (Returned)
   Dec (radians)


Notes
-----
- Assumes zero Hipparcos proper motion.
- Uses eraEpj2jd() and eraFk5hz.
  See SOFA/ERFA documentation for details.
     """
     cdef double rh
     cdef double dh
     cpal.palFk5hz( r5, d5, epoch, &rh, &dh )
     return (rh, dh)

def galeq( double dl, double db ):
     """
     (dr, dd) = galeq( dl, db )

Convert from galactic to J2000.0 equatorial coordinates

Arguments
---------
dl = double (Given)
  Galactic longitude (radians).
db = double (Given)
  Galactic latitude (radians).
dr = double * (Returned)
  J2000.0 RA (radians)
dd = double * (Returned)
  J2000.0 Dec (radians)


Notes
-----
The equatorial coordinates are J2000.0.  Use the routine
palGe50 if conversion to B1950.0 'FK4' coordinates is
required.
     """
     cdef double dr
     cdef double dd
     cpal.palGaleq( dl, db, &dr, &dd )
     return (dr, dd)

def galsup( double dl, double db ):
     """
     (dsl, dsb) = galsup( dl, db )

Convert from galactic to supergalactic coordinates

Arguments
---------
dl = double (Given)
  Galactic longitude.
db = double (Given)
  Galactic latitude.
dsl = double * (Returned)
  Supergalactic longitude.
dsb = double * (Returned)
  Supergalactic latitude.
     """
     cdef double dsl
     cdef double dsb
     cpal.palGalsup( dl, db, &dsl, &dsb )
     return (dsl, dsb)

def ge50( double dl, double db ):
     """
     (rd, dd) = ge50( dl, db )

Transform Galactic Coordinate to B1950 FK4

Arguments
---------
dl = double (Given)
   Galactic longitude (radians)
db = double (Given)
   Galactic latitude (radians)
dr = double * (Returned)
   B9150.0 FK4 RA.
dd = double * (Returned)
   B1950.0 FK4 Dec.


Notes
-----
- The equatorial coordinates are B1950.0 'FK4'. Use the routine
palGaleq if conversion to J2000.0 coordinates is required.
     """
     cdef double dr
     cdef double dd
     cpal.palGe50( dl, db, &dr, &dd )
     return (dr, dd)

def geoc( double p, double h ):
     """
     (r, z) = geoc( p, h )

Convert geodetic position to geocentric

Arguments
---------
p = double (Given)
  latitude (radians)
h = double (Given)
  height above reference spheroid (geodetic, metres)
r = double * (Returned)
  distance from Earth axis (AU)
z = double * (Returned)
  distance from plane of Earth equator (AU)


Notes
-----
- Geocentric latitude can be obtained by evaluating atan2(z,r)
- Uses WGS84 reference ellipsoid and calls eraGd2gc
     """
     cdef double r
     cdef double z
     cpal.palGeoc( p, h, &r, &z )
     return (r, z)

def gmst( double ut1 ):
     """
     t = gmst( ut1 )

Greenwich mean sidereal time (consistent with IAU 2006 precession).

Arguments
---------
ut1 = double (Given)
   Universal time (UT1) expressed as modified Julian Date (JD-2400000.5)


Returned Value
--------------
Greenwich mean sidereal time


Notes
-----
- Uses eraGmst06(). See SOFA/ERFA documentation for details.
     """
     return cpal.palGmst( ut1 )

def gmsta( double date, double ut1 ):
     """
     t = gmsta( date, ut1 )

Greenwich mean sidereal time (consistent with IAU 2006 precession).

Arguments
---------
date = double (Given)
   UT1 date (MJD: integer part of JD-2400000.5)
ut1 = double (Given)
   UT1 time (fraction of a day)


Returned Value
--------------
Greenwich mean sidereal time (in range 0 to 2 pi)


Notes
-----
- For best accuracy use eraGmst06() directly.
- Uses eraGmst06(). See SOFA/ERFA documentation for details.
     """
     return cpal.palGmsta( date, ut1 )

def hfk5z( double rh, double dh, double epoch ):
     """
     (r5, d5, dr5, dd5) = hfk5z( rh, dh, epoch )

Hipparcos star position to FK5 J2000

Arguments
---------
rh = double (Given)
   Hipparcos RA (radians)
dh = double (Given)
   Hipparcos Dec (radians)
epoch = double (Given)
   Julian epoch (TDB)
r5 = double * (Returned)
   RA (radians, FK5, equinox J2000, epoch "epoch")
d5 = double * (Returned)
   Dec (radians, FK5, equinox J2000, epoch "epoch")


Notes
-----
- Uses eraEpj2jd and eraHfk5z(). See SOFA/ERFA documentation for details.
     """
     cdef double r5
     cdef double d5
     cdef double dr5
     cdef double dd5
     cpal.palHfk5z( rh, dh, epoch, &r5, &d5, &dr5, &dd5 )
     return (r5, d5, dr5, dd5)

# We need to return the sign in order to work out whether -0
# is a negative integer (important when parsing "-0 22 33.0"
# sexagesimal format. I'm assuming that no-one is going to really
# use the intin() function.
# We also need to handle overflow. If we raise an exception on
# overflow we can't continue to traverse the string so we have
# to return the position to continue but then document the
# magic value of LONG_MAX and LONG_MIN somehow but where would
# that go? For now raise an exception.
def intin( string, int nstrt ):
     """
     (ireslt, nstrt, sign) = intin( string, nstrt )

Convert free-format input into an integer

Arguments
---------
string = const char * (Given)
   String containing number to be decoded.
nstrt = int * (Given and Returned)
   Character number indicating where decoding should start.
   On output its value is updated to be the location of the
   possible next value. For compatibility with SLA the first
   character is index 1.
ireslt = long * (Returned)
   Result. Not updated when jflag=1.
jflag = int * (Returned)
   status: -1 = -OK, 0 = +OK, 1 = null, 2 = error


Notes
-----
- Uses the strtol() system call to do the parsing. This may lead to
  subtle differences when compared to the SLA/F parsing.
- Commas are recognized as a special case and are skipped if one happens
  to be the next character when updating nstrt. Additionally the output
  nstrt position will skip past any trailing space.
- If no number can be found flag will be set to 1.
- If the number overflows or underflows jflag will be set to 2. For overflow
  the returned result will have the value LONG_MAX, for underflow it
  will have the value LONG_MIN.

     Raises
     ------
     OverflowError: Integer too large to fit in 32-bit integer
     """
     cdef long ireslt
     cdef int j
     string_bytes = string.encode('ascii')
     cdef char * cstring = string_bytes
     cpal.palIntin( cstring, &nstrt, &ireslt, &j)
     sign = 0
     if j==0:
          sign = 1
     elif j==-1:
          sign = -1
     elif j==1:
          return (None, nstrt, None)
     else:
          raise OverflowError( "Integer too large for pal.intin() function" )
     return ( ireslt, nstrt, sign )

def map(double rm, double dm, double pr, double pd, double px, double rv, double eq, double date ):
     """
     (ra, da) = map( rm, dm, pr, pd, px, rv, eq, date )

Convert star RA,Dec from mean place to geocentric apparent

Arguments
---------
rm = double (Given)
   Mean RA (radians)
dm = double (Given)
   Mean declination (radians)
pr = double (Given)
   RA proper motion, changes per Julian year (radians)
pd = double (Given)
   Dec proper motion, changes per Julian year (radians)
px = double (Given)
   Parallax (arcsec)
rv = double (Given)
   Radial velocity (km/s, +ve if receding)
eq = double (Given)
   Epoch and equinox of star data (Julian)
date = double (Given)
   TDB for apparent place (JD-2400000.5)
ra = double * (Returned)
   Apparent RA (radians)
dec = double * (Returned)
   Apparent dec (radians)


Notes
-----
- Calls palMappa and palMapqk
- The reference systems and timescales used are IAU 2006.
- EQ is the Julian epoch specifying both the reference frame and
  the epoch of the position - usually 2000.  For positions where
  the epoch and equinox are different, use the routine palPm to
  apply proper motion corrections before using this routine.

- The distinction between the required TDB and TT is always
  negligible.  Moreover, for all but the most critical
  applications UTC is adequate.

- The proper motions in RA are dRA/dt rather than cos(Dec)*dRA/dt.

- This routine may be wasteful for some applications because it
  recomputes the Earth position/velocity and the precession-
  nutation matrix each time, and because it allows for parallax
  and proper motion.  Where multiple transformations are to be
  carried out for one epoch, a faster method is to call the
  palMappa routine once and then either the palMapqk routine
  (which includes parallax and proper motion) or palMapqkz (which
  assumes zero parallax and proper motion).

- The accuracy is sub-milliarcsecond, limited by the
  precession-nutation model (see palPrenut for details).

- The accuracy is further limited by the routine palEvp, called
  by palMappa, which computes the Earth position and velocity.
  See eraEpv00 for details on that calculation.
     """
     cdef double ra
     cdef double da
     cpal.palMap( rm, dm, pr, pd, px, rv, eq, date, &ra, &da )
     return (ra, da)

def mappa( double eq, double date ):
     """
     amprms = mappa( eq, date )

Compute parameters needed by palAmpqk and palMapqk.

Arguments
---------
eq = double (Given)
   epoch of mean equinox to be used (Julian)
date = double (Given)
   TDB (JD-2400000.5)
amprms =   double[21]  (Returned)
   star-independent mean-to-apparent parameters:
   - (0)      time interval for proper motion (Julian years)
   - (1-3)    barycentric position of the Earth (AU)
   - (4-6)    heliocentric direction of the Earth (unit vector)
   - (7)      (grav rad Sun)*2/(Sun-Earth distance)
   - (8-10)   abv: barycentric Earth velocity in units of c
   - (11)     sqrt(1-v**2) where v=modulus(abv)
   - (12-20)  precession/nutation (3,3) matrix


Notes
-----
- For date, the distinction between the required TDB and TT
is always negligible.  Moreover, for all but the most
critical applications UTC is adequate.
- The vector amprms(1-3) is referred to the mean equinox and
equator of epoch eq.
- The parameters amprms produced by this function are used by
palAmpqk, palMapqk and palMapqkz.
     """
     cdef double camprms[21]
     cdef np.ndarray amprms = np.zeros( [21], dtype=np.float64 )
     cpal.palMappa( eq, date, camprms )
     for i in range(21):
          amprms[i] = camprms[i]
     return amprms

def mapqk( double rm, double dm, double pr, double pd, double px, double rv, np.ndarray[double, ndim=1] amprms not None):
     """
     (ra, da) = mapqk( rm, dm, pr, pd, px, rv, amprms )

Quick mean to apparent place

Arguments
---------
rm = double (Given)
   Mean RA (radians)
dm = double (Given)
   Mean declination (radians)
pr = double (Given)
   RA proper motion, changes per Julian year (radians)
pd = double (Given)
   Dec proper motion, changes per Julian year (radians)
px = double (Given)
   Parallax (arcsec)
rv = double (Given)
   Radial velocity (km/s, +ve if receding)
amprms = double [21] (Given)
   Star-independent mean-to-apparent parameters (see palMappa).
ra = double * (Returned)
   Apparent RA (radians)
dec = double * (Returned)
   Apparent dec (radians)


Notes
-----
- The reference frames and timescales used are post IAU 2006.
     """
     cdef double ra
     cdef double da
     cdef double camprms[21]
     for i in range(21):
          camprms[i] = amprms[i]
     cpal.palMapqk( rm, dm, pr, pd, px, rv, camprms, &ra, &da )
     return (ra, da)

def mapqkVector( np.ndarray rm, np.ndarray dm, np.ndarray pr, np.ndarray pd,
np.ndarray px, np.ndarray rv, np.ndarray[double, ndim=1] amprms not None):
     """
     This is just mapqk except that it accepts a vector of inputs and
     returns a vector of outputs
     """
     cdef int i
     cdef int length=len(rm)
     cdef np.ndarray raout=np.zeros(length,dtype=np.float64)
     cdef np.ndarray decout=np.zeros(length,dtype=np.float64)
     cdef double ra
     cdef double da
     cdef double camprms[21]
     for i in range(21):
          camprms[i] = amprms[i]
     for i in range(length):
         cpal.palMapqk( rm[i], dm[i], pr[i], pd[i], px[i], rv[i], camprms, &ra, &da )
         raout[i]=ra
         decout[i]=da

     return (raout, decout)

def mapqkz( double rm, double dm, np.ndarray[double, ndim=1] amprms not None):
     """
     (ra, da) = mapqkz( rm, dm, amprms )

Quick mean to apparent place (no proper motion or parallax).

Arguments
---------
rm = double (Given)
   Mean RA (radians).
dm = double (Given)
   Mean Dec (radians).
amprms = double[21] (Given)
   Star-independent mean-to-apparent parameters (see palMappa):
   (0-3)    not used
   (4-6)    not used
   (7)      not used
   (8-10)   abv: barycentric Earth velocity in units of c
   (11)     sqrt(1-v**2) where v=modulus(abv)
   (12-20)  precession/nutation (3,3) matrix
ra = double * (Returned)
   Apparent RA (radians).
da = double * (Returned)
   Apparent Dec (radians).
     """
     cdef double ra
     cdef double da
     cdef double camprms[21]
     for i in range(21):
          camprms[i] = amprms[i]
     cpal.palMapqkz( rm, dm, camprms, &ra, &da )
     return (ra, da)


def mapqkzVector( np.ndarray rm, np.ndarray dm, np.ndarray[double, ndim=1] amprms not None):
     """
     This is just mapqkz except that it accepts a vector of inputs
     and returns a vector of outputs
     """
     cdef int i
     cdef int length=len(rm)
     cdef np.ndarray raout=np.zeros(length,dtype=np.float64)
     cdef np.ndarray decout=np.zeros(length,dtype=np.float64)
     cdef double ra
     cdef double da
     cdef double camprms[21]
     for i in range(21):
          camprms[i] = amprms[i]
     for i in range(length):
          cpal.palMapqkz( rm[i], dm[i], camprms, &ra, &da )
          raout[i]=ra
          decout[i]=da
     return (raout, decout)

def nut( double date ):
     """
     rmatn = nut( date )

Form the matrix of nutation

Arguments
---------
date = double (Given)
   TT as modified Julian date (JD-2400000.5)
rmatn = double [3][3] (Returned)
   Nutation matrix in the sense v(true)=rmatn * v(mean)
   where v(true) is the star vector relative to the
   true equator and equinox of date and v(mean) is the
   star vector relative to the mean equator and equinox
   of date.


Notes
-----
- Uses eraNut06a via palNutc
- The distinction between TDB and TT is negligible. For all but
  the most critical applications UTC is adequate.
     """
     cdef double crmatn[3][3]
     cpal.palNut( date, crmatn )
     cdef np.ndarray rmatn = np.zeros( [3,3], dtype=np.float64 )
     for i in range(3):
          for j in range(3):
               rmatn[i,j] = crmatn[i][j]
     return rmatn

def nutc( double date):
     """
     (dpsi, deps, eps0) = nutc( date )

Calculate nutation longitude & obliquoty components

Arguments
---------
date = double (Given)
   TT as modified Julian date (JD-2400000.5)
dpsi = double * (Returned)
   Nutation in longitude
deps = double * (Returned)
   Nutation in obliquity
eps0 = double * (Returned)
   Mean obliquity.


Notes
-----
- Calls eraObl06 and eraNut06a and therefore uses the IAU 206
  precession/nutation model.
- Note the change from SLA/F regarding the date. TT is used
  rather than TDB.
     """
     cdef double dpsi
     cdef double deps
     cdef double eps0
     cpal.palNutc( date, &dpsi, &deps, &eps0 )
     return (dpsi, deps, eps0)

def oap( type, double ob1, double ob2, double date,
         double dut, double elongm, double phim, double hm,
         double xp, double yp, double tdk, double pmb,
         double rh, double wl, double tlr ):
     """
     (rap, dap) = oap( ob1, ob2, date, dut, elongm, phim,
                    hm, xp, yp, tdk, pmb, rh, wl, tlr )

Observed to apparent place

Arguments
---------
type = const char * (Given)
   Type of coordinates - 'R', 'H' or 'A' (see below)
ob1 = double (Given)
   Observed Az, HA or RA (radians; Az is N=0;E=90)
ob2 = double (Given)
   Observed ZD or Dec (radians)
date = double (Given)
   UTC date/time (Modified Julian Date, JD-2400000.5)
dut = double (Given)
   delta UT: UT1-UTC (UTC seconds)
elongm = double (Given)
   Mean longitude of the observer (radians, east +ve)
phim = double (Given)
   Mean geodetic latitude of the observer (radians)
hm = double (Given)
   Observer's height above sea level (metres)
xp = double (Given)
   Polar motion x-coordinates (radians)
yp = double (Given)
   Polar motion y-coordinates (radians)
tdk = double (Given)
   Local ambient temperature (K; std=273.15)
pmb = double (Given)
   Local atmospheric pressure (mb; std=1013.25)
rh = double (Given)
   Local relative humidity (in the range 0.0-1.0)
wl = double (Given)
   Effective wavelength (micron, e.g. 0.55)
tlr = double (Given)
   Tropospheric laps rate (K/metre, e.g. 0.0065)
rap = double * (Given)
   Geocentric apparent right ascension
dap = double * (Given)
   Geocentric apparent declination


Notes
-----
- Only the first character of the TYPE argument is significant.
'R' or 'r' indicates that OBS1 and OBS2 are the observed right
ascension and declination;  'H' or 'h' indicates that they are
hour angle (west +ve) and declination;  anything else ('A' or
'a' is recommended) indicates that OBS1 and OBS2 are azimuth
(north zero, east 90 deg) and zenith distance.  (Zenith
distance is used rather than elevation in order to reflect the
fact that no allowance is made for depression of the horizon.)

- The accuracy of the result is limited by the corrections for
refraction.  Providing the meteorological parameters are
known accurately and there are no gross local effects, the
predicted apparent RA,Dec should be within about 0.1 arcsec
for a zenith distance of less than 70 degrees.  Even at a
topocentric zenith distance of 90 degrees, the accuracy in
elevation should be better than 1 arcmin;  useful results
are available for a further 3 degrees, beyond which the
palRefro routine returns a fixed value of the refraction.
The complementary routines palAop (or palAopqk) and palOap
(or palOapqk) are self-consistent to better than 1 micro-
arcsecond all over the celestial sphere.

- It is advisable to take great care with units, as even
unlikely values of the input parameters are accepted and
processed in accordance with the models used.

- "Observed" Az,El means the position that would be seen by a
perfect theodolite located at the observer.  This is
related to the observed HA,Dec via the standard rotation, using
the geodetic latitude (corrected for polar motion), while the
observed HA and RA are related simply through the local
apparent ST.  "Observed" RA,Dec or HA,Dec thus means the
position that would be seen by a perfect equatorial located
at the observer and with its polar axis aligned to the
Earth's axis of rotation (n.b. not to the refracted pole).
By removing from the observed place the effects of
atmospheric refraction and diurnal aberration, the
geocentric apparent RA,Dec is obtained.

- Frequently, mean rather than apparent RA,Dec will be required,
in which case further transformations will be necessary.  The
palAmp etc routines will convert the apparent RA,Dec produced
by the present routine into an "FK5" (J2000) mean place, by
allowing for the Sun's gravitational lens effect, annual
aberration, nutation and precession.  Should "FK4" (1950)
coordinates be needed, the routines palFk524 etc will also
need to be applied.

- To convert to apparent RA,Dec the coordinates read from a
real telescope, corrections would have to be applied for
encoder zero points, gear and encoder errors, tube flexure,
the position of the rotator axis and the pointing axis
relative to it, non-perpendicularity between the mounting
axes, and finally for the tilt of the azimuth or polar axis
of the mounting (with appropriate corrections for mount
flexures).  Some telescopes would, of course, exhibit other
properties which would need to be accounted for at the
appropriate point in the sequence.

- This routine takes time to execute, due mainly to the rigorous
integration used to evaluate the refraction.  For processing
multiple stars for one location and time, call palAoppa once
followed by one call per star to palOapqk.  Where a range of
times within a limited period of a few hours is involved, and the
highest precision is not required, call palAoppa once, followed
by a call to palAoppat each time the time changes, followed by
one call per star to palOapqk.

- The DATE argument is UTC expressed as an MJD.  This is, strictly
speaking, wrong, because of leap seconds.  However, as long as
the delta UT and the UTC are consistent there are no
difficulties, except during a leap second.  In this case, the
start of the 61st second of the final minute should begin a new
MJD day and the old pre-leap delta UT should continue to be used.
As the 61st second completes, the MJD should revert to the start
of the day as, simultaneously, the delta UTC changes by one
second to its post-leap new value.

- The delta UT (UT1-UTC) is tabulated in IERS circulars and
elsewhere.  It increases by exactly one second at the end of
each UTC leap second, introduced in order to keep delta UT
within +/- 0.9 seconds.

- IMPORTANT -- TAKE CARE WITH THE LONGITUDE SIGN CONVENTION.
The longitude required by the present routine is east-positive,
in accordance with geographical convention (and right-handed).
In particular, note that the longitudes returned by the
palOBS routine are west-positive, following astronomical
usage, and must be reversed in sign before use in the present
routine.

- The polar coordinates XP,YP can be obtained from IERS
circulars and equivalent publications.  The maximum amplitude
is about 0.3 arcseconds.  If XP,YP values are unavailable,
use XP=YP=0D0.  See page B60 of the 1988 Astronomical Almanac
for a definition of the two angles.

- The height above sea level of the observing station, HM,
can be obtained from the Astronomical Almanac (Section J
in the 1988 edition), or via the routine palOBS.  If P,
the pressure in millibars, is available, an adequate
estimate of HM can be obtained from the expression

       HM ~ -29.3*TSL*LOG(P/1013.25).

where TSL is the approximate sea-level air temperature in K
(see Astrophysical Quantities, C.W.Allen, 3rd edition,
section 52).  Similarly, if the pressure P is not known,
it can be estimated from the height of the observing
station, HM, as follows:

       P ~ 1013.25*EXP(-HM/(29.3*TSL)).

Note, however, that the refraction is nearly proportional to the
pressure and that an accurate P value is important for precise
work.

- The azimuths etc. used by the present routine are with respect
to the celestial pole.  Corrections from the terrestrial pole
can be computed using palPolmo.
     """
     cdef double rap
     cdef double dap
     byte_string = type.encode('ascii')
     cdef char * ctype = byte_string
     cpal.palOap( ctype, ob1, ob2, date, dut, elongm, phim,
                  hm, xp, yp, tdk, pmb, rh, wl, tlr, &rap, &dap )
     return ( rap, dap )

def oapqk( type, double ob1, double ob2, np.ndarray[double, ndim=1] aoprms not None ):
     """
     (rap, dap) = oapqk( type, ob1, ob2, aoprms )

Quick observed to apparent place

Arguments
---------
Quick observed to apparent place.


Notes
-----
- Only the first character of the TYPE argument is significant.
'R' or 'r' indicates that OBS1 and OBS2 are the observed right
ascension and declination;  'H' or 'h' indicates that they are
hour angle (west +ve) and declination;  anything else ('A' or
'a' is recommended) indicates that OBS1 and OBS2 are azimuth
(north zero, east 90 deg) and zenith distance.  (Zenith distance
is used rather than elevation in order to reflect the fact that
no allowance is made for depression of the horizon.)

- The accuracy of the result is limited by the corrections for
refraction.  Providing the meteorological parameters are
known accurately and there are no gross local effects, the
predicted apparent RA,Dec should be within about 0.1 arcsec
for a zenith distance of less than 70 degrees.  Even at a
topocentric zenith distance of 90 degrees, the accuracy in
elevation should be better than 1 arcmin;  useful results
are available for a further 3 degrees, beyond which the
palREFRO routine returns a fixed value of the refraction.
The complementary routines palAop (or palAopqk) and palOap
(or palOapqk) are self-consistent to better than 1 micro-
arcsecond all over the celestial sphere.

- It is advisable to take great care with units, as even
unlikely values of the input parameters are accepted and
processed in accordance with the models used.

- "Observed" Az,El means the position that would be seen by a
perfect theodolite located at the observer.  This is
related to the observed HA,Dec via the standard rotation, using
the geodetic latitude (corrected for polar motion), while the
observed HA and RA are related simply through the local
apparent ST.  "Observed" RA,Dec or HA,Dec thus means the
position that would be seen by a perfect equatorial located
at the observer and with its polar axis aligned to the
Earth's axis of rotation (n.b. not to the refracted pole).
By removing from the observed place the effects of
atmospheric refraction and diurnal aberration, the
geocentric apparent RA,Dec is obtained.

- Frequently, mean rather than apparent RA,Dec will be required,
in which case further transformations will be necessary.  The
palAmp etc routines will convert the apparent RA,Dec produced
by the present routine into an "FK5" (J2000) mean place, by
allowing for the Sun's gravitational lens effect, annual
aberration, nutation and precession.  Should "FK4" (1950)
coordinates be needed, the routines palFk524 etc will also
need to be applied.

- To convert to apparent RA,Dec the coordinates read from a
real telescope, corrections would have to be applied for
encoder zero points, gear and encoder errors, tube flexure,
the position of the rotator axis and the pointing axis
relative to it, non-perpendicularity between the mounting
axes, and finally for the tilt of the azimuth or polar axis
of the mounting (with appropriate corrections for mount
flexures).  Some telescopes would, of course, exhibit other
properties which would need to be accounted for at the
appropriate point in the sequence.

- The star-independent apparent-to-observed-place parameters
in AOPRMS may be computed by means of the palAoppa routine.
If nothing has changed significantly except the time, the
palAoppat routine may be used to perform the requisite
partial recomputation of AOPRMS.

- The azimuths etc used by the present routine are with respect
to the celestial pole.  Corrections from the terrestrial pole
can be computed using palPolmo.
     """
     cdef double rap
     cdef double dap
     byte_string = type.encode('ascii')
     cdef char * ctype = byte_string
     cdef double caoprms[14]
     for i in range(14):
          caoprms[i] = aoprms[i]
     cpal.palOapqk( ctype, ob1, ob2, caoprms, &rap, &dap )
     return ( rap, dap )

# Numeric lookup is only useful when scanning through the
# list of telescopes. The python interface does not need this.
# Instead obs() returns a dict (which may be a bit less efficient
# than an iterable but it's easy) with a dict inside. No arguments.
def obs():
     """
     telescopes = pal.obs()

     Obtain telescope parameters.

     Returns a dict with keys corresponding to the short
     name of the telescope. The corresponding value is itself
     a dict with keys:

     name: long name of the telescope
     long: west longitude (radians)
     lat: geodetic latitude (radians)
     height: Height above sea level (metres)
     """
     cdef int n = 1
     cdef char c
     cdef char cident[11]
     cdef char cname[41]
     cdef double w
     cdef double p
     cdef double h
     cdef int retval = 0

     result = {}

     while True:
          retval = cpal.palObs( n, &c, cident, 11, cname, 41,
                                &w, &p, &h )
          n=n+1 # Next telescope

          if retval != 0:
               break
          newtel = { 'name': cname.decode('UTF-8'),
                     'long': w,
                     'lat': p,
                     'height': h }
          result[cident.decode('UTF-8')] = newtel

     return result

def pa( double ha, double dec, double phi):
     """
     a = pa( ha, dec, phi )

HA, Dec to Parallactic Angle

Arguments
---------
ha = double (Given)
   Hour angle in radians (Geocentric apparent)
dec = double (Given)
   Declination in radians (Geocentric apparent)
phi = double (Given)
   Observatory latitude in radians (geodetic)


Returned Value
--------------
palPa = double
   Parallactic angle in the range -pi to +pi.


Notes
-----
- The parallactic angle at a point in the sky is the position
  angle of the vertical, i.e. the angle between the direction to
  the pole and to the zenith.  In precise applications care must
  be taken only to use geocentric apparent HA,Dec and to consider
  separately the effects of atmospheric refraction and telescope
  mount errors.
- At the pole a zero result is returned.
     """
     return cpal.palPa( ha, dec, phi )

def pcd( double disco, double x, double y):
    """
    (cx, cy) = pcd( x, y )

    Returns the distorted coordinates and does not
    modify the supplied arguments.

Apply pincushion/barrel distortion to a tangent-plane [x,y]

Arguments
---------
disco = double (Given)
   Pincushion/barrel distortion coefficient.
x = double * (Given & Returned)
   On input the tangent-plane X coordinate, on output
   the distorted X coordinate.
y = double * (Given & Returned)
   On input the tangent-plane Y coordinate, on output
   the distorted Y coordinate.


Notes
-----
- The distortion is of the form RP = R*(1 + C*R**2), where R is
  the radial distance from the tangent point, C is the DISCO
  argument, and RP is the radial distance in the presence of
  the distortion.

- For pincushion distortion, C is +ve;  for barrel distortion,
  C is -ve.

- For X,Y in units of one projection radius (in the case of
  a photographic plate, the focal length), the following
  DISCO values apply:

      Geometry          DISCO

      astrograph         0.0
      Schmidt           -0.3333
      AAT PF doublet  +147.069
      AAT PF triplet  +178.585
      AAT f/8          +21.20
      JKT f/8          +13.32

    """
    cpal.palPcd( disco, &x, &y )
    return (x, y)

def polmo( double elongm, double phim, double xp, double yp):
    """
    (elong, phi, daz) = polmo( elongm, phim, xp, yp )

Correct for polar motion

Arguments
---------
elongm = double (Given)
   Mean logitude of the observer (radians, east +ve)
phim = double (Given)
   Mean geodetic latitude of the observer (radians)
xp = double (Given)
   Polar motion x-coordinate (radians)
yp = double (Given)
   Polar motion y-coordinate (radians)
elong = double * (Returned)
   True longitude of the observer (radians, east +ve)
phi = double * (Returned)
   True geodetic latitude of the observer (radians)
daz = double * (Returned)
   Azimuth correction (terrestrial-celestial, radians)


Notes
-----
- "Mean" longitude and latitude are the (fixed) values for the
  site's location with respect to the IERS terrestrial reference
  frame;  the latitude is geodetic.  TAKE CARE WITH THE LONGITUDE
  SIGN CONVENTION.  The longitudes used by the present routine
  are east-positive, in accordance with geographical convention
  (and right-handed).  In particular, note that the longitudes
  returned by the sla_OBS routine are west-positive, following
  astronomical usage, and must be reversed in sign before use in
  the present routine.

- XP and YP are the (changing) coordinates of the Celestial
  Ephemeris Pole with respect to the IERS Reference Pole.
  XP is positive along the meridian at longitude 0 degrees,
  and YP is positive along the meridian at longitude
  270 degrees (i.e. 90 degrees west).  Values for XP,YP can
  be obtained from IERS circulars and equivalent publications;
  the maximum amplitude observed so far is about 0.3 arcseconds.

- "True" longitude and latitude are the (moving) values for
  the site's location with respect to the celestial ephemeris
  pole and the meridian which corresponds to the Greenwich
  apparent sidereal time.  The true longitude and latitude
  link the terrestrial coordinates with the standard celestial
  models (for precession, nutation, sidereal time etc).

- The azimuths produced by sla_AOP and sla_AOPQK are with
  respect to due north as defined by the Celestial Ephemeris
  Pole, and can therefore be called "celestial azimuths".
  However, a telescope fixed to the Earth measures azimuth
  essentially with respect to due north as defined by the
  IERS Reference Pole, and can therefore be called "terrestrial
  azimuth".  Uncorrected, this would manifest itself as a
  changing "azimuth zero-point error".  The value DAZ is the
  correction to be added to a celestial azimuth to produce
  a terrestrial azimuth.

- The present routine is rigorous.  For most practical
  purposes, the following simplified formulae provide an
  adequate approximation:

  elong = elongm+xp*cos(elongm)-yp*sin(elongm)
  phi   = phim+(xp*sin(elongm)+yp*cos(elongm))*tan(phim)
  daz   = -sqrt(xp*xp+yp*yp)*cos(elongm-atan2(xp,yp))/cos(phim)

  An alternative formulation for DAZ is:

  x = cos(elongm)*cos(phim)
  y = sin(elongm)*cos(phim)
  daz = atan2(-x*yp-y*xp,x*x+y*y)

- Reference:  Seidelmann, P.K. (ed), 1992.  "Explanatory Supplement
              to the Astronomical Almanac", ISBN 0-935702-68-7,
              sections 3.27, 4.25, 4.52.
    """
    cdef double elong
    cdef double phi
    cdef double daz

    cpal.palPolmo( elongm, phim, xp, yp, &elong, &phi, &daz )

    return (elong, phi, daz)

def pertel(int jform, double date0, double date1,
            double epoch0, double orbi0, double anode0,
            double perih0, double aorq0, double e0, double am0):
    """
    (epoch1, orbi1, anode1, perih1, aorq1, e1, am1) = pertel( jform, date0, date1,
                                                            epoch0, orbi0, anode0, perih0,
                                                            aorq0, e0, am0 )

Update elements by applying planetary perturbations

Arguments
---------
jform = int (Given)
   Element set actually returned (1-3; Note 6)
date0 = double (Given)
   Date of osculation (TT MJD) for the given elements.
date1 = double (Given)
   Date of osculation (TT MJD) for the updated elements.
epoch0 = double (Given)
   Epoch of elements (TT MJD)
orbi0 = double (Given)
   inclination (radians)
anode0 = double (Given)
   longitude of the ascending node (radians)
perih0 = double (Given)
   longitude or argument of perihelion (radians)
aorq0 = double (Given)
   mean distance or perihelion distance (AU)
e0 = double (Given)
   eccentricity
am0 = double (Given)
   mean anomaly (radians, JFORM=2 only)
epoch1 = double * (Returned)
   Epoch of elements (TT MJD)
orbi1 = double * (Returned)
   inclination (radians)
anode1 = double * (Returned)
   longitude of the ascending node (radians)
perih1 = double * (Returned)
   longitude or argument of perihelion (radians)
aorq1 = double * (Returned)
   mean distance or perihelion distance (AU)
e1 = double * (Returned)
   eccentricity
am1 = double * (Returned)
   mean anomaly (radians, JFORM=2 only)
jstat = int * (Returned)
   status:
     -      +102 = warning, distant epoch
     -      +101 = warning, large timespan ( > 100 years)
     - +1 to +10 = coincident with planet (Note 6)
     -         0 = OK
     -        -1 = illegal JFORM
     -        -2 = illegal E0
     -        -3 = illegal AORQ0
     -        -4 = internal error
     -        -5 = numerical error


Notes
-----
- Two different element-format options are available:

  Option JFORM=2, suitable for minor planets:

  EPOCH   = epoch of elements (TT MJD)
  ORBI    = inclination i (radians)
  ANODE   = longitude of the ascending node, big omega (radians)
  PERIH   = argument of perihelion, little omega (radians)
  AORQ    = mean distance, a (AU)
  E       = eccentricity, e
  AM      = mean anomaly M (radians)

  Option JFORM=3, suitable for comets:

  EPOCH   = epoch of perihelion (TT MJD)
  ORBI    = inclination i (radians)
  ANODE   = longitude of the ascending node, big omega (radians)
  PERIH   = argument of perihelion, little omega (radians)
  AORQ    = perihelion distance, q (AU)
  E       = eccentricity, e

- DATE0, DATE1, EPOCH0 and EPOCH1 are all instants of time in
  the TT timescale (formerly Ephemeris Time, ET), expressed
  as Modified Julian Dates (JD-2400000.5).

  DATE0 is the instant at which the given (i.e. unperturbed)
  osculating elements are correct.

  DATE1 is the specified instant at which the updated osculating
  elements are correct.

  EPOCH0 and EPOCH1 will be the same as DATE0 and DATE1
  (respectively) for the JFORM=2 case, normally used for minor
  planets.  For the JFORM=3 case, the two epochs will refer to
  perihelion passage and so will not, in general, be the same as
  DATE0 and/or DATE1 though they may be similar to one another.
- The elements are with respect to the J2000 ecliptic and equinox.
- Unused elements (AM0 and AM1 for JFORM=3) are not accessed.
- See the palPertue routine for details of the algorithm used.
- This routine is not intended to be used for major planets, which
  is why JFORM=1 is not available and why there is no opportunity
  to specify either the longitude of perihelion or the daily
  motion.  However, if JFORM=2 elements are somehow obtained for a
  major planet and supplied to the routine, sensible results will,
  in fact, be produced.  This happens because the palPertue routine
  that is called to perform the calculations checks the separation
  between the body and each of the planets and interprets a
  suspiciously small value (0.001 AU) as an attempt to apply it to
  the planet concerned.  If this condition is detected, the
  contribution from that planet is ignored, and the status is set to
  the planet number (1-10 = Mercury, Venus, EMB, Mars, Jupiter,
  Saturn, Uranus, Neptune, Earth, Moon) as a warning.


    Raises
    ------
    ValueError: Illegal input arguments.
    ArithmeticError: Internal error.
    """
    cdef double epoch1
    cdef double orbi1
    cdef double anode1
    cdef double perih1
    cdef double aorq1
    cdef double e1
    cdef double am1
    cdef int jstat

    cpal.palPertel( jform, date0, date1,
                    epoch0, orbi0, anode0, perih0, aorq0, e0, am0,
                    &epoch1, &orbi1, &anode1, &perih1, &aorq1, &e1, &am1,
                    &jstat )
    if jstat == -1:
        raise ValueError( "Illegal jform" )
    elif jstat == -2:
        raise ValueError( "Illegal e0" )
    elif jstat == -3:
        raise ValueError( "Illegal aorq0" )
    elif jstat == -4:
        raise ArithmeticError( "Internal error" )
    elif jstat == -5:
        raise ArithmeticError( "Numerical error" )

    return ( epoch1, orbi1, anode1, perih1, aorq1, e1, am1 )

def pertue( double date, np.ndarray[double, ndim=1] u not None ):
    """
    u2 = pertue( date, u )

Update the universal elements by applying planetary perturbations

Arguments
---------
date = double (Given)
   Final epoch (TT MJD) for the update elements.
u = const double [13] (Given & Returned)
   Universal orbital elements (Note 1)
       (0)  combined mass (M+m)
       (1)  total energy of the orbit (alpha)
       (2)  reference (osculating) epoch (t0)
     (3-5)  position at reference epoch (r0)
     (6-8)  velocity at reference epoch (v0)
       (9)  heliocentric distance at reference epoch
      (10)  r0.v0
      (11)  date (t)
      (12)  universal eccentric anomaly (psi) of date, approx
jstat = int * (Returned)
   status:
              +102 = warning, distant epoch
              +101 = warning, large timespan ( > 100 years)
         +1 to +10 = coincident with major planet (Note 5)
                 0 = OK
                -1 = numerical error


Notes
-----
- The "universal" elements are those which define the orbit for the
  purposes of the method of universal variables (see reference 2).
  They consist of the combined mass of the two bodies, an epoch,
  and the position and velocity vectors (arbitrary reference frame)
  at that epoch.  The parameter set used here includes also various
  quantities that can, in fact, be derived from the other
  information.  This approach is taken to avoiding unnecessary
  computation and loss of accuracy.  The supplementary quantities
  are (i) alpha, which is proportional to the total energy of the
  orbit, (ii) the heliocentric distance at epoch, (iii) the
  outwards component of the velocity at the given epoch, (iv) an
  estimate of psi, the "universal eccentric anomaly" at a given
  date and (v) that date.
- The universal elements are with respect to the J2000 equator and
  equinox.
- The epochs DATE, U(3) and U(12) are all Modified Julian Dates
  (JD-2400000.5).
- The algorithm is a simplified form of Encke's method.  It takes as
  a basis the unperturbed motion of the body, and numerically
  integrates the perturbing accelerations from the major planets.
  The expression used is essentially Sterne's 6.7-2 (reference 1).
  Everhart and Pitkin (reference 2) suggest rectifying the orbit at
  each integration step by propagating the new perturbed position
  and velocity as the new universal variables.  In the present
  routine the orbit is rectified less frequently than this, in order
  to gain a slight speed advantage.  However, the rectification is
  done directly in terms of position and velocity, as suggested by
  Everhart and Pitkin, bypassing the use of conventional orbital
  elements.

  The f(q) part of the full Encke method is not used.  The purpose
  of this part is to avoid subtracting two nearly equal quantities
  when calculating the "indirect member", which takes account of the
  small change in the Sun's attraction due to the slightly displaced
  position of the perturbed body.  A simpler, direct calculation in
  double precision proves to be faster and not significantly less
  accurate.

  Apart from employing a variable timestep, and occasionally
  "rectifying the orbit" to keep the indirect member small, the
  integration is done in a fairly straightforward way.  The
  acceleration estimated for the middle of the timestep is assumed
  to apply throughout that timestep;  it is also used in the
  extrapolation of the perturbations to the middle of the next
  timestep, to predict the new disturbed position.  There is no
  iteration within a timestep.

  Measures are taken to reach a compromise between execution time
  and accuracy.  The starting-point is the goal of achieving
  arcsecond accuracy for ordinary minor planets over a ten-year
  timespan.  This goal dictates how large the timesteps can be,
  which in turn dictates how frequently the unperturbed motion has
  to be recalculated from the osculating elements.

  Within predetermined limits, the timestep for the numerical
  integration is varied in length in inverse proportion to the
  magnitude of the net acceleration on the body from the major
  planets.

  The numerical integration requires estimates of the major-planet
  motions.  Approximate positions for the major planets (Pluto
  alone is omitted) are obtained from the routine palPlanet.  Two
  levels of interpolation are used, to enhance speed without
  significantly degrading accuracy.  At a low frequency, the routine
  palPlanet is called to generate updated position+velocity "state
  vectors".  The only task remaining to be carried out at the full
  frequency (i.e. at each integration step) is to use the state
  vectors to extrapolate the planetary positions.  In place of a
  strictly linear extrapolation, some allowance is made for the
  curvature of the orbit by scaling back the radius vector as the
  linear extrapolation goes off at a tangent.

  Various other approximations are made.  For example, perturbations
  by Pluto and the minor planets are neglected and relativistic
  effects are not taken into account.

  In the interests of simplicity, the background calculations for
  the major planets are carried out en masse.  The mean elements and
  state vectors for all the planets are refreshed at the same time,
  without regard for orbit curvature, mass or proximity.

  The Earth-Moon system is treated as a single body when the body is
  distant but as separate bodies when closer to the EMB than the
  parameter RNE, which incurs a time penalty but improves accuracy
  for near-Earth objects.

- This routine is not intended to be used for major planets.
  However, if major-planet elements are supplied, sensible results
  will, in fact, be produced.  This happens because the routine
  checks the separation between the body and each of the planets and
  interprets a suspiciously small value (0.001 AU) as an attempt to
  apply the routine to the planet concerned.  If this condition is
  detected, the contribution from that planet is ignored, and the
  status is set to the planet number (1-10 = Mercury, Venus, EMB,
  Mars, Jupiter, Saturn, Uranus, Neptune, Earth, Moon) as a warning.

    Raises
    ------
    ArithmeticError: Numerical error
    """
    cdef double cu[13]
    cdef int jstat

    for i in range(13):
        cu[i] = u[i]

    cpal.palPertue( date, cu, &jstat )

    if jstat == -1:
        raise ArithmeticError( "Numerical error" )

    # We return the modified U and do not change in place
    cdef np.ndarray u2 = np.zeros( [13], dtype=np.float64)
    for i in range(13):
        u2[i] = cu[i]
    return u2

def planel( double date, int jform, double epoch, double orbinc,
            double anode, double perih, double aorq,  double e,
            double aorl, double dm ):
    """
    pv = planel( date, jform, epoch, orbinc, anode, perih, aorq, e, aorl, dm )

Transform conventional elements into position and velocity

Arguments
---------
date = double (Given)
   Epoch (TT MJD) of osculation (Note 1)
jform = int (Given)
   Element set actually returned (1-3; Note 3)
epoch = double (Given)
   Epoch of elements (TT MJD) (Note 4)
orbinc = double (Given)
   inclination (radians)
anode = double (Given)
   longitude of the ascending node (radians)
perih = double (Given)
   longitude or argument of perihelion (radians)
aorq = double (Given)
   mean distance or perihelion distance (AU)
e = double (Given)
   eccentricity
aorl = double (Given)
   mean anomaly or longitude (radians, JFORM=1,2 only)
dm = double (Given)
   daily motion (radians, JFORM=1 only)
u = double [13] (Returned)
   Universal orbital elements (Note 1)
       (0)  combined mass (M+m)
       (1)  total energy of the orbit (alpha)
       (2)  reference (osculating) epoch (t0)
     (3-5)  position at reference epoch (r0)
     (6-8)  velocity at reference epoch (v0)
       (9)  heliocentric distance at reference epoch
      (10)  r0.v0
      (11)  date (t)
      (12)  universal eccentric anomaly (psi) of date, approx
jstat = int * (Returned)
   status:  0 = OK
         - -1 = illegal JFORM
         - -2 = illegal E
         - -3 = illegal AORQ
         - -4 = illegal DM
         - -5 = numerical error


Notes
-----
- DATE is the instant for which the prediction is required.  It is
  in the TT timescale (formerly Ephemeris Time, ET) and is a
  Modified Julian Date (JD-2400000.5).
- The elements are with respect to the J2000 ecliptic and equinox.
- A choice of three different element-set options is available:

  Option JFORM = 1, suitable for the major planets:

    EPOCH  = epoch of elements (TT MJD)
    ORBINC = inclination i (radians)
    ANODE  = longitude of the ascending node, big omega (radians)
    PERIH  = longitude of perihelion, curly pi (radians)
    AORQ   = mean distance, a (AU)
    E      = eccentricity, e (range 0 to <1)
    AORL   = mean longitude L (radians)
    DM     = daily motion (radians)

  Option JFORM = 2, suitable for minor planets:

    EPOCH  = epoch of elements (TT MJD)
    ORBINC = inclination i (radians)
    ANODE  = longitude of the ascending node, big omega (radians)
    PERIH  = argument of perihelion, little omega (radians)
    AORQ   = mean distance, a (AU)
    E      = eccentricity, e (range 0 to <1)
    AORL   = mean anomaly M (radians)

  Option JFORM = 3, suitable for comets:

    EPOCH  = epoch of elements and perihelion (TT MJD)
    ORBINC = inclination i (radians)
    ANODE  = longitude of the ascending node, big omega (radians)
    PERIH  = argument of perihelion, little omega (radians)
    AORQ   = perihelion distance, q (AU)
    E      = eccentricity, e (range 0 to 10)

  Unused arguments (DM for JFORM=2, AORL and DM for JFORM=3) are not
  accessed.
- Each of the three element sets defines an unperturbed heliocentric
  orbit.  For a given epoch of observation, the position of the body
  in its orbit can be predicted from these elements, which are
  called "osculating elements", using standard two-body analytical
  solutions.  However, due to planetary perturbations, a given set
  of osculating elements remains usable for only as long as the
  unperturbed orbit that it describes is an adequate approximation
  to reality.  Attached to such a set of elements is a date called
  the "osculating epoch", at which the elements are, momentarily,
  a perfect representation of the instantaneous position and
  velocity of the body.

  Therefore, for any given problem there are up to three different
  epochs in play, and it is vital to distinguish clearly between
  them:

  . The epoch of observation:  the moment in time for which the
    position of the body is to be predicted.

  . The epoch defining the position of the body:  the moment in time
    at which, in the absence of purturbations, the specified
    position (mean longitude, mean anomaly, or perihelion) is
    reached.

  . The osculating epoch:  the moment in time at which the given
    elements are correct.

  For the major-planet and minor-planet cases it is usual to make
  the epoch that defines the position of the body the same as the
  epoch of osculation.  Thus, only two different epochs are
  involved:  the epoch of the elements and the epoch of observation.

  For comets, the epoch of perihelion fixes the position in the
  orbit and in general a different epoch of osculation will be
  chosen.  Thus, all three types of epoch are involved.

  For the present routine:

  . The epoch of observation is the argument DATE.

  . The epoch defining the position of the body is the argument
    EPOCH.

  . The osculating epoch is not used and is assumed to be close
    enough to the epoch of observation to deliver adequate accuracy.
    If not, a preliminary call to palPertel may be used to update
    the element-set (and its associated osculating epoch) by
    applying planetary perturbations.
- The reference frame for the result is with respect to the mean
  equator and equinox of epoch J2000.
- The algorithm was originally adapted from the EPHSLA program of
  D.H.P.Jones (private communication, 1996).  The method is based
  on Stumpff's Universal Variables.

    Raises
    ------
    ValueError: Illegal input arguments
    ArithmeticError: Numerical error
    """
    cdef int jstat
    cdef double cpv[6]
    cpal.palPlanel( date, jform, epoch, orbinc, anode, perih, aorq,
                    e, aorl, dm, cpv, &jstat )
    if jstat == -1:
        raise ValueError( "Illegal jform" )
    elif jstat == -2:
        raise ValueError( "Illegal e" )
    elif jstat == -3:
        raise ValueError( "Illegal aorq" )
    elif jstat == -4:
        raise ValueError( "Illegal dm" )
    elif jstat == -5:
        raise ArithmeticError( "Numerical error" )

    cdef np.ndarray pv = np.zeros( [6], dtype=np.float64 )
    for i in range(6):
        pv[i] = cpv[i]
    return pv

def planet( double date, int planetnum ):
    """
    pv = planet( date, planetnum )

Approximate heliocentric position and velocity of major planet

Arguments
---------
date = double (Given)
   TDB Modified Julian Date (JD-2400000.5).
np = int (Given)
   planet (1=Mercury, 2=Venus, 3=EMB, 4=Mars,
           5=Jupiter, 6=Saturn, 7=Uranus, 8=Neptune)
pv = double [6] (Returned)
   heliocentric x,y,z,xdot,ydot,zdot, J2000, equatorial triad
   in units AU and AU/s.
j = int * (Returned)
   - -2 = solution didn't converge.
   - -1 = illegal np (1-8)
   -  0 = OK
   - +1 = warning: year outside 1000-3000


Notes
-----
- See SOFA/ERFA eraPlan94 for details
- Note that Pluto is supported in SLA/F but not in this routine
- Status -2 is equivalent to eraPlan94 status +2.
- Note that velocity units here match the SLA/F documentation.

    Raises
    ------
    ValueError: Illegal planet number
    ArithmeticError: Solution did not converge
    """
    cdef int jstat
    cdef double cpv[6]
    cpal.palPlanet( date, planetnum, cpv, &jstat )
    if jstat == -2:
        raise ArithmeticError( "Solution didn't converge" )
    elif jstat == -1:
        raise ValueError( "Illegal planet number "+str(planetnum)+", must be in range (1-8)" )

    cdef np.ndarray pv = np.zeros( [6], dtype=np.float64 )
    for i in range(6):
        pv[i] = cpv[i]
    return pv

def plante( double date, double elong, double phi, int jform,
            double epoch, double orbinc, double anode, double perih,
            double aorq, double e, double aorl, double dm ):
    """
    (ra, dec, r) = plante( date, elong, phi, jform, epoch, orbinc, anode,
                           perih, aorq, e, aorl, dm )

Topocentric RA,Dec of a Solar-System object from heliocentric orbital elements

Arguments
---------
date = double (Given)
   TT MJD of observation (JD-2400000.5)
elong = double (Given)
   Observer's east longitude (radians)
phi = double (Given)
   Observer's geodetic latitude (radians)
jform = int (Given)
   Element set actually returned (1-3; Note 6)
epoch = double (Given)
   Epoch of elements (TT MJD)
orbinc = double (Given)
   inclination (radians)
anode = double (Given)
   longitude of the ascending node (radians)
perih = double (Given)
   longitude or argument of perihelion (radians)
aorq = double (Given)
   mean distance or perihelion distance (AU)
e = double (Given)
   eccentricity
aorl = double (Given)
   mean anomaly or longitude (radians, JFORM=1,2 only)
dm = double (Given)
   daily motion (radians, JFORM=1 only)
ra = double * (Returned)
   Topocentric apparent RA (radians)
dec = double * (Returned)
   Topocentric apparent Dec (radians)
r = double * (Returned)
   Distance from observer (AU)
jstat = int * (Returned)
   status: 0 = OK
        - -1 = illegal jform
        - -2 = illegal e
        - -3 = illegal aorq
        - -4 = illegal dm
        - -5 = numerical error


Notes
-----
- DATE is the instant for which the prediction is required.  It is
  in the TT timescale (formerly Ephemeris Time, ET) and is a
  Modified Julian Date (JD-2400000.5).
- The longitude and latitude allow correction for geocentric
  parallax.  This is usually a small effect, but can become
  important for near-Earth asteroids.  Geocentric positions can be
  generated by appropriate use of routines palEpv (or palEvp) and
  palUe2pv.
- The elements are with respect to the J2000 ecliptic and equinox.
- A choice of three different element-set options is available:

  Option JFORM = 1, suitable for the major planets:

    EPOCH  = epoch of elements (TT MJD)
    ORBINC = inclination i (radians)
    ANODE  = longitude of the ascending node, big omega (radians)
    PERIH  = longitude of perihelion, curly pi (radians)
    AORQ   = mean distance, a (AU)
    E      = eccentricity, e (range 0 to <1)
    AORL   = mean longitude L (radians)
    DM     = daily motion (radians)

  Option JFORM = 2, suitable for minor planets:

    EPOCH  = epoch of elements (TT MJD)
    ORBINC = inclination i (radians)
    ANODE  = longitude of the ascending node, big omega (radians)
    PERIH  = argument of perihelion, little omega (radians)
    AORQ   = mean distance, a (AU)
    E      = eccentricity, e (range 0 to <1)
    AORL   = mean anomaly M (radians)

  Option JFORM = 3, suitable for comets:

    EPOCH  = epoch of elements and perihelion (TT MJD)
    ORBINC = inclination i (radians)
    ANODE  = longitude of the ascending node, big omega (radians)
    PERIH  = argument of perihelion, little omega (radians)
    AORQ   = perihelion distance, q (AU)
    E      = eccentricity, e (range 0 to 10)

  Unused arguments (DM for JFORM=2, AORL and DM for JFORM=3) are not
  accessed.
- Each of the three element sets defines an unperturbed heliocentric
  orbit.  For a given epoch of observation, the position of the body
  in its orbit can be predicted from these elements, which are
  called "osculating elements", using standard two-body analytical
  solutions.  However, due to planetary perturbations, a given set
  of osculating elements remains usable for only as long as the
  unperturbed orbit that it describes is an adequate approximation
  to reality.  Attached to such a set of elements is a date called
  the "osculating epoch", at which the elements are, momentarily,
  a perfect representation of the instantaneous position and
  velocity of the body.

  Therefore, for any given problem there are up to three different
  epochs in play, and it is vital to distinguish clearly between
  them:

  . The epoch of observation:  the moment in time for which the
    position of the body is to be predicted.

  . The epoch defining the position of the body:  the moment in time
    at which, in the absence of purturbations, the specified
    position (mean longitude, mean anomaly, or perihelion) is
    reached.

  . The osculating epoch:  the moment in time at which the given
    elements are correct.

  For the major-planet and minor-planet cases it is usual to make
  the epoch that defines the position of the body the same as the
  epoch of osculation.  Thus, only two different epochs are
  involved:  the epoch of the elements and the epoch of observation.

  For comets, the epoch of perihelion fixes the position in the
  orbit and in general a different epoch of osculation will be
  chosen.  Thus, all three types of epoch are involved.

  For the present routine:

  . The epoch of observation is the argument DATE.

  . The epoch defining the position of the body is the argument
    EPOCH.

  . The osculating epoch is not used and is assumed to be close
    enough to the epoch of observation to deliver adequate accuracy.
    If not, a preliminary call to palPertel may be used to update
    the element-set (and its associated osculating epoch) by
    applying planetary perturbations.
- Two important sources for orbital elements are Horizons, operated
  by the Jet Propulsion Laboratory, Pasadena, and the Minor Planet
  Center, operated by the Center for Astrophysics, Harvard.

  The JPL Horizons elements (heliocentric, J2000 ecliptic and
  equinox) correspond to PAL/SLALIB arguments as follows.

   Major planets:

    JFORM  = 1
    EPOCH  = JDCT-2400000.5
    ORBINC = IN (in radians)
    ANODE  = OM (in radians)
    PERIH  = OM+W (in radians)
    AORQ   = A
    E      = EC
    AORL   = MA+OM+W (in radians)
    DM     = N (in radians)

    Epoch of osculation = JDCT-2400000.5

   Minor planets:

    JFORM  = 2
    EPOCH  = JDCT-2400000.5
    ORBINC = IN (in radians)
    ANODE  = OM (in radians)
    PERIH  = W (in radians)
    AORQ   = A
    E      = EC
    AORL   = MA (in radians)

    Epoch of osculation = JDCT-2400000.5

   Comets:

    JFORM  = 3
    EPOCH  = Tp-2400000.5
    ORBINC = IN (in radians)
    ANODE  = OM (in radians)
    PERIH  = W (in radians)
    AORQ   = QR
    E      = EC

    Epoch of osculation = JDCT-2400000.5

 The MPC elements correspond to SLALIB arguments as follows.

   Minor planets:

    JFORM  = 2
    EPOCH  = Epoch-2400000.5
    ORBINC = Incl. (in radians)
    ANODE  = Node (in radians)
    PERIH  = Perih. (in radians)
    AORQ   = a
    E      = e
    AORL   = M (in radians)

    Epoch of osculation = Epoch-2400000.5

  Comets:

    JFORM  = 3
    EPOCH  = T-2400000.5
    ORBINC = Incl. (in radians)
    ANODE  = Node. (in radians)
    PERIH  = Perih. (in radians)
    AORQ   = q
    E      = e

    Epoch of osculation = Epoch-2400000.5

    Raises
    ------
    ValueError: Illegal arguments
    ArithmeticError: Numerical error
    """
    cdef double ra
    cdef double dec
    cdef double r
    cdef int jstat

    cpal.palPlante(date, elong, phi, jform, epoch, orbinc, anode, perih, aorq,e, aorl, dm, &ra, &dec, &r, &jstat)
    if jstat == -1:
        raise ValueError( "Illegal jform" )
    elif jstat == -2:
        raise ValueError( "Illegal e" )
    elif jstat == -3:
        raise ValueError( "Illegal aorq" )
    elif jstat == -4:
        raise ValueError( "Illegal dm" )
    elif jstat == -5:
        raise ArithmeticError( "Numerical error" )
    return (ra, dec, r)

def plantu( double date, double elong, double phi, np.ndarray[double, ndim=1] u not None):
    """
    (ra, dec, r) = plantu( date, elong, phi, u )

Topocentric RA,Dec of a Solar-System object from universal elements

Arguments
---------
date = double (Given)
   TT MJD of observation (JD-2400000.5)
elong = double (Given)
   Observer's east longitude (radians)
phi = double (Given)
   Observer's geodetic latitude (radians)
u = const double [13] (Given)
   Universal orbital elements
     -   (0)  combined mass (M+m)
     -   (1)  total energy of the orbit (alpha)
     -   (2)  reference (osculating) epoch (t0)
     - (3-5)  position at reference epoch (r0)
     - (6-8)  velocity at reference epoch (v0)
     -   (9)  heliocentric distance at reference epoch
     -  (10)  r0.v0
     -  (11)  date (t)
     -  (12)  universal eccentric anomaly (psi) of date, approx
ra = double * (Returned)
   Topocentric apparent RA (radians)
dec = double * (Returned)
   Topocentric apparent Dec (radians)
r = double * (Returned)
   Distance from observer (AU)
jstat = int * (Returned)
   status: 0 = OK
        - -1 = radius vector zero
        - -2 = failed to converge


Notes
-----
- DATE is the instant for which the prediction is required.  It is
  in the TT timescale (formerly Ephemeris Time, ET) and is a
  Modified Julian Date (JD-2400000.5).
- The longitude and latitude allow correction for geocentric
  parallax.  This is usually a small effect, but can become
  important for near-Earth asteroids.  Geocentric positions can be
  generated by appropriate use of routines palEpv (or palEvp) and
  palUe2pv.
- The "universal" elements are those which define the orbit for the
  purposes of the method of universal variables (see reference 2).
  They consist of the combined mass of the two bodies, an epoch,
  and the position and velocity vectors (arbitrary reference frame)
  at that epoch.  The parameter set used here includes also various
  quantities that can, in fact, be derived from the other
  information.  This approach is taken to avoiding unnecessary
  computation and loss of accuracy.  The supplementary quantities
  are (i) alpha, which is proportional to the total energy of the
  orbit, (ii) the heliocentric distance at epoch, (iii) the
  outwards component of the velocity at the given epoch, (iv) an
  estimate of psi, the "universal eccentric anomaly" at a given
  date and (v) that date.
- The universal elements are with respect to the J2000 equator and
  equinox.

    Raises
    ------
    ValueError: Radius vector zero
    Arithmetic Error: Failed to converge
    """
    cdef double ra
    cdef double dec
    cdef double r
    cdef int jstat
    cdef double cu[13]

    for i in range(13):
        cu[i] = u[i]
    cpal.palPlantu( date, elong, phi, cu, &ra, &dec, &r, &jstat )
    if jstat == -1:
        raise ValueError( "Radius vector zero" )
    elif jstat == -2:
        raise ArithmeticError( "Failed to converge" )
    return (ra, dec, r )

def pm( double r0, double d0, double pr, double pd,
        double px, double rv, double ep0, double ep1 ):
     """
     (r1, d1) = pm( r0, d0, pr, pd, px, rv, ep0, ep1 )

Apply corrections for proper motion a star RA,Dec

Arguments
---------
r0 = double (Given)
   RA at epoch ep0 (radians)
d0 = double (Given)
   Dec at epoch ep0 (radians)
pr = double (Given)
   RA proper motion in radians per year.
pd = double (Given)
   Dec proper motion in radians per year.
px = double (Given)
   Parallax (arcsec)
rv = double (Given)
   Radial velocity (km/sec +ve if receding)
ep0 = double (Given)
   Start epoch in years, assumed to be Julian.
ep1 = double (Given)
   End epoch in years, assumed to be Julian.
r1 = double * (Returned)
   RA at epoch ep1 (radians)
d1 = double * (Returned)
   Dec at epoch ep1 (radians)


Notes
-----
- Uses eraStarpm but ignores the status returns from that routine.
  In particular note that parallax should not be zero when the
  proper motions are non-zero. SLA/F allows parallax to be zero.
- Assumes all epochs are Julian epochs.
     """
     cdef double r1
     cdef double d1
     cpal.palPm( r0, d0, pr, pd, px, rv, ep0, ep1, &r1, &d1 )
     return (r1, d1)

def pmVector( np.ndarray r0, np.ndarray d0, np.ndarray pr,
     np.ndarray pd, np.ndarray px, np.ndarray rv, double ep0,
     double ep1):
     """
     This is pm (see above), except that it accepts an
     ndarray of values for each argument
     """

     cdef int i
     cdef int length=len(r0)
     cdef np.ndarray r1out=np.zeros(length,dtype=np.float64)
     cdef np.ndarray d1out=np.zeros(length,dtype=np.float64)
     cdef double r1
     cdef double d1

     for i in range(length):
          cpal.palPm(r0[i],d0[i],pr[i],pd[i],px[i],rv[i],ep0,ep1,&r1,&d1)
          r1out[i]=r1
          d1out[i]=d1

     return(r1out,d1out)

def prebn( double bep0, double bep1 ):
     """
     rmatp = prebn( bep0, bep1 )

Generate the matrix of precession between two objects (old)

Arguments
---------
bep0 = double (Given)
   Beginning Besselian epoch.
bep1 = double (Given)
   Ending Besselian epoch
rmatp = double[3][3] (Returned)
   precession matrix in the sense V(BEP1) = RMATP * V(BEP0)
     """
     cdef double crmatp[3][3]
     cpal.palPrebn( bep0, bep1, crmatp )
     cdef np.ndarray rmatp = np.zeros( [3,3], dtype=np.float64 )
     for i in range(3):
          for j in range(3):
               rmatp[i,j] = crmatp[i][j]
     return rmatp

def prec( double ep0, double ep1 ):
     """
     rmatp = prec( ep0, ep1 )

Form the matrix of precession between two epochs (IAU 2006)

Arguments
---------
ep0 = double (Given)
   Beginning epoch
ep1 = double (Given)
   Ending epoch
rmatp = double[3][3] (Returned)
   Precession matrix
     """
     cdef double crmatp[3][3]
     cpal.palPrec( ep0, ep1, crmatp )
     cdef np.ndarray rmatp = np.zeros( [3,3], dtype=np.float64 )
     for i in range(3):
          for j in range(3):
               rmatp[i,j] = crmatp[i][j]
     return rmatp

def preces( sys, double ep0, double ep1, double ra, double dc ):
     """
     (ra, dc) = preces( sys, ep0, ep1, ra, dec)

Precession - either FK4 or FK5 as required.

Arguments
---------
sys = const char [3] (Given)
   Precession to be applied: FK4 or FK5. Case insensitive.
ep0 = double (Given)
   Starting epoch.
ep1 = double (Given)
   Ending epoch
ra = double * (Given & Returned)
   On input the RA mean equator & equinox at epoch ep0. On exit
   the RA mean equator & equinox of epoch ep1.
dec = double * (Given & Returned)
   On input the dec mean equator & equinox at epoch ep0. On exit
   the dec mean equator & equinox of epoch ep1.


Notes
-----
- Uses palPrec for FK5 data and palPrebn for FK4 data.
- The epochs are Besselian if SYSTEM='FK4' and Julian if 'FK5'.
   For example, to precess coordinates in the old system from
   equinox 1900.0 to 1950.0 the call would be:
        palPreces( "FK4", 1900.0, 1950.0, &ra, &dc );
- This routine will NOT correctly convert between the old and
  the new systems - for example conversion from B1950 to J2000.
  For these purposes see palFk425, palFk524, palFk45z and
  palFk54z.
- If an invalid SYSTEM is supplied, values of -99D0,-99D0 will
  be returned for both RA and DC.
     """
     byte_string = sys.encode('ascii')
     cdef char * csys = byte_string
     cpal.palPreces( csys, ep0, ep1, &ra, &dc )
     return (ra, dc)

def prenut( double epoch, double date):
    """
    rmatpn = prenut( epoch, date )

Form the matrix of bias-precession-nutation (IAU 2006/2000A)

Arguments
---------
epoch = double (Returned)
   Julian epoch for mean coordinates.
date = double (Returned)
   Modified Julian Date (JD-2400000.5) for true coordinates.
rmatpn = double[3][3] (Returned)
   combined NPB matrix
    """
    cdef double crmatpn[3][3]
    cpal.palPrenut( epoch, date, crmatpn )
    cdef np.ndarray rmatpn = np.zeros( [3,3], dtype=np.float64 )
    for i in range(3):
        for j in range(3):
            rmatpn[i,j]=crmatpn[i][j]
    return rmatpn

def pv2el(np.ndarray[double, ndim=1] pv not None, double date, double pmass, int jformr):
    """
    (jform, epoch, orbinc, anode, perih, aorq, e, aorl, dm) = pv2el( pv, date, pmass, jformr )

Position velocity to heliocentirc osculating elements

Arguments
---------
pv = const double [6] (Given)
   Heliocentric x,y,z,xdot,ydot,zdot of date,
   J2000 equatorial triad (AU,AU/s; Note 1)
date = double (Given)
   Date (TT Modified Julian Date = JD-2400000.5)
pmass = double (Given)
   Mass of the planet (Sun=1; Note 2)
jformr = int (Given)
   Requested element set (1-3; Note 3)
jform = int * (Returned)
   Element set actually returned (1-3; Note 4)
epoch = double * (Returned)
   Epoch of elements (TT MJD)
orbinc = double * (Returned)
   inclination (radians)
anode = double * (Returned)
   longitude of the ascending node (radians)
perih = double * (Returned)
   longitude or argument of perihelion (radians)
aorq = double * (Returned)
   mean distance or perihelion distance (AU)
e = double * (Returned)
   eccentricity
aorl = double * (Returned)
   mean anomaly or longitude (radians, JFORM=1,2 only)
dm = double * (Returned)
   daily motion (radians, JFORM=1 only)
jstat = int * (Returned)
   status:  0 = OK
          - -1 = illegal PMASS
          - -2 = illegal JFORMR
          - -3 = position/velocity out of range


Notes
-----
- The PV 6-vector is with respect to the mean equator and equinox of
  epoch J2000.  The orbital elements produced are with respect to
  the J2000 ecliptic and mean equinox.
- The mass, PMASS, is important only for the larger planets.  For
  most purposes (e.g. asteroids) use 0D0.  Values less than zero
  are illegal.
- Three different element-format options are supported:

  Option JFORM=1, suitable for the major planets:

  EPOCH  = epoch of elements (TT MJD)
  ORBINC = inclination i (radians)
  ANODE  = longitude of the ascending node, big omega (radians)
  PERIH  = longitude of perihelion, curly pi (radians)
  AORQ   = mean distance, a (AU)
  E      = eccentricity, e
  AORL   = mean longitude L (radians)
  DM     = daily motion (radians)

  Option JFORM=2, suitable for minor planets:

  EPOCH  = epoch of elements (TT MJD)
  ORBINC = inclination i (radians)
  ANODE  = longitude of the ascending node, big omega (radians)
  PERIH  = argument of perihelion, little omega (radians)
  AORQ   = mean distance, a (AU)
  E      = eccentricity, e
  AORL   = mean anomaly M (radians)

  Option JFORM=3, suitable for comets:

  EPOCH  = epoch of perihelion (TT MJD)
  ORBINC = inclination i (radians)
  ANODE  = longitude of the ascending node, big omega (radians)
  PERIH  = argument of perihelion, little omega (radians)
  AORQ   = perihelion distance, q (AU)
  E      = eccentricity, e

- It may not be possible to generate elements in the form
  requested through JFORMR.  The caller is notified of the form
  of elements actually returned by means of the JFORM argument:
   JFORMR   JFORM     meaning

     1        1       OK - elements are in the requested format
     1        2       never happens
     1        3       orbit not elliptical

     2        1       never happens
     2        2       OK - elements are in the requested format
     2        3       orbit not elliptical

     3        1       never happens
     3        2       never happens
     3        3       OK - elements are in the requested format

- The arguments returned for each value of JFORM (cf Note 5: JFORM
  may not be the same as JFORMR) are as follows:

    JFORM         1              2              3
    EPOCH         t0             t0             T
    ORBINC        i              i              i
    ANODE         Omega          Omega          Omega
    PERIH         curly pi       omega          omega
    AORQ          a              a              q
    E             e              e              e
    AORL          L              M              -
    DM            n              -              -

  where:

    t0           is the epoch of the elements (MJD, TT)
    T              "    epoch of perihelion (MJD, TT)
    i              "    inclination (radians)
    Omega          "    longitude of the ascending node (radians)
    curly pi       "    longitude of perihelion (radians)
    omega          "    argument of perihelion (radians)
    a              "    mean distance (AU)
    q              "    perihelion distance (AU)
    e              "    eccentricity
    L              "    longitude (radians, 0-2pi)
    M              "    mean anomaly (radians, 0-2pi)
    n              "    daily motion (radians)
    -             means no value is set

- At very small inclinations, the longitude of the ascending node
  ANODE becomes indeterminate and under some circumstances may be
  set arbitrarily to zero.  Similarly, if the orbit is close to
  circular, the true anomaly becomes indeterminate and under some
  circumstances may be set arbitrarily to zero.  In such cases,
  the other elements are automatically adjusted to compensate,
  and so the elements remain a valid description of the orbit.
- The osculating epoch for the returned elements is the argument
  DATE.

- Reference:  Sterne, Theodore E., "An Introduction to Celestial
              Mechanics", Interscience Publishers, 1960

    Raises
    ------
    ValueError: Illegal arguments
    """
    cdef int jform
    cdef double epoch
    cdef double orbinc
    cdef double anode
    cdef double perih
    cdef double aorq
    cdef double e
    cdef double aorl
    cdef double dm
    cdef int jstat
    cdef double cpv[6]

    for i in range(6):
        cpv[i] = pv[i]
    cpal.palPv2el( cpv, date, pmass, jformr, &jform, &epoch, &orbinc, &anode, &perih,
                   &aorq, &e, &aorl, &dm, &jstat )
    if jstat == -1:
        raise ValueError( "Illegal PMASS" )
    elif jstat == -2:
        raise ValueError( "Illegal JFORMR" )
    elif jstat == -3:
        raise ValueError( "Position/velocity out of range" )
    return (jform, epoch, orbinc, anode, perih, aorq, e, aorl, dm)

def pv2ue( np.ndarray[double, ndim=1] pv not None, double date, double pmass ):
    """
    u = pv2ue( pv, date, pmass )

Universal elements to position and velocity.

Arguments
---------
pv = double [6] (Given)
   Heliocentric x,y,z,xdot,ydot,zdot of date, (AU,AU/s; Note 1)
date = double (Given)
   Date (TT modified Julian Date = JD-2400000.5)
pmass = double (Given)
   Mass of the planet (Sun=1; note 2)
u = double [13] (Returned)
   Universal orbital elements (Note 3)

     -  (0)  combined mass (M+m)
     -   (1)  total energy of the orbit (alpha)
     -   (2)  reference (osculating) epoch (t0)
     - (3-5)  position at reference epoch (r0)
     - (6-8)  velocity at reference epoch (v0)
     -   (9)  heliocentric distance at reference epoch
     -  (10)  r0.v0
     -  (11)  date (t)
     -  (12)  universal eccentric anomaly (psi) of date, approx
jstat = int * (Returned)
   status: 0 = OK
          - -1 = illegal PMASS
          - -2 = too close to Sun
          - -3 = too slow


Notes
-----
- The PV 6-vector can be with respect to any chosen inertial frame,
  and the resulting universal-element set will be with respect to
  the same frame.  A common choice will be mean equator and ecliptic
  of epoch J2000.
- The mass, PMASS, is important only for the larger planets.  For
  most purposes (e.g. asteroids) use 0D0.  Values less than zero
  are illegal.
- The "universal" elements are those which define the orbit for the
  purposes of the method of universal variables (see reference).
  They consist of the combined mass of the two bodies, an epoch,
  and the position and velocity vectors (arbitrary reference frame)
  at that epoch.  The parameter set used here includes also various
  quantities that can, in fact, be derived from the other
  information.  This approach is taken to avoiding unnecessary
  computation and loss of accuracy.  The supplementary quantities
  are (i) alpha, which is proportional to the total energy of the
  orbit, (ii) the heliocentric distance at epoch, (iii) the
  outwards component of the velocity at the given epoch, (iv) an
  estimate of psi, the "universal eccentric anomaly" at a given
  date and (v) that date.
- Reference:  Everhart, E. & Pitkin, E.T., Am.J.Phys. 51, 712, 1983.

    Raises
    ------
    ValueError: Illegal arguments
    """
    cdef int jstat
    cdef double cu[13]
    cdef double cpv[6]

    for i in range(6):
        cpv[i] = pv[i]
    cpal.palPv2ue( cpv, date, pmass, cu, &jstat )
    if jstat == -1:
        raise ValueError( "Illegal PMASS" )
    elif jstat == -2:
        raise ValueError( "Too close to Sun" )
    elif jstat == -3:
        raise ValueError( "Too slow" )

    cdef np.ndarray u = np.zeros( [13], dtype=np.float64 )
    for i in range(13):
        u[i] = cu[i]
    return u

def pvobs( double p, double h, double stl ):
     """
     pv = pvobs( p, h, stl )

Position and velocity of an observing station.

Arguments
---------
p = double (Given)
   Latitude (geodetic, radians).
h = double (Given)
   Height above reference spheroid (geodetic, metres).
stl = double (Given)
   Local apparent sidereal time (radians).
pv = double[ 6 ] (Returned)
   position/velocity 6-vector (AU, AU/s, true equator
                               and equinox of date).


Notes
-----
- The WGS84 reference ellipsoid is used.
     """
     cdef double cpv[6]
     cpal.palPvobs( p, h, stl, cpv )
     cdef np.ndarray pv = np.zeros( [6], dtype=np.float64 )
     for i in range(6):
          pv[i] = cpv[i]
     return pv

def rdplan( double date, int np, double elong, double phi ):
    """
    (ra, dec, diam) = rdplan( date, np, elong, phi )

Approximate topocentric apparent RA,Dec of a planet

Arguments
---------
date = double (Given)
   MJD of observation (JD-2400000.5) in TDB. For all practical
   purposes TT can be used instead of TDB, and for many applications
   UT will do (except for the Moon).
np = int (Given)
   Planet: 1 = Mercury
           2 = Venus
           3 = Moon
           4 = Mars
           5 = Jupiter
           6 = Saturn
           7 = Uranus
           8 = Neptune
        else = Sun
elong = double (Given)
   Observer's east longitude (radians)
phi = double (Given)
   Observer's geodetic latitude (radians)
ra = double * (Returned)
   RA (topocentric apparent, radians)
dec = double * (Returned)
   Dec (topocentric apparent, radians)
diam = double * (Returned)
   Angular diameter (equatorial, radians)


Notes
-----
- Unlike with slaRdplan, Pluto is not supported.
- The longitude and latitude allow correction for geocentric
  parallax.  This is a major effect for the Moon, but in the
  context of the limited accuracy of the present routine its
  effect on planetary positions is small (negligible for the
  outer planets).  Geocentric positions can be generated by
  appropriate use of the routines palDmoon and eraPlan94.
    """
    cdef double ra
    cdef double dec
    cdef double diam
    cpal.palRdplan( date, np, elong, phi, &ra, &dec, &diam )
    return (ra, dec, diam)

def refco( double hm, double tdk, double pmb, double rh, double wl, double phi, double tlr, double eps):
    """
    (refa, refb) = refco( hm, tdk, pmb, rh, wl, phi, tlr, eps )

Determine constants in atmospheric refraction model

Arguments
---------
hm = double (Given)
   Height of the observer above sea level (metre)
tdk = double (Given)
   Ambient temperature at the observer (K)
pmb = double (Given)
   Pressure at the observer (millibar)
rh = double (Given)
   Relative humidity at the observer (range 0-1)
wl = double (Given)
   Effective wavelength of the source (micrometre)
phi = double (Given)
   Latitude of the observer (radian, astronomical)
tlr = double (Given)
   Temperature lapse rate in the troposphere (K/metre)
eps = double (Given)
   Precision required to terminate iteration (radian)
refa = double * (Returned)
   tan Z coefficient (radian)
refb = double * (Returned)
   tan**3 Z coefficient (radian)


Notes
-----
- Typical values for the TLR and EPS arguments might be 0.0065 and
1E-10 respectively.

- The radio refraction is chosen by specifying WL > 100 micrometres.

- The routine is a slower but more accurate alternative to the
palRefcoq routine.  The constants it produces give perfect
agreement with palRefro at zenith distances arctan(1) (45 deg)
and arctan(4) (about 76 deg).  It achieves 0.5 arcsec accuracy
for ZD < 80 deg, 0.01 arcsec accuracy for ZD < 60 deg, and
0.001 arcsec accuracy for ZD < 45 deg.
    """
    cdef double refa
    cdef double refb
    cpal.palRefco(hm,tdk,pmb,rh,wl,phi,tlr,eps,&refa,&refb)
    return (refa,refb)

def refcoq( double tdk, double pmb, double rh, double wl):
    """
    (refa, refb) = refcoq( tdk, pmb, rh, wl )

Determine the constants A and B in the atmospheric refraction model

Arguments
---------
tdk = double (Given)
   Ambient temperature at the observer (K)
pmb = double (Given)
   Pressure at the observer (millibar)
rh =  double (Given)
   Relative humidity at the observer (range 0-1)
wl =  double (Given)
   Effective wavelength of the source (micrometre).
   Radio refraction is chosen by specifying wl > 100 micrometres.
refa = double * (Returned)
   tan Z coefficient (radian)
refb = double * (Returned)
   tan**3 Z coefficient (radian)


Notes
-----
- Uses eraRefco(). See SOFA/ERFA documentation for details.
- Note that the SOFA/ERFA routine uses different order of
  of arguments and uses deg C rather than K.
    """
    cdef double refa
    cdef double refb
    cpal.palRefcoq( tdk, pmb, rh, wl, &refa, &refb )
    return (refa, refb)

def refro( double zobs, double hm, double tdk, double pmb,
           double rh, double wl, double phi, double tlr, double eps):
    """
    ref = refro( zobs, hm, tdk, pmb, rh, wl, phi, tlr, eps )

Atmospheric refraction for radio and optical/IR wavelengths

Arguments
---------
zobs = double (Given)
   Observed zenith distance of the source (radian)
hm = double (Given)
   Height of the observer above sea level (metre)
tdk = double (Given)
   Ambient temperature at the observer (K)
pmb = double (Given)
   Pressure at the observer (millibar)
rh = double (Given)
   Relative humidity at the observer (range 0-1)
wl = double (Given)
   Effective wavelength of the source (micrometre)
phi = double (Given)
   Latitude of the observer (radian, astronomical)
tlr = double (Given)
   Temperature lapse rate in the troposphere (K/metre)
eps = double (Given)
   Precision required to terminate iteration (radian)
ref = double * (Returned)
   Refraction: in vacuao ZD minus observed ZD (radian)


Notes
-----
- A suggested value for the TLR argument is 0.0065.  The
refraction is significantly affected by TLR, and if studies
of the local atmosphere have been carried out a better TLR
value may be available.  The sign of the supplied TLR value
is ignored.

- A suggested value for the EPS argument is 1E-8.  The result is
usually at least two orders of magnitude more computationally
precise than the supplied EPS value.

- The routine computes the refraction for zenith distances up
to and a little beyond 90 deg using the method of Hohenkerk
and Sinclair (NAO Technical Notes 59 and 63, subsequently adopted
in the Explanatory Supplement, 1992 edition - see section 3.281).

- The code is a development of the optical/IR refraction subroutine
AREF of C.Hohenkerk (HMNAO, September 1984), with extensions to
support the radio case.  Apart from merely cosmetic changes, the
following modifications to the original HMNAO optical/IR refraction
code have been made:

.  The angle arguments have been changed to radians.

.  Any value of ZOBS is allowed (see note 6, below).

.  Other argument values have been limited to safe values.

.  Murray's values for the gas constants have been used
   (Vectorial Astrometry, Adam Hilger, 1983).

.  The numerical integration phase has been rearranged for
   extra clarity.

.  A better model for Ps(T) has been adopted (taken from
   Gill, Atmosphere-Ocean Dynamics, Academic Press, 1982).

.  More accurate expressions for Pwo have been adopted
   (again from Gill 1982).

.  The formula for the water vapour pressure, given the
   saturation pressure and the relative humidity, is from
   Crane (1976), expression 2.5.5.
.  Provision for radio wavelengths has been added using
   expressions devised by A.T.Sinclair, RGO (private
   communication 1989).  The refractivity model currently
   used is from J.M.Rueger, "Refractive Index Formulae for
   Electronic Distance Measurement with Radio and Millimetre
   Waves", in Unisurv Report S-68 (2002), School of Surveying
   and Spatial Information Systems, University of New South
   Wales, Sydney, Australia.

.  The optical refractivity for dry air is from Resolution 3 of
   the International Association of Geodesy adopted at the XXIIth
   General Assembly in Birmingham, UK, 1999.

.  Various small changes have been made to gain speed.

- The radio refraction is chosen by specifying WL > 100 micrometres.
Because the algorithm takes no account of the ionosphere, the
accuracy deteriorates at low frequencies, below about 30 MHz.

- Before use, the value of ZOBS is expressed in the range +/- pi.
If this ranged ZOBS is -ve, the result REF is computed from its
absolute value before being made -ve to match.  In addition, if
it has an absolute value greater than 93 deg, a fixed REF value
equal to the result for ZOBS = 93 deg is returned, appropriately
signed.

- As in the original Hohenkerk and Sinclair algorithm, fixed values
of the water vapour polytrope exponent, the height of the
tropopause, and the height at which refraction is negligible are
used.

- The radio refraction has been tested against work done by
Iain Coulson, JACH, (private communication 1995) for the
James Clerk Maxwell Telescope, Mauna Kea.  For typical conditions,
agreement at the 0.1 arcsec level is achieved for moderate ZD,
worsening to perhaps 0.5-1.0 arcsec at ZD 80 deg.  At hot and
humid sea-level sites the accuracy will not be as good.

- It should be noted that the relative humidity RH is formally
defined in terms of "mixing ratio" rather than pressures or
densities as is often stated.  It is the mass of water per unit
mass of dry air divided by that for saturated air at the same
temperature and pressure (see Gill 1982).
- The algorithm is designed for observers in the troposphere. The
supplied temperature, pressure and lapse rate are assumed to be
for a point in the troposphere and are used to define a model
atmosphere with the tropopause at 11km altitude and a constant
temperature above that.  However, in practice, the refraction
values returned for stratospheric observers, at altitudes up to
25km, are quite usable.
    """
    cdef double ref
    cpal.palRefro(zobs, hm, tdk, pmb, rh, wl, phi, tlr, eps, &ref)
    return ref

def refv( np.ndarray[ double, ndim=1] vu not None, double refa, double refb):
    """
    vr = refv( vu, refa, refb )

Adjust an unrefracted Cartesian vector to include the effect of atmospheric refraction

Arguments
---------
vu[3] = double (Given)
   Unrefracted position of the source (Az/El 3-vector)
refa = double (Given)
   tan Z coefficient (radian)
refb = double (Given)
   tan**3 Z coefficient (radian)
vr[3] = double (Returned)
   Refracted position of the source (Az/El 3-vector)


Notes
-----
- This routine applies the adjustment for refraction in the
opposite sense to the usual one - it takes an unrefracted
(in vacuo) position and produces an observed (refracted)
position, whereas the A tan Z + B tan**3 Z model strictly
applies to the case where an observed position is to have the
refraction removed.  The unrefracted to refracted case is
harder, and requires an inverted form of the text-book
refraction models;  the algorithm used here is equivalent to
one iteration of the Newton-Raphson method applied to the above
formula.

- Though optimized for speed rather than precision, the present
routine achieves consistency with the refracted-to-unrefracted
A tan Z + B tan**3 Z model at better than 1 microarcsecond within
30 degrees of the zenith and remains within 1 milliarcsecond to
beyond ZD 70 degrees.  The inherent accuracy of the model is, of
course, far worse than this - see the documentation for palRefco
for more information.

- At low elevations (below about 3 degrees) the refraction
correction is held back to prevent arithmetic problems and
wildly wrong results.  For optical/IR wavelengths, over a wide
range of observer heights and corresponding temperatures and
pressures, the following levels of accuracy (arcsec, worst case)
are achieved, relative to numerical integration through a model
atmosphere:

         ZD    error

         80      0.7
         81      1.3
         82      2.5
         83      5
         84     10
         85     20
         86     55
         87    160
         88    360
         89    640
         90   1100
         91   1700         } relevant only to
         92   2600         } high-elevation sites

The results for radio are slightly worse over most of the range,
becoming significantly worse below ZD=88 and unusable beyond
ZD=90.

- See also the routine palRefz, which performs the adjustment to
the zenith distance rather than in Cartesian Az/El coordinates.
The present routine is faster than palRefz and, except very low down,
is equally accurate for all practical purposes.  However, beyond
about ZD 84 degrees palRefz should be used, and for the utmost
accuracy iterative use of palRefro should be considered.
    """
    cdef double cvr[3]
    cdef double cvu[3]
    cdef np.ndarray vr = np.zeros( [3], dtype=np.float64)
    for i in range(3):
        cvu[i] = vu[i]
    cpal.palRefv( cvu, refa, refb, cvr )
    for i in range(3):
        vr[i] = cvr[i]
    return vr

def refz( double zu, double refa, double refb ):
    """
    zr = refz( zu, refa, refb )

Adjust unrefracted zenith distance

Arguments
---------
zu = double (Given)
    Unrefracted zenith distance of the source (radians)
refa = double (Given)
    tan Z coefficient (radians)
refb = double (Given)
    tan**3 Z coefficient (radian)
zr = double * (Returned)
    Refracted zenith distance (radians)


Notes
-----
- This routine applies the adjustment for refraction in the
opposite sense to the usual one - it takes an unrefracted
(in vacuo) position and produces an observed (refracted)
position, whereas the A tan Z + B tan**3 Z model strictly
applies to the case where an observed position is to have the
refraction removed.  The unrefracted to refracted case is
harder, and requires an inverted form of the text-book
refraction models;  the formula used here is based on the
Newton-Raphson method.  For the utmost numerical consistency
with the refracted to unrefracted model, two iterations are
carried out, achieving agreement at the 1D-11 arcseconds level
for a ZD of 80 degrees.  The inherent accuracy of the model
is, of course, far worse than this - see the documentation for
palRefco for more information.

- At ZD 83 degrees, the rapidly-worsening A tan Z + B tan^3 Z
model is abandoned and an empirical formula takes over.  For
optical/IR wavelengths, over a wide range of observer heights and
corresponding temperatures and pressures, the following levels of
accuracy (arcsec, worst case) are achieved, relative to numerical
integration through a model atmosphere:

         ZR    error

         80      0.7
         81      1.3
         82      2.4
         83      4.7
         84      6.2
         85      6.4
         86      8
         87     10
         88     15
         89     30
         90     60
         91    150         } relevant only to
         92    400         } high-elevation sites

For radio wavelengths the errors are typically 50% larger than
the optical figures and by ZD 85 deg are twice as bad, worsening
rapidly below that.  To maintain 1 arcsec accuracy down to ZD=85
at the Green Bank site, Condon (2004) has suggested amplifying
the amount of refraction predicted by palRefz below 10.8 deg
elevation by the factor (1+0.00195*(10.8-E_t)), where E_t is the
unrefracted elevation in degrees.

The high-ZD model is scaled to match the normal model at the
transition point;  there is no glitch.

- Beyond 93 deg zenith distance, the refraction is held at its
93 deg value.

- See also the routine palRefv, which performs the adjustment in
Cartesian Az/El coordinates, and with the emphasis on speed
rather than numerical accuracy.
    """
    cdef double zr
    cpal.palRefz(zu,refa,refb,&zr)
    return zr

def rverot( double phi, double ra, double da, double st ):
     """
     r = rverot( phi, ra, da, st )

Velocity component in a given direction due to Earth rotation

Arguments
---------
phi = double (Given)
   latitude of observing station (geodetic) (radians)
ra = double (Given)
   apparent RA (radians)
da = double (Given)
   apparent Dec (radians)
st = double (Given)
   Local apparent sidereal time.


Returned Value
--------------
palRverot = double
   Component of Earth rotation in direction RA,DA (km/s).
   The result is +ve when the observatory is receding from the
   given point on the sky.
     """
     return cpal.palRverot( phi, ra, da, st )

def rvgalc( double r2000, double d2000 ):
     """
     rv = rvgalc( r2000, d2000 )

Velocity component in a given direction due to the rotation
of the Galaxy.

Arguments
---------
r2000 = double (Given)
   J2000.0 mean RA (radians)
d2000 = double (Given)
   J2000.0 mean Dec (radians)


Returned Value
--------------
Component of dynamical LSR motion in direction R2000,D2000 (km/s).


Notes
-----
- The Local Standard of Rest used here is a point in the
vicinity of the Sun which is in a circular orbit around
the Galactic centre.  Sometimes called the "dynamical" LSR,
it is not to be confused with a "kinematical" LSR, which
is the mean standard of rest of star catalogues or stellar
populations.

     """
     return cpal.palRvgalc( r2000, d2000 )

def rvlg( double r2000, double d2000 ):
     """
     rv = rvlg( r2000, d2000 )

Velocity component in a given direction due to Galactic rotation
and motion of the local group.

Arguments
---------
r2000 = double (Given)
   J2000.0 mean RA (radians)
d2000 = double (Given)
   J2000.0 mean Dec (radians)


Returned Value
--------------
Component of SOLAR motion in direction R2000,D2000 (km/s).
     """
     return cpal.palRvlg( r2000, d2000 )

def rvlsrd( double r2000, double d2000 ):
     """
     rv = rvlsrd( r2000, d2000 )

Velocity component in a given direction due to the Sun's motion
with respect to the dynamical Local Standard of Rest.

Arguments
---------
r2000 = double (Given)
   J2000.0 mean RA (radians)
d2000 = double (Given)
   J2000.0 mean Dec (radians)


Returned Value
--------------
Component of "peculiar" solar motion in direction R2000,D2000 (km/s).


Notes
-----
- The Local Standard of Rest used here is the "dynamical" LSR,
a point in the vicinity of the Sun which is in a circular orbit
around the Galactic centre.  The Sun's motion with respect to the
dynamical LSR is called the "peculiar" solar motion.
- There is another type of LSR, called a "kinematical" LSR.  A
kinematical LSR is the mean standard of rest of specified star
catalogues or stellar populations, and several slightly different
kinematical LSRs are in use.  The Sun's motion with respect to an
agreed kinematical LSR is known as the "standard" solar motion.
To obtain a radial velocity correction with respect to an adopted
kinematical LSR use the routine palRvlsrk.
     """
     return cpal.palRvlsrd( r2000, d2000 )

def rvlsrk( double r2000, double d2000 ):
     """
     rv = rvlsrk( r2000, d2000 )

Velocity component in a given direction due to the Sun's motion
with respect to an adopted kinematic Local Standard of Rest.

Arguments
---------
r2000 = double (Given)
   J2000.0 mean RA (radians)
d2000 = double (Given)
   J2000.0 mean Dec (radians)


Returned Value
--------------
Component of "standard" solar motion in direction R2000,D2000 (km/s).


Notes
-----
- The Local Standard of Rest used here is one of several
"kinematical" LSRs in common use.  A kinematical LSR is the mean
standard of rest of specified star catalogues or stellar
populations.  The Sun's motion with respect to a kinematical LSR
is known as the "standard" solar motion.
- There is another sort of LSR, the "dynamical" LSR, which is a
point in the vicinity of the Sun which is in a circular orbit
around the Galactic centre.  The Sun's motion with respect to
the dynamical LSR is called the "peculiar" solar motion.  To
obtain a radial velocity correction with respect to the
dynamical LSR use the routine palRvlsrd.
     """
     return cpal.palRvlsrk( r2000, d2000 )

def subet( double rc, double dc, double eq ):
     """
     (rm, dm) = subet( rc, dc, eq )

Remove the E-terms from a pre IAU 1976 catalogue RA,Dec

Arguments
---------
rc = double (Given)
   RA with E-terms included (radians)
dc = double (Given)
   Dec with E-terms included (radians)
eq = double (Given)
   Besselian epoch of mean equator and equinox
rm = double * (Returned)
   RA without E-terms (radians)
dm = double * (Returned)
   Dec without E-terms (radians)


Notes
-----
Most star positions from pre-1984 optical catalogues (or
derived from astrometry using such stars) embody the
E-terms.  This routine converts such a position to a
formal mean place (allowing, for example, comparison with a
pulsar timing position).
     """
     cdef double rm
     cdef double dm
     cpal.palSubet( rc, dc, eq, &rm, &dm )
     return ( rm, dm )

def supgal( double dsl, double dsb ):
     """
     (dl, db) = supgal( dsl, dsb )

Convert from supergalactic to galactic coordinates

Arguments
---------
dsl = double (Given)
  Supergalactic longitude.
dsb = double (Given)
  Supergalactic latitude.
dl = double * (Returned)
  Galactic longitude.
db = double * (Returned)
  Galactic latitude.
     """
     cdef double dl
     cdef double db
     cpal.palSupgal( dsl, dsb, &dl, &db )
     return (dl, db)

def ue2el(np.ndarray[double, ndim=1] u not None, int jformr ):
    """
    (jform, epoch, orbinc, anode, perih, aorq, e, aorl, dm) = ue2el( u, jformr )

Universal elements to heliocentric osculating elements

Arguments
---------
u = const double [13] (Given)
   Universal orbital elements (Note 1)
       (0)  combined mass (M+m)
       (1)  total energy of the orbit (alpha)
       (2)  reference (osculating) epoch (t0)
     (3-5)  position at reference epoch (r0)
     (6-8)  velocity at reference epoch (v0)
       (9)  heliocentric distance at reference epoch
      (10)  r0.v0
      (11)  date (t)
      (12)  universal eccentric anomaly (psi) of date, approx
jformr = int (Given)
   Requested element set (1-3; Note 3)
jform = int * (Returned)
   Element set actually returned (1-3; Note 4)
epoch = double * (Returned)
   Epoch of elements (TT MJD)
orbinc = double * (Returned)
   inclination (radians)
anode = double * (Returned)
   longitude of the ascending node (radians)
perih = double * (Returned)
   longitude or argument of perihelion (radians)
aorq = double * (Returned)
   mean distance or perihelion distance (AU)
e = double * (Returned)
   eccentricity
aorl = double * (Returned)
   mean anomaly or longitude (radians, JFORM=1,2 only)
dm = double * (Returned)
   daily motion (radians, JFORM=1 only)
jstat = int * (Returned)
   status:  0 = OK
           -1 = illegal combined mass
           -2 = illegal JFORMR
           -3 = position/velocity out of range


Notes
-----
- The "universal" elements are those which define the orbit for the
  purposes of the method of universal variables (see reference 2).
  They consist of the combined mass of the two bodies, an epoch,
  and the position and velocity vectors (arbitrary reference frame)
  at that epoch.  The parameter set used here includes also various
  quantities that can, in fact, be derived from the other
  information.  This approach is taken to avoiding unnecessary
  computation and loss of accuracy.  The supplementary quantities
  are (i) alpha, which is proportional to the total energy of the
  orbit, (ii) the heliocentric distance at epoch, (iii) the
  outwards component of the velocity at the given epoch, (iv) an
  estimate of psi, the "universal eccentric anomaly" at a given
  date and (v) that date.
- The universal elements are with respect to the mean equator and
  equinox of epoch J2000.  The orbital elements produced are with
  respect to the J2000 ecliptic and mean equinox.
- Three different element-format options are supported:

   Option JFORM=1, suitable for the major planets:

   EPOCH  = epoch of elements (TT MJD)
   ORBINC = inclination i (radians)
   ANODE  = longitude of the ascending node, big omega (radians)
   PERIH  = longitude of perihelion, curly pi (radians)
   AORQ   = mean distance, a (AU)
   E      = eccentricity, e
   AORL   = mean longitude L (radians)
   DM     = daily motion (radians)

   Option JFORM=2, suitable for minor planets:

   EPOCH  = epoch of elements (TT MJD)
   ORBINC = inclination i (radians)
   ANODE  = longitude of the ascending node, big omega (radians)
   PERIH  = argument of perihelion, little omega (radians)
   AORQ   = mean distance, a (AU)
   E      = eccentricity, e
   AORL   = mean anomaly M (radians)

   Option JFORM=3, suitable for comets:

   EPOCH  = epoch of perihelion (TT MJD)
   ORBINC = inclination i (radians)
   ANODE  = longitude of the ascending node, big omega (radians)
   PERIH  = argument of perihelion, little omega (radians)
   AORQ   = perihelion distance, q (AU)
   E      = eccentricity, e

- It may not be possible to generate elements in the form
  requested through JFORMR.  The caller is notified of the form
  of elements actually returned by means of the JFORM argument:

   JFORMR   JFORM     meaning

     1        1       OK - elements are in the requested format
     1        2       never happens
     1        3       orbit not elliptical

     2        1       never happens
     2        2       OK - elements are in the requested format
     2        3       orbit not elliptical

     3        1       never happens
     3        2       never happens
     3        3       OK - elements are in the requested format

- The arguments returned for each value of JFORM (cf Note 6: JFORM
  may not be the same as JFORMR) are as follows:

    JFORM         1              2              3
    EPOCH         t0             t0             T
    ORBINC        i              i              i
    ANODE         Omega          Omega          Omega
    PERIH         curly pi       omega          omega
    AORQ          a              a              q
    E             e              e              e
    AORL          L              M              -
    DM            n              -              -

where:

    t0           is the epoch of the elements (MJD, TT)
    T              "    epoch of perihelion (MJD, TT)
    i              "    inclination (radians)
    Omega          "    longitude of the ascending node (radians)
    curly pi       "    longitude of perihelion (radians)
    omega          "    argument of perihelion (radians)
    a              "    mean distance (AU)
    q              "    perihelion distance (AU)
    e              "    eccentricity
    L              "    longitude (radians, 0-2pi)
    M              "    mean anomaly (radians, 0-2pi)
    n              "    daily motion (radians)
    -             means no value is set

- At very small inclinations, the longitude of the ascending node
  ANODE becomes indeterminate and under some circumstances may be
  set arbitrarily to zero.  Similarly, if the orbit is close to
  circular, the true anomaly becomes indeterminate and under some
  circumstances may be set arbitrarily to zero.  In such cases,
  the other elements are automatically adjusted to compensate,
  and so the elements remain a valid description of the orbit.

    Raises
    ------
    ValueError: Illegal arguments
    """
    cdef int jform
    cdef double epoch
    cdef double orbinc
    cdef double anode
    cdef double perih
    cdef double aorq
    cdef double e
    cdef double aorl
    cdef double dm
    cdef int jstat
    cdef double cu[13]

    for i in range(13):
        cu[i] = u[i]
    cpal.palUe2el( cu, jformr, &jform, &epoch, &orbinc, &anode, &perih,
                   &aorq, &e, &aorl, &dm, &jstat )
    if jstat == -1:
        raise ValueError( "Illegal combined mass" )
    elif jstat == -2:
        raise ValueError( "Illegal jformr" )
    elif jstat == -3:
        raise ValueError( "Position/velocity out of range")
    return (jform, epoch, orbinc, anode, perih, aorq, e, aorl, dm)

#  Note that u is updated and returned
def ue2pv( double date, np.ndarray[double, ndim=1] u not None ):
    """
    (u2, pv) = ue2pv( date, u )

Heliocentric position and velocity of a planet, asteroid or comet, from universal elements

Arguments
---------
date = double (Given)
   TT Modified Julian date (JD-2400000.5).
u = double [13] (Given & Returned)
   Universal orbital elements (updated, see note 1)
   given    (0)   combined mass (M+m)
     "      (1)   total energy of the orbit (alpha)
     "      (2)   reference (osculating) epoch (t0)
     "    (3-5)   position at reference epoch (r0)
     "    (6-8)   velocity at reference epoch (v0)
     "      (9)   heliocentric distance at reference epoch
     "     (10)   r0.v0
  returned (11)   date (t)
     "     (12)   universal eccentric anomaly (psi) of date
pv = double [6] (Returned)
  Position (AU) and velocity (AU/s)
jstat = int * (Returned)
  status:  0 = OK
          -1 = radius vector zero
          -2 = failed to converge


Notes
-----
- The "universal" elements are those which define the orbit for the
  purposes of the method of universal variables (see reference).
  They consist of the combined mass of the two bodies, an epoch,
  and the position and velocity vectors (arbitrary reference frame)
  at that epoch.  The parameter set used here includes also various
  quantities that can, in fact, be derived from the other
  information.  This approach is taken to avoiding unnecessary
  computation and loss of accuracy.  The supplementary quantities
  are (i) alpha, which is proportional to the total energy of the
  orbit, (ii) the heliocentric distance at epoch, (iii) the
  outwards component of the velocity at the given epoch, (iv) an
  estimate of psi, the "universal eccentric anomaly" at a given
  date and (v) that date.
- The companion routine is palEl2ue.  This takes the conventional
  orbital elements and transforms them into the set of numbers
  needed by the present routine.  A single prediction requires one
  one call to palEl2ue followed by one call to the present routine;
  for convenience, the two calls are packaged as the routine
  palPlanel.  Multiple predictions may be made by again
  calling palEl2ue once, but then calling the present routine
  multiple times, which is faster than multiple calls to palPlanel.
- It is not obligatory to use palEl2ue to obtain the parameters.
  However, it should be noted that because palEl2ue performs its
  own validation, no checks on the contents of the array U are made
  by the present routine.
- DATE is the instant for which the prediction is required.  It is
  in the TT timescale (formerly Ephemeris Time, ET) and is a
  Modified Julian Date (JD-2400000.5).
- The universal elements supplied in the array U are in canonical
  units (solar masses, AU and canonical days).  The position and
  velocity are not sensitive to the choice of reference frame.  The
  palEl2ue routine in fact produces coordinates with respect to the
  J2000 equator and equinox.
- The algorithm was originally adapted from the EPHSLA program of
  D.H.P.Jones (private communication, 1996).  The method is based
  on Stumpff's Universal Variables.
- Reference:  Everhart, E. & Pitkin, E.T., Am.J.Phys. 51, 712, 1983.

    Raises
    ------
    ValueError: Radius vector zero
    ArithmeticError: Failed to converge
    """
    cdef double cu[13]
    cdef double cpv[6]
    cdef int jstat

    for i in range(13):
        cu[i] = u[i]
    cpal.palUe2pv( date, cu, cpv, &jstat )
    if jstat == -1:
        raise ValueError( "Radius vector zero" )
    elif jstat == -2:
        raise ArithmeticError( "Failed to converge" )

    # We need to return a completely new updated U
    # rather than overwrite in place
    cdef np.ndarray u2 = np.zeros( [13], dtype=np.float64)
    cdef np.ndarray pv = np.zeros( [6], dtype=np.float64)
    for i in range(13):
        u2[i] = cu[i]
    for i in range(6):
        pv[i] = cpv[i]
    return (u2, pv)

def unpcd( double disco, double x, double y):
    """
    (tx, ty) = unpcd( x, y )

    Returns the tangent plane coordinates and does not
    modify the supplied arguments.

Remove pincushion/barrel distortion

Arguments
---------
disco = double (Given)
   Pincushion/barrel distortion coefficient.
x = double * (Given & Returned)
   On input the distorted X coordinate, on output
   the tangent-plane X coordinate.
y = double * (Given & Returned)
   On input the distorted Y coordinate, on output
   the tangent-plane Y coordinate.


Notes
-----
- The distortion is of the form RP = R*(1+C*R^2), where R is
  the radial distance from the tangent point, C is the DISCO
  argument, and RP is the radial distance in the presence of
  the distortion.

- For pincushion distortion, C is +ve;  for barrel distortion,
  C is -ve.

- For X,Y in "radians" - units of one projection radius,
  which in the case of a photograph is the focal length of
  the camera - the following DISCO values apply:

      Geometry          DISCO

      astrograph         0.0
      Schmidt           -0.3333
      AAT PF doublet  +147.069
      AAT PF triplet  +178.585
      AAT f/8          +21.20
      JKT f/8          +13.32

- The present routine is a rigorous inverse of the companion
  routine palPcd.  The expression for RP in Note 1 is rewritten
  in the form x^3+a*x+b=0 and solved by standard techniques.

- Cases where the cubic has multiple real roots can sometimes
  occur, corresponding to extreme instances of barrel distortion
  where up to three different undistorted [X,Y]s all produce the
  same distorted [X,Y].  However, only one solution is returned,
  the one that produces the smallest change in [X,Y].
    """
    cpal.palUnpcd( disco, &x, &y )
    return (x, y)
