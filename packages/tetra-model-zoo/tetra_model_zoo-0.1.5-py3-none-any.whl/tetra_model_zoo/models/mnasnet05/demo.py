from tetra_model_zoo.models._shared.imagenet_classifier.demo import imagenet_demo
from tetra_model_zoo.models.mnasnet05.model import MODEL_ID, MNASNet05


def main(is_test: bool = False):
    imagenet_demo(MNASNet05, MODEL_ID, is_test)


if __name__ == "__main__":
    main()
