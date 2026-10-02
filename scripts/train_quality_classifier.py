import os
import fasttext
import argparse


def train_model(
        train_data: str,
        classifier_dir: str,
        lr: float,
        epoch:int,
):
    model = fasttext.train_supervised(
        input = train_data,
        lr=lr,
        epoch=epoch
    )

    model.save_model(classifier_dir)
    return model


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--train_data', type=str, required=False, default="local-shared-data/quality_train.txt")
    parser.add_argument('--val_data', type=str, required=False, default="local-shared-data/quality_val.txt")
    parser.add_argument('--classifier_dir', type=str, required=False, default="outputs/quality_classifier.bin")
    parser.add_argument('--lr', type=float, required=False, default=0.1)
    parser.add_argument('--epoch', type=int, required=False,default=5)

    args = parser.parse_args()

    output_dir = os.path.dirname(args.classifier_dir)

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    model = train_model(train_data=args.train_data, classifier_dir=args.classifier_dir, lr=args.lr, epoch=args.epoch)

    print(model.test(args.val_data))