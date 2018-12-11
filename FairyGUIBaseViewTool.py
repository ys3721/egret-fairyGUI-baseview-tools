import os
import shutil
from xml.dom import minidom

moduleConfig = {}
packagesConfig = {}

fairy_assets_path = ""
egret_workspace_root = ""
egret_workspace_view_path = ""
egret_workspace_source_path = ""

def generate_base_view(fairyGUI_assets_path, export_workspace):
    global egret_workspace_root
    egret_workspace_root = export_workspace
    global fairy_assets_path
    fairy_assets_path = fairyGUI_assets_path
    init_paths()

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
                if "image" == package_folder_name:
                    copy_image_to_workspace(image_element, package_folder_name)


def copy_image_to_workspace(image_element, package_folder_name):
    target_path = egret_workspace_source_path + "/image/" + image_element.getAttribute("path")
    if not os.path.exists(target_path):
        os.makedirs(target_path)

    image_path = fairy_assets_path + "/" + package_folder_name + image_element.getAttribute("path") + image_element.getAttribute("name")
    copy_image_command = "%s %s%s" % (image_path, target_path, image_element.getAttribute("name"))
    print("Will copy %s" % copy_image_command)
    shutil.copy(copy_image_command.split(" ")[0], copy_image_command.split(" ")[1])

generate_base_view("H:\\h5\\share\\UI\\gameui\\assets", "H:\\h5\\client_tools\\game\\")
