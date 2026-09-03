from setuptools import find_packages, setup

package_name = 'eurobot_vision'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='kamar',
    maintainer_email='chakrounkamar22@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            "test_aruco_node = eurobot_vision.aruco_detection_test:main",
            "camera_node = eurobot_vision.camera_publisher:main",
            "aruco_node = eurobot_vision.aruco_node_detection:main"
        ],
    },
)
