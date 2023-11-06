from DependMLMoi.depend_ml import run_setup
from DependMLMoi.arg_parser import parse_args
from dependencies import package_handler
from ..DependMLMoi.dependencies.PackageHandler import main_libraries

def main():
    args = parse_args()
    main_libraries()
    run_setup(auto_install=args.auto, args=args)

if __name__ == "__main__":
    main()
    