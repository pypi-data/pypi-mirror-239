from tetra_model_zoo.models._shared.imagenet_classifier.demo import imagenet_demo
from tetra_model_zoo.models.resnext101.model import MODEL_ID, ResNeXt101


def main(is_test: bool = False):
    imagenet_demo(ResNeXt101, MODEL_ID, is_test)


if __name__ == "__main__":
    main()
