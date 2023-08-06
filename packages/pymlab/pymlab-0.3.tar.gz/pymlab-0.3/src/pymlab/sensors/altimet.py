#!/usr/bin/env python


from pymlab.sensors import Device
import time


class ALTIMET01(Device):
    """
    Python library for ALTIMET01A MLAB module with MPL3115A2 Freescale Semiconductor i2c altimeter and barometer sensor.
    """
    
    def __init__(self, parent = None, address = 0x60, **kwargs):
        Device.__init__(self, parent, address, **kwargs)
        
        #MPL3115A register address
        self.MPL3115_STATUS              =0x00
        self.MPL3115_PRESSURE_DATA       =0x01
        self.MPL3115_DR_STATUS           =0x06
        self.MPL3115_DELTA_DATA          =0x07
        self.MPL3115_WHO_AM_I            =0x0c
        self.MPL3115_FIFO_STATUS         =0x0d
        self.MPL3115_FIFO_DATA           =0x0e
        self.MPL3115_FIFO_SETUP          =0x0e
        self.MPL3115_TIME_DELAY          =0x10
        self.MPL3115_SYS_MODE            =0x11
        self.MPL3115_INT_SORCE           =0x12
        self.MPL3115_PT_DATA_CFG         =0x13
        self.MPL3115_BAR_IN_MSB          =0x14
        self.MPL3115_P_ARLARM_MSB        =0x16
        self.MPL3115_T_ARLARM            =0x18
        self.MPL3115_P_ARLARM_WND_MSB    =0x19
        self.MPL3115_T_ARLARM_WND        =0x1b
        self.MPL3115_P_MIN_DATA          =0x1c
        self.MPL3115_T_MIN_DATA          =0x1f
        self.MPL3115_P_MAX_DATA          =0x21
        self.MPL3115_T_MAX_DATA          =0x24
        self.MPL3115_CTRL_REG1           =0x26
        self.MPL3115_CTRL_REG2           =0x27
        self.MPL3115_CTRL_REG3           =0x28
        self.MPL3115_CTRL_REG4           =0x29
        self.MPL3115_CTRL_REG5           =0x2a
        self.MPL3115_OFFSET_P            =0x2b
        self.MPL3115_OFFSET_T            =0x2c
        self.MPL3115_OFFSET_H            =0x2d
    
    def initialize(self):
        # Set to Barometer  
        self.bus.write_byte_data(self.address, self.MPL3115_CTRL_REG1, 0xB8);
        # Enable Data Flags in PT_DATA_CFG
        self.bus.write_byte_data(self.address, self.MPL3115_PT_DATA_CFG, 0x07)
        # Set Active, barometer mode with an OSR = 128
        self.bus.write_byte_data(self.address, self.MPL3115_CTRL_REG1, 0x39)
    
    def get_tp(self):
        # Read STATUS Register
        #STA = self.bus.read_byte(MPL3115_STATUS)
        # check if pressure or temperature are ready (both) [STATUS, 0x00 register]
        #if (int(STA,16) & 0x04) == 4:
        # OUT_P
        p_MSB = self.bus.read_byte_data(self.address,0x01)
        p_CSB = self.bus.read_byte_data(self.address,0x02)
        p_LSB = self.bus.read_byte_data(self.address,0x03)
        
        t_MSB = self.bus.read_byte_data(self.address,0x04)
        t_LSB = self.bus.read_byte_data(self.address,0x05)
        
        #Determine sign and output
        if (t_MSB > 0x7F):
            t_MSB = ~t_MSB + 1
            sign = -1
        else:
                sign = 1
        # conversion of register values to measured values according to sensor datasheet
        t = sign * float(t_MSB + (t_LSB >> 4)/16.0)    
        p = float((p_MSB << 10)|(p_CSB << 2)|(p_LSB >> 6)) + float((p_LSB >> 4)/4.0)
        return (t, p);


class SDP6XX(Device):
    """
    Python library for Sensirion SDP6XX/5xx differential preassure sensors.
    """
    
    def __init__(self, parent = None, address = 0x40, **kwargs):
        Device.__init__(self, parent, address, **kwargs)

        self.TRIGGER_MEASUREMENT = 0xF1     # command: trigger differential pressure measurement
        self.SOFT_RESET          = 0xFE     # command: soft reset
        self.READ_USER_REGISTER  = 0xE5     # command: read advanced user register
        self.WRITE_USER_REGISTER = 0xE4     # command: write advanced user register

        self.RESOLUTION_9BIT     = 0x00
        self.RESOLUTION_10BIT    = 0x01
        self.RESOLUTION_11BIT    = 0x02
        self.RESOLUTION_12BIT    = 0x03
        self.RESOLUTION_13BIT    = 0x04
        self.RESOLUTION_14BIT    = 0x05
        self.RESOLUTION_15BIT    = 0x06
        self.RESOLUTION_16BIT    = 0x07

    def get_p(self):
        self.bus.write_byte(self.address, self.TRIGGER_MEASUREMENT);    # trigger measurement
        MSB = self.bus.read_byte(self.address)      # read data
        LSB = self.bus.read_byte(self.address)
        check = self.bus.read_byte(self.address)    # read CRC
        print hex(MSB), hex(LSB), hex(check)
        pressure = (MSB << 8) | LSB
        if (pressure & 0x1000):
            pressure -= 65536

        return (pressure/60.0)


# bit;        // bit mask
# crc = 0x00; // calculated checksum
# byteCtr;    // byte counter
  
#          # calculates 8-Bit checksum with given polynomial
#          for(byteCtr = 0; byteCtr < nbrOfBytes; byteCtr++)
#            crc ^= (data[byteCtr]);
#            for(bit = 8; bit > 0; --bit)
#              if(crc & 0x80) crc = (crc << 1) ^ POLYNOMIAL;
#              else           crc = (crc << 1);
          
          # verify checksum
#          if(crc != checksum) return CHECKSUM_ERROR;
#          else                return NO_ERROR;

    def reset(self):
        self.bus.write_byte(self.address, 0xFE);    # trigger measurement
        time.sleep(0.01)


def main():
    print __doc__


if __name__ == "__main__":
    main()

