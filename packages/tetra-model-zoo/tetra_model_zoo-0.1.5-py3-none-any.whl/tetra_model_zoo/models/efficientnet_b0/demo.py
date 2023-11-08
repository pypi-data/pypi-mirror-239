from tetra_model_zoo.models._shared.imagenet_classifier.demo import imagenet_demo
from tetra_model_zoo.models.efficientnet_b0.model import MODEL_ID, EfficientNetB0


def main(is_test: bool = False):
    imagenet_demo(EfficientNetB0, MODEL_ID, is_test)


if __name__ == "__main__":
    main()
