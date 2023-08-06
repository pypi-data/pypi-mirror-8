# -*- coding: utf-8 -*-
#
# Output to File classes.
#
# Author: Just van den Broecke
#
from stetl.output import Output
from stetl.util import Util
from stetl.packet import FORMAT

import os

log = Util.get_log('fileoutput')


class FileOutput(Output):
    """
    Pretty print input to file. Input may be an etree doc or any other stringify-able input.

    consumes=FORMAT.any
    """

    def __init__(self, configdict, section):
        Output.__init__(self, configdict, section, consumes=FORMAT.any)
        log.info("working dir %s" % os.getcwd())

    def write(self, packet):
        if packet.data is None:
            return packet

        file_path = self.cfg.get('file_path')
        return self.write_file(packet, file_path)

    def write_file(self, packet, file_path):
        log.info('writing to file %s' % file_path)
        out_file = open(file_path, 'w')

        out_file.write(packet.to_string())

        out_file.close()
        log.info("written to %s" % file_path)
        return packet

class MultiFileOutput(FileOutput):
    """
    Print to multiple files from subsequent packets like strings or etree docs.

    consumes=FORMAT.any
    """
    def __init__(self, configdict, section):
        Output.__init__(self, configdict, section, consumes=FORMAT.any)
        self.file_num = 1

    def write(self, packet):
        if packet.data is None:
            return packet

        # file_path can be of the form: gmlcities-%03d.gml
        file_path = self.cfg.get('file_path')
        file_path %= self.file_num
        self.file_num += 1
        return self.write_file(packet, file_path)
