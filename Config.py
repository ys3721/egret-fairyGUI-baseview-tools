# -*- coding: utf-8 -*-
import os,sys
import commandsutils
SVN_ROOT_PATH="svn://10.5.30.252:81"
# shared 需要更新的文件
SHARED_FILE_LIST=[
"策划文档/界面测试",
"策划文档/配置",
"策划文档/GenerateConfiguration",
"Resource",
"clientResource",
"server"]

SDK="feiliu"
BuildTarget=["iOS","Android","OSX","Win"]
LOCALETYPES=["zh_CN","en_US"]
HomePath = os.path.expanduser('~')
SVN_TAG="trunk"
SVN_VERSION="0.0.0"
SVN_GAMECLIENT="%s/work/ungame/client/trunk" %(HomePath)
SVN_SHARED="%s/work/ungame/shared/trunk" %(HomePath)
# 固定地址不会随版本号变化改变
SVN_GAMECLIENT_TRUNK=SVN_GAMECLIENT
SVN_SHARED_TRUNK=SVN_SHARED
def setSvnTag(tag):
    global SVN_TAG
    global SVN_VERSION
    global SVN_GAMECLIENT
    global SVN_SHARED
    global projectPath
    global sharedPath
    SVN_TAG = tag
    if tag == "trunk":
        SVN_VERSION="0.0.0"
    else:
        SVN_VERSION=tag.replace("tags/","")
    SVN_GAMECLIENT="%s/work/ungame/client/%s" %(HomePath,SVN_TAG)
    SVN_SHARED="%s/work/ungame/shared/%s" %(HomePath,SVN_TAG)
    #自动更新 创建新的tag后 自动更新
    if not os.path.isdir(SVN_GAMECLIENT):
        commandsutils.execCmd("mkdir -p %s/work/ungame/client/%s" %(HomePath,tag))
        commandsutils.execCmd("svn co %s/client/%s/gameClient %s/work/ungame/client/%s/gameClient" %(SVN_ROOT_PATH,tag,HomePath,tag))
    if not os.path.isdir(SVN_SHARED):
        commandsutils.execCmd("mkdir -p %s/work/ungame/shared/%s/策划文档" %(HomePath,tag))
        for fpath in SHARED_FILE_LIST:
            commandsutils.execCmd("svn co %s/shared/%s/%s %s/work/ungame/shared/%s/%s" %(SVN_ROOT_PATH,tag,fpath,HomePath,tag,fpath))
            # Resource 自动复制出多分 需要多线程发布
            if "Resource" == fpath:
                for target in BuildTarget:
                    if target!=BuildTarget[3]:
                        commandsutils.execCmd("cp -r %s/work/ungame/shared/%s/Resource %s/work/ungame/shared/%s/Resource%s" %(HomePath,tag,HomePath,tag,target))
    projectPath="%s/gameClient" %(SVN_GAMECLIENT)
    sharedPath="%s/Resource" %(SVN_SHARED)
    print ("SVN_TAG: %s" % (SVN_TAG))
    print ("SVN_VERSION: %s" % (SVN_VERSION))
    print ("SVN_GAMECLIENT: %s" % (SVN_GAMECLIENT))
    print ("SVN_SHARED: %s" % (SVN_SHARED))
    print ("projectPath: %s" % (projectPath))
    print ("sharedPath: %s" % (sharedPath))
projectPath="%s/work/ungame/client/trunk/gameClient" %(HomePath)
sharedPath="%s/work/ungame/shared/trunk/Resource" %(HomePath)
IOSICONSIZE={
			"AppIcon29x29"         : 29,
			"AppIcon29x29~ipad"    : 29,
			"AppIcon29x29@2x"      : 58,
			"AppIcon29x29@2x~ipad" : 58,
			"AppIcon29x29@3x"      : 87,
			"AppIcon40x40~ipad"    : 40,
			"AppIcon40x40@2x"      : 80,
			"AppIcon40x40@3x"      : 210,
			"AppIcon50x50~ipad"    : 50,
			"AppIcon50x50@2x~ipad" : 50,
			"AppIcon57x57"         : 57,
			"AppIcon57x57@2x"      : 114,
			"AppIcon60x60@2x"      : 120,
			"AppIcon60x60@3x"      : 180,
			"AppIcon72x72~ipad"    : 72,
			"AppIcon72x72@2x~ipad" : 144,
			"AppIcon76x76~ipad"    : 76,
			"AppIcon76x76@2x~ipad" : 152,
			"AppIcon83.5x83.5@2x~ipad":167,
            "AppIcon1024x1024":1024
			}
IOSSPLASSIZE={
        "Default-568h@2x":"640x1136",
        "Default-667h@2x":"750x1334",
        "Default-Landscape-2436h@3x":"2436x1125",
        "Default-Landscape":"1024x768",
        "Default-Landscape@2x":"2048x1536",
        "Default-Landscape@3x":"2208x1242",
        "Default-Portrait-2436h@3x":"1125x2436",
        "Default-Portrait":"768x1024",
        "Default-Portrait@2x":"1536x2048",
        "Default-Portrait@3x":"1242x2208",
        "Default":"320x480",
        "Default@2x":"640x960",
}

ANDROIDSICONSIZE={
                    "drawable"         : 48,
                    "drawable-ldpi"    : 36,
                    "drawable-ldpi-v4" : 36,
                    "drawable-mdpi"    : 48,
                    "drawable-mdpi-v4" : 48,
                    "drawable-hdpi"    : 72,
                    "drawable-hdpi-v4" : 72,
                    "drawable-xhdpi"   : 96,
                    "drawable-xhdpi-v4": 96,
                    "drawable-xxhdpi"  : 144,
                    "drawable-xxxhdpi" : 192
            }
if __name__=="__main__":
    setSvnTag("tags/0.0.1")