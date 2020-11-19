from multiprocessing.pool import ThreadPool
import json
import requests
import os
import io
import re
from tqdm import tqdm
from functools import partial

#def index_labeler(index):
#    if index < 10:
#        prefix = "000" + str(index)
#    elif index < 100:
#        prefix = "00" + str(index)
#    elif index < 1000:
#        prefix = "0" + str(index)
#    else:
#        prefix = str(index)
#
#    return prefix

def get_image(url, name):
    img_data = requests.get(url).content
    with open(os.path.join(output_path, name), 'wb') as handler:
        handler.write(img_data)


def extract_url_and_target_path(file):
    """
    Returns a list of urls by extracting the image urls from JSON data files
    """
    file_name = file.replace(".json", "")
    year = re.search(r"(?<=_)\d+(?=_)", file_name).group(0)
    month = re.search(r"(?<=_)\d+$", file_name).group(0)

    data_name = file_name.replace("_" + year + "_" + month, "")

    with open(os.path.join('data', file)) as f:
        data = json.load(f)

    subfolder_path  = os.path.join(data_name, os.path.join(year,month))
    output_path = os.path.join(output_dir, subfolder_path)

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    urls = []

    for news_item in data:
        for image_url in news_item['images']:
            urls.append(image_url)

    return urls, output_path

def image_downloader(img_url: str, output_dir: str):
    """
    Input:
    img_url str (Image url)
    output_dir  str (output directory path)
    Tries to download the image url and use name provided in headers. Else it randomly picks a name
    """
    res = requests.get(img_url, stream=True)
    count = 1
    while res.status_code != 200 and count <= 5:
        res = requests.get(img_url, stream=True)
        print(f'Retry: {count} {img_url}')
        count += 1
    # checking the type for image
    if 'image' not in res.headers.get("content-type", ''):
        print('ERROR: URL doesnot appear to be an image')
        return False
    # Trying to red image name from response headers
    try:
        image_name = str(img_url[(img_url.rfind('/')) + 1:])
        if '?' in image_name:
            image_name = image_name[:image_name.find('?')]
    except:
        image_name = str(random.randint(11111, 99999))+'.jpg'

    img_data = res.content
    with open(os.path.join(output_dir, image_name), 'wb') as handler:
        handler.write(img_data)



def save_image_from_url(process: int, images_url: list, output_dir: str):
    """
    Inputs:
        process: (int) number of process to run
        images_url:(list) list of images url
    """
    pool = ThreadPool(process)
    params = partial(image_downloader, output_dir = output_dir)
    for _ in tqdm(pool.imap(params, images_url), total = len(images_url)):
        pass
    pool.close()
    pool.join()

if __name__ == '__main__':
    data_files = os.listdir('data')
    output_dir = 'images'

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file_counter = 0
    for file in data_files:
        file_counter += 1
        print("Processing file:", file, "\t\t", file_counter, "out of", len(data_files) )
        all_image_urls, file_dir = extract_url_and_target_path(file)
        save_image_from_url(10, all_image_urls, file_dir)
