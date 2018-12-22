import argparse
import json
from multiprocessing import Manager
from multiprocessing.pool import ThreadPool

import PIL.Image as Image
import imagehash
import requests


def get_image(url):
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raw.decode_content = True
        return 0, Image.open(response.raw)
    except Exception as a:
        return 1, a


def get_hashes(image):
    return imagehash.dhash(image, 32), imagehash.phash(image, 32), imagehash.whash(image, 32)


def classify_image(url):
    error, image = get_image(url)
    if error != -1:
        if image.mode == 'P':
            dhash, phash, whash = get_hashes(image.convert('RGBA'))
        else:
            dhash, phash, whash = get_hashes(image)
        return (dhash, phash, whash), None, image
    else:
        print(image)


def worker(input):
    name, link, lock, image_dir = input
    try:
        response, image = get_image(link)
        if response == 1:
            return name, 1, str(image), None, None, None, None,None,None
        else:
            lock.acquire()
            if image.mode == 'P':
                dhash, phash, whash = get_hashes(image.convert('RGBA'))
            else:
                dhash, phash, whash = get_hashes(image)
            lock.release()
            if image.format == "JPEG" or ((image.format == "MPO" or image.format == None or image.format == "BMP") and (
                    image.mode == 'RGB' or image.mode == 'L')):
                if image.format != "JPEG" or image.format != "MPO":
                    image.save(image_dir + str(name) + ".jpg", "JPEG", optimize=True,
                               progressive=True)
                else:
                    image.save(image_dir + str(name) + ".jpg", "JPEG", quality="keep", optimize=True,
                               progressive=True, subsampling="keep", icc_profile=image.info.get('icc_profile'))
            elif image.format == "PNG" or (
                    image.format == None and (image.mode == 'RGBA' or image.mode == 'LA')):
                image.save(image_dir + str(name) + ".png", "PNG", optimize=True,
                           icc_profile=image.info.get('icc_profile'))
            elif image.format == "GIF" or (image.format == None and image.mode == 'P'):
                image.save(image_dir + str(name) + ".gif", "GIF", save_all=True, include_color_table=True,
                           optimze=True)
            else:
                image.convert("RGBA")
                image.save(image_dir + str(name) + ".png", "PNG", optimize=True,
                           icc_profile=image.info.get('icc_profile'))
            width, height = image.size
            return name, 0,None, width, height, image.mode, dhash, phash, whash

    except Exception as e:

        return name, 1, str(e), None, None, None, None,None,None

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Test")
    parser.add_argument("job_id", help="json which to take the links from", type=str)
    parser.add_argument("data", help="json which to take the links from", type=str)
    parser.add_argument("dir", help="", type=str, default="")
    args = parser.parse_args()
    print(args.data)
    link_list = json.loads(args.data)
    m = Manager()
    lock = m.Lock()
    amount_threads = 10
    a = open(args.dir + args.job_id + ".json", "r")
    a.close()
    if len(link_list)<amount_threads:
        pool=ThreadPool(amount_threads)
    else:
        pool=ThreadPool(len(link_list))
    for i in range(len(link_list)):
        link_list[i].append(lock)
        link_list[i].append(args.dir)
    result_list=pool.map(worker,link_list)
    a = open(args.dir + args.job_id + ".json", "w")
    json.dump(result_list,a)
    a.close()