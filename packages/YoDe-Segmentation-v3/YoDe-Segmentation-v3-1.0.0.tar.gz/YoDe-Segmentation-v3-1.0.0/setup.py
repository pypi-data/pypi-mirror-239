from setuptools import setup, find_packages

setup(
    name='YoDe-Segmentation-v3',
    version='1.0.0',
    author='onechorm',
    author_email='zconechorm@163.com',
    description='test',
    packages=find_packages(),
    install_requires=[
        'matplotlib',
		'numpy==1.25.2',
		'opencv_python',
		'pandas',
		'Pillow==10.0.0',
		'PyYAML==6.0.1',
		'scipy',
		'seaborn==0.11.2',
		'tqdm==4.64.1',
		'python-office'
    ],
)