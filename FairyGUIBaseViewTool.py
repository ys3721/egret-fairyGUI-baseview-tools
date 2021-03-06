import os
import shutil
from xml.dom import minidom
from PIL import Image
import json
import tenjin
import Config


CONFIG_SCREEN_WIDTH = 960
CONFIG_SCREEN_HEIGHT = 540
WINDOWSVIEW = {"Account":0}
# 关键字 不可使用
KEYVALE={"name":True,"apexIndex":True,"mask":True,"baseUserData":True,"viewWidth":True,"viewHeight":True, "x":True,"y":True,"scrollPane":True,"opaque":True,"margin":True,"childrenRenderOrder":True}
packagesImport={"wuy3bh5gasf42v":True,"js0d6vmkcwn9t7":True,"xkpsx4uivd0a2o":True,"62g0ma7tdyidb":True,"wuy3bh5gilz148":True, "xkpsx4uietk131":True}

moduleConfig = {}
packagesConfig = {}

fairy_assets_path = ""
egret_workspace_root = ""
egret_workspace_view_path = ""
egret_workspace_source_path = ""

imageTS = {}
NEWLUAFILES=[]
CLASSNAMES={}
packagesType={}


def generate_base_view(fairyGUI_assets_path, export_workspace):
    global egret_workspace_root
    egret_workspace_root = export_workspace
    global fairy_assets_path
    fairy_assets_path = fairyGUI_assets_path
    init_paths()
    # 遍历所有的fairyGUI的assert下的目录
    for package_xml_folder_name in os.listdir(fairy_assets_path):
        package_xml_file_path = os.path.join(fairyGUI_assets_path, package_xml_folder_name) + "/package.xml"
        print("Begin read file :" + package_xml_file_path)
        if package_xml_folder_name not in moduleConfig:
            moduleConfig[package_xml_folder_name] = {}
        read_package(package_xml_file_path, package_xml_folder_name)

    for pkgid in packagesConfig:
        pcckageName = packagesConfig[pkgid]
        createPackage(os.path.join(fairyGUI_assets_path, package_xml_folder_name), package_xml_folder_name)
    engin = tenjin.Engine()
    template = tenjin.SafeTemplate('template/ModuleConfigAuto.ts.py')
    wirte2file(egret_workspace_root+"/ModuleConfigAuto.ts", template.render({"modules":moduleConfig}))


def init_paths():
    global egret_workspace_view_path
    egret_workspace_view_path = egret_workspace_root + "/src/bingogame/view"
    global egret_workspace_source_path
    egret_workspace_source_path = egret_workspace_root + "/resource"


def read_package(package_xml_file_path, package_folder_name):
    doc = minidom.parse(package_xml_file_path)
    root_element = doc.documentElement
    package_id = root_element.getAttribute("id")
    packagesConfig[package_id] = package_xml_file_path
    # publish element
    publish_element = root_element.getElementsByTagName("publish")[0]
    excluded_image_ids = publish_element.getAttribute("excluded").split(",")
    # image elements
    image_elements = root_element.getElementsByTagName("image")
    # 遍历所有的image elements取它的id
    for image_element in image_elements:
        image_id = image_element.getAttribute("id")
        for excluded_image_id in excluded_image_ids:
            if excluded_image_id == image_id:
                copy_image_to_workspace(image_element, package_folder_name)
                assemble_img_res(package_id, package_folder_name, image_element)


def assemble_img_res(package_xml_id, package_folder_name, image_element):
    """这个地方会每次都一个assets文件夹 就会写一次文件 所以效率应该是很低的
    """
    global imageTS
    image_path = fairy_assets_path + "/" + package_folder_name + image_element.getAttribute(
        "path") + image_element.getAttribute("name")
    image_id = image_element.getAttribute("id")
    image = Image.open(image_path)
    image_info = {"path" : "image" + image_element.getAttribute("path") + image_element.getAttribute("name"), "size" : image.size}
    imageTS["ui://" + package_xml_id + image_id] = image_info

    if not os.path.exists("%s/config/" % egret_workspace_source_path):
        os.maakedirs("%s/config/" % egret_workspace_source_path)
    """
    image_res_file = open("%s/config/ImageResPath.json" % egret_workspace_source_path, "w")
    image_res_file.write(json.dumps(imageTS, sort_keys=True, indent=4, separators=(',', ':')))
    image_res_file.close()
    """

def copy_image_to_workspace(image_element, package_folder_name):
    if package_folder_name == "image":
        target_path = egret_workspace_source_path + "/" + package_folder_name + "/" + image_element.getAttribute("path")
    else:
        target_path = egret_workspace_source_path + "/image/" + package_folder_name

    if not os.path.exists(target_path):
        os.makedirs(target_path)

    image_path = fairy_assets_path + "/" + package_folder_name + image_element.getAttribute(
        "path") + image_element.getAttribute("name")
    copy_image_command = "%s %s/%s" % (image_path, target_path, image_element.getAttribute("name"))
    print("Will copy %s" % copy_image_command)
    shutil.copy(copy_image_command.split(" ")[0], copy_image_command.split(" ")[1])


def general_view_class():
    for package_xml_id in packagesConfig:
        package_xml_file_path = packagesConfig[package_xml_id]


def createPackage(path,packageName):
    doc = minidom.parse(path+"/package.xml")
    rootElement = doc.documentElement
    pkgid = rootElement.getAttribute("id")
    if pkgid not in packagesConfig:
        packagesConfig[pkgid] = packageName
    componentlist=rootElement.getElementsByTagName("component")
    for component in componentlist:
        if "true" == component.getAttribute("exported"):
            packageid=component.getAttribute("id")
            file=component.getAttribute("name")
            subpath = component.getAttribute("path")
            if path!="":
               file= subpath[1:]+file
            name=file[:-4]
            name=name.split("/")[-1]
            className=name[0].upper()+name[1:]
            if className not in moduleConfig:
                moduleConfig[packageName][className]={"id":packageid,"packageNames":[packageName],"ui":"ui://"+getPackageId(packageName)+packageid,"className":className,"outsideTouchCancel":False,"viewPath":"oyeahgame."+packageName+"."+className,"bgsound":False,"fullScreen":False}#,"controlPath":"oyeahgame."+packageName+".view."+className+"Base"}
                if not os.path.exists(egret_workspace_view_path):
                    os.makedirs(egret_workspace_source_path)
                xml2lua(path+"/"+file,packageName,name,packageid)


def getPackageId(packageName):
    for x in packagesConfig:
        if packagesConfig[x] == packageName:
            return x
    return ""

def xml2lua(file, packageName, luaname, componentid):
    global readFileList
    global CLASSNAMES
    if file not in readFileList or not os.path.exists(file):
        return
    luaname=luaname[0].upper() + luaname[1:]
    readFileList[file]=True
    doc = minidom.parse(file)
    rootElement = doc.documentElement
    size = rootElement.getAttribute("size")
    size = size.split(",")
    size = [int(size[0]), int(size[1])]
    panelType = 1
    if size[0] >= CONFIG_SCREEN_WIDTH or size[1] >= CONFIG_SCREEN_HEIGHT:
        panelType = 2
    superView = "framework.BaseView"
    contentView = "contentPane"
    extention = rootElement.getAttribute("extention")
    if "" == extention or luaname in WINDOWSVIEW:
        if size[0] > 100 and not hasbeImport(getPackageId(packageName), componentid):
            superView = "framework.BaseWindow"
    else:
        superView = "fairygui.G" + extention
    components = []
    importClcass = {}
    contentPane = "contentPane"
    displayList = rootElement.getElementsByTagName("displayList")
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
                        if packageName in moduleConfig and luaname in moduleConfig[packageName]:
                            addToList(moduleConfig[packageName][luaname]["packageNames"], subpkg)
                # moduleConfig[packageName][luaname]["packageNames"].append(packagesConfig[pkg])
            elif "loader" == nodeName:
                pkg = node.getAttribute("url")
                if pkg != "" and pkg.find("ui:") > -1:
                    pkg = pkg[5:13]
                    if pkg in packagesConfig:
                        subpkg = packagesConfig[pkg]
                        if packageName in moduleConfig and luaname in moduleConfig:
                            addToList(moduleConfig[packageName][luaname]["packageNames"], subpkg)
            elif "text" == nodeName:
                pkg = node.getAttribute("font")
                if pkg != "" and pkg.find("ui:") > -1:
                    pkg = pkg[5:13]
                    if pkg in packagesConfig:
                        subpkg = packagesConfig[pkg]
                        if packageName in moduleConfig and luaname in moduleConfig:
                            addToList(moduleConfig[packageName][luaname]["packageNames"], subpkg)
            if "#text" != nodeName:
                defaultItem = node.getAttribute("defaultItem")
                touchable = node.getAttribute("touchable") != "false"
                if defaultItem != "":
                    module = addSubPackages(defaultItem[5:13], defaultItem[13:])
                    if module:
                        packageNames = moduleConfig[packageName][luaname]["packageNames"]
                        virtualdefaultItem = module["className"]
                        for subpkg in module["packageNames"]:
                            addToList(packageNames, subpkg)
                elif "list" == nodeName:
                    displayList = node.getElementsByTagName("item")
                    for subnode in displayList:
                        defaultItem = subnode.getAttribute("url")
                        if len(defaultItem) > 13:
                            module = addSubPackages(defaultItem[5:13], defaultItem[13:])
                            if module:
                                packageNames = moduleConfig[packageName][luaname]["packageNames"]
                                for subpkg in module["packageNames"]:
                                    addToList(packageNames, subpkg)

                filterName = node.getAttribute("name")
                pkgfileName = node.getAttribute("fileName")
                if pkgfileName == "CloseButtonBack.xml":
                    moduleConfig[packageName][luaname]["outsideTouchCancel"] = True
                    pass
                elif filterName == "title" or filterName == "icon":
                    pass
                else:
                    if nodeName == "component":
                        subpkg = packageName
                        # path = file.split("/")
                        # path[-1]=node.getAttribute("src")+".xml"
                        pkg = node.getAttribute("pkg")
                        if pkg != "":
                            if pkg in packagesConfig:
                                subpkg = packagesConfig[pkg]
                                # path[-2]=subpkg
                                if packageName in moduleConfig and moduleConfig[packageName].has_key(luaname):
                                    addToList(moduleConfig[packageName][luaname]["packageNames"], subpkg)
                        # path="/".join(path)
                        luaClass, nodeName = getComponentName(subpkg, node.getAttribute("src"))
                        if luaClass != "":
                            module = addSubPackages(getPackageId(subpkg), node.getAttribute("src"))
                            if module:
                                importClcass[luaClass] = subpkg
                                packageNames = moduleConfig[packageName][luaname]["packageNames"]
                                for subpkg in module["packageNames"]:
                                    addToList(packageNames, subpkg)
                    nameID = node.getAttribute("name")
                    if isWrongName(nameID):
                        print("%s 控件名称错误 请修改 '%s'" % (luaname, nameID))
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
                                print("请修改 %s ERROR:包含重复名字 %s " % (luaname, nameID))
                                raise ValueError
                        if KEYVALE.has_key(nameID):
                            print("请修改 %s ERROR: 包含关键字 %s " % (luaname, nameID))
                            raise ValueError
                        components.append(
                            {"name": nameID, "touchable": touchable, "luaClass": luaClass, "type": nodeName,
                             "defaultItem": virtualdefaultItem, "contentPane": contentPane})
        # else:
        #   log nodeName
    if panelType == 2:
        moduleConfig[packageName][luaname]["fullScreen"] = True
    else:
        moduleConfig[packageName][luaname]["fullScreen"] = False

    if CLASSNAMES.has_key(luaname):
        print("请修改 %s ERROR: 文件名冲突 %s " % (luaname, luaname))
        raise ValueError
    if isWrongName(luaname):
        print("%s 文件名称错误 请修改 '%s'" % (luaname, luaname))
        raise ValueError
    CLASSNAMES[luaname] = True;
    # sort by name
    components.sort(key=lambda components: components.get('name'), reverse=False)
    context = {"viewName": luaname,
               "packageName": packageName,
               "superView": superView,
               "importClcass": importClcass,
               "contentView": contentView,
               "components": components,
               "version": Config.SVN_VERSION
               }
    moduleConfig[packageName][luaname]["layerTag"] = "UI_VIEW_TYPE.WINLAYER"
    engine = tenjin.Engine()
    wirte2file(egret_workspace_source_path + "/" + packageName.lower() + "/view/" + luaname + "Base.ts",
               engine.render('template/BaseView.ts.py', context))
    if os.path.exists(egret_workspace_source_path + "/" + packageName.lower() + "/" + luaname + ".ts"):
        # mergeLuaFunction(saveluapath+"/"+packageName.lower()+"/"+luaname+".ts",luaname,engine.render('template/View.ts.py', context))
        print("file exits:%s/%s.ts" % (packageName, luaname))
        pass
    else:
        wirte2file(egret_workspace_source_path + "/" + packageName.lower() + "/" + luaname + ".ts",
                   engine.render('template/View.ts.py', context))


def wirte2file(filname,values):
    f = open(filname,"wb")
    f.write(values)
    f.close()
    NEWLUAFILES.append(filname)

def getComponentName(packageName,xmlName):
    key = packageName+"."+xmlName
    if key not in packagesType:
        doc = minidom.parse(fairy_assets_path+"/"+packageName+"/package.xml")
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
            doc = minidom.parse(fairy_assets_path+"/"+packageName+node.getAttribute("path")+className)
            extention = doc.documentElement.getAttribute("extention")
            className=className[0].upper()+className[1:-4]
            packagesType[key]=[className,extention]
    return packagesType[key][0], packagesType[key][1]


def hasbeImport(packageId,componentid):
    packagekey = packageId+componentid
    if packagesImport.has_key(packagekey):
        return packagesImport[packagekey]
    else:
        for __packageId in packagesConfig:
            packageName = packagesConfig[__packageId]
            doc = minidom.parse(fairy_assets_path+"/"+packageName+"/package.xml")
            rootElement = doc.documentElement
            componentlist=rootElement.getElementsByTagName("component")
            for component in componentlist:
                file=component.getAttribute("name")
                path = component.getAttribute("path")
                file = fairy_assets_path+"/"+packageName+path+file
                try:
                    doc = minidom.parse(file)
                except Exception as e:
                    print ("解析文件错误:%s" %(file))
                    raise e
                rootElement = doc.documentElement
                displayList=rootElement.getElementsByTagName("displayList")
                if len(displayList)>0:
                    displayList=displayList[0]
                    for node in displayList.childNodes:
                        if "#text" != node.nodeName:
                            pkg = node.getAttribute("pkg")
                            if len(pkg)<5:
                                pkg=__packageId
                            if pkg==packageId:
                                if node.getAttribute("src") == componentid :
                                    packagesImport[packagekey]=True
                                    return packagesImport[packagekey]
                                else:
                                    defaultItem =node.getAttribute("defaultItem")
                                    if len(defaultItem)>13:
                                        if defaultItem[13:]==componentid and defaultItem[5:13]==packageId:
                                            packagesImport[packagekey]=True
                                            return packagesImport[packagekey]
                displayList=rootElement.getElementsByTagName("item")
                for node in displayList:
                    defaultItem = node.getAttribute("url")
                    if len(defaultItem)>13:
                        if defaultItem[13:]==componentid and defaultItem[5:13]==packageId:
                            packagesImport[packagekey]=True
                            return packagesImport[packagekey]

    packagesImport[packagekey]=False
    return packagesImport[packagekey]


def isWrongName(luaname):
    return False


def addToList(list,item):
    for x in list:
        if x== item:
            return
    list.append(item)


def addSubPackages(package,componentid):
    # log ("%s-%s" %(packagesConfig[package],componentid))
    packageName = packagesConfig[package]
    doc = minidom.parse(fairy_assets_path+"/"+packageName+"/package.xml")
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
                if not os.path.exists(egret_workspace_root+"/"+packageName.lower()+"/view"):
                    os.makedirs(egret_workspace_root+"/"+packageName.lower()+"/view")
                xml2lua(fairy_assets_path+"/"+packageName+path+file,packageName,className,componentid)
            return moduleConfig[packageName][className]


def get_package_id(packageName):
    for x in packagesConfig:
        if packagesConfig[x] == packageName:
            return x


generate_base_view("H:\\h5\\share\\UI\\gameui\\assets", "H:\\h5\\client_tools\\game\\")
