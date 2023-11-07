import setuptools

setuptools.setup(
    name="placo",
    version="0.1.4",
    author="Rhoban team",
    author_email="team@rhoban.com",
    description="PlaCo: Planing and Control for Robots",
    long_description="",
    long_description_content_type="",
    url="https://github.com/rhoban/placo/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    keywords="robot robotics kinematics dynamics urdf pinocchio",
    install_requires=[
        "meshcat", "numpy", "pin"
    ],
    packages=["placo", "placo_utils"],
    include_package_data=True,
    python_requires='>=3.6',
)
