import sys
import setuptools
from setuptools import find_packages, setup
from numpy.distutils.core import setup
from numpy.distutils.misc_util import Configuration
from os.path import join, dirname, realpath

str_version = '0.0.38'



def configuration(parent_package='', top_path=''):
    # this will automatically build the scattering extensions, using the
    # setup.py files located in their subdirectories
    config = Configuration(None, parent_package, top_path)

    pkglist = setuptools.find_packages()
    for i in pkglist:
        config.add_subpackage(i)
    config.add_data_files(join('mtutils', 'assets', '*.json'))
    config.add_data_files(join('mtutils', 'assets', '*.jpg'))

    return config


if __name__ == '__main__':
    setup(configuration=configuration,
          name='adtcls',
          version=str_version,
          description='ADT classification algorithm package',
          author='phw',
          author_email='haoweipu@163.com',
          requires= ['numpy','matplotlib'], # 定义依赖哪些模块
          packages=find_packages(),  # 系统自动从当前目录开始找包
          # 如果有的文件不用打包，则只能指定需要打包的文件
          #packages=['代码1','代码2','__init__']  #指定目录中需要打包的py文件，注意不要.py后缀
          license="apache 3.0"
          )
