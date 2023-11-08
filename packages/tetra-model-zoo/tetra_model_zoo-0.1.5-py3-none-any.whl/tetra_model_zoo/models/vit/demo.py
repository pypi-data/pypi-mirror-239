from tetra_model_zoo.models._shared.imagenet_classifier.demo import imagenet_demo
from tetra_model_zoo.models.vit.model import MODEL_ID, VIT


def main(is_test: bool = False):
    imagenet_demo(VIT, MODEL_ID, is_test)


if __name__ == "__main__":
    main()
