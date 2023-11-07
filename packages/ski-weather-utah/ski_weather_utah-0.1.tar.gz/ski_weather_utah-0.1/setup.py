from setuptools import setup, find_packages
from setuptools.command.install import install

class CustomInstallCommand(install):
    def run(self):
        # Run the setup script during installation
        import subprocess
        subprocess.run(["python", "setup_script.py"])
        super().run()

setup(
    name="ski_weather_utah",
    version="0.1",
    description="A server-side app that sends daily updates for weather at select Utah ski resorts.",
    author="Alex Calder",
    packages=find_packages(),
    install_requires=[
        "selenium",
        "webdriver-manager",
        "configparser",
    ],
    cmdclass={
        "install": CustomInstallCommand,
    }
)
