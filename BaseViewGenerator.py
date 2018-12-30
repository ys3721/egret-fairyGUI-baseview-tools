from xml.dom import minidom
import os
import tenjin
from tenjin.helpers import *
from tenjin.escaped import is_escaped, as_escaped, to_escaped

CONFIG_SCREEN_WIDTH  = 960
CONFIG_SCREEN_HEIGHT = 540
WINDOWSVIEW={"Account":0}

packagesConfig = {}
moduleConfig = {}

save_lua_path = r'H:\h5\client_tools\game'
uipath = "H:\\h5\\share\\UI\\gameui\\assets\\"

readFileList = {}
CLASSNAMES = {}
packagesImport = {"wuy3bh5gasf42v":True,"js0d6vmkcwn9t7":True,"xkpsx4uivd0a2o":True,"62g0ma7tdyidb":True,"wuy3bh5gilz148":True, "xkpsx4uietk131":True}
# 关键字 不可使用
KEYVALE={"name":True,"apexIndex":True,"mask":True,"baseUserData":True,"viewWidth":True,"viewHeight":True, "x":True,"y":True,"scrollPane":True,"opaque":True,"margin":True,"childrenRenderOrder":True}

packagesType={}
NEWLUAFILES=[]

def general_base_view(assets_path):
    init_configs(assets_path)

    for package_id in packagesConfig:
        package_name = packagesConfig[package_id]
        create_package(os.path.join(uipath, package_name), package_name)


def init_configs(assets_path):
    """主要用来初始化 packageConfig 和 moduleConfig， 其中packageConfig记录了package id和package name的字典，
       moduleConfig记录了，key=packag_name value={}字典的字典
    """
    for package_name in os.listdir(assets_path):
        doc = minidom.parse(os.path.join(assets_path, package_name, "package.xml"))
        root_element = doc.documentElement
        package_id = root_element.getAttribute("id")
        packagesConfig[package_id] = package_name
        if package_name not in moduleConfig:
            moduleConfig[package_name] = {}


def create_package(path, package_name):
    """ path是每个模块的path， 也就是package的path，package name 其实就是module name 啦。
    这个函数实在是太长了，我都不知道是在干什么"""
    # 开始读取了package xml， 每个模块下的
    doc = minidom.parse(os.path.join(path, "package.xml"))
    root_element = doc.documentElement
    package_id = root_element.getAttribute("id")
    if package_id not in packagesConfig:
        packagesConfig[package_id] = package_name
    # 取package的每个 component 节点
    component_list = root_element.getElementsByTagName("component")
    for component in component_list:
        if "true" == component.getAttribute("exported"):
            component_id = component.getAttribute("id")
            file = component.getAttribute("name")
            # sub path 指的是component的xml的path， 大多是“/”
            sub_path = component.getAttribute("path")
            if path != "":
                # file is the component xlm 's relative path
                file = sub_path[1:] + file
            name = file[:-4]
            name = name.split("/")[-1]
            # class name is the component xml's name, use the component name as class name.
            className = name[0].upper() + name[1:]
            moduleConfig[package_name][className] = {
                "id": component_id,
                "package_names": [package_name],
                "ui": "ui://" + package_id + component_id,
                "className": className,
                "outsideTouchCancel": False,
                "viewPath": "oyeahgame." + package_name + "." + className,
                "bgsound": False,
                "fullScreen": False}  # ,"controlPath":"oyeahgame."+package_name+".view."+className+"Base"}
            if not os.path.exists(save_lua_path):
                os.makedirs(save_lua_path + "/" + package_name.lower() + "/view")
            xml2lua(path + "/" + file, package_name, name, component_id)


def xml2lua(file, package_name, lua_name, component_id):
    """file is component.xml 's relative path, lua_name is the class name of component ,
     package_name is moudle name, component_id is component id in package.xml"""
    global readFileList
    global CLASSNAMES
    if file in readFileList or not os.path.exists(file):
        return
    lua_name = lua_name[0].upper() + lua_name[1:]
    readFileList[file] = True
    # Begin read component xml, first read the size, assert the panel type. Second
    doc = minidom.parse(file)
    root_element = doc.documentElement
    size = root_element.getAttribute("size")
    size= size.split(",")
    size = [int(size[0]), int(size[1])]
    panel_type = 1
    if size[0] >= CONFIG_SCREEN_WIDTH or size[1] >= CONFIG_SCREEN_HEIGHT:
        panel_type = 2;
    superView = "framework.BaseView"
    contentView = "contentPane"
    # This extention only Button value. I Look.
    extention = root_element.getAttribute("extention")
    if "" == extention or lua_name in WINDOWSVIEW:
        # I don't know the has be import means but not important
        if size[0] > 100 and not has_be_import(get_package_id(package_name), component_id):
            superView = "framework.BaseWindow"
    else:
        superView = "fairygui.G" + extention
    components = []
    importClcass = {}
    contentPane = "contentPane"
    # This is the image loader text ext. in the component xml
    displayList = root_element.getElementsByTagName("displayList")
    if len(displayList) > 0:
        displayList = displayList[0]
        for node in displayList.childNodes:
            # Begin loop thought the nodes of display
            nodeName = node.nodeName
            luaClass = ""
            virtualdefaultItem = ""
            # Process image loader and text
            if "image" == nodeName or "movieclip" == nodeName:
                # Image maybe in other package folder
                pkg = node.getAttribute("pkg")
                if pkg != "":
                    # 跨包引用图片
                    if pkg in packagesConfig:
                        # package name of the Image or MovieClip belong in folder
                        subpkg = packagesConfig[pkg]
                        if package_name in moduleConfig and lua_name in moduleConfig[package_name]:
                            # 把package name存到了一个list中
                            addToList(moduleConfig[package_name][lua_name]["package_names"], subpkg)
                # moduleConfig[package_name][lua_name]["package_names"].append(packagesConfig[pkg])
            elif "loader" == nodeName:
                pkg = node.getAttribute("url")
                if pkg != "" and pkg.find("ui:") > -1:
                    # loader's uri is ui://110ys6klhxyuum, first 5 bit is ui://  And list 6 bit is image id,
                    # 5:13 is package id
                    pkg = pkg[5:13]
                    if pkg in packagesConfig:
                        subpkg = packagesConfig[pkg]
                        if package_name in moduleConfig and lua_name in moduleConfig[package_name]:
                            addToList(moduleConfig[package_name][lua_name]["package_names"], subpkg)
            elif "text" == nodeName:
                pkg = node.getAttribute("font")
                # font = "ui://rm6hhqi3q7th13q" As same as loader
                if pkg != "" and pkg.find("ui:") > -1:
                    pkg = pkg[5:13]
                    if pkg in packagesConfig:
                        subpkg = packagesConfig[pkg]
                        if package_name in moduleConfig and lua_name in moduleConfig[package_name]:
                            addToList(moduleConfig[package_name][lua_name]["package_names"], subpkg)
            # 然后判断了 不是 这个 #text 我不知道这个是个什么东西 而且是不为#text
            if "#text" != nodeName:
                defaultItem = node.getAttribute("defaultItem")
                touchable = node.getAttribute("touchable") != "false"
                if defaultItem != "":
                    module = addSubPackages(defaultItem[5:13], defaultItem[13:])
                    if module:
                        package_names = moduleConfig[package_name][lua_name]["package_names"]
                        virtualdefaultItem = module["className"]
                        for subpkg in module["package_names"]:
                            addToList(package_names, subpkg)
                elif "list" == nodeName:
                    displayList = node.getElementsByTagName("item")
                    for subnode in displayList:
                        defaultItem = subnode.getAttribute("url")
                        if len(defaultItem) > 13:
                            module = addSubPackages(defaultItem[5:13], defaultItem[13:])
                            if module:
                                package_names = moduleConfig[package_name][lua_name]["package_names"]
                                for subpkg in module["package_names"]:
                                    addToList(package_names, subpkg)

                filterName = node.getAttribute("name")
                pkgfileName = node.getAttribute("fileName")
                if pkgfileName == "CloseButtonBack.xml":
                    moduleConfig[package_name][lua_name]["outsideTouchCancel"] = True
                    pass
                elif filterName == "title" or filterName == "icon":
                    pass
                else:
                    if nodeName == "component":
                        subpkg = package_name
                        # path = file.split("/")
                        # path[-1]=node.getAttribute("src")+".xml"
                        pkg = node.getAttribute("pkg")
                        if pkg != "":
                            if pkg in packagesConfig:
                                subpkg = packagesConfig[pkg]
                                # path[-2]=subpkg
                                if package_name in moduleConfig and lua_name in moduleConfig[package_name]:
                                    addToList(moduleConfig[package_name][lua_name]["package_names"], subpkg)
                        # path="/".join(path)
                        luaClass, nodeName = getComponentName(subpkg, node.getAttribute("src"))
                        if luaClass != "":
                            module = addSubPackages(get_package_id(subpkg), node.getAttribute("src"))
                            if module:
                                importClcass[luaClass] = subpkg
                                package_names = moduleConfig[package_name][lua_name]["package_names"]
                                for subpkg in module["package_names"]:
                                    addToList(package_names, subpkg)
                    nameID = node.getAttribute("name")
                    if isWrongName(nameID):
                        print("%s 控件名称错误 请修改 '%s'" % (lua_name, nameID))
                        raise ValueError
                    # 普通组不生成代码
                    if "group" == nodeName:
                        if "true" != node.getAttribute("advanced"):
                            nodeName = "groupSimple"
                    if "text" == nodeName:
                        if "true" == node.getAttribute("input"):
                            nodeName = "input"
                    if nameID != "":
                        for component in components:
                            if component["name"] == nameID:
                                print("请修改 %s ERROR:包含重复名字 %s " % (lua_name, nameID))
                                raise ValueError
                        if nameID in KEYVALE:
                            print("请修改 %s ERROR: 包含关键字 %s " % (lua_name, nameID))
                            raise ValueError
                        components.append(
                            {"name": nameID, "touchable": touchable, "luaClass": luaClass, "type": nodeName,
                             "defaultItem": virtualdefaultItem, "contentPane": contentPane})
        # else:
        #   log nodeName
    if panel_type == 2:
        moduleConfig[package_name][lua_name]["fullScreen"] = True
    else:
        moduleConfig[package_name][lua_name]["fullScreen"] = False

    if lua_name in CLASSNAMES:
        print("请修改 %s ERROR: 文件名冲突 %s " % (lua_name, lua_name))
        raise ValueError
    if isWrongName(lua_name):
        print("%s 文件名称错误 请修改 '%s'" % (lua_name, lua_name))
        raise ValueError
    CLASSNAMES[lua_name] = True;
    # sort by name
    components.sort(key=lambda components: components.get('name'), reverse=False)
    context = {"viewName": lua_name,
               "package_name": package_name,
               "superView": superView,
               "importClcass": importClcass,
               "contentView": contentView,
               "components": components,
               "version": '0.0.0'
               }
    moduleConfig[package_name][lua_name]["layerTag"] = "UI_VIEW_TYPE.WINLAYER"
    engine = tenjin.Engine(path=['base_view_template'])
    wirte2file(save_lua_path + "/" + package_name.lower() + "/view/" + lua_name + "Base.ts", engine.render('BaseView.pyts', context))
    if os.path.exists(save_lua_path + "/" + package_name.lower() + "/" + lua_name + ".ts"):
        # mergeLuaFunction(save_lua_path+"/"+package_name.lower()+"/"+lua_name+".ts",lua_name,engine.render('template/View.ts.py', context))
        print("file exits:%s/%s.ts" % (package_name, lua_name))
        pass
    else:
        wirte2file(save_lua_path + "/" + package_name.lower() + "/" + lua_name + ".ts",
                   engine.render('template/View.ts.py', context))
def wirte2file(filname,values):
    f = open(filname,"w")
    f.write(values)
    f.close()
    NEWLUAFILES.append(filname)

def addToList(list,item):
    for x in list:
        if x== item:
            return
    list.append(item)

def isWrongName(nameID):
    return False

def has_be_import(package_id, component_id):
    package_key = package_id + component_id
    if package_key in packagesImport:
        return packagesImport[package_key]
    else:
        for __packageId in packagesConfig:
            package_name = packagesConfig[__packageId]
            doc = minidom.parse(uipath + "/" + package_name + "/package.xml")
            rootElement = doc.documentElement
            componentlist = rootElement.getElementsByTagName("component")
            for component in componentlist:
                file = component.getAttribute("name")
                path = component.getAttribute("path")
                file = uipath + "/" + package_name + path + file
                try:
                    doc = minidom.parse(file)
                except Exception as e:
                    print("解析文件错误:%s" % (file))
                    raise e
                rootElement = doc.documentElement
                displayList = rootElement.getElementsByTagName("displayList")
                if len(displayList) > 0:
                    displayList = displayList[0]
                    for node in displayList.childNodes:
                        if "#text" != node.nodeName:
                            pkg = node.getAttribute("pkg")
                            if len(pkg) < 5:
                                pkg = __packageId
                            if pkg == package_id:
                                if node.getAttribute("src") == component_id:
                                    packagesImport[package_key] = True
                                    return packagesImport[package_key]
                                else:
                                    defaultItem = node.getAttribute("defaultItem")
                                    if len(defaultItem) > 13:
                                        if defaultItem[13:] == component_id and defaultItem[5:13] == package_id:
                                            packagesImport[package_key] = True
                                            return packagesImport[package_key]
                displayList = rootElement.getElementsByTagName("item")
                for node in displayList:
                    defaultItem = node.getAttribute("url")
                    if len(defaultItem) > 13:
                        if defaultItem[13:] == component_id and defaultItem[5:13] == package_id:
                            packagesImport[package_key] = True
                            return packagesImport[package_key]

        packagesImport[package_key] = False
        return packagesImport[package_key]


def get_package_id(package_name):
    for x in packagesConfig:
        if packagesConfig[x] == package_name:
            return x
    return package_id

def addSubPackages(package,componentid):
    # log ("%s-%s" %(packagesConfig[package],componentid))
    packageName = packagesConfig[package]
    doc = minidom.parse(uipath+"/"+packageName+"/package.xml")
    rootElement = doc.documentElement
    componentlist=rootElement.getElementsByTagName("component")
    for component in componentlist:
        packageid=str(component.getAttribute("id"))
        if componentid == packageid:
            folder=component.getAttribute("folder")
            file=component.getAttribute("name")
            path=component.getAttribute("path")
            name=file[:-4]
            className=name[0].upper()+name[1:]
            if not packageName in moduleConfig:
                moduleConfig[packageName]={}
            if className not in moduleConfig[packageName]:
                moduleConfig[packageName][className]={"id":packageid,"packageNames":[packageName],"ui":"ui://"+package+componentid,"className":className,"outsideTouchCancel":False,"viewPath":"oyeahgame."+packageName+"."+className,"bgsound":False,"fullScreen":False} #,"controlPath":"oyeahgame."+packageName+".view."+className+"Base"}
                if not os.path.exists(save_lua_path+"/"+packageName.lower()+"/view"):
                    os.makedirs(save_lua_path+"/"+packageName.lower()+"/view")
                xml2lua(uipath+"/"+packageName+path+file,packageName,className,componentid)
            return moduleConfig[packageName][className]

def getComponentName(packageName,xmlName):
    key = packageName+"."+xmlName
    if key not in packagesType:
        doc = minidom.parse(uipath+"/"+packageName+"/package.xml")
        rootElement = doc.documentElement
        components=rootElement.getElementsByTagName("component")
        className= xmlName
        for node in components:
            if xmlName == node.getAttribute("id"):
                className =  node.getAttribute("name")
                break
        if className == xmlName:
            packagesType[key]=["",""]
        else:
            doc = minidom.parse(uipath+"/"+packageName+node.getAttribute("path")+className)
            extention = doc.documentElement.getAttribute("extention")
            className=className[0].upper()+className[1:-4]
            packagesType[key]=[className,extention]
    return packagesType[key][0], packagesType[key][1]

general_base_view("H:\\h5\\share\\UI\\gameui\\assets\\")
