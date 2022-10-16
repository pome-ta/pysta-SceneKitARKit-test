from objc_util import load_framework, ObjCClass, CGRect
import ui

import pdbg

load_framework('ARKit')


class View(ui.View):
  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.bg_color = 'maroon'

    self.arkit_view = ObjCClass('ARSCNView').alloc()
    frame = CGRect((0, 0), (100, 100))
    flex_w, flex_h = (1 << 1), (1 << 4)
    self.arkit_view.initWithFrame_options_(frame, None)
    self.arkit_view.autoresizingMask = (flex_w | flex_h)
    self.arkit_view.showsStatistics = True
    self.arkit_view.debugOptions = (1 << 1) | (1 << 31)
    self.view_did_appear()
    
    self.objc_instance.addSubview_(self.arkit_view)
    

  def view_did_appear(self):
    ARBodyTrackingConfiguration = ObjCClass('ARBodyTrackingConfiguration')
    if not (ARBodyTrackingConfiguration.isSupported()):
      print('This feature is only supported on devices with an A12 chip')
      raise
    # xxx: あとでチェック
    configuration = ARBodyTrackingConfiguration.new()
    self.arkit_view.session().runWithConfiguration_(configuration)
    
  def will_close(self):
    self.arkit_view.session().pause()
    


if __name__ == '__main__':
  view = View()
  view.present(style='fullscreen', orientations=['portrait'])

