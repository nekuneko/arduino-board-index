from setuptools import setup, find_packages
setup(name='updateBoards',
      version='1.0.0',
      description='Programa que actualiza las placas de arduino generando automáticamente el .json',
      url='https://github.com/nekuneko',
      author='NekuNeko',
      author_email='jvramallo@gmail.com',
      license='GNU',
      packages=find_packages(),
      install_requires=[
 #         'gitpython',
      ],
      zip_safe=False)

import os
import sys
import json
import hashlib
import tarfile
from copy import deepcopy
#from git import *


nombrePlataforma: 	str = 'nekuneko-samd'
githubBaseURL:	 	str = 'https://nekuneko.github.io/arduino-board-index/'
nombrePackageJson:	str = 'package_nekuneko_index.json'


# To Do:
	# Necesito el json con las placas para saber cual es la ultima version 
	# Borrar copia de json si hubiera en directorio
	# Descargar  json actual


# Función para crear un fichero comprimido
def make_tarfile(str_nombreArchivoComprimido: str, str_directorio: str):
    with tarfile.open(str_nombreArchivoComprimido + '.tar.bz2', "x:bz2") as tar:
        tar.add(str_directorio, arcname=str_nombreArchivoComprimido)
        tar.close()


# Funcion para incrementar la versión de una release
# Versioning: <major>.<minor>.<release> ->> 1.6.4
	# Increment <major> for non-backwards compatible changes
	# Increment <minor> for new features
	# Increment <revision> for bug fixes.
def incrementVersion(version: str='0.0.0', campo: str='release'):
	campo 		 = str(campo).lower()
	version 	 = str(version)
	list_version = version.split('.') # list = ['0', '0', '0']

	if (campo == 'major'):
		list_version[0] = str(int(list_version[0]) + 1)
	elif (campo == 'minor'):
		list_version[1] = str(int(list_version[1]) + 1)
	elif (campo == 'release'):
		list_version[2] = str(int(list_version[2]) + 1)
	else:
		pass

	version = '.'.join(list_version)
	return str(version)




# Fichero json a cargar:

# package_nekuneko_index.json
# dic_jsonArduino = {
# 	'packages': [ 										# Lista de paquetes, generalmente solo hay uno.
# 		dic_package
# 	]
# }

# dic_package = {
# 	'name' : 		'nekuneko', 						# Nombre paquete = nombre de la empresa
# 	'websiteURL': 	'https://github.com/nekuneko',		# Web de la empresa
# 	'maintainer':	'Neku', 							# Nombre del mantenedor
#  		'email': 		'jvramallo@gmail.com', 			# Email del mantenedor
#  		'help':	{ 										# Ayuda online
#  			'online':	'https://github.com/nekuneko/arduino-board-index' # Wiki del paquete
#  		},
#  		'platforms': [ 									# Lista de plataformas, pueden ser distintas arquitecturas (Placas AVR, Placas SAMD, etc.) o incrementos de versiones de una arquitectura determinada
#  			dic_platform
#  		]
# }

# dic_platform = {
# 	'name': 'NekuNeko SAMD Boards', 					# Nombre del conjunto de placas
#  	'architecture': 'samd', 							# Arquitectura
#  	'archiveFileName': 'nekuneko-samd-1.0.0.zip', 		# Nombre del fichero que contiene una carpeta nombreFichero-version 
#  	'checksum': 'SHA-256:C78532D78360C9889E79BCEE6212DE7AA53F9FA12958FE20A330B086EB12E49E',  	# Hash Sha256 del fichero
#  	'size': '1363968', 									# Tamaño en bytes del fichero
#  	'url': 'https://nekuneko.github.io/arduino-board-index/boards/nekuneko-samd-1.0.0.zip', 	# Localización del fichero
#  	'version': '1.0.0',
#  	'category': 'Contributed', 							# Este campo está reservado, un core de terceros tiene que ponerlo a Contributed
#  	'help': { 											# Ayuda online
# 		'online': 'https://github.com/nekuneko/NekuNeko_Arduino_Boards' 	# Wiki de la plataforma
# 	},

#  	'boards': [ 										# Lista de placas incluidas en el paquete
# 		{'name': 'Stimey SAMD21G18A'},
# 	],
#  	'toolsDependencies': [ 								# Herramientas necesarias para compilación
#  		{'packager': 'arduino', 'name': 'arm-none-eabi-gcc', 'version': '4.8.3-2014q1'},
#   	{'packager': 'arduino', 'name': 'bossac', 			 'version': '1.8.0-48-gb176eee'},
#   	{'packager': 'arduino', 'name': 'openocd', 			 'version': '0.9.0-arduino'},
#   	{'packager': 'arduino', 'name': 'CMSIS', 			 'version': '4.5.0'},
#   	{'packager': 'arduino', 'name': 'CMSIS-Atmel', 		 'version': '1.2.0'}
#   ]
# }

## START MAIN ###
def main ():
	# Variables usadas
	hasher:				hashlib.sha256 = hashlib.sha256()
	lastVersion:  		str  	= "0.0.0"
	lastPlatform: 		dict 	= {}
	statinfo:			os.stat_result 	# clase con atributos: st_mode, st_ino, st_dev, st_nlink, st_uid, is_gid, st_size, st_atime, st_mtime, st_ctime
	version:			str 	= "0.0.0"
	archiveFileName:	str 	= "nekuneko-samd-1.0.0.tar.bz2"
	checksum:			str 	= "SHA-256: abcde"
	size:				int 	= 0
	url:				str 	= "https://"


	# Comprobar que exista el directorio ../NekuNeko_Arduino_Boards
	if (not os.path.isdir('../NekuNeko_Arduino_Boards')):
		print("Error. Su árbol de directorios debe ser así:")
		print("GitHub/")
		print("		arduino-board-index/")
		print("		NekuNeko_Arduino_Boards/")
		sys.exit(1)
		

	# Cargar json en python
	with open (nombrePackageJson, 'r') as json_file:
		dic_jsonArduino = json.load(json_file)
	json_file.close()

	# Obtener última versión de las deficiones de NekuNeko SAMD Boards
	lastVersion  = "0.0.0"
	lastPlatform = {}
	for platform in dic_jsonArduino['packages'][0]['platforms']:
		if (platform['name'] 			== 'NekuNeko SAMD Boards' and
			platform['architecture'] 	== 'samd' and
			platform['version'] 		>  lastVersion):
				lastVersion  = deepcopy(platform['version'])
				lastPlatform = deepcopy(platform)



	# Incrementar la versión según sea <major>, <minor> o <release>, 1.0.0 to 1.0.1
	version = incrementVersion(lastVersion, 'release')

	# Determinar el nuevo nombre de archivo: nekuneko-samd - 1.2.0
	nombrePlataformaVersion: str  = nombrePlataforma + '-' + version
	archiveFileName = nombrePlataformaVersion + '.tar.bz2'

	# Comprimir el archivo de las placas
	print("Comprimiendo boards....")
	make_tarfile(nombrePlataformaVersion, '../NekuNeko_Arduino_Boards')
	print('Hecho')

	# Calcular hash sha256 del archivo
	with open (archiveFileName, 'rb') as zip_file:
		buf = zip_file.read()
		hasher.update(buf)
		checksum = hasher.hexdigest()
	zip_file.close()


	# Calcular tamaño en disco del archivo
	statinfo = os.stat(archiveFileName)
	size = statinfo.st_size

	# Mover archivo a directorio 'boards/'
	os.rename(archiveFileName, 'boards/'+archiveFileName)

	# Nuevo platform con campos actualizados
	lastPlatform['version'] 		= str(version)
	lastPlatform['archiveFileName'] = str(archiveFileName)
	lastPlatform['checksum'] 		= str('SHA-256:' + checksum)
	lastPlatform['size'] 			= str(size)
	lastPlatform['url']	  	= str(githubBaseURL + 'boards/' + archiveFileName)

	# Añadir plataforma a fichero json
	dic_jsonArduino['packages'][0]['platforms'].append(lastPlatform) 

	# Actualizar json
	with open (nombrePackageJson, 'w') as json_file:
		json_file.dumps(dic_jsonArduino)
	json_file.close()

	





# Calcular hash del fichero

