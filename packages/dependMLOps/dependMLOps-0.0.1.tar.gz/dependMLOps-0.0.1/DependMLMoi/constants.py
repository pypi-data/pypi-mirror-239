from .arg_parser import parse_args

#Default
NAME = None
TYPE = "LLM"
AUTO_INSTALL = False
REQUIRED_DOTENV_VERSION = "1.0.0"
LEVEL = "DEBUG"
DEBUG = False
LOGGING = True
QUIET = False
REQUIREMENTS_PATH = "./requirements.txt"
LOGS_DIR = "./utils/donmor.log"

args = parse_args()



if args:
    NAME = args.name
    TYPE = args.type
    AUTO_INSTALL = args.auto
    DEBUG = args.debug
    LOGGING = args.logging
    QUIET = args.quiet
    CUSTOM = args.custom
    LEVEL = args.level




