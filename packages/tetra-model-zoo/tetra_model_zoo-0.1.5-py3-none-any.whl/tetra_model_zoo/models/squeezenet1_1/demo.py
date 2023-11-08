from tetra_model_zoo.models._shared.imagenet_classifier.demo import imagenet_demo
from tetra_model_zoo.models.squeezenet1_1.model import MODEL_ID, SqueezeNet


def main(is_test: bool = False):
    imagenet_demo(SqueezeNet, MODEL_ID, is_test)


if __name__ == "__main__":
    main()
