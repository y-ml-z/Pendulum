import sys
import os
import rlglue.network.Network as Network


def get_svn_codec_version():
    SVN_GLUE_VERSION="$Revision: 738 $"
    justTheNumber=SVN_GLUE_VERSION[11:len(SVN_GLUE_VERSION)-2]
    return justTheNumber

def get_codec_version():
    return "2.1"

network = None
class Observation_action(object):
    def __init__(self,theObservation=None,theAction=None):
        if theObservation != None:
            self.o = theObservation
        else:
            self.o = Observation()
        if theAction != None:
            self.a = theAction
        else:
            self.a = Action()
class Reward_observation_action_terminal(object):
    def __init__(self,reward=None, theObservation=None, theAction=None, terminal=None):
        if reward != None:
            self.r = reward
        else:
            self.r = 0.0
        if theObservation != None:
            self.o = theObservation
        else:
            self.o = Observation()
        if theAction != None:
            self.a = theAction
        else:
            self.a = Action()
        if terminal != None:
            self.terminal = terminal
        else:
            self.terminal = False

def forceConnection():
    global network
    if network == None:

        theSVNVersion=get_svn_codec_version()
        theCodecVersion=get_codec_version()

        host = Network.kLocalHost
        port = Network.kDefaultPort

        hostString = os.getenv("RLGLUE_HOST")
        portString = os.getenv("RLGLUE_PORT")

        if (hostString != None):
            host = hostString

        try:
            port = int(portString)
        except TypeError:
            port = Network.kDefaultPort

        print "RL-Glue Python Experiment Codec Version: "+theCodecVersion+" (Build "+theSVNVersion+")"
        print "\tConnecting to " + host + " on port " + str(port) + "..."
        sys.stdout.flush()


        network = Network.Network()
        network.connect(host,port)
        network.clearSendBuffer()
        network.putInt(Network.kExperimentConnection)
        network.putInt(0)
        network.send()

def doStandardRecv(state):
    network.clearRecvBuffer()
    recvSize = network.recv(8) - 8

    glueState = network.getInt()
    dataSize = network.getInt()
    remaining = dataSize - recvSize

    if remaining < 0:
        remaining = 0

    remainingReceived = network.recv(remaining)

    # Already read the header, so discard it
    network.getInt()
    network.getInt()

    if (glueState != state):
        sys.stderr.write("Not synched with server. glueState = " + str(glueState) + " but should be " + str(state) + "\n")
        sys.exit(1)


def doCallWithNoParams(state):
    network.clearSendBuffer()
    network.putInt(state)
    network.putInt(0)
    network.send()


def RL_init():
    forceConnection()
    doCallWithNoParams(Network.kRLInit)
    doStandardRecv(Network.kRLInit)
    #Brian Tanner added
    taskSpecResponse = network.getString()
    return taskSpecResponse


def RL_start():
    obsact = None
    doCallWithNoParams(Network.kRLStart)
    doStandardRecv(Network.kRLStart)
    obsact = Observation_action()
    obsact.o = network.getObservation()
    obsact.a = network.getAction()
    return obsact

 
def RL_step():
    roat = None
    doCallWithNoParams(Network.kRLStep)
    doStandardRecv(Network.kRLStep)
    roat = Reward_observation_action_terminal()
    roat.terminal = network.getInt()
    roat.r = network.getDouble()
    roat.o = network.getObservation()
    roat.a = network.getAction()
    return roat

def RL_cleanup():
    doCallWithNoParams(Network.kRLCleanup)
    doStandardRecv(Network.kRLCleanup)

def RL_agent_message(message):
    if message == None:
        message=""
    response = ""
    forceConnection()
    network.clearSendBuffer()
    network.putInt(Network.kRLAgentMessage)
    #Payload Size
    network.putInt(len(message) + 4)
    network.putString(message)
    network.send()
    doStandardRecv(Network.kRLAgentMessage)
    response = network.getString()
    return response

def RL_env_message(message):
    if message == None:
        message=""
    response = ""
    forceConnection()
    network.clearSendBuffer()
    network.putInt(Network.kRLEnvMessage)
    #Payload Size
    network.putInt(len(message) + 4)
    network.putString(message)
    network.send()
    doStandardRecv(Network.kRLEnvMessage)
    response = network.getString()
    return response

def RL_return():
    reward = 0.0
    doCallWithNoParams(Network.kRLReturn)
    doStandardRecv(Network.kRLReturn)
    reward = network.getDouble()
    return reward

def RL_num_steps():
    numSteps = 0
    doCallWithNoParams(Network.kRLNumSteps)
    doStandardRecv(Network.kRLNumSteps)
    numSteps = network.getInt()
    return numSteps

def RL_num_episodes():
    numEpisodes = 0
    doCallWithNoParams(Network.kRLNumEpisodes)
    doStandardRecv(Network.kRLNumEpisodes)
    numEpisodes = network.getInt()
    return numEpisodes


def RL_episode(num_steps):
    network.clearSendBuffer()
    network.putInt(Network.kRLEpisode)
    network.putInt(Network.kIntSize)
    network.putInt(num_steps)
    network.send()
    doStandardRecv(Network.kRLEpisode)
    #Brian Tanner added
    exitStatus = network.getInt()
    return exitStatus