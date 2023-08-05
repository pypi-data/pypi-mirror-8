#!/usr/bin/env python

from barobo import Linkbot, Dongle
import barobo
import time
import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print ("Usage: {0} <Com_Port> [Linkbot Serial ID]".format(sys.argv[0]))
        quit()
    if len(sys.argv) == 3:
        serialID = sys.argv[2]
    else:
        serialID = None
    dongle = Dongle()
    dongle.connectDongleSFP(sys.argv[1])
    linkbot = dongle.getLinkbot(serialID)

    linkbot.recordAnglesBegin(delay=0.1)
    linkbot.setAcceleration(120)
    for _ in range(1):
        linkbot.setJointStates(
                [barobo.ROBOT_FORWARD, barobo.ROBOT_FORWARD, barobo.ROBOT_BACKWARD], 
                [120, 120, 120])
        time.sleep(5)
        linkbot.setJointStates(
                [barobo.ROBOT_BACKWARD, barobo.ROBOT_BACKWARD, barobo.ROBOT_FORWARD], 
                [120, 120, 120])
        time.sleep(2)
    linkbot.stop()
    linkbot.recordAnglesEnd()
    linkbot.recordAnglesPlot()
