import os
from xml.dom import minidom

moduleConfig = {}
packagesConfig = {}


def createLua(uipropath, luapatch):
    global saveLuaPath
    global uiPath
    uiPath = uipropath
    saveLuaPath = luapatch;
    resourcePath = saveLuaPath.replace("src/bingogame/view", "resource")
    if os.path.isdir(uipropath):
        imageTS = {}
        for packageName in os.listdir(uipropath):
            packagePath = os.path.join(uipropath, packageName) + "/package.xml"
            if packageName[0] != "." and os.path.exists(packagePath):
                if packageName not in moduleConfig:
                    moduleConfig[packageName] = {}
                try:
                    doc = minidom.parse(packagePath)
                    rootElement = doc.documentElement
                    pkgid = rootElement.getAttribute("id")
                    packagesConfig[pkgid] = packageName
                    publish = rootElement.getElementsByTagName("publish")[0]
                    imagelist = rootElement.getElementsByTagName("image")
                    excluded = publish.getAttribute("excluded").split(",")
                    for image in imagelist:
                        imageid = image.getAttribute("id")
                        for exid in excluded:
                            if exid == imageid:
                                if "image" == packageName:
                                    if not os.path.exists(resourcePath + "/image/" + image.getAttribute("path")):
                                        os.makedirs(resourcePath + "/image/" + image.getAttribute("path"))
                                    imagePath = packagePath.replace("/package.xml", image.getAttribute("path") + image.getAttribute("name"))
                                    execCmd("xcopy %s %s/image/%s/%s" % (imagePath, resourcePath.packageName.image.getAttribute("name")))
                                print("begin to fuck the exclude id of %s, in packageName=%s" %(imageid, packageName))
                except Exception as e:
                    print(e)

def execCmd(cmd):
    return os.popen(cmd).read()

createLua("H:\\h5\\share\\UI\\gameui\\assets", "H:\\h5\\client_tools\\game\\src\\bingogame\\view")
