from setuptools import find_packages, setup

setup(
    name="marvlcli",
    version='0.0.6',
    py_modules= ['marvlcli','info','ssh','list', 'create', 'delete'],
    packages=find_packages(),
    install_requires=[
        'click',
        'pyyaml',
        'python-novaclient',
        'python-cinderclient',
        'python-neutronclient',
        'python-openstackclient',
        'ws4py',
        
    ],
    entry_points='''
    [console_scripts]
    marvl=marvlcli:marvlcli
    
    
    '''
    
)

