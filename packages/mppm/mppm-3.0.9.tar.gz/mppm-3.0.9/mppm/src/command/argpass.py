import sys
import argparse
from src.common.const import *


class DefaultHelpParser(argparse.ArgumentParser):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.version = None

	def error(self, message):
		print('error: %s\n' % message, file=sys.stderr)
		self.print_help()
		sys.exit(2)

	def add_version_argument(self, version):
		self.version = version
		self.add_argument(f'-{ARG_VERSION_SHORT}', f'--{ARG_VERSION}', action='version',
						  version=f'{APP_NAME} {version}')


class Parser:
	def __init__(self):
		self.parser = DefaultHelpParser(
			description=f'{APP_NAME} Manage pip sources and dependent packages',
			usage=f"{APP_NAME}  <sub-commands>  [<args>] \n",
			allow_abbrev=False)
		self.parser.add_version_argument(f"{APP_VERSION_MAJOR}.{APP_VERSION_MINOR}")
		self.subparser = self.parser.add_subparsers(dest='sub_cmd')
		self._add_all_parsers()

	def _add_all_parsers(self):
		self._add_download_module()
		self._add_uninstall_module()
		self._add_rewrite_module()

	def parse(self):
		args = self.parser.parse_args()
		return args

	def _add_rewrite_module(self):
		subparse = self.subparser.add_parser(SUB_CMD_REWRITE, help="rewrite pip configuration", allow_abbrev=False)
		subparse.add_argument(f'-{ARG_CONFIG_REWRITE_FORCE_SHORT}', f'--{ARG_CONFIG_REWRITE_FORCE}',
							  action='store_true', default=False,
							  required=False, help="force rewrite pip configuration")

	def _add_download_module(self):
		subparser = self.subparser.add_parser(SUB_CMD_DOWNLOAD, help="download modules", allow_abbrev=False)
		group = subparser.add_mutually_exclusive_group(required=True)
		group.add_argument(f'-{ARG_DOWNLOAD_MODULE_SHORT}', f'--{ARG_DOWNLOAD_MODULE}',
						   help="download specified modules and dependencies")
		group.add_argument(f'-{ARG_DOWNLOAD_REQUIREMENT_SHORT}', f'--{ARG_DOWNLOAD_REQUIREMENT}',
						   help="download the modules and dependencies specified in the file. like requirements.txt")
		subparser.add_argument(f'-{ARG_DOWNLOAD_SAVE_PATH_SHORT}', f'--{ARG_DOWNLOAD_SAVE_PATH}',
							   default="./", required=False, help="download module save path")
		subparser.add_argument(f'-{ARG_DOWNLOAD_REWRITE_PIP_CONFIG_SHORT}', f'--{ARG_DOWNLOAD_REWRITE_PIP_CONFIG}',
							   action='store_true', default=False, required=False, help="rewrite the pip configuration")

	def _add_uninstall_module(self):
		subparser = self.subparser.add_parser(SUB_CMD_UNINSTALL, help="uninstall modules", allow_abbrev=False)
		group = subparser.add_mutually_exclusive_group(required=True)
		group.add_argument(f'-{ARG_UNINSTALL_MODULE_SHORT}', f'--{ARG_UNINSTALL_MODULE}',
						   help="uninstall specified modules and dependencies")
		group.add_argument(f'-{ARG_UNINSTALL_REQUIREMENT_SHORT}', f'--{ARG_UNINSTALL_REQUIREMENT}',
						   help="uninstall the modules and dependencies specified in the file. like requirements.txt")
		subparser.add_argument(f'-{ARG_UNINSTALL_FORCE_SHORT}', f'--{ARG_UNINSTALL_FORCE}',
							   action='store_true', default=False, required=False, help="interactive")
