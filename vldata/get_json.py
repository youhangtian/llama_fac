import json
import random

data_path = '/file/tian/data/coco'

with open(f'{data_path}/annotations/instances_train2017.json') as f:
    anno_data = json.load(f)

cate = {}
for c in anno_data['categories']:
    cate[c['id']] = c['name']

images = {}
for i in anno_data['images']:
    images[i['id']] = [i['height'], i['width']]

anno = {}
for a in anno_data['annotations']:
    image_id = a['image_id']

    img_h = images[image_id][0]
    img_w = images[image_id][1]
    bbox = a['bbox']
    c = cate[a['category_id']]
    x = (bbox[0] + bbox[2]/2) / img_w
    y = (bbox[1] + bbox[3]/2) / img_h 

    arr = anno.get(image_id, [])
    arr.append([c, f'{x:.2f}', f'{y:.2f}'])
    anno[image_id] = arr 

print('anno data len:', len(anno_data['annotations']))
print('anno len:', len(anno))

output_arr = []
for k, v in anno.items():
    d = {}
    d['messages'] = []
    d['images'] = []

    content = f'图片里有{len(v)}个目标'
    for i in range(len(v)):
        content += f'\n第{i+1}个目标类别是{v[i][0]}, 该目标在图片中的坐标是({v[i][1]}, {v[i][2]})'

    d['messages'].append({'content': '<image>图片里有哪些目标？', 'role': 'user'})
    d['messages'].append({
        'content': content,
        'role': 'assistant'
    })

    d['images'].append(f'{data_path}/train2017/{k:0>12}.jpg')

    output_arr.append(d)

print('output len:', len(output_arr))
print(random.choices(output_arr))

with open('data.json', 'w') as f:
    json.dump(output_arr, f, indent=2, ensure_ascii=False)

print('done')
