from setuptools import setup, find_packages

setup(
    name='dicom_to_jpeg_converter',
    version='0.1.0',
    author='Vasantharan K',
    author_email='vasantharank.learn@gmail.com',
    description='Convert DICOM files to JPEG format using Python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/KUMARANVASANTH/dicom_to_jpeg_converter',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'pydicom',
        'Pillow',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    entry_points={
        'console_scripts': [
            'dicom_to_jpeg_converter=dicom_to_jpeg_converter.converter:main',
        ],
    },
)
