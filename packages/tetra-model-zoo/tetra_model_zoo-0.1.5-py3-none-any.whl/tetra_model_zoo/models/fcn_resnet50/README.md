[![Tetra AI](https://tetra-public-assets.s3.us-west-2.amazonaws.com/model-zoo/logo.svg)](https://tetra.ai/)


# [FCN_ResNet50: Fully-convolutional network model for image segmentation.](https://tetra.ai/model-zoo/fcn_resnet50)

FCN_ResNet50 is a machine learning model that can segment images from the COCO dataset. It uses ResNet50 as a backbone. We present an optimized implementation of the model suitable to be exported for and run on device.

This is based on the implementation of FCN_ResNet50 found [here](https://github.com/pytorch/vision/blob/main/torchvision/models/segmentation/fcn.py).

More details, such as model latency and throughput running on various devices, can be found at https://tetra.ai/model-zoo/fcn_resnet50


## Example & Usage

Run the demo:
```bash
python -m tetra_model_zoo.models.fcn_resnet50.demo [--help]
```

See [demo.py](demo.py) for sample usage of the model and app.

Please refer to our [general instructions on using models](../../#tetra-model-zoo) for more usage instructions.


## Optimize, Profile, and Validate FCN_ResNet50 for a device with Tetra Hub
Using Tetra Hub, you can easily optimize, profile, and validate FCN_ResNet50 for a device.

Run the following python script to export and optimize for iOS and Android:
```bash
python -m tetra_model_zoo.models.fcn_resnet50.export [ --help ]
```

## Model In-Application Deployment instructions
<a href="mailto:support@tetra.ai?subject=Request Access for Tetra Hub&body=Interest in using FCN_ResNet50 in model zoo for deploying on-device.">Get in touch with us</a> to learn more!


## License
- Code in the Tetra Model Zoo repository is covered by the LICENSE file at the repository root.
- The license for the original implementation of FCN_ResNet50 can be found [here](https://github.com/pytorch/vision/blob/main/LICENSE).


## References
* [Fully Convolutional Networks for Semantic Segmentation](https://arxiv.org/abs/1411.4038)
* [Source Model Implementation](https://github.com/pytorch/vision/blob/main/torchvision/models/segmentation/fcn.py)
