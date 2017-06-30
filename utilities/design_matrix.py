import numpy

from pyhdf.SD import SD, SDC


class DesignMatrix:

    def __init__(self):
        self.predictors = None
        self.response = None
        self.variable_names = None

    def from_hdf(self, hdf_file):
        sd = SD(hdf_file)
        sds = sd.select("design_matrix")
        self.set_predictors_and_response(sds.get())
        self.variable_names = sds.variable_names
        sds.endaccess()
        sd.end()

    def from_csv(self, csv_file):
        dat = numpy.genfromtxt(csv_file, delimiter=',', skip_header=True)
        self.set_predictors_and_response(dat)
        return self.predictors, self.response

    def from_headed_csv(self, csv_file):
        dat = numpy.genfromtxt(csv_file, dtype=numpy.float, delimiter=',', names=True,
                               deletechars="""~!@#$%^&-=~\|]}[{';: /?.>,<""")
        self.set_predictors_and_response(dat)
        self.variable_names = dat.dtype.names[:-1]
        return self.predictors, self.response

    def to_hdf(self, dat, file_name):
        sd = SD(file_name, SDC.WRITE | SDC.CREATE)
        sds = sd.create('design_matrix', SDC.FLOAT64, (self.predictors.shape(0), self.predictors.shape(1) + 1))
        sds.variable_names = self.variable_names
        sds[:] = dat
        sds.endaccess()
        sd.end()

    def to_headed_csv(self, dat, file_name):
        numpy.savetxt(file_name, X=dat, delimiter=',', header=','.join(self.variable_names))

    def set_predictors_and_response(self, dat):
        self.predictors = dat[:, :-1]
        self.response = dat[:, -1]
