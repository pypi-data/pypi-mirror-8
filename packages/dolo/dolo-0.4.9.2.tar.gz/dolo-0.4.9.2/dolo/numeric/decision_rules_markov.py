import numpy
from numpy import array, zeros
from dolo.numeric.misc import mlinspace


class MarkovDecisionRule:


    def __init__(self, n_m, a, b, orders, values=None):

        dtype = numpy.double
        self.n_m = int(n_m)
        self.a = array(a, dtype=dtype)
        self.b = array(b, dtype=dtype)
        self.orders = array(orders, dtype=int)

        # for backward compatibility
        self.smin = self.a
        self.smax = self.b

        self.dtype = dtype

        self.N = self.orders.prod()

        self.__grid__ = None

        if values is not None:
            self.set_values(values)
        else:
            self.__values__ = None

    @property
    def grid(self):

        if self.__grid__ is None:
            self.__grid__ = mlinspace(self.smin, self.smax, self.orders)
        return self.__grid__

    def set_values(self, values):

        self.__values__ = values
        self.__coefs__ = filter_controls(self.smin, self.smax, self.orders, values)

    def __call__(self, i_m, points, out=None):


        from dolo.numeric.interpolation.eval_cubic_splines import vec_eval_cubic_multi_spline
        n_x = self.__values__.shape[-1]

        assert(1<=points.ndim<=2)

        if points.ndim == 2:
            N = points.shape[0]

            out = zeros((N,n_x))
            if isinstance(i_m, (float,int)):
                coefs = self.__coefs__[i_m,...]
                vec_eval_cubic_multi_spline(self.a, self.b, self.orders, coefs, points, out)
            else:
                assert(len(i_m)==N)
                for n in range(N):
                    coefs = self.__coefs__[i_m[n]]
                    vec_eval_cubic_multi_spline(self.a, self.b, self.orders, coefs, points[n:n+1,:], out[n:n+1,:])

            return out

        elif points.ndim == 1:

            pp = numpy.atleast_2d(points)
            out = self.__call__(i_m, pp)
            return out.ravel()

    def eval_all(self, points):

        N = points.shape[0]
        dims = self.__coefs__.shape
        n_m = dims[0]
        n_x = dims[1]
        coefs = self.__coefs__.reshape( [n_m*n_x] + dims[2:] )
        out = numpy.zeros( (N, n_m*n_x) )
        vec_eval_cubic_multi_spline(self.a, self.b, self.orders, coefs, points, out)
        out = numpy.transpose(out, (1,2,0))
        return out


def filter_controls(a,b,ndims,controls):
    from dolo.numeric.interpolation.filter_cubic_splines import filter_data
    dinv = (b-a)/(ndims-1)
    ndims = array(ndims)
    n_m, N, n_x = controls.shape
    coefs = zeros( (n_m, n_x) + tuple(ndims + 2) )
    for i_m in range(n_m):
        for i_x in range(n_x):
            coefs[i_m,i_x,...] = filter_data(dinv, controls[i_m,:,i_x].reshape(ndims))
    return coefs
