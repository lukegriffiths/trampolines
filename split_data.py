import shutil
import os
from sklearn import model_selection

def copy_files(files, type="train"):
    for f in files:
        try:
            shutil.copyfile(DATAPATH + f, f'./data/labels/{type}/{f}')
        except:
            print(f"Could not copy {f}")
        image_f = f[:-4] + '.jpg'

        try:
            shutil.copyfile(DATAPATH + image_f, f'./data/images/{type}/{image_f}')
        except:
            print(f"Could not copy {f}")

if __name__ == '__main__':
   
    DATAPATH = "images/data_3-2022-01-22/"

    text_files = [f for f in os.listdir(DATAPATH) if f.endswith('.txt')]

    train, test = model_selection.train_test_split(text_files, test_size=0.1, random_state=42, shuffle=True)

    print(f"{len(train)} images for training.")
    print(f"{len(test)} images for testing.")

    copy_files(train, type='train')
    copy_files(test, type='validation')
