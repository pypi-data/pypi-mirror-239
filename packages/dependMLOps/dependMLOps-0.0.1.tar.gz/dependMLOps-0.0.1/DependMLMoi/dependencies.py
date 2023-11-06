import os
import sys
import subprocess
import pkg_resources
import logging
from DependMLMoi.constants import REQUIREMENTS_PATH

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class PackageHandler:
    @staticmethod
    def upgrade_pip():
        try:
            logging.info("Upgrading pip...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
        except subprocess.CalledProcessError as e:
            logging.error("Failed to upgrade pip.")
            raise RuntimeError("Pip upgrade failed.") from e

    @staticmethod
    def check_requirements_file():
        if not os.path.isfile(REQUIREMENTS_PATH):
            logging.error(f"The required {REQUIREMENTS_PATH} file is missing.")
            raise FileNotFoundError(f"Requirements file {REQUIREMENTS_PATH} is missing.")
        with open(REQUIREMENTS_PATH, 'r') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]

    @staticmethod
    def check_packages(required_packages):
        missing_packages = []
        for requirement in required_packages:
            try:
                pkg_resources.require(requirement)
            except pkg_resources.DistributionNotFound:
                missing_packages.append(requirement)
            except pkg_resources.VersionConflict as e:
                installed_version = pkg_resources.get_distribution(requirement.split('==')[0]).version
                missing_packages.append(f"{requirement} (Installed: {installed_version})")
        return missing_packages

    @staticmethod
    def install_packages(requirements_path):
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', requirements_path])
        except subprocess.CalledProcessError as e:
            logging.error("Failed to install required packages.")
            raise RuntimeError("Package installation failed.") from e

def main_libraries():
    package_handler = PackageHandler()
    try:
        package_handler.upgrade_pip()
    except Exception as e:
        logging.error(e)
        sys.exit(1)

    try:
        required_packages = package_handler.check_requirements_file()
        missing_packages = package_handler.check_packages(required_packages)
        if missing_packages:
            logging.info("Missing packages detected.")
            for package in missing_packages:
                logging.info(f" - {package}")
            answer = input("Would you like to automatically install the missing packages? (y/n): ").strip().lower()
            if answer == 'y':
                package_handler.install_packages(REQUIREMENTS_PATH)
                logging.info("All missing packages were successfully installed.")
            else:
                logging.info("Please install the missing packages manually.")
                sys.exit(1)
    except Exception as e:
        logging.error(e)
        sys.exit(1)

    # Safe to import after ensuring all packages are installed
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv())

if __name__ == "__main__":
    main_libraries()



