# whaTFRecordsWriter

# Overview

Are you having trouble saving your precious data into an easy format for training and testing? Well, you're in luck because with `whaTFRecordsWriter` we are trying to minimize the effort required to simplify your dataset with [TFRecord]('https://www.tensorflow.org/tutorials/load_data/tfrecord'). 

# Installation

Python 3.6+ is required

```Python
pip install whaTFRecordsWriter
```

# Example

## Converting Images with no labels to tfrecords

```python
# 'test.tfrecords' is what you want to name your tfrecords
# 'test_data' is the file directory that has the following structure:
# test_data: /
#       [image_0001.jpg]
#       [image_0002.jpg]
#       [image_000x.jpg]
#       ...
# 'writes_per_tfrecords' is the number of images to save per tfrecord.
import whaTFRecordsWriter as wr
wr.write_images_folder('test.tfrecords', 'test_data', writes_per_tfrecords=10)
```

## Custom dataset

To encode images to tfrecords, you can use this method:

```python
filename = 'test.tfrecords'
my = wr.Writer(filename)
my.addfeature('image', wr.encode_bytes, preporcessing=wr.load_image)
my.write('test_data')
```

Note: Make sure that the given directory when writing has all the images that you want to store.

To extract the images you can do this:

```python
raw_image_dataset = tf.data.TFRecordDataset('test.tfrecords')

def _parse_image_function(example_proto):
    # Parse the input tf.Example proto using the dictionary above.
    img = tf.io.parse_single_example(example_proto, {"image": tf.io.FixedLenFeature([], tf.string)})
    img = img['image']
    img = tf.image.decode_jpeg(img, channels=3)
    #   image = tf.image.resize_images(image, [224, 224])
    #   image /= 255.0  # normalize to [0,1] range
    # img = tf.cast(img, tf.float32)
    # img = (img / 127.5) - 1 # normalized to [-1, 1]
    return img

parsed_image_dataset = raw_image_dataset.map(_parse_image_function)
parsed_image_dataset= parsed_image_dataset.batch(3)
c = 0
if not os.path.exists('test_prod'):
    os.mkdir('test_prod')
for image in parsed_image_dataset.take(100):
    im = Image.fromarray(image.numpy(), 'RGB')
    c += 1
    im.save('./test_prod/test_%d.png' % c)
```