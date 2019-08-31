import os
import zipfile

# ====================================================================================
# XJUtils функции использующиеся во всех классах
# ====================================================================================


class XJUtils:
	# ====================================================================================
	# проверяет наличие элемента в массиве
	# ====================================================================================
	@staticmethod
	def is_array_element(key, array):
		for tmp in array:
			if tmp == key:
				return True
		return False

	# ====================================================================================
	# проверяет наличие элемента в массиве
	# ====================================================================================
	@staticmethod
	def read_from_file(path):
		file = open(path, 'rb')
		result = file.read()
		file.close()
		return result

	# ====================================================================================
	# записывает данные в файл
	# ====================================================================================
	@staticmethod
	def write_data_to_file(data, path):
		file = open(path, 'w')
		file.write(data)
		file.close()

	# ====================================================================================
	# расспаковывает зипку в дирректорию с именим зипки
	# ====================================================================================
	@staticmethod
	def unpack_zip(path):
		file = zipfile.ZipFile(path)
		file.extractall(path.replace(".zip", "") + "\\")
		file.close()
		os.remove(path)

	# ====================================================================================
	# создает ZIP файл со всем содержимым директории
	# ====================================================================================
	@staticmethod
	def pack_to_zip(_input, _output):
		file_zip = zipfile.ZipFile(_output, 'w')

		for folder, sub, files in os.walk(_input):
			for file in files:
				file_zip.write(
					os.path.join(folder, file),
					os.path.relpath(os.path.join(folder, file), _input),
					compress_type=zipfile.ZIP_DEFLATED
				)
		
		file_zip.close()
