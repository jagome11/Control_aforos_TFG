import os
import glob
import xml.etree.ElementTree as ET

def replace_name(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    # Itera sobre todos los elementos <object>
    for obj in root.findall('object'):
        # Encuentra el elemento <name> dentro de <object>
        name = obj.find('name')
        if name.text == 'h' or name.text == '0' or name.text == 'people' or name.text == 'person' or name.text == 'Heads' or name.text == 'P':
            name.text = 'person'
        else:
            root.remove(obj)
    tree.write(xml_file)

def process_xml_files_in_folder(folder_path):
    print(folder_path)
    for xml_file in glob.glob(folder_path + '/*.xml'):
        replace_name(xml_file)

def main():
    for folder in ['train','valid', 'test']:
        folder_path = os.path.join(os.getcwd(), ('images/' + folder))
        process_xml_files_in_folder(folder_path)
    print('Successfully done.')

main()