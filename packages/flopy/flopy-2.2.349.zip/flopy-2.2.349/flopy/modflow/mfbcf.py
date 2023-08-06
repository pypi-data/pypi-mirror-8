import numpy as np
from flopy.mbase import Package
from flopy.utils import util_2d,util_3d

class ModflowBcf(Package):
    '''Block centered flow package class
    intercellt: specifies how to compute intercell conductance
    laycon: specifies the layer type
    trpy: horizontal anisotropy factor for each layer
    hdry: head in cells that are converted to dry during a simulation
    iwdflg: flag that determines if the wetting capability is active
    wetfct: factor that is included in the calculation of the head when a cell is converted from dry to wet
    iwetit: iteration interval for attempting to wet cells
    ihdwet: flag that determines which equation is used to define the initial head at cells that become wet
    tran : transmissivity of each layer; tran is used when laycon = 0 or 2
    hy : hydraulic conductivity of each layer; hy is used when laycon = 1 or >2
    vcont : leakance between layers
    sf1: 
    sf2: 
    wetdry: 
    '''
    def __init__(self, model, ibcfcb = 0, intercellt=0,laycon=3, trpy=1.0, hdry=-1E+30, iwdflg=0, wetfct=0.1, iwetit=1, ihdwet=0, \
                 tran=1.0, hy=1.0, vcont=1.0, sf1=1e-5, sf2=0.15, wetdry=-0.01, extension='bcf', unitnumber=15):
        Package.__init__(self, model, extension, 'BCF6', unitnumber) # Call ancestor's init to set self.parent, extension, name and unit number
        self.url = 'bcf.htm'
        nrow, ncol, nlay, nper = self.parent.nrow_ncol_nlay_nper
#        # Set values of all parameters
#        self.intercellt = self.assignarray((nlay,), np.int, intercellt, name='intercellt') # Specifies how to compute intercell conductance
#        self.laycon = self.assignarray((nlay,), np.int, laycon, name='laycon') # Specifies the layer type (LAYCON)
#        self.trpy = self.assignarray((nlay,), np.float, trpy, name='trpy') # Horizontal anisotropy factor for each layer
#        self.ibcfcb = ibcfcb # Unit number for file with cell-by-cell flow terms
#        self.hdry = hdry # Head in cells that are converted to dry during a simulation
#        self.iwdflg = iwdflg # Flag that determines if the wetting capability is active
#        self.wetfct = wetfct # Factor that is included in the calculation of the head when a cell is converted from dry to wet
#        self.iwetit = iwetit # Iteration interval for attempting to wet cells
#        self.ihdwet = ihdwet # Flag that determines which equation is used to define the initial head at cells that become wet     
#        self.tran = self.assignarray((nlay,nrow,ncol), np.float, tran, name='tran', load=True)
#        self.hy = self.assignarray((nlay,nrow,ncol), np.float, hy, name='hy', load=True)
#        self.vcont = self.assignarray((nlay-1,nrow,ncol), np.float, vcont, name='vcont', load=True)
#        self.sf1 = self.assignarray((nlay,nrow,ncol), np.float, sf1, name='sf1', load=True)
#        self.sf2 = self.assignarray((nlay,nrow,ncol), np.float, sf2, name='sf2', load=True)
#        self.wetdry = self.assignarray((nlay,nrow,ncol), np.float, wetdry, name='wetdry', load=True)
        # Set values of all parameters
        #self.intercellt = self.assignarray((nlay,), np.int, intercellt, name='intercellt') # Specifies how to compute intercell conductance
        #self.laycon = self.assignarray((nlay,), np.int, laycon, name='laycon') # Specifies the layer type (LAYCON)
        self.intercellt = util_2d(model,(nlay,),np.int,intercellt,name='laycon',locat=self.unit_number[0])
        self.laycon = util_2d(model,(nlay,),np.int,laycon,name='laycon',locat=self.unit_number[0])
        self.trpy = util_2d(model,(nlay,),np.int,trpy,name='Anisotropy factor',locat=self.unit_number[0])
        self.ibcfcb = ibcfcb # Unit number for file with cell-by-cell flow terms
        self.hdry = hdry # Head in cells that are converted to dry during a simulation
        self.iwdflg = iwdflg # Flag that determines if the wetting capability is active
        self.wetfct = wetfct # Factor that is included in the calculation of the head when a cell is converted from dry to wet
        self.iwetit = iwetit # Iteration interval for attempting to wet cells
        self.ihdwet = ihdwet # Flag that determines which equation is used to define the initial head at cells that become wet     
        self.tran = util_3d(model,(nlay,nrow,ncol),np.float32,tran,'Transmissivity',locat=self.unit_number[0])    
        self.hy = util_3d(model,(nlay,nrow,ncol),np.float32,hy,'Horizontal Hydraulic Conductivity',locat=self.unit_number[0])    
        self.vcont = util_3d(model,(nlay-1,nrow,ncol),np.float32,vcont,'Vertical Conductance',locat=self.unit_number[0])    
        self.sf1 = util_3d(model,(nlay,nrow,ncol),np.float32,sf1,'Primary Storage Coefficient',locat=self.unit_number[0])    
        self.sf2 = util_3d(model,(nlay,nrow,ncol),np.float32,sf2,'Secondary Storage Coefficient',locat=self.unit_number[0])    
        self.wetdry = util_3d(model,(nlay,nrow,ncol),np.float32,wetdry,'WETDRY',locat=self.unit_number[0])
        
        self.parent.add_package(self)
    def write_file(self):
        nrow, ncol, nlay, nper = self.parent.nrow_ncol_nlay_nper
        # Open file for writing
        f_bcf = open(self.fn_path, 'w')
        # Item 1: IBCFCB, HDRY, IWDFLG, WETFCT, IWETIT, IHDWET
        f_bcf.write('%10d%10.1e%10d%10f%10d%10d\n' % (self.ibcfcb, self.hdry, self.iwdflg, self.wetfct, self.iwetit, self.ihdwet))
        # LAYCON array
        for k in range(nlay):            
            f_bcf.write('{0:1d}{1:1d} '.format(self.intercellt[k],self.laycon[k]))
        f_bcf.write('\n')
#        for k in range(nlay):
#            f_bcf.write('%1i%1i ' %(self.intercellt[k],self.laycon[k]))
#        f_bcf.write('\n')
#        self.parent.write_vector(f_bcf, self.trpy, self.unit_number[0], True, 13, -5, 'TRPY(): Anisotropy factor of layers') # npln is negative as it needs to print all layers even if they are all the same
        f_bcf.write(self.trpy.get_file_entry())
        transient = not self.parent.get_package('DIS').steady.all()
        for k in range(nlay):
            if (transient == True):
                #comment = 'Sf1() = Confined storage coefficient of layer ' + str(k + 1)
                #self.parent.write_array( f_bcf, self.sf1[k], self.unit_number[0], True, 13, ncol, comment,ext_base='sf1' )
                f_bcf.write(self.sf1[k].get_file_entry())
            if ((self.laycon[k] == 0) or (self.laycon[k] == 2)):
                #comment = 'TRANS() = Transmissivity of layer ' + str(k + 1)
                #self.parent.write_array( f_bcf, self.tran[k], self.unit_number[0], True, 13, ncol, comment,ext_base='tran' )
                f_bcf.write(self.tran[k].get_file_entry())
            else:
                #comment = 'HY() = Hydr. Conductivity of layer ' + str(k + 1)
                #self.parent.write_array( f_bcf, self.hy[k], self.unit_number[0], True, 13, ncol, comment,ext_base='hy')
                f_bcf.write(self.hy[k].get_file_entry())
            if k < nlay - 1:
                #comment = 'VCONT() = Vert. leakance of layer ' + str(k + 1)
                #self.parent.write_array( f_bcf, self.vcont[k], self.unit_number[0], True, 13, ncol, comment,ext_base='vcont' )
                f_bcf.write(self.vcont[k].get_file_entry())
            if ((transient == True) and ((self.laycon[k] == 2) or (self.laycon[k] == 3))):
                #comment = 'Sf2() = Specific yield of layer ' + str(k + 1)
                #self.parent.write_array( f_bcf, self.sf2[k], self.unit_number[0], True, 13, ncol, comment,ext_base='sf2' )
                f_bcf.write(self.sf2[k].get_file_entry())
            if ((self.iwdflg <> 0) and ((self.laycon[k] == 1) or (self.laycon[k] == 3))):
                #comment = 'Wetdry() = Wetdry array of layer ' + str(k + 1)
                #self.parent.write_array( f_bcf, self.wetdry[k], self.unit_number[0], True, 13, ncol, comment,ext_base='wetdry' )
                f_bcf.write(self.wetdry[k].get_file_entry())
        f_bcf.close()

    @staticmethod
    def load(f, model, ext_unit_dict=None):
        '''
        f is either a filename or a file handle.  if the arrays in the file
        are specified using interal, external, or older style array control
        records, then f should be a file handle, and the ext_unit_dict
        dictionary of unitnumber:open(filename, 'r') must be included.
        '''
        if type(f) is not file:
            filename = f
            f = open(filename, 'r')
        #dataset 0 -- header
        while True:
            line = f.readline()
            if line[0] != '#':
                break
        # determine problem dimensions
        nrow, ncol, nlay, nper = model.get_nrow_ncol_nlay_nper()
        # Item 1: IBCFCB, HDRY, IWDFLG, WETFCT, IWETIT, IHDWET - line already read above
        print '   loading IBCFCB, HDRY, IWDFLG, WETFCT, IWETIT, IHDWET...'
        t = line.strip().split()
        ibcfcb,hdry,iwdflg,wetfct,iwetit,ihdwet = int(t[0]),float(t[1]),int(t[2]),float(t[3]),int(t[4]),int(t[5])
        if ibcfcb != 0:
            ibcfcb = 53
        # LAYCON array
        print '   loading LAYCON...'
        line = f.readline()
        t = line.strip().split()
        intercellt = np.zeros(nlay, dtype=np.int)
        laycon = np.zeros(nlay, dtype=np.int)
        for k in xrange(nlay):
            ival = int(t[k])
            if ival > 9:
                intercellt[k] = int(t[k][0])
                laycon[k] = int(t[k][1])
            else:
                laycon[k] = ival
        # TRPY array
        print '   loading TRPY...'
        trpy = util_2d.load(f, model, (1, nlay), np.float32, 'trpy', ext_unit_dict)
        trpy = trpy.array.reshape( (nlay) )
        # property data for each layer based on options
        transient = not model.get_package('DIS').steady.all()
        sf1 = np.empty((nlay,nrow,ncol), dtype=np.float)
        tran = np.empty((nlay,nrow,ncol), dtype=np.float)
        hy = np.empty((nlay,nrow,ncol), dtype=np.float)
        if nlay > 1:
            vcont = np.empty((nlay-1,nrow,ncol), dtype=np.float)
        else:
            vcont = 1.0
        sf2 = np.empty((nlay,nrow,ncol), dtype=np.float)
        wetdry = np.empty((nlay,nrow,ncol), dtype=np.float)
        for k in xrange(nlay):
            if transient == True:
                print '   loading sf1 layer {0:3d}...'.format(k+1)
                t = util_2d.load(f, model, (nrow,ncol), np.float32, 'sf1', ext_unit_dict)
                sf1[k,:,:] = t.array
            if ((laycon[k] == 0) or (laycon[k] == 2)):
                print '   loading tran layer {0:3d}...'.format(k+1)
                t = util_2d.load(f, model, (nrow,ncol), np.float32, 'tran', ext_unit_dict)
                tran[k,:,:] = t.array
            else:
                print '   loading hy layer {0:3d}...'.format(k+1)
                t = util_2d.load(f, model, (nrow,ncol), np.float32, 'hy', ext_unit_dict)
                hy[k,:,:] = t.array
            if k < (nlay - 1):
                print '   loading vcont layer {0:3d}...'.format(k+1)
                t = util_2d.load(f, model, (nrow,ncol), np.float32, 'vcont', ext_unit_dict)
                vcont[k,:,:] = t.array
            if ((transient == True) and ((laycon[k] == 2) or (laycon[k] == 3))):
                print '   loading sf2 layer {0:3d}...'.format(k+1)
                t = util_2d.load(f, model, (nrow,ncol), np.float32, 'sf2', ext_unit_dict)
                sf2[k,:,:] = t.array
            if ((iwdflg <> 0) and ((laycon[k] == 1) or (laycon[k] == 3))):
                print '   loading sf2 layer {0:3d}...'.format(k+1)
                t = util_2d.load(f, model, (nrow,ncol), np.float32, 'wetdry', ext_unit_dict)
                wetdry[k,:,:] = t.array

        bcf = ModflowBcf(model,ibcfcb=ibcfcb,intercellt=intercellt,laycon=laycon,trpy=trpy,hdry=hdry,iwdflg=iwdflg,wetfct=wetfct,iwetit=iwetit,ihdwet=ihdwet,
                         tran=tran,hy=hy,vcont=vcont,sf1=sf1,sf2=sf2,wetdry=wetdry)
        return bcf
