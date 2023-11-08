from tetra_model_zoo.models._shared.imagenet_classifier.demo import imagenet_demo
from tetra_model_zoo.models.mobilenet_v3_small.model import MODEL_ID, MobileNetV3Small


def main(is_test: bool = False):
    imagenet_demo(MobileNetV3Small, MODEL_ID, is_test)


if __name__ == "__main__":
    main()
