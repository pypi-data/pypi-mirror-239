from distutils.core import setup
setup(
  name = 'immich-face-to-album',
  packages = ['immich_face_to_album'],
  version = '1.0.0',
  license='WTFPL',
  description = 'Tool to import a user\'s face from Immich into an album, mimicking the Google Photos "auto-updating album" feature.',
  author = 'romainrbr',
  author_email = 'contact@romain.tech',
  url = 'https://github.com/romainrbr/immich-face-to-album',
  download_url = 'https://github.com/romainrbr/immich-face-to-album/archive/v_01.tar.gz',
  keywords = ['immich'],
  install_requires=[
          'click',
          'requests'
      ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Programming Language :: Python :: 3.12',
  ],
  entry_points={
        "console_scripts": [
            "immich-face-to-album = immich_face_to_album.__main__:main"
        ]
    }
)


