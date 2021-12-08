import logging
import time

from dataset import create_dataset_txts
from window import Application
from pathlib import Path


if __name__ == "__main__":
    print('PROGRAM STARTING...\n')
    
    """Start time"""
    start_time = time.perf_counter()

    """Logging"""
    level = logging.DEBUG
    fmt = '[%(levelname)s] %(asctime)s --> %(message)s'
    logging.basicConfig(level=level, format=fmt)
    class_names = ['paper', 'glass', 'metal', 'plastic']

    """Paths"""
    #src = Path("D:\\asztal\suli\szakdoga\DATASET\waste\\0_GYHG\\budder")
    src = Path("D:\\asztal\suli\szakdoga\DATASET\waste\\final_dataset")
    #src = Path("D:\\asztal\suli\szakdoga\DATASET\waste\\0_GYHG\All_orginal_images\\2-test\\resized_tested")
    dest = Path("D:\\asztal\programing\VS_CODE\BBoxViewer")
    #data = load_imgs_and_labels(src)

    """Runs"""
    #create_dataset_txts(src, dest, [60, 30, 10])

    # app = Application(1280, 900)
    # app.mainloop()

    """End of running time"""
    end_time = time.perf_counter()
    print(f"\n---- Running time: {end_time - start_time} s ----\n")





    # data = load_labels_to_list(src)
    # df = pd.DataFrame(data=data)
    # df_head = pd.DataFrame(data={'File': ['a'], 'Data': ['b']})
    # print(df)
    # df[['Class', 'x', 'y', 'w', 'h']] = df[1].str.split(' ', expand=True)
    # df = df.drop(columns=1)
    # df = df.rename(columns={0:"FILE"})
    # new_df = df[1].str.split(' ', expand=True)
    # #print(df)
    # new_df = new_df.rename(columns={0:"Class", 1:"x", 2:"y", 3:"h", 4:"w"})
    # new_df = pd.concat([new_df, df])

    # print(new_df.head(3))

    # print(df.loc[df['Class'] == '1'])
    # print(df['Class'].value_counts()).sort()
