from setuptools import setup

setup(
    name="BJA_plot_helpers",
    version="0.1",
    description="Convenience functions for plotting with matplotlib and seaborn",
    packages=["BJA_plot_helpers"],
    install_requires=['pandas', 'numpy', 'matplotlib>=3.5.0', 'seaborn>=0.10.0'],
)