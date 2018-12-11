import os
import shutil
from xml.dom import minidom
from PIL import Image
import json

moduleConfig = {}
packagesConfig = {}

fairy_assets_path = ""
egret_workspace_root = ""
egret_workspace_view_path = ""
egret_workspace_source_path = ""

imageTS = {}


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
        read_package(package_xml_file_path, package_xml_folder_name)


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
        os.makedirs("%s/config/" % egret_workspace_source_path)
    image_res_file = open("%s/config/ImageResPath.json" % egret_workspace_source_path, "w")
    image_res_file.write(json.dumps(imageTS, sort_keys=True, indent=4, separators=(',', ':')))
    image_res_file.close()


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


generate_base_view("H:\\h5\\share\\UI\\gameui\\assets", "H:\\h5\\client_tools\\game\\")
