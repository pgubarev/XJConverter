import json
import os
import shutil

from lxml import etree
from lxml import objectify

from XJOptions import XJOptions
from XJUtils import XJUtils
from XJLogger import XJLogger 


class XJConverter:
    def __init__(self, _options=XJOptions()):

        self.__xmlDataList = []
        self.__arrays_key = []
        self.__options = _options
        self.__error_message = None

        if self.__options.enabledLogs:
            XJLogger.start_write_logs(self.__options.clearLogs)

    def set_options(self, _options):
        self.__options = _options

# ====================================================================================
# конвертирует файлы из XML в JSON или заменяет все XML на JSON внутри ZIP
# ====================================================================================
    def convert_files(self, files):
        try:
            self.__error_message = None

            for file in files:
                self.__convert_file(file)

            return True
        except FileNotFoundError as file_error:

            if " " in file_error.filename:
                self.__error_message = "Space symbol are not allowed."
            else:
                self.__error_message = file_error.args[1] + ": " + file_error.filename

            if self.__options.enabledLogs:
                XJLogger.log('something went wrong: ' + self.__error_message)
        except PermissionError as access_errror:

            self.__error_message = "Access error: " + access_errror.filename

            if self.__options.enabledLogs:
                XJLogger.log('something went wrong: ' + self.__error_message)
        except Exception:
            self.__error_message = "Unexpected error"

            if self.__options.enabledLogs:
                XJLogger.log('something went wrong: ' + self.__error_message)
        finally:
            return self.__error_message is None

# ====================================================================================
# конвертирует все XML в JSON внутри директории и zip архивов
# ====================================================================================
    def convert_directory(self, path):
        try:
            self.__error_message = None

            self.__parse_xml_in_dir(path)
            self.__parse_zip_in_dir(path)
        except FileNotFoundError as file_error:

            if " " in file_error.filename:
                self.__error_message = "Space symbol are not allowed."
            else:
                self.__error_message = file_error.args[1] + ": " + file_error.filename

            if self.__options.enabledLogs:
                XJLogger.log('something went wrong: ' + self.__error_message)
        except PermissionError as access_errror:

            self.__error_message = "Access error: " + access_errror.filename

            if self.__options.enabledLogs:
                XJLogger.log('something went wrong: ' + self.__error_message)
        except Exception:
            self.__error_message = "Unexpected error"

            if self.__options.enabledLogs:
                XJLogger.log('something went wrong: ' + self.__error_message)
        finally:
            return self.__error_message is None

# ====================================================================================
# конвертирует все XML в JSON внутри директории и zip архивов
# ====================================================================================
    def get_error_message(self):
        return self.__error_message

# ====================================================================================
# конвертирует файл из XML в JSON или заменяет все XML на JSON внутри ZIP
# ====================================================================================
    def __convert_file(self, path):
        if ".xml" in path and self.__options.parseXML:
            self.__parse_single_xml(path)
        elif ".zip" in path and self.__options.parseZip:
            self.__parse_single_zip(path)
        elif self.__options.enabledLogs:
            XJLogger.log("skip file or directory: " + path)

# ====================================================================================
# проверяет наличие списков в файле
# ====================================================================================
    def __check_arrays(self):

        def check(data):
            if len(vars(data)) > 0:
                for key in vars(data):
                    if key != 'comment':
                        if len(data[key]) > 1 and not XJUtils.is_array_element(key, self.__arrays_key):
                            self.__arrays_key.append(key)
                            if self.__options.enabledLogs:
                                XJLogger.log("using tag as array: " + key)
                        check(data[key])
        
        for xmlData in self.__xmlDataList:
            check(xmlData['data'])

# ====================================================================================
# переводит XML представление в объект
# ====================================================================================
    def __parse(self, data):
        result = {}

        for attr in data.attrib:    
            result[attr] = data.get(attr)
        
        if len(vars(data)) == 0:
            if data.text is not None or self.__options.emptyValue:
                if self.__options.emptyValue or len(data.attrib) > 0:
                    result['value'] = data.text
                else:
                    result = data.text
        else:
            for key in vars(data):
                if key != 'comment':
                    if not self.__options.asArray and len(data[key]) == 1 and not XJUtils.is_array_element(key, self.__arrays_key):
                        result[key] = self.__parse(data[key])
                    else:
                        result[key] = []
                        for elem in data[key]:
                            result[key].append(self.__parse(elem))
        
        if self.__options.emptyValue and 'value' not in result:
            result['value'] = None
        
        return result

# ====================================================================================
# получает XML представление данных из файла
# ====================================================================================
    def __parse_xml(self, path):
        raw_xml = XJUtils.read_from_file(path)

        parser = etree.XMLParser(recover=True, remove_comments=True, remove_pis=True)
        xml_str = etree.tostring(etree.XML(raw_xml, parser))
        xml_data = objectify.fromstring(xml_str)

        data = {'data': xml_data, 'path': path}

        self.__xmlDataList.append(data)

# ====================================================================================
# рекурсивно просматривает директорию
# ====================================================================================
    def __walk(self, directory):
        try:
            for file_name in os.listdir(directory):
                if "." not in file_name:
                    self.__walk(directory + file_name + "\\")
                elif ".xml" in file_name: 
                    self.__parse_xml(directory + file_name)
        except Exception:
            print("path: " + directory + " is not correct directory")

# ====================================================================================
# перевести все *.xml в *.json
# ====================================================================================
    def __parse_xml_in_dir(self, directory):

        if self.__options.enabledLogs:
            XJLogger.log("convert files in directory: " + directory)

        self.__walk(directory)
        self.__check_arrays()

        # for xmlData in __xmlDataList:
        while len(self.__xmlDataList):
            xml_data = self.__xmlDataList.pop()
            to_json = self.__parse(xml_data['data'])
            XJUtils.write_data_to_file(json.dumps({'data': to_json}), xml_data['path'].replace('.xml', '.json'))
            if self.__options.removeXML:
                os.remove(xml_data['path'])

# ====================================================================================
# парсинг всех *.zip в директории
# ====================================================================================
    def __parse_zip_in_dir(self, directory):
        for file_name in os.listdir(directory):
            if "." not in file_name:
                self.__parse_zip_in_dir(directory + file_name + "\\")
            elif ".zip" in file_name:
                self.__parse_single_zip(directory + file_name)

# ====================================================================================
# парсинг zip файла
# ====================================================================================
    def __parse_single_zip(self, path):
        
        if self.__options.enabledLogs:
            XJLogger.log("convert file: " + path)
        
        temp_dir = path.replace(".zip", "") + '\\'
        XJUtils.unpack_zip(path)
        self.__parse_xml_in_dir(temp_dir)
        XJUtils.pack_to_zip(temp_dir, path)
        shutil.rmtree(temp_dir, ignore_errors=True)

# ====================================================================================
# парсинг xml файла
# ====================================================================================
    def __parse_single_xml(self, path):

        if self.__options.enabledLogs:
            XJLogger.log("convert file: " + path)

        self.__parse_xml(path)
        self.__check_arrays()

        xml_data = self.__xmlDataList.pop()
        to_json = self.__parse(xml_data['data'])
        XJUtils.write_data_to_file(json.dumps({'data': to_json}), xml_data['path'].replace('.xml', '.json'))

        if self.__options.removeXML:
            os.remove(xml_data['path'])
