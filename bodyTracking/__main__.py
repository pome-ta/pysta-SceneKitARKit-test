from objc_util import load_framework, ObjCClass
import ui

import pdbg

load_framework('ARKit')

ARSCNView = ObjCClass('ARSCNView')
ARBodyTrackingConfiguration = ObjCClass('ARBodyTrackingConfiguration')


class View(ui.View):
  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.bg_color = 'maroon'
    self.view_did_appear()

  def view_did_appear(self):
    if not (ARBodyTrackingConfiguration.isSupported()):
      print('This feature is only supported on devices with an A12 chip')
      raise
    # xxx: あとでチェック
    configuration = ARBodyTrackingConfiguration.new()
    
    


if __name__ == '__main__':
  view = View()
  view.present(style='fullscreen', orientations=['portrait'])

