#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import whaTFRecordsWriter as wr
import tensorflow as tf
import os
from PIL import Image

class UnitTests(unittest.TestCase):
    def test_creating_and_reading(self):
        filename = 'test.tfrecords'
        my = wr.Writer(filename)
        my.addfeature('image', wr.encode_bytes, preporcessing=wr.load_image)
        my.write('test_data')

        raw_image_dataset = tf.data.TFRecordDataset(filename)
        def _parse_image_function(example_proto):
            # Parse the input tf.Example proto using the dictionary above.
            img = tf.io.parse_single_example(example_proto, my.decoding_features)
            img = img['image']
            img = tf.image.decode_jpeg(img, channels=3)
            #   image = tf.image.resize_images(image, [224, 224])
            #   image /= 255.0  # normalize to [0,1] range
            # img = tf.cast(img, tf.float32)
            # img = (img / 127.5) - 1 # normalized to [-1, 1]
            return img

        parsed_image_dataset = raw_image_dataset.map(_parse_image_function)
        c = 0
        if not os.path.exists('test_prod'):
            os.mkdir('test_prod')
        for image in parsed_image_dataset.take(5):
            im = Image.fromarray(image.numpy(), 'RGB')
            c += 1
            im.save('./test_prod/test_%d.png' % c)
        self.assertIsNotNone(my)