import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from os import getcwd
from src.utils.utils import get_classes


dataset_folder  = 'dataset/wheel'
classes_path    = f'{dataset_folder}/cls_classes.txt'
sets            = ["train", "val"]
classes, _      = get_classes(classes_path)
if __name__ == "__main__":
    for se in sets:
        list_file = open(os.path.join(dataset_folder,'cls_' + se + '.txt'), 'w')
        datasets_path_t = os.path.join(dataset_folder, se)
        types_name    = os.listdir(datasets_path_t)
        types_name    = [item for item in types_name if not item.endswith('txt')]
        for type_name in types_name:
            if type_name not in classes:
                continue
            cls_id = classes.index(type_name)
            photos_path = os.path.join(datasets_path_t, type_name)
            photos_name = os.listdir(photos_path)
            for photo_name in photos_name:
                _, postfix = os.path.splitext(photo_name)
                if postfix not in ['.jpg', '.png', '.jpeg']:
                    continue
                list_file.write(str(cls_id) + ";" + '%s'%(os.path.join(photos_path, photo_name).replace('\\', '/')))
                list_file.write('\n')
        list_file.close()

