from dataclasses import dataclass

from puepy import t, Component
from puepy.router import Route
from puepy.util import jsobj


@dataclass
class SidebarItem:
    label: str
    icon: str
    route: Route


@t.component()
class AppLayout(Component):
    sidebar_items = [
        SidebarItem("Dashboard", "emoji-sunglasses", "welcome_page"),
        SidebarItem("Charts", "graph-up", "charts_page"),
        SidebarItem("Forms", "input-cursor-text", "forms_page"),
    ]

    def populate(self):
        with t.sl_drawer(label="Menu", placement="start", classes="drawer-placement-start", ref="drawer"):
            self.populate_sidebar()

        with t.div(classes="container"):
            with t.div(classes="header"):
                with t.div():
                    with t.sl_button(classes="menu-btn", on_click=self.show_drawer):
                        t.sl_icon(name="list")
                t.div("The Dapper App")
                self.populate_topright()
            with t.div(classes="sidebar", id="sidebar"):
                self.populate_sidebar()
            with t.div(classes="main"):
                self.insert_slot()
            with t.div(classes="footer"):
                t("Business Time!")

    def populate_topright(self):
        with t.div(classes="dropdown-hoist"):
            with t.sl_dropdown(hoist=""):
                t.sl_icon_button(slot="trigger", label="User Settings", name="person-gear")
                with t.sl_menu(on_sl_select=self.on_menu_select):
                    t.sl_menu_item(
                        "Profile",
                        t.sl_icon(slot="suffix", name="person-badge"),
                        value="profile",
                    )
                    t.sl_menu_item("Settings", t.sl_icon(slot="suffix", name="gear"), value="settings")
                    t.sl_divider()
                    t.sl_menu_item("Logout", t.sl_icon(slot="suffix", name="box-arrow-right"), value="logout")

    def on_menu_select(self, event):
        print("You selected", event.detail.item.value)

    def populate_sidebar(self):
        for item in self.sidebar_items:
            with t.div():
                with t.sl_button(
                    item.label,
                    variant="text",
                    classes="sidebar-button",
                    href=self.page.router.reverse(item.route),
                ):
                    if item.icon:
                        t.sl_icon(name=item.icon, slot="prefix")

    def show_drawer(self, event):
        self.refs["drawer"].element.show()


@t.component()
class Chart(Component):
    props = ["type", "data", "options"]
    enclosing_tag = "canvas"

    def post_render(self, element):
        import js

        js.Chart.new(
            element,
            jsobj(type=self.type, data=self.data, options=self.options),
        )
