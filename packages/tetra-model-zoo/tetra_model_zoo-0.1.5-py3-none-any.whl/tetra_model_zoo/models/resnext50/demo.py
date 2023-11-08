from tetra_model_zoo.models._shared.imagenet_classifier.demo import imagenet_demo
from tetra_model_zoo.models.resnext50.model import MODEL_ID, ResNeXt50


def main(is_test: bool = False):
    imagenet_demo(ResNeXt50, MODEL_ID, is_test)


if __name__ == "__main__":
    main()
