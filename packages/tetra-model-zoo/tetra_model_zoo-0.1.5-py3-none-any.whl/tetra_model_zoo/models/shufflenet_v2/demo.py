from tetra_model_zoo.models._shared.imagenet_classifier.demo import imagenet_demo
from tetra_model_zoo.models.shufflenet_v2.model import MODEL_ID, ShufflenetV2


def main(is_test: bool = False):
    imagenet_demo(ShufflenetV2, MODEL_ID, is_test)


if __name__ == "__main__":
    main()
