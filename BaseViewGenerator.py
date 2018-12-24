from xml.dom import minidom
import os

CONFIG_SCREEN_WIDTH  = 960
CONFIG_SCREEN_HEIGHT = 540
WINDOWSVIEW={"Account":0}

packageConfig = {}
moduleConfig = {}

save_lua_path = r'H:\h5\client_tools\game'

readFileList = {}
CLASSNAMES = {}

def general_base_view(assets_path):
    init_configs(assets_path)


def init_configs(assets_path):
    for package_name in os.listdir(assets_path):
        doc = minidom.parse(os.path.join(assets_path, package_name, "package.xml"))
        root_element = doc.documentElement
        package_id = root_element.getAttribute("id")
        packageConfig[package_id] = package_name
        if package_name not in moduleConfig:
            moduleConfig[package_name] = {}


def create_package(path, package_name):
    doc = minidom.parse(os.path.join(path, "package.xml"))
    root_element = doc.documentElement
    package_id = root_element.getAttribute("id")
    if package_id not in packageConfig:
        packageConfig[package_id] = package_name
    component_list = root_element.getElementsByTagName("component")
    for component in component_list:
        if "true" == component.getArribute("exported"):
            component_id = component.getArribute("id")
            file = component.getAttribute("name")
            sub_path = component.getArribute("path")
            if path != "":
                file = sub_path[1:] + file
            name = file[:-4]
            name = name.split("/")[-1]
            className = name[0].upper() + name[1:]
            moduleConfig[package_name][className] = {
                "id": component_id,
                "packageNames": [package_name],
                "ui": "ui://" + package_id + component_id,
                "className": className,
                "outsideTouchCancel": False,
                "viewPath": "oyeahgame." + package_name + "." + className,
                "bgsound": False,
                "fullScreen": False}  # ,"controlPath":"oyeahgame."+packageName+".view."+className+"Base"}
            if not os.path.exists(save_lua_path):
                os.makedirs(save_lua_path + "/" + package_name.lower() + "/view")
            xml2lua(path + "/" + file, package_name, name, component_id)

def xml2lua(file, package_name, lua_name, component_id):
    global readFileList
    global CLASSNAMES
    if file in readFileList or not os.path.exists(file):
        return
    lua_name = lua_name[0].upper() + lua_name[1:]

    readFileList[file] = True
    doc = minidom.parse(file)
    root_element = doc.documentElement
    size = root_element.getAttribute("size")
    size= size.split(",")
    size = [int(size[0]), int(size[1])]
    panel_type = 1
    if size[0] >= CONFIG_SCREEN_WIDTH or size[1] >= CONFIG_SCREEN_HEIGHT:
        panel_type = 2;
    super_view = "framework.BaseView"
    content_view = "contentPane"
    extention = root_element.getAttribute("extention")
    if "" == extention or lua_name in WINDOWSVIEW:
        if size[0] > 100 and not hasbeImport(getPackageId(package_name), component_id):
            superView = "framework.BaseWindow"
    else:
        superView = "fairygui.G" + extention





general_base_view("H:\\h5\\share\\UI\\gameui\\assets\\")
