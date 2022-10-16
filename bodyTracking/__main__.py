from objc_util import load_framework, ObjCClass
import ui


load_framework('RealityKit')

ARView = ObjCClass('ARView')

class View(ui.View):
  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.bg_color = 'maroon'


if __name__ == '__main__':
  view = View()
  view.present(style='fullscreen', orientations=['portrait'])

