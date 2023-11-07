from setuptools import setup, find_packages

setup(
    name='iwort',
    version='1.0',
    packages=find_packages(),
    author='Ankur Napa',
    author_email='napaankur@gmail.com',
    description='An intelligent Wort is a sophisticated Python library designed for advanced text processing and linguistic analysis, leveraging state-of-the-art machine learning techniques.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/Iwort',  # Replace with the actual URL to your package repository
    install_requires=[
        # Add your package dependencies here
        # 'numpy',
        # 'pandas',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',  # Update the license as needed
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    keywords='machine learning, text analysis, linguistics',  # Add keywords related to your package
)
