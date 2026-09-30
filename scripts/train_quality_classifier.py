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



if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--train_data', type=str, required=True)
    parser.add_argument('--classifier_dir', type=str, default="outputs/quality_classifier.bin")
    parser.add_argument('--lr', type=float, default=0.1)
    parser.add_argument('--epoch', type=int, default=5)

    args = parser.parse_args()

    output_dir = os.path.dirname(args.classifier_dir)

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    train_model(train_data=args.train_data, classifier_dir=args.classifier_dir, lr=args.lr, epoch=args.epoch)