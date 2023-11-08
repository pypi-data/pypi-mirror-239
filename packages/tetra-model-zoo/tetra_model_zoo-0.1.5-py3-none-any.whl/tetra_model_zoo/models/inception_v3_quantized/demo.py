from tetra_model_zoo.models._shared.imagenet_classifier.demo import imagenet_demo
from tetra_model_zoo.models.inception_v3_quantized import MODEL_ID
from tetra_model_zoo.models.inception_v3_quantized.model import InceptionNetV3Quantized


def main(is_test: bool = False):
    imagenet_demo(InceptionNetV3Quantized, MODEL_ID, is_test)


if __name__ == "__main__":
    main()
