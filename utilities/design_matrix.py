import numpy

from pyhdf.SD import SD, SDC


class DesignMatrix:

    def __init__(self):
        self.dat = None
        self.predictors = None
        self.response = None
        self.variable_names = None

    def from_hdf(self, hdf_file):
        sd = SD(hdf_file)
        sds = sd.select("design_matrix")
        self.dat = sds.get()
        self.set_predictors_and_response()
        if sds.variable_names:
            self.variable_names = sds.variable_names.split(",")
        else:
            self.variable_names = self.generate_simple_variable_names()
        sds.endaccess()
        sd.end()

    def from_csv(self, csv_file):
        self.dat = numpy.genfromtxt(csv_file, delimiter=',', skip_header=True)
        self.set_predictors_and_response()
        self.variable_names = self.generate_simple_variable_names()
        return self.predictors, self.response

    def from_headed_csv(self, csv_file):
        self.dat = numpy.genfromtxt(csv_file, dtype=numpy.float, delimiter=',', names=True,
                                    deletechars="""~!@#$%^&-=~\|]}[{';: /?.>,<""")
        self.set_predictors_and_response()
        self.variable_names = self.dat.dtype.names[:-1]
        return self.predictors, self.response

    def from_data(self, matrix, variable_names):
        self.dat = matrix
        self.set_predictors_and_response()
        if variable_names:
            self.variable_names = variable_names
        else:
            self.generate_simple_variable_names()

    def to_hdf(self, file_name):
        sd = SD(file_name, SDC.WRITE | SDC.CREATE)
        sds = sd.create('design_matrix', SDC.FLOAT64, (self.predictors.shape[0], self.predictors.shape[1] + 1))
        sds.variable_names = ",".join(self.variable_names)
        sds[:] = self.dat
        sds.endaccess()
        sd.end()

    def to_headed_csv(self, file_name):
        numpy.savetxt(file_name, X=self.dat, delimiter=',', header=','.join(self.variable_names))

    def set_predictors_and_response(self):
        self.predictors = self.dat[:, :-1]
        self.response = self.dat[:, -1]

    def generate_simple_variable_names(self):
        return ['X' + str(x) for x in range(0, self.predictors.shape[1])]
