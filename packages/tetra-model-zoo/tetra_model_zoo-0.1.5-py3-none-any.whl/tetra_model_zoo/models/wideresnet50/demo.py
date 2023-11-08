from tetra_model_zoo.models._shared.imagenet_classifier.demo import imagenet_demo
from tetra_model_zoo.models.wideresnet50.model import MODEL_ID, WideResNet50


def main(is_test: bool = False):
    imagenet_demo(WideResNet50, MODEL_ID, is_test)


if __name__ == "__main__":
    main()
