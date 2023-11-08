from tetra_model_zoo.models._shared.imagenet_classifier.demo import imagenet_demo
from tetra_model_zoo.models.googlenet.model import MODEL_ID, GoogLeNet


def main(is_test: bool = False):
    imagenet_demo(GoogLeNet, MODEL_ID, is_test)


if __name__ == "__main__":
    main()
