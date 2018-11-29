import os
from xml.dom import minidom

moduleConfig={}
packagesConfig={}

def createLua(uipropath, luapatch):
    global saveLuaPath
    global uiPath
    upPath = uipropath
    resourcePath = saveLuaPath.replace("src/bingogame/view", "resource")
    if os.path.isdir(uipropath):
        imageTS={}
        for packageName in os.listdir(uipropath):
            packagePath = os.path.join(uipropath, packageName) + "/package.xml"
            if packageName[0]!="." and os.path.exists(packagePath):
                if not moduleConfig.has_key(packageName):
                    moduleConfig[packageName] = {}
                try:
                    doc = minidom.parse(packagePath)
                    rootElement = doc.documentElement
                    pkgid = rootElement.getAttribute("id")
                    packagesConfig[pkgid] = packageName
                    publish = rootElement.getElementsByTagName("publish")[0]
                    imagelist = rootElement.getElementByTagName("image")
                    excluded = publish.getAttribute("excluded").split(",")
