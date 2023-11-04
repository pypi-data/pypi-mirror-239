from rataGUI import launch_config, add_file_logger
import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    "--start-menu",
    help=(
        "Show start menu to reconfigure launch config."
    ),
    action="store_const",
    const=True,
    default=False,
)

# parser.add_argument(
#     "--reset",
#     help=(
#         "Reset session settings back to defaults."
#     ),
#     action="store_const",
#     const=True,
#     default=False,
# )

args = parser.parse_args()

if args.start_menu:
    launch_config["Don't show again"] = False

import os
import darkdetect
from PyQt6.QtWidgets import QApplication

from rataGUI.interface.main_window import MainWindow
from rataGUI.interface.start_menu import StartMenu

from rataGUI.cameras.BaseCamera import BaseCamera
from rataGUI.plugins.base_plugin import BasePlugin
from rataGUI.triggers.base_trigger import BaseTrigger

import logging
logger = logging.getLogger(__package__)


def main():
    """Starts new instance of RataGUI"""
    logger.info("__________Starting RataGUI__________")
    QApplication.setStyle('Fusion')
    app = QApplication([])

    if not launch_config.get("Don't show again") or len(launch_config) < 3:    # Load start menu
        start_menu = StartMenu(camera_modules=BaseCamera.modules.values(), plugin_modules=BasePlugin.modules.values(), 
                                trigger_modules=BaseTrigger.modules.values())
        start_menu.show()
        start_menu.exec()
    else:
        logger.info("Using saved launch settings. Run \"rataGUI --start-menu\" to reconfigure.")
        logger.info(f"Saving all session data to {launch_config['Save Directory']}")
        os.makedirs(launch_config["Save Directory"], exist_ok=True)
    
    try:
        camera_modules = [BaseCamera.modules[module] for module in launch_config["Enabled Camera Modules"]]
        plugin_modules = [BasePlugin.modules[module] for module in launch_config["Enabled Plugin Modules"]]
        trigger_modules = [BaseTrigger.modules[module] for module in launch_config["Enabled Trigger Modules"]]
        session_settings = launch_config["Session Settings"]
        add_file_logger(os.path.join(launch_config["Save Directory"], "logs"))
    except:
        logger.error("Unable to launch RataGUI due to incomplete launch_config")
        return

    main_window = MainWindow(camera_models=camera_modules, plugins=plugin_modules, trigger_types=trigger_modules,
                                dark_mode=darkdetect.isDark(), restore_dir=session_settings)
    main_window.show()
    app.exit(app.exec())
    logger.info("RataGUI successfully exited")

if __name__ == "__main__":
    main()