
class DOSManager(FileManager):
    def __init__(self, file_location:str=None, name:str=None, **kwargs):
        """
        Initialize OutFileManager class.
        :param file_location: Location of the file to be read.
        :param name: Name identifier for the file.
        :param kwargs: Additional keyword arguments.
        """
        super().__init__(name=name, file_location=file_location)


    def load(self, file_location=None):
        file_location = file_location if type(file_location) == str else self._file_location

        lines = [n for n in self.read_file() ]
        
        f = open(self.file_name,'r')

        self.n_E = 6
        self.E = [] 
        self.E_total = [] 
        for i, n in enumerate(f):
            vec = [ m for m in n.split(' ') if m != '']
            if i == 5:  self.n_E = float(vec[2]) ; self.fermi = float(vec[3])
            
            if i > 5 and i < self.n_E+1+5: self.E_total.append([float(m) for m in vec])

            if i-5%(self.n_E+1) > 0 and int((i-5)/(self.n_E+1)) == 0: self.E_total.append([float(m) for m in vec])

            if int(i-5)%(self.n_E+1) == 0 and int((i-5)/(self.n_E+1)) > 0: self.E.append([])
            if int(i-5)%int(self.n_E+1) > 0 and int((i-5)/(self.n_E+1)) > 0: self.E[-1].append([float(m) for m in vec])

        self.E = np.array(self.E)
        self.n_oins, var, self.n_orb = self.E.shape
        print( f' >> Load complete :: data shape {self.E.shape} :: {file_name}')
        
        f.close()

        return self.E