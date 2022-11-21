import math
from objc_util import load_framework, ObjCClass, ObjCInstance, on_main_thread, CGRect, nsurl
import ui
import editor

from pprint import pprint

load_framework('SceneKit')

SCNScene = ObjCClass('SCNScene')
SCNNode = ObjCClass('SCNNode')
SCNSphere = ObjCClass('SCNSphere')
SCNMaterial = ObjCClass('SCNMaterial')
SCNLight = ObjCClass('SCNLight')
SCNCamera = ObjCClass('SCNCamera')
SCNView = ObjCClass('SCNView')

UIColor = ObjCClass('UIColor')
UIImage = ObjCClass('UIImage')
NSData = ObjCClass('NSData')


class View(ui.View):
  def __init__(self):
    self.bg_color = 'maroon'
    self.instance = ObjCInstance(self)
    self.viewDidLoad()
    self.setup_ui()

  @on_main_thread
  def viewDidLoad(self):
    ship_URL = nsurl('./assets/ship.scn')
    bkSky_URL = NSData.dataWithContentsOfURL_(
      nsurl('./assets/Background_sky.png'))
    tex_bks = UIImage.alloc().initWithData_(bkSky_URL)
    # --- Scene
    scene = SCNScene.sceneWithURL_options_(ship_URL, None)
    ship_node = scene.rootNode().objectInChildNodesAtIndex_(0)
    scene.background().contents = tex_bks
    scene.lightingEnvironment().contents = tex_bks
    scene.lightingEnvironment().intensity = 1.0

    ship_material = SCNMaterial.material()
    ship_material.diffuse().contents = UIColor.purpleColor()
    ship_material.lightingModelName = 'SCNLightingModelPhysicallyBased'

    ship_geometry = ship_node.childNodes().objectAtIndex_(0).geometry()
    ship_geometry.material = ship_material

    ball_color = UIColor.colorWithRed_green_blue_alpha_(0.0, 0.5, 0.8, 0.5)
    ball_geometry = SCNSphere.sphereWithRadius_(0.5)
    ball_geometry.geodesic = True
    ball_geometry.segmentCount = 5
    ball_geometry.material(
    ).lightingModelName = 'SCNLightingModelPhysicallyBased'
    ball_geometry.firstMaterial().diffuse().contents = ball_color
    ball_node = SCNNode.nodeWithGeometry_(ball_geometry)
    ball_node.position = (0.0, 6.0, 1.0)
    ball_node.eulerAngles = (1, 0, 0)
    scene.rootNode().addChildNode_(ball_node)

    # --- Light
    omni_object = SCNLight.light()
    omni_object.type = 'omni'
    omni_object.intensity = 250
    omni_object.castsShadow = True
    omni_node = SCNNode.node()
    omni_node.light = omni_object
    omni_node.position = (0, 10.0, 0)
    scene.rootNode().addChildNode_(omni_node)

    # --- Camera
    camera_object = SCNCamera.camera()
    camera_object.wantsHDR = True
    camera_object.bloomBlurRadius = 18.0
    camera_object.bloomIntensity = 1.0
    camera_object.bloomThreshold = 1.0
    camera_object.colorFringeIntensity = 4.0
    camera_object.colorFringeStrength = 4.0
    camera_object.motionBlurIntensity = 6
    camera_object.xFov = 35.0
    camera_object.yFov = 35.0
    camera_node = SCNNode.node()
    camera_node.camera = camera_object
    camera_node.position = (0.0, 0.0, 25.0)
    scene.rootNode().addChildNode_(camera_node)

    # --- View
    frame = CGRect((0, 0), (100, 100))
    flex_w, flex_h = (1 << 1), (1 << 4)
    scn_view = SCNView.alloc()
    scn_view.initWithFrame_options_(frame, None)
    scn_view.autorelease()
    scn_view.autoresizingMask = (flex_w | flex_h)
    scn_view.allowsCameraControl = True
    scn_view.showsStatistics = True
    '''
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
    '''
    scn_view.debugOptions = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 10)
    scn_view.scene = scene
    self.instance.addSubview_(scn_view)

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


view = View()
editor.present_themed(
  view,
  theme_name='Theme09_Editorial',
  style='fullscreen',
  hide_title_bar=True,
  orientations=['portrait'])

