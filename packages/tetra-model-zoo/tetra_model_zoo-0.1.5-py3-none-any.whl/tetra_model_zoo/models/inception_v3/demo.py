from tetra_model_zoo.models._shared.imagenet_classifier.demo import imagenet_demo
from tetra_model_zoo.models.inception_v3.model import MODEL_ID, InceptionNetV3


def main(is_test: bool = False):
    imagenet_demo(InceptionNetV3, MODEL_ID, is_test)


if __name__ == "__main__":
    main()
