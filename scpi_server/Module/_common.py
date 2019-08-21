import Adafruit_BBIO.GPIO as GPIO
from Adafruit_BBIO.SPI import SPI
import Lib

__methods__ = []
register_method = Lib.register_method(__methods__)


@register_method
def common_dict(self):
    self.common = {
        '*CLS': self.clear_status(),
        '*ESE': self.set_ese(),
        '*ESE?': self.reg_status(),
        '*ESR?': self.reg_status_clean(),
        '*IDN?': self.device_id(),
        '*IST?': self.status(),
        '*OPC': self.op_complete(),
        '*OPC?': self.is_op_complete(),
        '*RST': self.reset_tree(),
        '*SRE': self.serv_enable(),
        '*SRE?': self.serv_query(),
        '*STB?': self.status_byte(),
        '*TST?': self.self_test(),
        '*WAI': self.wait()
    }


@register_method
def clear_status(self):
    pass


@register_method
def set_ese(self):
    pass


@register_method
def reg_status(self):
    pass


@register_method
def reg_status_clean(self):
    pass


@register_method
def device_id(self):
    self.response = "The device is created for the request of precise voltage controlling using " \
                    "boards with DAC chips. Implementation project for MPQ by Maksymilian " \
                    "Kliczkowski\n "


@register_method
def status(self):
    pass


@register_method
def op_complete(self):
    pass


@register_method
def is_op_complete(self):
    pass


@register_method
def reset_tree(self):
    self.clear_path()


@register_method
def serv_enable(self):
    pass


@register_method
def serv_query(self):
    pass


@register_method
def status_byte(self):
    pass


@register_method
def self_test(self):
    pass


@register_method
def wait(self):
    pass
