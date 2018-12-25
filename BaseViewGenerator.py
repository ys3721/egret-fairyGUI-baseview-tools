from xml.dom import minidom
import os
import tenjin

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


def init_configs(assets_path):
    for package_name in os.listdir(assets_path):
        doc = minidom.parse(os.path.join(assets_path, package_name, "package.xml"))
        root_element = doc.documentElement
        package_id = root_element.getAttribute("id")
        packagesConfig[package_id] = package_name
        if package_name not in moduleConfig:
            moduleConfig[package_name] = {}


def create_package(path, package_name):
    doc = minidom.parse(os.path.join(path, "package.xml"))
    root_element = doc.documentElement
    package_id = root_element.getAttribute("id")
    if package_id not in packagesConfig:
        packagesConfig[package_id] = package_name
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
    superView = "framework.BaseView"
    contentView = "contentPane"
    extention = root_element.getAttribute("extention")
    if "" == extention or lua_name in WINDOWSVIEW:
        if size[0] > 100 and not has_be_import(get_package_id(package_name), component_id):
            superView = "framework.BaseWindow"
    else:
        superView = "fairygui.G" + extention
    components = []
    importClcass = {}
    contentPane = "contentPane"
    displayList = root_element.getElementsByTagName("displayList")
    if len(displayList) > 0:
        displayList = displayList[0]
        for node in displayList.childNodes:
            nodeName = node.nodeName
            luaClass = ""
            virtualdefaultItem = ""
            if "image" == nodeName or "movieclip" == nodeName:
                pkg = node.getAttribute("pkg")
                if pkg != "":
                    # 挎包引用图片
                    if pkg in packagesConfig:
                        subpkg = packagesConfig[pkg]
                        if package_name in moduleConfig and lua_name in moduleConfig[package_name]:
                            addToList(moduleConfig[package_name][lua_name]["package_names"], subpkg)
                # moduleConfig[package_name][lua_name]["package_names"].append(packagesConfig[pkg])
            elif "loader" == nodeName:
                pkg = node.getAttribute("url")
                if pkg != "" and pkg.find("ui:") > -1:
                    pkg = pkg[5:13]
                    if packagesConfig.has_key(pkg):
                        subpkg = packagesConfig[pkg]
                        if moduleConfig.has_key(package_name) and moduleConfig[package_name].has_key(lua_name):
                            addToList(moduleConfig[package_name][lua_name]["package_names"], subpkg)
            elif "text" == nodeName:
                pkg = node.getAttribute("font")
                if pkg != "" and pkg.find("ui:") > -1:
                    pkg = pkg[5:13]
                    if packagesConfig.has_key(pkg):
                        subpkg = packagesConfig[pkg]
                        if moduleConfig.has_key(package_name) and moduleConfig[package_name].has_key(lua_name):
                            addToList(moduleConfig[package_name][lua_name]["package_names"], subpkg)
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
                            if packagesConfig.has_key(pkg):
                                subpkg = packagesConfig[pkg]
                                # path[-2]=subpkg
                                if moduleConfig.has_key(package_name) and moduleConfig[package_name].has_key(lua_name):
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
                        if KEYVALE.has_key(nameID):
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

    if CLASSNAMES.has_key(lua_name):
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
    engine = tenjin.Engine()
    wirte2file(save_lua_path + "/" + package_name.lower() + "/view/" + lua_name + "Base.ts",
               engine.render('template/BaseView.ts.py', context))
    if os.path.exists(save_lua_path + "/" + package_name.lower() + "/" + lua_name + ".ts"):
        # mergeLuaFunction(save_lua_path+"/"+package_name.lower()+"/"+lua_name+".ts",lua_name,engine.render('template/View.ts.py', context))
        print("file exits:%s/%s.ts" % (package_name, lua_name))
        pass
    else:
        wirte2file(save_lua_path + "/" + package_name.lower() + "/" + lua_name + ".ts",
                   engine.render('template/View.ts.py', context))
def wirte2file(filname,values):
    f = open(filname,"wb")
    f.write(values)
    f.close()
    NEWLUAFILES.append(filname)

def addToList(list,item):
    for x in list:
        if x== item:
            return
    list.append(item)

def isWrongName(nameID):
    return True

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
        if (x == package_name):
            return x
    return 'nil'

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
            if not moduleConfig.has_key(packageName):
                moduleConfig[packageName]={}
            if not moduleConfig[packageName].has_key(className):
                moduleConfig[packageName][className]={"id":packageid,"packageNames":[packageName],"ui":"ui://"+package+componentid,"className":className,"outsideTouchCancel":False,"viewPath":"oyeahgame."+packageName+"."+className,"bgsound":False,"fullScreen":False} #,"controlPath":"oyeahgame."+packageName+".view."+className+"Base"}
                if not os.path.exists(save_lua_path+"/"+packageName.lower()+"/view"):
                    os.makedirs(save_lua_path+"/"+packageName.lower()+"/view")
                xml2lua(uipath+"/"+packageName+path+file,packageName,className,componentid)
            return moduleConfig[packageName][className]

def getComponentName(packageName,xmlName):
    key = packageName+"."+xmlName
    if not packagesType.has_key(key):
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
