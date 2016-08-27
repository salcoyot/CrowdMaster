import bpy
from bpy.types import NodeTree, Node, NodeSocket
from bpy.props import FloatProperty, StringProperty, BoolProperty
from bpy.props import EnumProperty, IntProperty, FloatVectorProperty
from .. icon_load import cicon

class CrowdMasterAGenTree(NodeTree):
    '''CrowdMaster agent generation node tree'''
    bl_idname = 'CrowdMasterAGenTreeType'
    bl_label = 'CrowdMaster Agent Generation'
    bl_icon = 'MOD_ARRAY'

class GeoSocket(NodeSocket):
    '''Geo node socket type'''
    bl_idname = 'GeoSocketType'
    bl_label = 'Geo Node Socket'

    def draw(self, context, layout, node, text):
        layout.label(text)

    def draw_color(self, context, node):
        return (0.125, 0.125, 0.575, 1.0)

class VectorSocket(NodeSocket):
    '''Vector node socket type'''
    bl_idname = 'VectorSocketType'
    bl_label = 'Vector Node Socket'

    def draw(self, context, layout, node, text):
        layout.label(text)

    def draw_color(self, context, node):
        return (0.35, 0.35, 0.35, 1.0)

class TemplateSocket(NodeSocket):
    '''Template node socket type'''
    bl_idname = 'TemplateSocketType'
    bl_label = 'Template Node Socket'

    def draw(self, context, layout, node, text):
        layout.label(text)

    def draw_color(self, context, node):
        return (0.125, 0.575, 0.125, 1.0)
        

class ObjectSocket(NodeSocket):
    '''Object node socket type'''
    bl_idname = 'ObjectSocketType'
    bl_label = 'Object Node Socket'

    inputObject = StringProperty(name="Object")

    def draw(self, context, layout, node, text):
        if self.is_linked:
            layout.label(text)
        else:
            layout.prop_search(self, "inputObject", context.scene, "objects", text=text)

    def draw_color(self, context, node):
        return (1.0, 0.5, 0.2, 0.5)

class GroupSocket(NodeSocket):
    '''Group node socket type'''
    bl_idname = 'GroupSocketType'
    bl_label = 'Group Node Socket'

    inputGroup = StringProperty(name="Group")

    def draw(self, context, layout, node, text):
        if self.is_linked:
            layout.label(text)
        else:
            layout.prop_search(self, "inputGroup", bpy.data, "groups", text=text)

    def draw_color(self, context, node):
        return (1.0, 0.5, 0.2, 0.5)

class CrowdMasterAGenTreeNode:
    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'CrowdMasterAGenTreeType'

class GenerateNode(Node, CrowdMasterAGenTreeNode):
    '''The generate node'''
    bl_idname = 'GenerateNodeType'
    bl_label = 'Generate'
    bl_icon = 'SOUND'

    def init(self, context):
        self.inputs.new('TemplateSocketType', "Templates")
        self.inputs[0].link_limit = 4095

    def draw_buttons(self, context, layout):
        layout.scale_y = 1.5
        layout.operator("scene.cm_gen_agents", icon_value=cicon('plus_yellow'))

class ObjectInputNode(Node, CrowdMasterAGenTreeNode):
    '''The object input node'''
    bl_idname = 'ObjectInputNodeType'
    bl_label = 'Object'
    bl_icon = 'SOUND'

    inputObject = StringProperty(name="Object")

    def init(self, context):
        self.outputs.new('GeoSocketType', "Geometry")
        self.outputs.new('VectorSocketType', "Location")
    
    def draw_buttons(self, context, layout):
        layout.prop_search(self, "inputObject", context.scene, "objects")

class GroupInputNode(Node, CrowdMasterAGenTreeNode):
    '''The group input node'''
    bl_idname = 'GroupInputNodeType'
    bl_label = 'Group'
    bl_icon = 'SOUND'

    inputGroup = StringProperty(name="Group")

    def init(self, context):
        self.outputs.new('GeoSocketType', "Geometry")
    
    def draw_buttons(self, context, layout):
        layout.prop_search(self, "inputGroup", bpy.data, "groups")

class VectorInputNode(Node, CrowdMasterAGenTreeNode):
    '''The vector input node'''
    bl_idname = 'VectorInputNodeType'
    bl_label = 'Vector'
    bl_icon = 'SOUND'

    inputVector = FloatVectorProperty(name="Vector", default = [0, 0, 0], subtype = "XYZ")

    def init(self, context):
        self.outputs.new('VectorSocketType', "Vector")
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "inputVector")

class GeoSwitchNode(Node, CrowdMasterAGenTreeNode):
    '''The geo switch node'''
    bl_idname = 'GeoSwitchNodeType'
    bl_label = 'Geo Switch'
    bl_icon = 'SOUND'

    switchAmount = FloatProperty(name="Amount", default = 0.5, min=0.0, max=1.0, precision=0)

    def init(self, context):
        self.inputs.new('GeoSocketType', "Object 1")
        self.inputs.new('GeoSocketType', "Object 2")
        self.inputs[0].link_limit = 1
        self.inputs[1].link_limit = 1
        
        self.outputs.new('GeoSocketType', "Objects")
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "switchAmount")

class TemplateSwitchNode(Node, CrowdMasterAGenTreeNode):
    '''The template switch node'''
    bl_idname = 'TemplateSwitchNodeType'
    bl_label = 'Template Switch'
    bl_icon = 'SOUND'

    switchAmount = FloatProperty(name="Amount", default = 0.5, min=0.0, max=1.0, precision=0)

    def init(self, context):
        self.inputs.new('TemplateSocketType', "Template 1")
        self.inputs.new('TemplateSocketType', "Template 2")
        self.inputs[0].link_limit = 1
        self.inputs[1].link_limit = 1
        
        self.outputs.new('TemplateSocketType', "Templates")
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "switchAmount")

class ParentNode(Node, CrowdMasterAGenTreeNode):
    '''The parent node'''
    bl_idname = 'ParentNodeType'
    bl_label = 'Parent'
    bl_icon = 'SOUND'
    
    parentTo = StringProperty(name="Parent To")

    def init(self, context):
        self.inputs.new('GeoSocketType', "Parent Group")
        self.inputs.new('GeoSocketType', "Child Object")
        self.inputs[0].link_limit = 1
        self.inputs[1].link_limit = 1
        
        self.outputs.new('GeoSocketType', "Objects")
    
    def draw_buttons(self, context, layout):
        layout.prop_search(self, "parentTo", context.scene, "objects")

class TemplateNode(Node, CrowdMasterAGenTreeNode):
    '''The template node'''
    bl_idname = 'TemplateNodeType'
    bl_label = 'Template'
    bl_icon = 'SOUND'
    
    brainType = StringProperty(name="Brain Type")

    def init(self, context):
        self.inputs.new('GeoSocketType', "Objects")
        self.inputs[0].link_limit = 1
        
        self.outputs.new('TemplateSocketType', "Template")
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "brainType")

class RandomNode(Node, CrowdMasterAGenTreeNode):
    '''The random node'''
    bl_idname = 'RandomNodeType'
    bl_label = 'Random'
    bl_icon = 'SOUND'

    maxRandRot = FloatProperty(name="Max Rand Rotation", description="The maximum random rotation in the Z axis for each agent.", default = 360.0, max=360.0)
    minRandRot = FloatProperty(name="Min Rand Rotation", description="The minimum random rotation in the Z axis for each agent.", default = 0.0, min=-360.0)

    maxRandSz = FloatProperty(name="Max Rand Scale", description="The maximum random scale for each agent.", default = 2.0, precision=3)
    minRandSz = FloatProperty(name="Min Rand Scale", description="The minimum random scale for each agent.", default = 1.0, precision=3)

    def init(self, context):
        self.inputs.new('VectorSocketType', "Vector")
        self.inputs[0].link_limit = 1
        
        self.outputs.new('TemplateSocketType', "Template")
    
    def draw_buttons(self, context, layout):
        row = layout.row(align=True)
        row.alignment = 'EXPAND'
        row.prop(self, "minRandRot")
        row.prop(self, "maxRandRot")
        
        row = layout.row(align=True)
        row.alignment = 'EXPAND'
        row.prop(self, "minRandSz")
        row.prop(self, "maxRandSz")

class RandomPositionNode(Node, CrowdMasterAGenTreeNode):
    '''The random positioing node'''
    bl_idname = 'RandomPositionNodeType'
    bl_label = 'Random Positioning'
    bl_icon = 'SOUND'
    
    locationType = EnumProperty(
        items = [('vector', 'Vector', 'Vector location type'),
                 ('scene', 'Scene', 'Scene location type')],
        name = "Location Type",
        description = "Which location type to use",
        default = "vector")
    
    MaxX = FloatProperty(name="Max X", description="The maximum distance in the X direction around the center point where the agents will be randomly spawned.", default = 50.0)
    MaxY = FloatProperty(name="Max Y", description="The maximum distance in the Y direction around the center point where the agents will be randomly spawned.", default = 50.0)
    MinX = FloatProperty(name="Min X", description="The minimum distance in the X direction around the center point where the agents will be randomly spawned.", default = -50.0)
    MinY = FloatProperty(name="Min Y", description="The minimum distance in the Y direction around the center point where the agents will be randomly spawned.", default = -50.0)

    def init(self, context):
        self.inputs.new('TemplateSocketType', "Template")
        self.inputs.new('VectorSocketType', "Vector")
        self.inputs.new('GeoSocketType', "Obstacles")
        self.inputs[0].link_limit = 1
        self.inputs[1].link_limit = 1
        self.inputs[2].link_limit = 1
        
        self.outputs.new('TemplateSocketType', "Template")
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "locationType")
        if self.locationType == "vector":
            row = layout.row(align=True)
            row.alignment = 'EXPAND'
            row.prop(self, "MaxX")
            row.prop(self, "MaxY")
        elif self.locationType == "scene":
            row = layout.row(align=True)
            row.alignment = 'EXPAND'
            row.prop(self, "MinX")
            row.prop(self, "MaxX")
            row = layout.row(align=True)
            row.alignment = 'EXPAND'
            row.prop(self, "MinY")
            row.prop(self, "MaxY")

class FormationPositionNode(Node, CrowdMasterAGenTreeNode):
    '''The formation positioing node'''
    bl_idname = 'FormationPositionNodeType'
    bl_label = 'Formation Positioning'
    bl_icon = 'SOUND'

    ArrayRows = IntProperty(name="Rows", description="The number of rows in the array.", default=1, min=1)
    ArrayRowMargin = FloatProperty(name="Row Margin", description="The margin between each row.")
    ArrayColumnMargin = FloatProperty(name="Column Margin", description="The margin between each column.")
    
    def init(self, context):
        self.inputs.new('TemplateSocketType', "Template")
        self.inputs.new('VectorSocketType', "Vector")
        self.inputs.new('GeoSocketType', "Obstacles")
        self.inputs[0].link_limit = 1
        self.inputs[1].link_limit = 1
        self.inputs[2].link_limit = 1
        
        self.outputs.new('TemplateSocketType', "Template")
    
    def draw_buttons(self, context, layout):
        row = layout.row()
        row.prop(self, "ArrayRows")
        row = layout.row(align=True)
        row.alignment = 'EXPAND'
        row.prop(self, "ArrayRowMargin")
        row.prop(self, "ArrayColumnMargin")

class TargetPositionNode(Node, CrowdMasterAGenTreeNode):
    '''The target positioing node'''
    bl_idname = 'TargetPositionNodeType'
    bl_label = 'Target Positioning'
    bl_icon = 'SOUND'

    targetOffset = FloatVectorProperty(name="Offset", description="Tweak the location of the generated agents.", default = [0, 0, 0], subtype = "XYZ")
    
    def init(self, context):
        self.inputs.new('TemplateSocketType', "Template")
        self.inputs.new('GeoSocketType', "Objects")
        self.inputs.new('GeoSocketType', "Obstacles")
        self.inputs[0].link_limit = 1
        self.inputs[1].link_limit = 1
        self.inputs[2].link_limit = 1
        
        self.outputs.new('TemplateSocketType', "Template")
    
    def draw_buttons(self, context, layout):
        row = layout.row()
        row.prop(self, "targetOffset")

import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem

class CrowdMasterAGenCategories(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'CrowdMasterAGenTreeType'

agen_node_categories = [
    CrowdMasterAGenCategories("template", "Template", items=[
        NodeItem("TemplateNodeType"),
        NodeItem("TemplateSwitchNodeType", label="Switch"),
        NodeItem("RandomNodeType"),
        ]),
    CrowdMasterAGenCategories("geometry", "Geometry", items=[
        NodeItem("ObjectInputNodeType"),
        NodeItem("GroupInputNodeType"),
        NodeItem("GeoSwitchNodeType", label="Switch"),
        NodeItem("ParentNodeType"),
        ]),
    CrowdMasterAGenCategories("position", "Positioning", items=[
        NodeItem("RandomPositionNodeType", label="Random"),
        NodeItem("FormationPositionNodeType", label="Formation"),
        NodeItem("TargetPositionNodeType", label="Target"),
        ]),
    CrowdMasterAGenCategories("other", "Other", items=[
        NodeItem("GenerateNodeType"),
        NodeItem("VectorInputNodeType"),
        ]),
    ]

def register():
    bpy.utils.register_class(CrowdMasterAGenTree)
    bpy.utils.register_class(GeoSocket)
    bpy.utils.register_class(VectorSocket)
    bpy.utils.register_class(TemplateSocket)
    bpy.utils.register_class(ObjectSocket)
    bpy.utils.register_class(GroupSocket)

    bpy.utils.register_class(GenerateNode)
    bpy.utils.register_class(ObjectInputNode)
    bpy.utils.register_class(GroupInputNode)
    bpy.utils.register_class(VectorInputNode)
    bpy.utils.register_class(GeoSwitchNode)
    bpy.utils.register_class(TemplateSwitchNode)
    bpy.utils.register_class(ParentNode)
    bpy.utils.register_class(TemplateNode)
    bpy.utils.register_class(RandomNode)
    bpy.utils.register_class(RandomPositionNode)
    bpy.utils.register_class(FormationPositionNode)
    bpy.utils.register_class(TargetPositionNode)

    nodeitems_utils.register_node_categories("AGEN_CUSTOM_NODES", agen_node_categories)

def unregister():
    nodeitems_utils.unregister_node_categories("AGEN_CUSTOM_NODES")

    bpy.utils.unregister_class(CrowdMasterAGenTree)
    bpy.utils.unregister_class(GeoSocket)
    bpy.utils.unregister_class(VectorSocket)
    bpy.utils.unregister_class(TemplateSocket)
    bpy.utils.unregister_class(ObjectSocket)
    bpy.utils.unregister_class(GroupSocket)

    bpy.utils.unregister_class(ObjectInputNode)
    bpy.utils.unregister_class(GroupInputNode)
    bpy.utils.unregister_class(VectorInputNode)
    bpy.utils.unregister_class(GeoSwitchNode)
    bpy.utils.unregister_class(TemplateSwitchNode)
    bpy.utils.unregister_class(ParentNode)
    bpy.utils.unregister_class(TemplateNode)
    bpy.utils.unregister_class(RandomNode)
    bpy.utils.unregister_class(RandomPositionNode)
    bpy.utils.unregister_class(FormationPositionNode)
    bpy.utils.unregister_class(TargetPositionNode)

if __name__ == "__main__":
    register()
