from __future__ import unicode_literals
import json

import maya.api.OpenMaya as om

def maya_useNewAPI():
    pass

class cwSubmission(om.MPxNode):
    # pass

    aTitle = None
    aOutput = None

    id = om.MTypeId(0x880501)

    @staticmethod
    def creator():
        return cwSubmission()

    @classmethod
    def initialize(cls):
        cls.make_title_att()
        cls.make_output_att()
        cls.setup_attribute_affects()
        
    @classmethod
    def make_title_att(cls):
        tAttr = om.MFnTypedAttribute()
        cls.aTitle = tAttr.create("title", "ttl", om.MFnData.kString)
        tAttr.hidden = False
        tAttr.storable = True
        tAttr.readable = True
        tAttr.writable = True
        om.MPxNode.addAttribute(cls.aTitle)
        
    @classmethod
    def make_output_att(cls):
        """
        Output atttribute.
        """
        tAttr = om.MFnTypedAttribute()
        cls.aOutput = tAttr.create("output", "out", om.MFnData.kString)
        tAttr.readable = True
        tAttr.storable = False
        tAttr.writable = False
        tAttr.keyable = False

        om.MPxNode.addAttribute(cls.aOutput)

    @classmethod
    def setup_attribute_affects(cls):
        om.MPxNode.attributeAffects(cls.aTitle, cls.aOutput)

    def compute(self, plug, data):
        """Compute output json from input attribs."""
        if not (
            (plug == self.aOutput)
        ):
            return None
        result = {}
        result.update(self.get_title(data))
        
        handle = data.outputValue(self.aOutput)
        handle.setString(json.dumps(result))

        data.setClean(plug)
        return self

    @classmethod
    def get_title(cls, data):
        title = data.inputValue(cls.aTitle).asString()
        return {"job_title": title}
