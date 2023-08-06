from twisted.internet.ssl import CertificateOptions, ContextFactory

from txsni.only_noticed_pypi_pem_after_i_wrote_this import (
    certificateOptionsFromPileOfPEM
)

class SNIMap(ContextFactory, object):
    def __init__(self, mapping):
        self.mapping = mapping
        try:
            self.context = self.mapping['DEFAULT'].getContext()
        except KeyError:
            self.context = CertificateOptions().getContext()
        self.context.set_tlsext_servername_callback(
            self.selectContext
        )

    def getContext(self):
        return self.context

    def selectContext(self, connection):
        connection.set_context(
            self.mapping[connection.get_servername()]
            .getContext()
        )



class HostDirectoryMap(object):
    def __init__(self, directoryPath):
        self.directoryPath = directoryPath


    def __getitem__(self, hostname):
        filePath = self.directoryPath.child(hostname + ".pem")
        if filePath.isfile():
            return certificateOptionsFromPileOfPEM(filePath.getContent())
        else:
            raise KeyError("no pem file for " + hostname)
