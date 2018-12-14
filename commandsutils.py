#!/usr/bin/python
# coding=utf-8
# -*- coding: utf-8 -*-
import os, sys
import re
import Config

try:
    from PIL import Image
except ImportError:
    print
    "no install PIL"
try:
    from hashlib import md5
except ImportError:
    print
    "no install hashlib"
try:
    import pexpect
    import biplist
except ImportError:
    print
    "no install pexpect"

import shutil
import zlib
import time
import platform

try:
    import pylzma
except ImportError:
    print
    "no install pylzma"
# 更具系统判断 可执行文件路径
TexturePacker = "TexturePacker"
if platform.system() == "Linux":
    TexturePacker = "/mnt/c/Program\ Files\ \(x86\)/CodeAndWeb/TexturePacker/bin/TexturePacker.exe"
    if not os.path.exists("/mnt/c/Program Files (x86)/CodeAndWeb/TexturePacker/bin/TexturePacker.exe"):
        TexturePacker = "/mnt/d/Program\ Files\ \(x86\)/CodeAndWeb/TexturePacker/bin/TexturePacker.exe"


# svn propset svn:ignore "*.meta" oyeahgame/Force/view
def execCmd(cmd):
    log(cmd)
    # commands.getstatusoutput(cmd)
    return os.popen(cmd).read()


# retcode= subprocess.call(cmd,shell=True)
def calMD5ForFile(file):
    m = md5()
    f = open(file, 'rb')
    m.update(f.read())
    f.close()
    return m.hexdigest()


def log(message):
    print(message)
    sys.stdout.flush()


def scp(local, remote):
    ret = -1
    print
    'scp %s %s:%s' % (local, IP, remote)
    ssh = pexpect.spawn('scp %s %s:%s' % (local, IP, remote))
    try:
        i = ssh.expect(['password', 'continue connecting (yes/no)?', 'Enter passphrase for key'], timeout=5)
        if i == 0:
            ssh.sendline(password)
        elif i == 1:
            ssh.sendline('yes\n')
            ssh.expect('password: ')
            ssh.sendline(password)
        elif i == 2:
            ssh.sendline(password)
        ret = ssh.expect('100%')
        print
        ret
        r = ssh.read()
        print
        r
        r = ssh.read()
        print
        r
        ret = ssh.expect('$', timeout=100)
        print
        ret
        r = ssh.read()
        print
        r
        ret = 0
    except pexpect.EOF:
        print
        "EOF"
        ssh.close()
        ret = -1
    except pexpect.TIMEOUT:
        print
        "TIMEOUT"
        ssh.close()
        ret = -2
    return ret


def hostPlatform():
    return platform.system()


def copytree(src, dst, symlinks=False):
    names = os.listdir(src)
    if not os.path.isdir(dst):
        os.makedirs(dst)

    errors = []
    for name in names:
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if symlinks and os.path.islink(srcname):
                linkto = os.readlink(srcname)
                os.symlink(linkto, dstname)
            elif os.path.isdir(srcname):
                copytree(srcname, dstname, symlinks)
            else:
                if os.path.isdir(dstname):
                    os.rmdir(dstname)
                elif os.path.isfile(dstname):
                    os.remove(dstname)
                shutil.copy2(srcname, dstname)
            # XXX What about devices, sockets etc.?
        except (IOError, os.error) as why:
            errors.append((srcname, dstname, str(why)))
        # catch the Error from the recursive copytree so that we can
        # continue with other files
        except OSError as err:
            errors.extend(err.args[0])
    if errors:
        raise Error(errors)


def deleteGapDir(dir):
    if os.path.isdir(dir):
        for d in os.listdir(dir):
            deleteGapDir(os.path.join(dir, d))
        if not os.listdir(dir):
            os.rmdir(dir)


def zipFile(file):
    f = open(file, 'rb+')
    line = f.read()
    result = zlib.compress(line)
    f.seek(0)
    f.truncate()
    f.write(result)
    f.close()


def unzipFile(file):
    f = open(file, 'rb+')
    line = f.read()
    result = zlib.decompress(line)
    f.seek(0)
    f.truncate()
    f.write(result)
    f.close()


def LZMAzipfile(file):
    f = open(file, 'rb+')
    line = f.read()
    result = pylzma.compress(line)
    f.seek(0)
    f.truncate()
    f.write(result)
    f.close()


def unLZMAzipfile(file):
    f = open(file, 'rb+')
    line = f.read()
    result = pylzma.decompress(line)
    f.seek(0)
    f.truncate()
    f.write(result)
    f.close()


def svnRevertAndUpdate(path):
    info = execCmd("cd %s/ && svn revert --depth infinity . && svn up " % (path))
    if info.find("cleanup") > -1:
        execCmd("cd %s/ && svn cleanup && svn revert --depth infinity . && svn up " % (path))


def svnCommit(path, skipmeta=True):
    if skipmeta:
        execCmd(
            "cd %s && svn st |grep '.meta' | grep '^\M' | sed 's/^M/ /g' | sed 's/[ ]*//' | sed 's/[ ]/\\\\ /g' | xargs svn revert " % (
                path))
    execCmd(
        "cd %s && svn st | grep '^\!' | tr '^\!' ' ' | sed 's/[ ]*//' | sed 's/[ ]/\\\\ /g' | xargs -I {} svn del '{}@'" % (
            path))
    execCmd(
        "cd %s && svn st | grep '^\?' | tr '^\?' ' ' | sed 's/[ ]*//' | sed 's/[ ]/\\\\ /g' | xargs -I {} svn add '{}@'" % (
            path))
    execCmd("svn commit %s -m 'auto commit file no .meta -%s'" % (path, time.strftime('%Y_%m_%d_%H_%M_%S')))


def replacefile(file, replaceText):
    f = open(file, 'r+')
    line = f.read()
    f.seek(0)
    f.truncate()
    for kvs in replaceText:
        line = re.sub(kvs[0], kvs[1], line)
    f.write(line)
    f.close()


def svnignore(dir):
    if os.path.isdir(dir):
        for d in os.listdir(dir):
            svnignore(os.path.join(dir, d))
        execCmd('svn propset svn:ignore "*.meta" %s' % (dir))


# TexturePacker dir to image
def texturePackerImage(intDir, outFile, isCompress=True):
    info = ""
    if isCompress:
        info = execCmd(
            "%s %s --disable-rotation --opt RGBA4444 --force-squared --dither-fs-alpha --format unity --trim-mode Trim --max-width 2048 --max-height 2048 --size-constraints POT --sheet %s.png --data %s.txt " % (
            TexturePacker, pwdphysical(intDir), pwdphysical(outFile), pwdphysical(outFile)))
    else:
        info = execCmd(
            "%s %s --disable-rotation --format unity --trim-mode Trim --max-width 2048 --max-height 2048 --size-constraints AnySize --sheet %s.png --data %s.txt " % (
            TexturePacker, pwdphysical(intDir), pwdphysical(outFile), pwdphysical(outFile)))
    if info.find("error:") > -1:
        log(intDir)
        log(info)


# --dither-fs                 Enables Floyd-Steinberg dithering without alpha for color reduction
# --dither-fs-alpha           Enables Floyd-Steinberg dithering with alpha for color reduction
# --dither-atkinson           Enables Atkinson dithering without alpha for color reduction
# --dither-atkinson-alpha
def TexturePackerDithering(infile, dither="--dither-fs"):
    PVRTC4 = "PVRTC4"
    if infile.endswith(".jpg"):
        PVRTC4 = "PVRTC4_NOALPHA"
    info = execCmd(
        "%s %s --opt %s %s --disable-rotation --border-padding 0 --trim-mode None --format unity --size-constraints AnySize --sheet %s.pvr --data %s.txt" % (
        TexturePacker, pwdphysical(infile), PVRTC4, dither, pwdphysical(infile), pwdphysical(infile)))
    execCmd("rm -rf %s.txt" % (infile))
    if info.find("error:") > -1:
        log(info)


def TexturePackerDirDithering(indir, dither="--dither-fs"):
    for root, subdirs, files in os.walk(indir):
        for file in files:
            if file.endswith(".png") or file.endswith(".jpg"):
                TexturePackerDithering(os.path.join(root, file), dither)


def installApp(appPath):
    info = execCmd("fruitstrap -d -b %s" % (appPath))
    if info.find("failed:") > -1:
        result = info[info.find("failed:") + 7:].strip()
        if result == "-402620395":
            log("A valid provisioning profile for this executable was not found.(err:%s)" % (result))
        elif result == "-402653109":
            log("A valid provisioning profile for this executable was not found.(err:%s)" % (result))
        elif result == "-402620394":
            log(
                "The entitlements specified in your application’s Code Signing Entitlements file are invalid, not permitted, or do not match those specified in your provisioning profile. (0xE8008016).(err:%s)" % (
                    result))
        else:
            log("AMDeviceInstallApplication failed: %s" % (result))
        log("installed FAILED")
    else:
        log("installed SUCCESS")


# string array dict bool real integer date data
def getPlistNodeType(value):
    nodeTyep = "string"
    if isinstance(value, bool):
        nodeTyep = "bool"
    elif isinstance(value, list):
        nodeTyep = "array"
    elif isinstance(value, dict):
        nodeTyep = "dict"
    elif isinstance(value, int):
        nodeTyep = "integer"
    return nodeTyep


def addPlist(key, value, path):
    nodeTyep = getPlistNodeType(value)
    execCmd("/usr/libexec/PlistBuddy -c 'Add :%s %s' %s" % (key, nodeTyep, path))
    if nodeTyep == "array":
        for v in value:
            addPlist(key + ":", v, path)
    elif nodeTyep == "dict":
        for v in value:
            addPlist(key + ":" + v, value[v], path)
    else:
        execCmd("/usr/libexec/PlistBuddy -c 'Set :%s %s' %s" % (key, value, path))


def mergeDict(oldDict, newDict):
    for k in newDict:
        if oldDict.has_key(k):
            nodeTyep = getPlistNodeType(newDict[k])
            if nodeTyep == "array":
                print
                "skip"
            elif nodeTyep == "dict":
                mergeDict(oldDict[k], newDict[k])
            else:
                oldDict[k] = newDict[k]
        else:
            oldDict[k] = newDict[k]


def setPlist(path, value):
    plist = biplist.readPlist(path)
    mergeDict(plist, value)
    try:
        biplist.writePlist(plist, path, False)
    except Exception as e:
        print
        "Something bad happened:", e


def delPlist(key, path):
    plist = biplist.readPlist(path)
    if plist.has_key(key):
        del plist[key]
    try:
        biplist.writePlist(plist, path, False)
    except Exception as e:
        print
        "Something bad happened:", e


def importP12(path, pwd):
    # execCmd("security unlock-keychain -p mengjie ~/Library/Keychains/login.keychain")
    execCmd("security import %s -k ~/Library/Keychains/login.keychain -P %s -T /usr/bin/codesign" % (path, pwd))


def checkTeamName(path, teamname):
    # execCmd("security unlock-keychain -p mengjie ~/Library/Keychains/login.keychain")
    codesigning = execCmd(
        "/usr/libexec/PlistBuddy -c 'Print TeamName' /dev/stdin <<< $(security cms -D -i %s)" % (path)).strip()
    dev = execCmd(
        "/usr/libexec/PlistBuddy -c 'Print Entitlements:aps-environment' /dev/stdin <<< $(security cms -D -i %s)" % (
            path)).strip()
    if dev == "development":
        codesigning = "iPhone Developer: " + codesigning
    else:
        codesigning = "iPhone Distribution: " + codesigning
    identities = execCmd("security find-identity -v codesigning ~/Library/Keychains/login.keychain").strip()
    group = re.findall(r'"iPhone[^"]+"', identities)
    for gp in group:
        if gp.find(codesigning) > -1:
            return gp
    return teamname


def printentitlements(mobileprovision, entitlements):
    execCmd(
        '/usr/libexec/PlistBuddy -x -c "print :Entitlements " /dev/stdin <<< $(security cms -D -i ' + mobileprovision + ')>' + entitlements)


def checkP12AndProvision(p12path, p12pwd, provisionpath, dev):
    if not checkTeamName(provisionpath, dev):
        importP12(p12path, p12pwd)
    return checkTeamName(provisionpath, dev)


def resignIPA(ipa, mobileprovision, p12path, p12pwd):
    temp = "/Volumes/RamDisk/temp/signipa"
    if os.path.isdir(temp):
        execCmd("rm -rf %s/*" % (temp))
    else:
        execCmd("mkdir -p %s" % (temp))
    execCmd("unzip %s -d %s/" % (ipa, temp))
    app = execCmd("find %s -name '*.app' -type d" % (temp)).strip()
    if len(app) > 4 and os.path.isdir(app):
        codesignAPP(app, mobileprovision)
        ipaName = "iOS_%s" % (time.strftime('%Y_%m_%d_%H_%M_%S'))
        execCmd("cd %s && zip -r %s.ipa ./Payload" % (temp, ipaName))
        execCmd("scp %s/%s.ipa macmini:~/www/app/slgame/%s.ipa" % (temp, ipaName, ipaName))
    else:
        log("not fond app")
    # codesignAPP( "%s/Payload/" mobileprovision)


def codesignAPP(app, mobileprovision, p12path, p12pwd, teamname):
    # 1 复制mobileprovision 到 app目录下面
    execCmd("rm -rf %s/embedded.mobileprovision" % (app))
    execCmd("cp -r %s  %s/embedded.mobileprovision" % (mobileprovision, app))
    # linux 签名
    if hostPlatform() == "Linux":
        return isignResignAPP(app, mobileprovision, p12path, p12pwd)
    # 2 生成 entitlements 文件
    execCmd("rm -rf %s/../../entitlements.plist" % (app))
    execCmd(
        '/usr/libexec/PlistBuddy -x -c "print :Entitlements " /dev/stdin <<< $(security cms -D -i %s)> %s/../../entitlements.plist' % (
        mobileprovision, app))
    # bug resource fork, Finder information, or similar detritus not allowed
    execCmd("xattr -rc %s" % (app))

    identifier = execCmd(
        '/usr/libexec/PlistBuddy -c "print :application-identifier" %s/../../entitlements.plist' % (app)).strip()
    identifier = identifier[identifier.find(".") + 1:]
    print
    identifier
    # setPlist("%s/Info.plist" %(app),{"CFBundleIdentifier":identifier})
    # 签名
    teameName = checkTeamName(mobileprovision, teamname)
    if teameName:
        execCmd('/usr/bin/codesign -f -vv -s %s --entitlements %s/../../entitlements.plist %s' % (teameName, app, app))
        return True
    else:
        return False


def isignResignAPP(ipa, mobileprovision, p12path, p12pwd):
    certificatePath = os.path.dirname(p12path) + "/.isign"
    # 1 转换ising 证书
    if not os.path.exists(certificatePath + "/certificate.pem"):
        ssh = pexpect.spawn('/usr/local/bin/isign_export_creds.sh %s %s' % (p12path, certificatePath))
        isDone = False
        while not isDone:
            try:
                i = ssh.expect(['Enter Import Password', 'Find matching provisioning profile?', '[Y/n]'], timeout=5)
                if i == 0:
                    print
                    "输入密码"
                    ssh.sendline(p12pwd)
                    ssh.sendline('\n')
                elif i == 1:
                    isDone = True
                    ssh.sendline('n')
                    ssh.close()
                elif i == 2:
                    print
                    "[Y/n]？"
                    ssh.sendline('n')
                elif i == 3:
                    ssh.sendline('n')
            except pexpect.EOF:
                print
                "EOF"
                ssh.close()
                isDone = True
            except pexpect.TIMEOUT:
                print
                "TIMEOUT"
                ssh.close()
                isDone = True
    # 2 签名
    execCmd("/usr/local/bin/isign -c %s/certificate.pem -k %s/key.pem -p %s  -o %s %s" % (
    certificatePath, certificatePath, mobileprovision, ipa, ipa))
    return True


# 转换成绝对路径
def pwdphysical(path):
    if hostPlatform() == "Linux":
        paths = path.strip().split("/")
        paths.reverse()
        path = paths.pop()
        while len(paths) > 0 and os.path.isdir(path + "/" + paths[len(paths) - 1]):
            path = path + "/" + paths.pop()
        path = execCmd("cd %s && pwd -P" % (path)).strip().replace("/mnt/", "")
        path = path[0] + ":" + path[1:]
        if len(paths) > 0:
            paths.reverse()
            path = path + "/" + "/".join(paths)
    return path


def generateIosSplash(imagePath, outPath):
    img = Image.open(imagePath)
    for key in Config.IOSSPLASSIZE.keys():
        size = Config.IOSSPLASSIZE[key].split("x")
        imageSize = img.size
        if int(size[0]) < int(size[1]):
            out = img.transpose(Image.ROTATE_270)
            imageSize = (img.size[1], img.size[0])
        else:
            out = img
        _x = float(size[0]) / imageSize[0]
        _y = float(size[1]) / imageSize[1]
        if _x > _y:
            _y = int(_x * imageSize[1])
            _x = int(size[0])
        else:
            _x = int(_y * imageSize[0])
            _y = int(size[1])
        # 调整尺寸
        out = out.resize((_x, _y), Image.ANTIALIAS)
        # for x in xrange((_x-int(size[0]))/2+1,(_x-int(size[0]))/2+int(size[0])-1):
        # 	out.putpixel((x,(_y-int(size[1]))/2+1),(255,255,255))
        # 	out.putpixel((x,(_y-int(size[1]))/2+int(size[1])-1),(255,255,255))
        # for y in xrange((_y-int(size[1]))/2+1,(_y-int(size[1]))/2+int(size[1])-1):
        # 	out.putpixel(((_x-int(size[0]))/2+1,y),(255,255,255))
        # 	out.putpixel(((_x-int(size[0]))/2+int(size[0])-1,y),(255,255,255))
        _x = int((_x - int(size[0])) / 2)
        _y = int((_y - int(size[1])) / 2)
        out = out.crop((_x, _y, _x + int(size[0]), _y + int(size[1])))
        out.save(outPath + key + ".png", "PNG")


def getSvnRevision(path):
    info = execCmd("svn log %s -l 1" % (path))
    for x in info.split("\n"):
        infos = x.strip().split("|")
        for v in infos:
            v = v.strip()
            if "r" == v[0]:
                return v[1:]
    return "0"


def upkfile(path):
    upk = open("%s.upk" % (path), "wb")
    for root, subdirs, files in os.walk(path):
        for file in files:
            filefullpath = os.path.join(root, file)
            f = open(filefullpath, 'r')
            line = f.read()
            upk.write(line)
            f.close()
    upk.close()
    LZMAzipfile("%s.upk" % (path))


if __name__ == "__main__":
    TexturePackerDirDithering("~/work/ungame/client/trunk/gameClient/Assets/StreamingAssets/image")