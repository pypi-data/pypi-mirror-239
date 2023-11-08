from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="py3status-fbox",
    version="0.1.2",
    description="Python module to monitor your freebox in py3status bar",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/patzy/py3status-fbox",
    author="patzy",
    classifiers=[
        "Environment :: X11 Applications",
        "Intended Audience :: End Users/Desktop",
        "Operating System :: POSIX :: Linux",
        "Topic :: Desktop Environment :: Window Managers",
        "Topic :: System :: Monitoring",
    ],
    keywords=["freebox", "monitor", "status", "i3", "py3status"],
    packages=find_packages(where="src"),
    python_requires=">=3.7, <4",
    install_requires=["requests>=2.31",
                      "py3status>=3.54"],
    entry_points={
        "py3status": ["module = fbox"],
    },
)
