import codecs
import os
import sys

import setuptools

"""
打包的用的setup必须引入，
"""

def read(fname):
    """
    定义一个read方法，用来读取目录下的长描述
    我们一般是将README文件中的内容读取出来作为长描述，这个会在PyPI中你这个包的页面上展现出来，
    你也可以不用这个方法，自己手动写内容即可，
    PyPI上支持.rst格式的文件。暂不支持.md格式的文件，<BR>.rst文件PyPI会自动把它转为HTML形式显示在你包的信息页面上。
    """
    return codecs.open(os.path.join(os.path.dirname(__file__), fname), encoding='utf-8').read()

setuptools.setup(
  name="mpfsim",
  version="1.0.0",
  author="He Ma",
  author_email="mahepetroleum@163.com",
  description="Multiphase Simulation",
  long_description=read("README.md"),
  long_description_content_type="text/markdown",
  url="https://gitee.com/mmmahhhhe/mpfsim",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
  keywords="multiphase simulation, pipesim",

)