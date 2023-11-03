from PyFiberModes.fiber_geometry.geometry import Geometry
from PyFiberModes import constants
from math import sqrt
import numpy
from scipy.special import jn, yn, iv, kn
from scipy.special import j0, y0, i0, k0
from scipy.special import j1, y1, i1, k1
from scipy.special import jvp, yvp, ivp, kvp


class StepIndex(Geometry):
    DEFAULT_PARAMS = []

    def get_index(self, radius: float, wavelength: float) -> float:
        """
        Gets the index of the local layer at a given radius.

        :param      radius:      The radius for evaluation
        :type       radius:      float
        :param      wavelength:  The wavelength
        :type       wavelength:  float

        :returns:   The index at given radius.
        :rtype:     float
        """
        if self.radius_in <= abs(radius) <= self.radius_out:
            return self._m.n(wavelength, *self._mp)
        else:
            return None

    def get_minimum_index(self, wavelength: float) -> float:
        """
        Gets the minimum index of the local layer.

        :param      wavelength:  The wavelength
        :type       wavelength:  float

        :returns:   The maximum index.
        :rtype:     float
        """
        return self._m.n(wavelength, *self._mp)

    def get_maximum_index(self, wavelength: float) -> float:
        """
        Gets the maximum index of the local layer.

        :param      wavelength:  The wavelength
        :type       wavelength:  float

        :returns:   The maximum index.
        :rtype:     float
        """
        return self._m.n(wavelength, *self._mp)

    def get_u_parameter(self, radius: float, neff: float, wavelength: float) -> float:
        """
        Gets the u parameter. Whatever it defines.

        :param      radius:      The radius
        :type       radius:      float
        :param      neff:        The neff
        :type       neff:        float
        :param      wavelength:  The wavelength
        :type       wavelength:  float

        :returns:   The u parameter at given radius.
        :rtype:     float
        """
        index = self.get_index(radius, wavelength)

        return wavelength.k0 * radius * sqrt(abs(index**2 - neff**2))

    def Psi(self, radius: float, neff: float, wavelength: float, nu, C):

        u = self.get_u_parameter(
            radius=radius,
            neff=neff,
            wavelength=wavelength
        )

        if neff < self.get_maximum_index(wavelength):
            psi = (C[0] * jn(nu, u) + C[1] * yn(nu, u) if C[1] else
                   C[0] * jn(nu, u))
            psip = u * (C[0] * jvp(nu, u) + C[1] * yvp(nu, u) if C[1] else
                        C[0] * jvp(nu, u))
        else:
            psi = (C[0] * iv(nu, u) + C[1] * kn(nu, u) if C[1] else
                   C[0] * iv(nu, u))
            psip = u * (C[0] * ivp(nu, u) + C[1] * kvp(nu, u) if C[1] else
                        C[0] * ivp(nu, u))

        # if numpy.isnan(psi):
        #     print(neff, self.get_maximum_index(wavelength), C, r)
        return psi, psip

    def lpConstants(self,
            radius: float,
            neff: float,
            wavelength: float,
            nu: int,
            A: list) -> tuple:

        u = self.get_u_parameter(
            radius=radius,
            neff=neff,
            wavelength=wavelength
        )

        maximum_index = self.get_maximum_index(wavelength=wavelength)

        if neff < maximum_index:
            W = numpy.pi / 2
            term_0 = W * (u * yvp(nu, u) * A[0] - yn(nu, u) * A[1])
            term_1 = W * (jn(nu, u) * A[1] - u * jvp(nu, u) * A[0])

        else:
            term_0 = u * kvp(nu, u) * A[0] - kn(nu, u) * A[1]
            term_1 = iv(nu, u) * A[1] - u * ivp(nu, u) * A[0]

        return term_0, term_1

    def EH_fields(self,
            radius_in: float,
            radius_out: float,
            nu: int,
            neff: float,
            wavelength: float,
            EH: object,
            TM: bool = True):
        """

        modify EH in-place (for speed)

        """
        maximum_index = self.get_maximum_index(wavelength=wavelength)

        u = self.get_u_parameter(
            radius=radius_out,
            neff=neff,
            wavelength=wavelength
        )

        if radius_in == 0:
            if nu == 0:
                if TM:
                    self.C = numpy.array([1., 0., 0., 0.])
                else:
                    self.C = numpy.array([0., 0., 1., 0.])
            else:
                self.C = numpy.zeros((4, 2))
                self.C[0, 0] = 1  # Ez = 1
                self.C[2, 1] = 1  # Hz = alpha

        elif nu == 0:
            self.C = numpy.zeros(4)
            if TM:
                c = constants.Y0 * maximum_index**2
                idx = (0, 3)

                self.C[:2] = self.tetmConstants(
                    radius_in=radius_in,
                    radius_out=radius_out,
                    neff=neff,
                    wavelength=wavelength,
                    EH=EH,
                    c=c,
                    idx=idx
                )
            else:
                c = -constants.eta0
                idx = (1, 2)

                self.C[2:] = self.tetmConstants(
                    radius_in=radius_in,
                    radius_out=radius_out,
                    neff=neff,
                    wavelength=wavelength,
                    EH=EH,
                    c=c,
                    idx=idx
                )
        else:
            self.C = self.vConstants(
                radius_in=radius_in,
                radius_out=radius_out,
                neff=neff,
                wavelength=wavelength,
                nu=nu,
                EH=EH
            )

        # Compute EH fields
        if neff < maximum_index:
            c1 = wavelength.k0 * radius_out / u
            F3 = jvp(nu, u) / jn(nu, u)
            F4 = yvp(nu, u) / yn(nu, u)
        else:
            c1 = -wavelength.k0 * radius_out / u
            F3 = ivp(nu, u) / iv(nu, u)
            F4 = kvp(nu, u) / kn(nu, u)

        c2 = neff * nu / u * c1
        c3 = constants.eta0 * c1
        c4 = constants.Y0 * maximum_index**2 * c1

        EH[0] = self.C[0] + self.C[1]
        EH[1] = self.C[2] + self.C[3]
        EH[2] = (c2 * (self.C[0] + self.C[1]) - c3 * (F3 * self.C[2] + F4 * self.C[3]))
        EH[3] = (c4 * (F3 * self.C[0] + F4 * self.C[1]) - c2 * (self.C[2] + self.C[3]))

        return EH

    def vConstants(self, radius_in: float, radius_out: float, neff, wavelength: float, nu, EH):
        a = numpy.zeros((4, 4))

        maximum_index = self.get_maximum_index(wavelength)

        u = self.get_u_parameter(
            radius=radius_out,
            neff=neff,
            wavelength=wavelength
        )

        urp = self.get_u_parameter(
            radius=radius_in,
            neff=neff,
            wavelength=wavelength
        )

        if neff < maximum_index:
            B1 = jn(nu, u)
            B2 = yn(nu, u)
            F1 = jn(nu, urp) / B1
            F2 = yn(nu, urp) / B2
            F3 = jvp(nu, urp) / B1
            F4 = yvp(nu, urp) / B2
            c1 = wavelength.k0 * radius_out / u
        else:
            B1 = iv(nu, u)
            B2 = kn(nu, u)
            F1 = iv(nu, urp) / B1 if u else 1
            F2 = kn(nu, urp) / B2
            F3 = ivp(nu, urp) / B1 if u else 1
            F4 = kvp(nu, urp) / B2
            c1 = -wavelength.k0 * radius_out / u
        c2 = neff * nu / urp * c1
        c3 = constants.eta0 * c1
        c4 = constants.Y0 * maximum_index**2 * c1

        a[0, 0] = F1
        a[0, 1] = F2
        a[1, 2] = F1
        a[1, 3] = F2
        a[2, 0] = F1 * c2
        a[2, 1] = F2 * c2
        a[2, 2] = -F3 * c3
        a[2, 3] = -F4 * c3
        a[3, 0] = F3 * c4
        a[3, 1] = F4 * c4
        a[3, 2] = -F1 * c2
        a[3, 3] = -F2 * c2

        return numpy.linalg.solve(a, EH)

    def tetmConstants(self, radius_in: float, radius_out: float, neff: float, wavelength: float, EH, c, idx):
        a = numpy.empty((2, 2))

        maximum_index = self.get_maximum_index(wavelength=wavelength)

        u = self.get_u_parameter(
            radius=radius_out,
            neff=neff,
            wavelength=wavelength
        )

        urp = self.get_u_parameter(
            radius=radius_in,
            neff=neff,
            wavelength=wavelength
        )

        if neff < maximum_index:
            B1 = j0(u)
            B2 = y0(u)
            F1 = j0(urp) / B1
            F2 = y0(urp) / B2
            F3 = -j1(urp) / B1
            F4 = -y1(urp) / B2
            c1 = wavelength.k0 * radius_out / u
        else:
            B1 = i0(u)
            B2 = k0(u)
            F1 = i0(urp) / B1
            F2 = k0(urp) / B2
            F3 = i1(urp) / B1
            F4 = -k1(urp) / B2
            c1 = -wavelength.k0 * radius_out / u

        c3 = c * c1

        a[0, 0] = F1
        a[0, 1] = F2
        a[1, 0] = F3 * c3
        a[1, 1] = F4 * c3

        return numpy.linalg.solve(a, EH.take(idx))
