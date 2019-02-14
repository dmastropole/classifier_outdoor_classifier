import csv
import tensorflow as tf
import os
import requests
import re
from collections import defaultdict, Counter
import random
import errno

# Get long video id from short video id
def get_id(video_id):
    base_url = 'http://data.yt8m.org/2/j/i/'
    pattern = re.compile(r'i\("\w{4}","(.*)"\);')
    
    url = base_url + video_id[0:2] + '/' + video_id + '.js'
    resp = requests.get(url=url)
    resp_text = resp.text
    match = pattern.match(resp_text)
    return match.group(1)
    
# Get video frame
def save_image(path, id_long):
    filename = id_long + '.jpg'
    filename_path = os.path.join(path, filename)
 
    # Download and save image if it doesn't exist
    if not os.path.isfile(filename_path):
        image_url = 'http://i.ytimg.com/vi/' + id_long + '/mqdefault.jpg'
        img_data = requests.get(image_url).content
        with open(filename_path, 'wb') as handler:
            handler.write(img_data)
            
    # Return filename path
    return filename_path

if __name__ == '__main__':
    # Get all index name pairs
    with open('vocabulary.csv') as f:
        reader = csv.DictReader(f)
        category_map = {}
        category_counts = {}
        for row in reader:
            category_map[row['Name']] = int(row['Index'])
            category_counts[int(row['Index'])] = int(row['TrainVideoCount'])

    # Define indoor and outdoor categories from tags
    indoor_categories = {'Wall','Bathroom','Bedroom','Living room','Classroom',
                         'Shower','Basement','Loft','Floor','Carpet',
                         'Gym','Room','Wall','Elevator','Dining room',
                         'Ceiling','Kitchen','Laundry','Fireplace','Couch'
                        }
    indoor_ids = {category_map[name] for name in list(indoor_categories)}
    indoor_total = sum([category_counts[cat] for cat in indoor_ids ])
    indoor_p = {cat: 1-1.0*category_counts[cat]/indoor_total for cat in indoor_ids }

    outdoor_categories = {'Outdoor recreation','Sunset','Snow','Lake',
                          'Mountain','Volcano','Underwater','River','Dune',
                          'Beach','Wildlife','Forest','Desert','Sky','Garden',
                          'Military parade','Skiing','Marching band',
                          'Carnival','Gardening','Nature','Off-road vehicle',
                          'Graffiti','Trail','Camping','Hiking','Lawn','Roof',
                          'Thunderstorm','Traffic','Rafting','Campsite','Cave'
                         }
    outdoor_ids = {category_map[name] for name in list(outdoor_categories)}
    outdoor_total = sum([category_counts[cat] for cat in outdoor_ids ])
    outdoor_p = {cat: 1-1.0*category_counts[cat]/outdoor_total for cat in outdoor_ids }

    print 'number indoor videos:', indoor_total
    print 'number outdoor videos:', outdoor_total

    # Get paths to all video record files
    all_video_paths = []
    dataDir = 'video'
    for root, dirs, files in os.walk(dataDir): 
        for filename in files:
            if not dirs and 'tfrecord' in filename:
                all_video_paths.append(os.path.join(root, filename))

    print 'number of records:', len(all_video_paths)

    # Read all video files and get ids for images
    label_ids = defaultdict(list)
    for k, filename in enumerate(all_video_paths):
        if k > 150: # Stop after k iterations
            break
        
        reader = tf.python_io.tf_record_iterator(filename)
        video_records = [tf.train.Example().FromString(video_str)
                      for video_str in reader]
     
        print k, ' of ', len(all_video_paths), ' : ', len(video_records)
        for record in video_records:
            video_id = record.features.feature['id'].bytes_list.value[0]
            labels = set(map(int,record.features.feature['labels'].int64_list.value))
            indoor = indoor_ids & labels
            outdoor = outdoor_ids & labels
            
            # Determine whether you should keep indoor and outdoor photos
            if outdoor and (random.random() < outdoor_p[random.sample(outdoor,1)[0]]):
                try:
                    label_ids['outdoor'].append(get_id(video_id))
                except:
                    pass
            if indoor and (random.random() < indoor_p[random.sample(indoor,1)[0]]):
                try:
                    label_ids['indoor'].append(get_id(video_id))
                except:
                    pass

    print 'outdoor photos: ', len(label_ids['outdoor'])
    print 'indoor photos: ', len(label_ids['indoor'])

    # Create directories for images
    imageDirs = ['train_images', 'test_images']
    dirNames = label_ids.keys()
    for imageDir in imageDirs:
        try:
            os.mkdir(imageDir)
            print 'Directory ' , imageDir, ' Created '
        except OSError as e:
            if e.errno == errno.EEXIST:
                print 'Directory ' , imageDir ,  ' already exists'
            else:
                raise
        for dirName in dirNames:
            try:
                os.mkdir(os.path.join(imageDir, dirName))
                print 'Directory ' , dirName ,  ' Created '
            except OSError as e:
                if e.errno == errno.EEXIST:
                    print 'Directory ' , dirName ,  ' already exists'
                else:
                    raise

    # Download and save images
    counts = Counter(['indoor', 'outdoor'])
    filenames = []
    for key, id_list in label_ids.iteritems():
        path_train = os.path.join(imageDirs[0], key)
        path_test = os.path.join(imageDirs[1], key)
        
        # Shuffle and split
        for k, label_id in enumerate(random.sample(id_list, len(id_list))):
            if counts[key] < 800: #training directory
                print 'Saving ', key, ' image ', k
                filenames.append(save_image(path_train, label_id))
                counts[key] += 1
            elif counts[key] < 1000: #testing directory
                print 'Saving ', key, ' image ', k
                filenames.append(save_image(path_test, label_id))
                counts[key] += 1
            else:
                pass
