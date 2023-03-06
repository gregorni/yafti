from gi.repository import Gtk, Adw
from yafti.registry import SCREENS


_xml = """\
<?xml version="1.0" encoding="UTF-8"?>
<interface>
  <requires lib="gtk" version="4.0"/>
  <requires lib="libadwaita" version="1.0" />
  <template class="YaftiWindow" parent="AdwApplicationWindow">
    <property name="default-width">750</property>
    <property name="default-height">640</property>
    <property name="title">Welcome!</property>
    <child>
      <object class="GtkBox">
        <property name="orientation">vertical</property>
        <child>
          <object class="AdwHeaderBar" id="headerbar">
            <style>
              <class name="flat" />
            </style>
            <property name="title_widget">
              <object class="AdwCarouselIndicatorDots" id="carousel_indicator">
                <property name="carousel">carousel</property>
                <property name="orientation">horizontal</property>
              </object>
            </property>
            <child type="start">
              <object class="GtkButton" id="btn_back">
                <property name="label" translatable="yes">Back</property>
                <property name="halign">center</property>
                <property name="visible">False</property>
              </object>
            </child>
            <child>
              <object class="GtkButton" id="btn_next">
                <property name="label" translatable="yes">Next</property>
                <property name="halign">center</property>
                <property name="visible">True</property>
                <style>
                  <class name="suggested-action" />
                </style>
              </object>
            </child>
          </object>
        </child>
        <child>
          <object class="AdwToastOverlay" id="toasts">
            <child>
              <object class="AdwCarousel" id="carousel">
                <property name="vexpand">True</property>
                <property name="hexpand">True</property>
                <property name="allow_scroll_wheel">False</property>
                <property name="allow_mouse_drag">False</property>
                <property name="allow_long_swipes">False</property>
              </object>
            </child>
          </object>
        </child>
      </object>
    </child>
  </template>
</interface>
"""


@Gtk.Template(string=_xml)
class Window(Adw.ApplicationWindow):
    __gtype_name__ = "YaftiWindow"

    carousel_indicator = Gtk.Template.Child()
    carousel = Gtk.Template.Child()
    headerbar = Gtk.Template.Child()
    btn_back = Gtk.Template.Child()
    btn_next = Gtk.Template.Child()
    toasts = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app = kwargs.get("application")

        self.btn_next.connect("clicked", self.next)
        self.btn_back.connect("clicked", self.back)
        self.carousel.connect("page-changed", self.changed)

        self.draw()

    def draw(self):
        screens = self.app.config.screens
        for name, details in screens.items():
            if details.source not in SCREENS:
                continue
            screen = SCREENS.get(details.source)
            self.carousel.append(screen.from_config(details.values))

    @property
    def idx(self):
        return self.carousel.get_position()

    def goto(self, page: int, animate: bool = True):
        if page < 0:
            page = 0

        if page > self.carousel.get_n_pages():
            page = self.carousel.get_n_pages()

        screen = self.carousel.get_nth_page(page)
        self.carousel.scroll_to(screen, animate)

    def next(self, test):
        self.goto(self.idx + 1)

    def back(self, test):
        self.goto(self.idx - 1)

    def changed(self, *args):
        self.btn_back.set_visible(self.idx > 0)