import argparse


class TrainOptions:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="Training options for super-resolution models"
        )
        self.initialized = False

    def initialize(self):
        if self.initialized:
            return
        self.parser.add_argument(
            "--dataroot", type=str, required=True, help="Path to the dataset directory"
        )
        self.parser.add_argument(
            "--name",
            type=str,
            default="experiment",
            help="Experiment name for saving logs and models",
        )
        self.parser.add_argument(
            "--model_type",
            type=str,
            required=True,
            help="Type of model to train: e.g., 'sr_unet', 'gdn'",
        )
        self.parser.add_argument(
            "--batch_size", type=int, default=8, help="Batch size for training"
        )
        self.parser.add_argument(
            "--n_epochs",
            type=int,
            default=50,
            help="Number of epochs at the initial learning rate",
        )
        self.parser.add_argument(
            "--n_epochs_decay",
            type=int,
            default=50,
            help="Number of epochs to linearly decay the learning rate to zero",
        )
        self.parser.add_argument(
            "--continue_train",
            action="store_true",
            help="Continue training from the last saved epoch",
        )
        self.parser.add_argument(
            "--checkpoint_dir",
            type=str,
            default="./checkpoints/",
            help="Directory to save model checkpoints",
        )
        self.parser.add_argument(
            "--which_epoch",
            type=str,
            default="latest",
            help="Epoch to start resuming training ('latest' or specific epoch number)",
        )
        self.parser.add_argument(
            "--lr",
            type=float,
            default=0.0002,
            help="Initial learning rate for Adam optimizer",
        )
        self.parser.add_argument(
            "--gpu_ids",
            type=str,
            default="0",
            help="Comma-separated GPU IDs (e.g., '0,1,2') for training; '-1' for CPU",
        )
        self.parser.add_argument(
            "--print_freq",
            type=int,
            default=100,
            help="Frequency of printing training results to the console",
        )
        self.parser.add_argument(
            "--save_latest_freq",
            type=int,
            default=5000,
            help="Frequency of saving the latest results during training",
        )
        self.parser.add_argument(
            "--save_epoch_freq",
            type=int,
            default=5,
            help="Frequency of saving checkpoints at the end of specified number of epochs",
        )
        self.parser.add_argument(
            "--display_freq",
            type=int,
            default=400,
            help="Frequency of displaying results on the training console",
        )
        # More options can be added as necessary
        self.initialized = True

    def parse(self):
        if not self.initialized:
            self.initialize()
        opt = self.parser.parse_args()
        self.print_options(opt)
        return opt

    def print_options(self, opt):
        message = "----------------- Options ---------------\n"
        for k, v in sorted(vars(opt).items()):
            default = self.parser.get_default(k)
            comment = f"\t[default: {default}]" if v != default else ""
            message += f"{k:>25}: {v:<30}{comment}\n"
        message += "----------------- End -------------------"
        print(message)
