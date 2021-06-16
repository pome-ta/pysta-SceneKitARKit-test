import re
import math
from objc_util import load_framework, ObjCClass, ObjCInstance, create_objc_class, on_main_thread, CGRect
import ui
import editor

from pprint import pprint

load_framework('ARKit')
load_framework('SceneKit')

UIColor = ObjCClass('UIColor')

ARSCNView = ObjCClass('ARSCNView')
ARWorldTrackingConfiguration = ObjCClass('ARWorldTrackingConfiguration')

SCNScene = ObjCClass('SCNScene')
SCNNode = ObjCClass('SCNNode')
SCNBox = ObjCClass('SCNBox')


def anchor_attribute(anchor):
  id_pattern = r'\"(.*?)\"'
  _identifier = re.search(id_pattern, anchor).group(1)
  prm_pattern = r'(center|extent)\=\((.*?)\)'
  greps = re.findall(prm_pattern, anchor)
  _center = [float(i) for i in re.split(r'\s', greps[0][1])]
  _extent = [float(j) for j in re.split(r'\s', greps[1][1])]
  return _center, _extent, _identifier


def renderer_didAddNode_forAnchor_(_self, _cmd, renderer, node, anchor):
  get_anchor = repr(str(ObjCInstance(anchor)))
  center, extent, identifier = anchor_attribute(get_anchor)
  #print(center)
  #print(extent)
  #print(identifier)
  after_color = UIColor.colorWithRed_green_blue_alpha_(0.0, 0.2, 0.8, 1.0)
  view.vc.box_geometry.firstMaterial().diffuse().contents = after_color


def renderer_didUpdateNode_forAnchor_(_self, _cmd, renderer, node, anchor):
  pass


def renderer_didRemoveNode_forAnchor_(_self, _cmd, renderer, node, anchor):
  pass


class ViewController:
  ''' debugOptions
  OptionNone = 0
  ShowPhysicsShapes = (1 << 0)
  ShowBoundingBoxes = (1 << 1)
  ShowLightInfluences = (1 << 2)
  ShowLightExtents = (1 << 3)
  ShowPhysicsFields = (1 << 4)
  ShowWireframe = (1 << 5)
  RenderAsWireframe = (1 << 6)
  ShowSkeletons = (1 << 7)
  ShowCreases = (1 << 8)
  ShowConstraints = (1 << 9)
  ShowCameras = (1 << 10)
  ARSCNDebugOptionShowFeaturePoints = (1 << 30)
  ARSCNDebugOptionShowWorldOrigin = (1 << 32)
  '''

  def __init__(self):
    # create delegate
    methods = [
      renderer_didAddNode_forAnchor_, #renderer_didUpdateNode_forAnchor_,
      #renderer_didRemoveNode_forAnchor_
    ]
    protocols = ['ARSCNViewDelegate']
    pyARSCNViewDelegate = create_objc_class(
      'pyARSCNViewDelegate', methods=methods, protocols=protocols)
    self.view_did_load()
    self.view_will_appear(pyARSCNViewDelegate)

  def view_did_load(self):
    self.scene = SCNScene.scene()
    before_color = UIColor.colorWithRed_green_blue_alpha_(0.8, 0.0, 0.0, 0.5)
    self.box_geometry = SCNBox.box()
    self.box_geometry.width = 0.1
    self.box_geometry.height = 0.1
    self.box_geometry.length = 0.1
    self.box_geometry.material(
    ).lightingModelName = 'SCNLightingModelPhysicallyBased'
    self.box_geometry.firstMaterial().diffuse().contents = before_color
    box_node = SCNNode.nodeWithGeometry_(self.box_geometry)
    box_node.position = (0, -0.5, -0.5)
    box_node.eulerAngles = (1, 1, 0)
    self.scene.rootNode().addChildNode_(box_node)

    self.scn_view = ARSCNView.alloc()
    self.scn_view.initWithFrame_options_(CGRect((0, 0), (100, 100)), None)
    self.scn_view.autorelease()
    self.scn_view.autoresizingMask = (18)
    self.scn_view.showsStatistics = True
    self.scn_view.autoenablesDefaultLighting = True
    self.scn_view.debugOptions = (1 << 1) | (1 << 30) | (1 << 32)
    self.scn_view.scene = self.scene

  def view_will_appear(self, delegate):
    configuration = ARWorldTrackingConfiguration.new()
    configuration.planeDetection = (1 << 0)
    self.scn_view.session().runWithConfiguration_(configuration)
    self.scn_view.delegate = delegate.alloc().init()

  def view_will_disappear(self):
    self.scn_view.session().pause()


class View(ui.View):
  def __init__(self):
    self.instance = ObjCInstance(self)
    self.setup_objc()
    self.setup_ui()

  @on_main_thread
  def setup_objc(self):
    self.vc = ViewController()
    self.instance.addSubview_(self.vc.scn_view)

  def setup_ui(self):
    self.close_btn = self.create_btn('iob:ios7_close_32')
    self.close_btn.action = (lambda sender: self.close())
    self.add_subview(self.close_btn)

  def create_btn(self, icon):
    btn_icon = ui.Image.named(icon)
    return ui.Button(image=btn_icon)

  def layout(self):
    _x, _y, _w, _h = self.frame
    _bx, _by, btn_w, btn_h = self.close_btn.frame
    self.close_btn.x = (_w * .92) - (btn_w / 2)
    self.close_btn.y = (_h * .08) - (btn_h / 2)

  def will_close(self):
    self.vc.view_will_disappear()


view = View()
editor.present_themed(
  view,
  theme_name='Theme09_Editorial',
  style='fullscreen',
  hide_title_bar=True,
  orientations=['portrait'])

