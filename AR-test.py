from objc_util import *
import ui
from pprint import pprint


def pPass():
  print('Pass')
def pdbg(obj):
  print('# --- name______')
  try:
    pprint(obj)
  except:
    pPass()
  print('# --- vars( )______')
  try:
    pprint(vars(obj))
  except:
    pPass()
  print('# --- dir( )______')
  try:
    pprint(dir(obj))
  except:
    pPass()
  
  # todo: 落ちる時は落ちる
  print('# --- ivarDescription')
  try:
    #pass
    pprint(obj._ivarDescription())
  except:
    pPass()
  print('# --- shortMethodDescription')
  try:
    pprint(obj._shortMethodDescription())
  except:
    pPass()
  print('# --- methodDescription')
  try:
    pprint(obj._methodDescription())
  except:
    pPass()
  
  print('# --- recursiveDescription')
  try:
    pprint(obj.recursiveDescription())
  except:
    pPass()
  print('# --- autolayoutTrace')
  try:
    pprint(obj._autolayoutTrace())
  except:
    pPass()



load_framework('SceneKit')
load_framework('ARKit')

SCNScene=ObjCClass('SCNScene')
SCNView=ObjCClass('SCNView')
SCNNode=ObjCClass('SCNNode')
SCNCamera=ObjCClass('SCNCamera')
SCNMaterial=ObjCClass('SCNMaterial')
SCNBox=ObjCClass('SCNBox')
UIColor=ObjCClass('UIColor')
SCNLight=ObjCClass('SCNLight')


ARWorldTrackingConfiguration=ObjCClass('ARWorldTrackingConfiguration')
ARSCNView=ObjCClass('ARSCNView')
ARSession=ObjCClass('ARSession')




class MainView(ui.View):
  def __init__(self,*args,**kwargs):
    self.bg_color='red'
    f = CGRect(CGPoint(0, 0), CGSize(self.width, self.height))
    flex_width, flex_height = (1<<1), (1<<4)
    
    selfIns=ObjCInstance(self)
    
    
    # --- view
    # todo: options ？🤔
    # todo: autorelease() とりま呼び出し
    s_view=ARSCNView.alloc().initWithFrame_options_(f, None).autorelease()
    s_view.setAutoresizingMask_(flex_width|flex_height)
    #s_view.delegate=selfIns
    s_scene=SCNScene.scene()
    s_view.scene=s_scene
    s_view.showsStatistics=1
    
    
    box_obj=SCNBox.boxWithWidth_height_length_chamferRadius_(0.1,0.1,0.1,0.05)
    box_obj.material().setColor_(UIColor.cyanColor().CGColor())
    bNode=SCNNode.nodeWithGeometry_(box_obj)
    bNode.setPosition_((0, 0, -0.2))
    s_scene.rootNode().addChildNode_(bNode)
    
    # --- 光
    lght=SCNLight.light()
    lght.setType_('omni')
    #lght.type='omni' これもいける
    lght.setColor_(UIColor.blueColor().CGColor())
    lNode=SCNNode.node()
    lNode.setLight_(lght)
    lNode.setPosition_((-40.0,40.0,60.0))
    s_scene.rootNode().addChildNode_(lNode)
    
    amb_obj=SCNLight.light()
    amb_obj.setType_('ambient')
    amb_obj.setColor_(UIColor.purpleColor().CGColor())
    aNode=SCNNode.node()
    aNode.setLight_(amb_obj)
    s_scene.rootNode().addChildNode_(aNode)
    
    
    
    ar_cnfg = ARWorldTrackingConfiguration.new()
    ar_session=ARSession.new()
    ar_session.delegate=selfIns
    ar_session.runWithConfiguration_(ar_cnfg)
    s_view.setSession_(ar_session)
    
    
    
    
    
    selfIns.addSubview_(s_view)

v=MainView()
v.present()


