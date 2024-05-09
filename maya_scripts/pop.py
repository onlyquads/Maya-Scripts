import os
import platform
import subprocess as sp
import maya.cmds as mc
from dwmaya.path import get_scene_path


def open_dir(path):
    fixed_path = os.path.normpath(path)
    print("Trying to open directory path: " + fixed_path)
    if os.path.isdir(fixed_path):
        if platform.system() == "Windows":

            cmd = ["explorer", fixed_path]

        elif platform.system() == "Darwin":

            cmd = ["open", "%s" % fixed_path]

        elif platform.system() == "Linux":
            cmd = ["xdg-open", "%s" % fixed_path]

        sp.call(cmd)
    else:
        mc.warning("The following directory doesn't exist: " + fixed_path)


def open_current_file_directory():
    path = get_scene_path()
    if not path:
        mc.warning('No directory to open')
        return
    sp.Popen(['explorer', os.path.normpath(os.path.dirname(path))])


def add_to_rv_session(path):
    return sp.Popen('rvpush -tag playblast merge [{}]'.format(path), shell=True)


def open_with_rv(path):
    return sp.Popen(['rv', path])


def open_with_rv_or_add_to_rv_session(path):
    if is_process_running('rv.exe'):
        add_to_rv_session(path)
    else:
        open_with_rv(path)


def is_process_running(process_name):
    if platform.system() == 'Windows':
        cmd = 'tasklist /FI "IMAGENAME eq {}"'.format(process_name)
    else:
        cmd = 'ps aux | grep -v grep | grep {}'.format(process_name)
    output = sp.getoutput(cmd)
    return process_name in output


def open_latest_pblayblast():
    pblayblast_file = os.path.splitext(get_scene_path())[0] + '.mp4'
    if not os.path.isfile(pblayblast_file):
        return mc.warning('No playblast found!')
    open_with_rv(pblayblast_file)


def open_current_project_root_directory():

    # Let's get the current project directory.
    path = mc.workspace(q=True, rootDirectory=True)

    # Next we need to find out what platform we are running
    open_dir(path)
    return


def open_assets_textures_directory():

    # Let's get the current project directory.
    project_path = mc.workspace(q=True, rootDirectory=True)
    path = project_path + "04_Assets/Textures/"
    open_dir(path)
    return


def open_current_game_export_directory():

    # Works only with prism pipeline
    # Let's get the current directory. We add the / at the end of the path
    # to make sure we get inside of the current directory.
    scene_path = mc.file(query=True, sceneName=True, shortName=False)

    # let's go three parent above in the folder hierarchy
    game_exporter_dir = os.path.abspath(os.path.join(
        scene_path, "../../../..")) + "Export/GameExporter/"
    path = game_exporter_dir
    open_dir(path)
    return


def open_dailies_directory():

    # Let's get the current project directory.
    project_path = mc.workspace(q=True, rootDirectory=True)
    path = project_path+"05_Dailies/"

    # Next we need to find out what platform we are running
    open_dir(path)
    return


def get_current_latest_render_directory():

    scene_path = mc.file(query=True, sceneName=True, shortName=False)
    renders_dir_path = os.path.abspath(os.path.join(
        scene_path, "../../../.."))+"/Rendering/3dRender/"

    if os.path.isdir(renders_dir_path):

        # Get only a list of existing folders inside the Playblasts folder
        renders_dir_list = [
            f for f in os.listdir(renders_dir_path) if os.path.isdir(
                os.path.join(renders_dir_path, f))]

        # Let's list all the existing versions
        # First create an empty list
        version_list = []

        # For each existing folder, let's only look at the v#### part.

        for i in renders_dir_list:
            # Let's divide all the underscore parts
            folder_name = i.split("_")

            # Let's take only the "v#####"" part of the name
            full_version_number = folder_name[0]

            # Let's remove the "v" of the name
            version_number = full_version_number.replace("v", "")

            # Let's add that version to the version list
            version_list.append(version_number)

        # Set the latest playblast version
        latest_version = "v" + max(version_list)

        render_comment = ""

        # Get the associated comment
        for i in renders_dir_list:
            if latest_version in i:
                if "_" in i:
                    folder_name = i.split("_")
                    render_comment = "_" + folder_name[1]
                    print("comment is :" + render_comment)
                else:
                    render_comment = ""

        # Let's set the latest playblast directory available
        latest_render_path = (
            renders_dir_path + latest_version + render_comment + "/")

        # Let's find the folders available and get rid of DS_store
        render_folder_list = mc.getFileList(
            folder=latest_render_path)

        if ".DS_Store" in render_folder_list:
            render_folder_list.remove(".DS_Store")
        render_folder_name = render_folder_list[0]
        render_folder_full_path = latest_render_path + render_folder_name
        fixed_latest_render_path = os.path.normpath(render_folder_full_path)
        path = fixed_latest_render_path

        if os.path.isdir(fixed_latest_render_path):
            path = path
            print("path is =" + path)
            return path
    else:
        mc.warning("Render folder not found, are youin a Prism project ?")


def open_current_render_directory():
    path = get_current_latest_render_directory()
    open_dir(path)