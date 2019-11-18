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

SCNScene=ObjCClass('SCNScene')
SCNView=ObjCClass('SCNView')
SCNNode=ObjCClass('SCNNode')
SCNCamera=ObjCClass('SCNCamera')
SCNMaterial=ObjCClass('SCNMaterial')

SCNPyramid=ObjCClass('SCNPyramid')
UIColor=ObjCClass('UIColor')
SCNLight=ObjCClass('SCNLight')
SCNSphere=ObjCClass('SCNSphere')
SCNSphere=ObjCClass('SCNSphere')
SCNFloor=ObjCClass('SCNFloor')


class MainView(ui.View):
  def __init__(self,wf=0,*args,**kwargs):
    self.bg_color='red'
    f = CGRect(CGPoint(0, 0), CGSize(self.width, self.height))
    flex_width, flex_height = (1<<1), (1<<4)
    
    # todo: CGColor() いるかな？
    grn=UIColor.greenColor().CGColor()
    blu=UIColor.blueColor().CGColor()
    cyn=UIColor.cyanColor().CGColor()
    wht=UIColor.whiteColor().CGColor()
    dkg=UIColor.darkGrayColor().CGColor()
    red=UIColor.redColor().CGColor()
    ppl=UIColor.purpleColor().CGColor()
    
    selfIns=ObjCInstance(self)
    
    # --- view
    # todo: options ？🤔
    # todo: autorelease() とりま呼び出し
    s_view=SCNView.alloc().initWithFrame_options_(f, None).autorelease()
    s_view.setAutoresizingMask_(flex_width|flex_height)
    s_scene=SCNScene.scene()
    s_view.scene=s_scene
    s_view.backgroundColor=UIColor.darkGrayColor()
    s_view.showsStatistics=1
    s_view.allowsCameraControl=1
    
    # --- 球体
    sp_obj=SCNSphere.sphereWithRadius_(1)
    sp_obj.material().setColor_(wht)
    sNode=SCNNode.nodeWithGeometry_(sp_obj)
    s_scene.rootNode().addChildNode_(sNode)
    
    # --- 床
    floor = SCNFloor.floor()
    #floor.reflectivity = .5
    fNode= SCNNode.nodeWithGeometry_(floor)
    fNode.setPosition_((0, -2, 0))
    
    # --- 光
    lght=SCNLight.light()
    lght.setType_('omni')
    #lght.type='omni' <- This is okay too🙆‍♀️
    lght.setColor_(blu)
    #lght.setCastsShadow_(True) 🤔
    lNode=SCNNode.node()
    lNode.setLight_(lght)
    lNode.setPosition_((-40.0,40.0,60.0))
    
    amb_obj=SCNLight.light()
    amb_obj.setType_('ambient')
    amb_obj.setColor_(ppl)
    #amb_obj.setCastsShadow_(True) 🤔
    aNode=SCNNode.node()
    aNode.setLight_(amb_obj)
    
    # --- wireframe look
    if wf == 0:
      s_scene.rootNode().addChildNode_(lNode)
      s_scene.rootNode().addChildNode_(aNode)
      s_scene.rootNode().addChildNode_(fNode)
    else:
      s_view.debugOptions=1 << 5
      sp_obj.material().setColor_(dkg)
    
    # --- カメラ
    cam=SCNCamera.camera()
    cam.xFov=80.0
    cam.yFov=80.0
    camNode=SCNNode.node()
    camNode.camera=cam
    camNode.position=(0.0,0.0,2.0)
    s_scene.rootNode().addChildNode_(camNode)
    
    selfIns.addSubview_(s_view)

v=MainView(wf=1)
v.present()
