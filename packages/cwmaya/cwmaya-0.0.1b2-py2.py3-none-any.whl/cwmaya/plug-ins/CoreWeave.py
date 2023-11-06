import sys

import maya.api.OpenMaya as om
from cwmaya.nodes.cwSubmission import cwSubmission
from cwmaya.lib import coreweave_menu

def maya_useNewAPI():
    pass

def initializePlugin(obj):
 
    plugin = om.MFnPlugin(obj, "CoreWeave", "0.0.1-beta.2", "Any")
 
    try:
        plugin.registerNode(
            "cwSubmission",
            cwSubmission.id,
            cwSubmission.creator,
            cwSubmission.initialize,
            om.MPxNode.kDependNode,
        )
    except:
        sys.stderr.write("Failed to register cwSubmission\n")
        raise


    coreweave_menu.load()

    # coredata.init("maya-io")


def uninitializePlugin(obj):
    plugin = om.MFnPlugin(obj)

    try:
        plugin.deregisterNode(cwSubmission.id)
    except:
        sys.stderr.write("Failed to deregister cwSubmission\n")
        raise

    coreweave_menu.unload()
