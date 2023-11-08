from src.common.utility import *
from src.config.pip_conf import *
import os


class DownloadCmd():
    def __init__(self, args):
        self.args = args

    def exec(self, pip_path):
        if self.args.yes:        
            verification_pypi_url()

        if self.args.requirement is not None:
          base_output = f"{self.args.output}/{ARG_DOWNLOAD_REQUIREMENT}"

        if self.args.module is not None:
            base_output = f"{self.args.output}/{self.args.module}"
        
        create_dir(base_output)

        if self.args.module:
            download_pip_pkg_cmd = "{} download {} -d {}".format(pip_path, self.args.module, base_output)
        else:
            download_pip_pkg_cmd = "{} download -r {} -d {}".format(pip_path, self.args.requirement,
                                                                    base_output)
        
        cmd_result = exec_cmd(download_pip_pkg_cmd)
        if cmd_result is None or ignore_errors[self.args.sub_cmd] in cmd_result:
            print_colored(f"the module and dependencies have been downloaded. Please check the {base_output} path", "green")
        else:
            print_colored(cmd_result, "red")

