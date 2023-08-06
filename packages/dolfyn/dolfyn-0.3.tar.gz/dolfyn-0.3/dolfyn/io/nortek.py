"""
This module provides the routines for reading data from Nortek data
files.
"""

import numpy as np
from ..adv import base as adv_base
from .. import adp
from ..tools import misc as tbx
from struct import unpack
from struct import error as str_err
from ..data.base import ma
from . import nortek_defs
time = nortek_defs.time


def read_nortek(filename, do_checksum=False, **kwargs):
    """
    Read a nortek file.

    Parameters
    ----------
    filename : string
               Filename of Nortek file to read.
    **kwargs : keyword arguments to :class:`NortekReader`

    Returns
    -------
    adv_data : :class:`ADVraw <dolfyn.adv.base.ADVraw>`

    """
    with NortekReader(filename, do_checksum=do_checksum, **kwargs) as rdr:
        rdr.readfile()
    rdr.dat2sci()
    return rdr.data


def _bcd2char(cBCD):
    """
    Taken from the Nortek System Integrator
    Manual "Example Program" Chapter.
    """
    cBCD = min(cBCD, 153)
    c = (cBCD & 15)
    c += 10 * (cBCD >> 4)
    return c


def _bitshift8(val):
    return val >> 8


class NortekReader(object):

    """
    A class for reading reading nortek binary files.

    This reader currently only supports AWAC and Vector data formats.

    Parameters
    ----------
    fname : string
            Nortek file filename to read.
    endian : {'<','>'} (optional)
             Specifies if the file is in 'little' or 'big' endian
             format. By default the reader will attempt to determine
             this.
    debug : {True, False*} (optional)
            Print debug/progress information?
    do_checksum : {True*, False} (optional)
                  Specifies whether to perform the checksum.
    bufsize : int (default 100000)
              The size of the read buffer to use.
    npings : int or None (default: None)
             The number of pings to read from the file. By default,
    the entire file is read.


    """

    fun_map = {'0x00': 'read_user_cfg',
               '0x04': 'read_head_cfg',
               '0x05': 'read_hw_cfg',
               '0x07': 'read_vec_checkdata',
               '0x10': 'read_vec_data',
               '0x11': 'read_vec_sysdata',
               '0x12': 'read_vec_hdr',
               '0x71': 'read_microstrain',
               '0x20': 'read_awac_profile',
               }

    def __init__(self, fname, endian=None, debug=False,
                 do_checksum=True, bufsize=100000, npings=None):
        self.fname = fname
        self._bufsize = bufsize
        self.f = open(fname, 'rb', 1000)
        self.read = self.f.read
        self.do_checksum = do_checksum
        self.filesize  # initialize the filesize.
        self.debug = debug
        self.c = -1
        self._dtypes = []
        self._npings = npings
        if endian is None:
            if unpack('<HH', self.f.read(4)) == (1445, 24):
                endian = '<'
            elif unpack('>HH', self.f.read(4)) == (1445, 24):
                endian = '>'
            else:
                raise Exception("I/O error: could not determine the \
                'endianness' of the file.  Are you sure this is a Nortek \
                file?")
        self.endian = endian
        self.f.seek(0, 0)
        # print( unpack(self.endian+'HH',self.read(4)) )
        # This is the configuration data:
        self.config = adv_base.db.config(config_type='NORTEK Header Data')
        # Now read the header:
        err_msg = "I/O error: The file does not \
                   appear to be a Nortek data file."
        if self.read_id() == 5:
            self.read_hw_cfg()
        else:
            raise Exception()
        if self.read_id() == 4:
            self.read_head_cfg()
        else:
            raise Exception(err_msg)
        if self.read_id() == 0:
            self.read_user_cfg()
        else:
            raise Exception(err_msg)
        if self.config.hardware.serialNum[0:3].upper() == 'WPR':
            self.config.config_type = 'AWAC'
        elif self.config.hardware.serialNum[0:3].upper() == 'VEC':
            self.config.config_type = 'ADV'
        # Initialize the instrument type:
        self._inst = self.config.config_type
        # This is the position after reading the 'hardware',
        # 'head', and 'user' configuration.
        pnow = self.pos
        # Run the appropriate initialization routine (e.g. init_ADV).
        getattr(self, 'init_' + self._inst)()
        self.f.close()  # This has a small buffer, so close it.
        self.f = open(fname, 'rb', bufsize)  # This has a large buffer...
        self.close = self.f.close
        self.read = self.f.read
        if npings is not None:
            self.n_samp_guess = npings + 1
        self.f.seek(pnow, 0)  # Seek to the previous position.

    def _sci_data(self, vardict):
        """Convert the data to scientific units accordint to vardict.

        Parameters
        ----------
        vardict : (dict of :class:`<VarAttrs>`)
          The variable definitions in the :class:`<VarAttrs>` specify
          how to scale each data variable.

        """
        for nm, vd in vardict.iteritems():
            retval = vd.sci_func(getattr(self.data, nm))
            # This checks whether a new data object was created:
            # sci_func returns None if it modifies the existing data.
            if retval is not None:
                setattr(self.data, nm, retval)

    def _init_data(self, vardict):
        """Initialize the data object according to vardict.

        Parameters
        ----------
        vardict : (dict of :class:`<VarAttrs>`)
          The variable definitions in the :class:`<VarAttrs>` specify
          how to initialize each data variable.

        """
        for nm, va in vardict.iteritems():
            if not hasattr(self.data, nm):
                self.data.add_data(nm,
                                   va._empty_array(self.n_samp_guess),
                                   va.group)

    def checksum(self, byts):
        """
        Perform a checksum on `byts` and read the checksum value.
        """
        if self.do_checksum:
            if not np.sum(unpack(self.endian + (1 + len(byts) / 2) * 'H',
                                 self._thisid_bytes + byts)) + \
                    46476 - unpack(self.endian + 'H', self.read(2)):

                # !!!FIXTHIS error message.
                raise adv_base.db.CheckSumError('CheckSum Failed at ...')

        else:
            self.f.seek(2, 1)

    def read_id(self,):
        """
        Read the next 'ID' from the file.
        """
        self._thisid_bytes = bts = self.read(2)
        tmp = unpack(self.endian + 'BB', bts)
        if tmp[0] != 165:  # This catches a corrupted data block.
            print('Corrupted data block sync code. \
            Searching for next valid code...')
            val = int(self.findnext(do_cs=False), 0)
            self.f.seek(2, 1)
            return val
        # if self.debug:
        #    print( tmp[1] )
        return tmp[1]

    def read_user_cfg(self,):
        # ID: '0x00
        if self.debug:
            print('Reading user configuration (0x00)...')
        self.config.add_data('user', adv_base.ADVconfig('USER'))
        byts = self.read(508)
        tmp = unpack(
            self.endian + '2x5H13H6s4HI8H2x90H180s6H4xH2x2H2xH30x8H', byts)
            # the first two are the size.
        self.config.user.add_data(
            'Transmit', {'pulse length': tmp[0],
                         'blank distance': tmp[1],
                         'receive length': tmp[2],
                         'time_between_pings': tmp[3],
                         'time_between_bursts': tmp[4],
                         })
        self.config.user.add_data('Npings', tmp[5])
        self.config.user.add_data('AvgInterval', tmp[6])
        self.config.user.add_data('NBeams', tmp[7])
        self.config.user.add_data('TimCtrlReg', bin(tmp[8])[2:])
        self.config.user.add_data('PwrCtrlReg', bin(tmp[9])[2:])
        self.config.user.add_data('A1', tmp[10])
        self.config.user.add_data('B0', tmp[11])
        self.config.user.add_data('B1', tmp[12])
        self.config.user.add_data('CompassUpdRate', tmp[13])
        self.config.user.add_data(
            'CoordSystem', ['ENU', 'XYZ', 'BEAM'][tmp[14]])
        self.config.user.add_data('NBins', tmp[15])
        self.config.user.add_data('BinLength', tmp[16])
        self.config.user.add_data('MeasInterval', tmp[17])
        self.config.user.add_data('DeployName', tmp[18].partition('\x00')[0])
        self.config.user.add_data('WrapMode', tmp[19])
        self.config.user.add_data('ClockDeploy', np.array(tmp[20:23]))
        self.config.user.add_data('DiagInterval', tmp[23])
        self.config.user.add_data('Mode0', bin(tmp[24])[2:])
        self.config.user.add_data('AdjSoundSpeed', tmp[25])
        self.config.user.add_data('NSampDiag', tmp[26])
        self.config.user.add_data('NBeamsCellDiag', tmp[27])
        self.config.user.add_data('NPingsDiag', tmp[28])
        self.config.user.add_data('ModeTest', tmp[29])
        self.config.user.add_data('AnaInAddr', tmp[30])
        self.config.user.add_data('SWVersion', tmp[31])
        self.config.user.add_data('VelAdjTable', np.array(tmp[32:122]))
        self.config.user.add_data('Comments', tmp[122].partition('\x00')[0])
        self.config.user.add_data('Mode1', bin(tmp[123])[2:])
        self.config.user.add_data('DynPercPos', tmp[124])
        self.config.user.add_data('T1w', tmp[125])
        self.config.user.add_data('T2w', tmp[126])
        self.config.user.add_data('T3w', tmp[127])
        self.config.user.add_data('NSamp', tmp[128])
        self.config.user.add_data('NBurst', tmp[129])
        self.config.user.add_data('AnaOutScale', tmp[130])
        self.config.user.add_data('CorrThresh', tmp[131])
        self.config.user.add_data('TiLag2', tmp[132])
        self.config.user.add_data('QualConst', np.array(tmp[133:141]))
        self.checksum(byts)

    def read_head_cfg(self,):
        # ID: '0x04
        if self.debug:
            print('Reading head configuration (0x04)...')
        self.config.add_data('head', adv_base.ADVconfig('HEAD'))
        byts = self.read(220)
        tmp = unpack(self.endian + '2x3H12s176s22xH', byts)
        self.config.head.add_data('config', tmp[0])
        self.config.head.add_data('freq', tmp[1])
        self.config.head.add_data('type', tmp[2])
        self.config.head.add_data('serialNum', tmp[3])
        self.config.head.add_data('system', tmp[4])
        self.config.head.add_data('TransMatrix', np.array(
            unpack(self.endian + '9h', tmp[4][8:26])).reshape(3, 3) / 4096.)
        self.config.head.add_data('NBeams', tmp[5])
        self.checksum(byts)

    def read_hw_cfg(self,):
        # ID 0x05
        if self.debug:
            print('Reading hardware configuration (0x05)...')
        self.config.add_data('hardware', adv_base.ADVconfig('HARDWARE'))
        byts = self.read(44)
        tmp = unpack(self.endian + '2x14s6H12xI', byts)
        self.config.hardware.add_data('serialNum', tmp[0][:8])
        self.config.hardware.add_data('ProLogID', unpack('B', tmp[0][8])[0])
        self.config.hardware.add_data('ProLogFWver', tmp[0][10:])
        self.config.hardware.add_data('config', tmp[1])
        self.config.hardware.add_data('freq', tmp[2])
        self.config.hardware.add_data('PICversion', tmp[3])
        self.config.hardware.add_data('HWrevision', tmp[4])
        self.config.hardware.add_data('recSize', tmp[5] * 65536)
        self.config.hardware.add_data('status', tmp[6])
        self.config.hardware.add_data('FWversion', tmp[7])
        # tmp=unpack(self.endian+'2x8sBx4s6H12xI',byts)
        # self.config.hardware.add_data('serialNum',tmp[0][:8])
        # self.config.hardware.add_data('ProLogID',unpack('B',tmp[0][8])[0])
        # self.config.hardware.add_data('ProLogFWver',tmp[0][10:])
        # self.config.hardware.add_data('config',tmp[1])
        # self.config.hardware.add_data('freq',tmp[2])
        # self.config.hardware.add_data('PICversion',tmp[3])
        # self.config.hardware.add_data('HWrevision',tmp[4])
        # self.config.hardware.add_data('recSize',tmp[5]*65536)
        # self.config.hardware.add_data('status',tmp[6])
        # self.config.hardware.add_data('FWversion',tmp[7])
        self.checksum(byts)

    def read_vec_checkdata(self,):
        # ID: '0x07
        if self.debug:
            print('Reading vector check data (0x07)...')
        byts0 = self.read(6)
        tmp = unpack(self.endian + '2x2H', byts0)  # The first two are size.
        self.config.add_data('checkdata', adv_base.ADVconfig('CHECKDATA'))
        self.config.checkdata.add_data('Samples', tmp[0])
        n = self.config.checkdata.Samples
        self.config.checkdata.add_data('First_samp', tmp[1])
        self.config.checkdata.add_data('Amp1', np.empty(n, dtype=np.uint8))
        self.config.checkdata.add_data('Amp2', np.empty(n, dtype=np.uint8))
        self.config.checkdata.add_data('Amp3', np.empty(n, dtype=np.uint8))
        byts1 = self.read(3 * n)
        tmp = unpack(self.endian + (3 * n * 'B'), byts1)
        for idx, nm in enumerate(['Amp1', 'Amp2', 'Amp3']):
            self.config.checkdata[nm] = np.array(tmp[idx * n:(idx + 1) * n])
        self.checksum(byts0 + byts1)

    def sci_vec_data(self,):
        self._sci_data(nortek_defs.vec_data)

        self.data.add_data(
            'pressure', (self.data.PressureMSB.astype('float32') * 65536 +
                         self.data.PressureLSW.astype('float32')) / 1000.,
            None, 'env')

        self.data.pressure = ma.marray(
            self.data.pressure,
            ma.varMeta('P', ma.unitsDict({'dbar': 1}), ['time'])
        )

        self.data.del_data('PressureMSB', 'PressureLSW')

        self.data.props['fs'] = self.config.fs
        self.data.props['coord_sys'] = {
            'XYZ': 'inst',
            'ENU': 'earth',
            'BEAM': 'beam'}[self.config.user.CoordSystem]
        self.data.props['toff'] = 0
        # I must be able to calculate this here, right? # !!!TODO!!!
        self.data.props['doppler_noise'] = [0, 0, 0]

    def read_vec_data(self,):
        """
        Read vector data.
        """
        # ID: 0x10
        if not self.flag_lastread_sysdata:
            self.c += 1
        c = self.c

        if self.debug:
            print('Reading vector data (0x10)...')

        if not hasattr(self.data, '_u'):
            self._init_data(nortek_defs.vec_data)
            self._dtypes += ['vec_data']

        byts = self.read(20)
        (self.data.AnaIn2LSB[c],
         self.data.Count[c],
         self.data.PressureMSB[c],
         self.data.AnaIn2MSB[c],
         self.data.PressureLSW[c],
         self.data.AnaIn1[c],
         self.data._u[0, c],
         self.data._u[1, c],
         self.data._u[2, c],
         self.data._amp[0, c],
         self.data._amp[1, c],
         self.data._amp[2, c],
         self.data._corr[0, c],
         self.data._corr[1, c],
         self.data._corr[2, c]) = unpack(self.endian + '4B2H3h6B', byts)

        self.flag_lastread_sysdata = False
        self.checksum(byts)

    def sci_vec_sysdata(self,):
        """
        Turn the data in the vec_sysdata structure into scientific units.
        """
        self._sci_data(nortek_defs.vec_sysdata)
        self.data.add_data('_sysi', ~np.isnan(self.data.mpltime), '_essential')
        # These are the indices in the sysdata variables
        # that are not interpolated.
        # Skip the first entry for the interpolation process
        inds = np.nonzero(~np.isnan(self.data.mpltime))[0][1:]
        p = np.poly1d(np.polyfit(inds, self.data.mpltime[inds], 1))
        self.data.mpltime = p(np.arange(len(self.data.mpltime))
                              ).view(time.time_array)
        tbx.fillgaps(self.data.batt)
        tbx.fillgaps(self.data.c_sound)
        tbx.fillgaps(self.data.heading)
        tbx.fillgaps(self.data.pitch)
        tbx.fillgaps(self.data.roll)
        tbx.fillgaps(self.data.temp)

        tmpd = np.empty_like(self.data.heading)
        tmpd[:] = np.NaN
        # The first status bit should be the orientation.
        tmpd[self.data._sysi] = self.data.status[self.data._sysi] & 1
        tbx.fillgaps(tmpd, extrapFlg=True)
        slope = np.diff(tmpd)
        tmpd[1:][slope < 0] = 1
        tmpd[:-1][slope > 0] = 0
        self.data.add_data('orientation_down',
                           tmpd.astype('bool'),
                           '_essential')

    def read_vec_sysdata(self,):
        """
        Read vector system data.
        """
        # ID: 0x11
        self.flag_lastread_sysdata = True
        self.c += 1
        c = self.c
        # Need to make this a vector...
        if self.debug:
            print('Reading vector system data (0x11)...')
        if not hasattr(self.data, 'mpltime'):
            self._init_data(nortek_defs.vec_sysdata)
            self._dtypes += ['vec_sysdata']
        byts = self.read(24)
        # The first two are size (skip them).
        self.data.mpltime[c] = self.rd_time(byts[2:8])
        (self.data.batt[c],
         self.data.c_sound[c],
         self.data.heading[c],
         self.data.pitch[c],
         self.data.roll[c],
         self.data.temp[c],
         self.data.error[c],
         self.data.status[c],
         self.data.AnaIn[c]) = unpack(self.endian + '2H3hH2BH', byts[8:])
        self.checksum(byts)

    def sci_microstrain(self,):
        """
        Rotate orientation data into ADV coordinate system.
        """
        # MS = MicroStrain
        for nm in self._orient_dnames:
            # Rotate the MS orientation data (in MS coordinate system)
            # to be consistent with the ADV coordinate system.
            # (x,y,-z)_ms = (z,y,x)_adv
            (self.data[nm][2],
             self.data[nm][0]) = (self.data[nm][0],
                                  -self.data[nm][2].copy())
            # tmp=self.data[nm][2].copy()
            # self.data[nm][2]=self.data[nm][0]
            # self.data[nm][0]=tmp
            # self.data[nm][2]*=-1
            # self.data[nm]=np.roll(self.data[nm],-1,axis=0) # I think this is
            # wrong.
        if 'orientmat' in self._orient_dnames:
            # MS coordinate system is in North-East-Down (NED),
            # we want East-North-Up (ENU)
            self.data.orientmat[:, 2] *= -1
            (self.data.orientmat[:, 0],
             self.data.orientmat[:, 1]) = (self.data.orientmat[:, 1],
                                           self.data.orientmat[:, 0].copy())
        if hasattr(self.data, 'Accel'):
            # This value comes from the MS 3DM-GX3 MIP manual.
            self.data.Accel *= 9.80665
            self.data.Accel = ma.marray(self.data.Accel, ma.varMeta(
                'accel', units={'m': 1, 's': -2}, dim_names=['xyz', 'time'],))
            self.data.AngRt = ma.marray(self.data.AngRt, ma.varMeta(
                'angRt', units={'s': -1}, dim_names=['xyz', 'time'],))

    def read_microstrain(self,):
        """
        Read microstrain sensor data.
        """
        # 0x71
        if self.flag_lastread_sysdata:
            # This handles a bug where the system data gets written between the
            # last 'vec_data' and its associated 'microstrain' data.
            self.flag_lastread_sysdata = False
            self.c -= 1
        if self.debug:
            print('Reading vector microstrain data (0x71)...')
        byts0 = self.read(4)
        ahrsid = unpack(self.endian + '3xB', byts0)[
            0]  # The first 2 are the size, 3rd is count, 4th is the id.
        c = self.c
        if not hasattr(self.data, 'Accel'):
            self._dtypes += ['microstrain']
            if ahrsid in [204, 210]:
                self._orient_dnames = ['Accel', 'AngRt', 'Mag', 'orientmat']
                self.data.add_data(
                    'Accel',
                    np.empty((3, self.n_samp_guess), dtype=np.float32),
                    'orient'
                )
                self.data.add_data(
                    'AngRt',
                    np.empty((3, self.n_samp_guess), dtype=np.float32),
                    'orient')
                self.data.add_data(
                    'Mag',
                    np.empty((3, self.n_samp_guess), dtype=np.float32),
                    'orient'
                )
                self.data.props['rotate_vars'].update(
                    {'Accel', 'AngRt', 'Mag'})
                if ahrsid == 204:
                    self.data.add_data('orientmat', np.empty(
                        (3, 3, self.n_samp_guess), dtype=np.float32), 'orient')
            elif ahrsid == 211:
                self._orient_dnames = ['Angle', 'Veloc', 'MagVe']
                self.data.add_data(
                    'Angle',
                    np.empty((3, self.n_samp_guess), dtype=np.float32),
                    'orient'
                )
                self.data.add_data(
                    'Veloc',
                    np.empty((3, self.n_samp_guess), dtype=np.float32),
                    'orient'
                )
                self.data.add_data(
                    'MagVe',
                    np.empty((3, self.n_samp_guess), dtype=np.float32),
                    'orient'
                )
                self.data.props['rotate_vars'].update(
                    {'Angle', 'Veloc', 'MagVe'})
        if ahrsid == 204:  # 0xcc
            byts = self.read(78)
            dt = unpack(self.endian + 'ffffffffffffffffff6x', byts)
                        # This skips the "DWORD" (4 bytes) and the AHRS
                        # checksum (2 bytes)
            self.data.Accel[:, c], self.data.AngRt[
                :, c], self.data.Mag[:, c] = (dt[0:3], dt[3:6], dt[6:9],)
            self.data.orientmat[:,:, c] = ((dt[9:12], dt[12:15], dt[15:18]))
        # Still need to add a reader for the other two ahrsid's (211,210).
        self.checksum(byts0 + byts)

    def read_vec_hdr(self,):
        # ID: '0x12
        if self.debug:
            print('Reading vector header data (0x12)...')
        byts = self.read(38)
        tmp = unpack(self.endian + '8xH7B21x', byts)
                     # The first two are size, the next 6 are time.
        self.config.add_data('data_header', adv_base.ADVconfig('DATA HEADER'))
        self.config.data_header.add_data('time', self.rd_time(byts[2:8]))
        self.config.data_header.add_data('NRecords', tmp[0])
        self.config.data_header.add_data('Noise1', tmp[1])
        self.config.data_header.add_data('Noise2', tmp[2])
        self.config.data_header.add_data('Noise3', tmp[3])
        self.config.data_header.add_data('Spare0', tmp[4])
        self.config.data_header.add_data('Corr1', tmp[5])
        self.config.data_header.add_data('Corr2', tmp[6])
        self.config.data_header.add_data('Corr3', tmp[7])
        self.checksum(byts)

    def read_awac_profile(self,):
        # ID: '0x20'
        if self.debug:
            print('Reading AWAC velocity data (0x20)...')
        nbins = self.config.user.NBins
        if not hasattr(self.data, 'temp'):
            self._init_data(nortek_defs.awac_profile)
            self._dtypes += ['awac_profile']

        byts = self.read(116 + 9 * nbins + np.mod(nbins, 2))
                         # There is a 'fill' byte at the end, if nbins is odd.
        self.c += 1
        c = self.c
        self.data.mpltime[c] = self.rd_time(byts[2:8])
        (self.data.Error[c],
         self.data.AnaIn1[c],
         self.data.batt[c],
         self.data.c_sound[c],
         self.data.heading[c],
         self.data.pitch[c],
         self.data.roll[c],
         p_msb,
         self.data.status[c],
         p_lsw,
         self.data.temp[c],) = unpack(self.endian + '7HBB2H', byts[8:28])
        self.data.pressure[c] = (65536 * p_msb + p_lsw)
        # The nortek system integrator manual specifies an 88byte 'spare'
        # field, therefore we start at 116.
        tmp = unpack(self.endian + str(3 * nbins) + 'h' +
                     str(3 * nbins) + 'B', byts[116:116 + 9 * nbins])
        for idx in range(3):
            self.data._u[idx,:, c] = tmp[idx * nbins: (idx + 1) * nbins]
            self.data._amp[idx,:, c] = tmp[(idx + 3) * nbins:
                                            (idx + 4) * nbins]
        self.checksum(byts)

    def sci_awac_profile(self,):
        self._sci_data(nortek_defs.awac_profile)
        # Calculate the ranges.
        # This information comes from the nortek knowledgebase:
        # http://www.nortekusa.com/en/knowledge-center/forum/hr-profilers/736804717
        cs_coefs = {2000: 0.0239,
                    1000: 0.0478,
                    600: 0.0797,
                    400: 0.1195}
        h_ang = 25 * np.pi / 180  # The head angle is 25 degrees for all awacs.
        cs = np.float(self.config.user.BinLength) / 256. * \
            cs_coefs[self.config.head.freq] * np.cos(h_ang)
        bd = self.config.user.Transmit['blank distance'] * \
            0.0229 * np.cos(h_ang) - cs

        # These are the centers of the cells:
        self.data.add_data(
            'range',
            ma.marray(
                np.float32(np.arange(self.config.user.NBins) + cs / 2 + bd),
                ma.varMeta('range', {'m': 1}, ['depth'])), '_essential')
        self.config.add_data('cell_size', cs)
        self.config.add_data('blank_dist', bd)
        # self.

    def code_spacing(self, searchcode, iternum=50):
        """
        Find the spacing, in bytes, between a specific hardware code.
        Repeat this * iternum * times(default 50).
        Returns the average spacing, in bytes, between the code.
        """
        p0 = self.findnextid(searchcode)
        for i in range(iternum):
            self.findnextid(searchcode)
        # Compute the average of the data size:
        return (self.pos - p0) / iternum

    def init_ADV(self,):
        self.data = adv_base.ADVraw()
        self.data.add_data('config', self.config, 'config')
        self.data.props = {}
        self.data.props['inst_make'] = 'Nortek'
        self.data.props['inst_model'] = 'VECTOR'
        self.data.props['inst_type'] = 'ADV'
        self.data.props['rotate_vars'] = {'_u', }
        # Question to Nortek: How do they determine how many samples are in a
        # file, in order to initialize arrays?
        dlta = self.code_spacing('0x11')
        self.config.add_data('fs', 512 / self.config.user.AvgInterval)
        self.n_samp_guess = self.filesize / dlta + 1
        self.n_samp_guess *= self.config.fs

    def init_AWAC(self,):
        self.data = adp.adcp_raw()
        self.data.add_data('config', self.config, 'config')
        self.data.props = {}
        self.data.props['inst_make'] = 'Nortek'
        self.data.props['inst_model'] = 'AWAC'
        self.data.props['inst_type'] = 'ADP'
        self.n_samp_guess = self.filesize / self.code_spacing('0x20') + 1
        # self.n_samp_guess=1000
        # self.n_samp_guess*=self.config.fs

    @property
    def filesize(self,):
        if not hasattr(self, '_filesz'):
            pos = self.pos
            self.f.seek(0, 2)
                        # Seek to the end of the file to determine the
                        # filesize.
            self._filesz = self.pos
            self.f.seek(pos, 0)  # Return to the initial position.
        return self._filesz

    @property
    def pos(self,):
        return self.f.tell()

    def rd_time(self, strng):
        """
        Read the time from the first 6bytes of the input string.
        """
        min, sec, day, hour, year, month = unpack('BBBBBB', strng[:6])
        return time.date2num(time.datetime(
            time._fullyear(_bcd2char(year)),
            _bcd2char(month),
            _bcd2char(day),
            _bcd2char(hour),
            _bcd2char(min),
            _bcd2char(sec)
        ))

    def findnext(self, do_cs=True):
        """
        Find the next data block by checking the checksum,
        and the sync byte(0xa5).
        """
        # I may want to use fd.cs for this,
        # but right now I'm not going to worry about it.
        # cstmp=self.fd.cs._cs # reset this at the end of the script
        # eb=self.fd.cs._error_behavior # reset this at the end of the script
        # self.fd.cs.init(46476,2,'silent')
        sum = np.uint16(int('0xb58c', 0))  # Initialize the sum
        cs = 0
        func = _bitshift8
        func2 = np.uint8
        if self.endian == '<':
            func = np.uint8
            func2 = _bitshift8
        while True:
            try:
                val = unpack(self.endian + 'H', self.read(2))[0]
            except:
                if not len(self.read(2)) == 2:
                    break
            if func(val) == 165 and (not do_cs or cs == np.uint16(sum)):
                self.f.seek(-2, 1)
                return hex(func2(val))
            sum += cs
            cs = val

    def findnextid(self, id):
        if id.__class__ is str:
            id = int(id, 0)
        while int(self.findnext(), 0) != id:
            pass
        return self.pos

    def readnext(self,):
        try:
            id = '0x%02x' % self.read_id()
        except str_err:
            return 1
        if id in self.fun_map.keys():
            # This can cause some funny behavior if self.f.read throws an
            # "error". It is an attempt at finding the eof, but there may be a
            # better way.
            try:
                getattr(self, self.fun_map[id])()
                return
            except str_err:
                return 2
        else:
            print('Unrecognized identifier: ' + id)
            self.f.seek(-2, 1)
            return 10

    def readfile(self, nlines=None):
        print('Reading file %s ...' % self.fname)
        # self.progbar=db.progress_bar(self.filesz)
        # self.progbar.init()
        retval = None
        while not retval:
            if self.c == nlines:
                break
            retval = self.readnext()
            if retval == 10:
                self.findnext()
                retval = None
            if self._npings is not None and self.c >= self._npings:
                break
        if retval == 2:
            self.c -= 1
        for nm, dat in self.data.iter():
            if (hasattr(getattr(self.data, nm), 'shape') and
                (getattr(self.data, nm).shape[-1]
                 == self.n_samp_guess)):
                setattr(self.data, nm, dat[..., :self.c])

    def dat2sci(self,):
        for nm in self._dtypes:
            getattr(self, 'sci_' + nm)()

    def __exit__(self, type, value, trace,):
        self.close()

    def __enter__(self,):
        return self


if __name__ == '__main__':

    datdir = 'home/lkilcher/data/ttm_dem_june2012/TTM_AWAC/'

    datfile = datdir + '/TTM_AWAC_Jun2012.wpr'

    # d=np.zeros(100)
    rdr = NortekReader(datfile, debug=False, do_checksum=True)
    rdr.readfile()
    rdr.dat2sci()

    # with vec_reader(datfile,debug=False,do_checksum=False) as rdr:
    # rdr.readfile()
    # rdr.dat2sci()
