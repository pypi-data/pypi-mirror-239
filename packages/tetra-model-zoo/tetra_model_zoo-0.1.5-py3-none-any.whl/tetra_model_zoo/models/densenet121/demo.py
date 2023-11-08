from tetra_model_zoo.models._shared.imagenet_classifier.demo import imagenet_demo
from tetra_model_zoo.models.densenet121.model import MODEL_ID, DenseNet


def main(is_test: bool = False):
    imagenet_demo(DenseNet, MODEL_ID, is_test)


if __name__ == "__main__":
    main()
