# Set sensors to indicate that C/MRI nodes are polling OK
#
# Created by Bob Jacobsen 2014
#
# Since JMRI 3.9.4

import jmri

import java

class CmriNodeMonitor(jmri.jmrit.automat.AbstractAutomaton) :
    nodeList = []
    nodeAddrList = []
    maxNodeAddr = 128
    delay = 2000
    
    def init(self) :
        i = 0
        while i < self.maxNodeAddr :
            x = (i * 1000) + 1
            txt = "CT" + str(x)
            node = jmri.jmrix.cmri.serial.SerialAddress.getNodeFromSystemName(txt)
            if (node != None) :
                print "Start monitoring C/MRI node " + str(i)
                self.nodeList.append(node)
                self.nodeAddrList.append(i)
            i = i + 1
        return

    # handle() will execute periodically, each time setting the sensors
    def handle(self) :
        i = 0
        while i < len(self.nodeAddrList) :
            if (self.nodeList[i].isPollingOK()) :
                sensors.provideSensor("IS$CMRI_NODE$"+str(self.nodeAddrList[i])).setKnownState(ACTIVE)
            else :
                sensors.provideSensor("IS$CMRI_NODE$"+str(self.nodeAddrList[i])).setKnownState(INACTIVE)
            i = i + 1

        self.waitMsec(self.delay)        
        return 1

CmriNodeMonitor().start()
