#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact
"""
import argparse
import logging
import wandb
import os

import pandas as pd


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    ######################
    # YOUR CODE HERE     #
    ######################
    logger.info("Downloading and reading artifact")
    artifact_local_path = run.use_artifact(args.input_artifact).file()
    df = pd.read_csv(artifact_local_path)

    logger.info("Cleaning data")
    df = df[df["price"].between(args.min_price, args.max_price)].copy()
    df['last_review'] = pd.to_datetime(df['last_review'])

    logger.info("Saving file")
    df.to_csv(args.output_artifact, index=False, index_label=False)

    logger.info("Attaching saved file to artifact")
    artifact = wandb.Artifact(
        name=args.output_artifact,
        type=args.output_type,
        description=args.output_description
    )
    artifact.add_file(args.output_artifact)

    logger.info("Logging artifact")
    run.log_artifact(artifact)

    logger.info("Removing unnecessary files")
    os.remove(args.output_artifact)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic data cleaning")


    parser.add_argument(
        "--input_artifact", 
        type=str,
        help="Fully-qualified name for the input artifact",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="Fully-qualified name for the output artifact",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="Type of the output artifact",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help="Description for the output artifact",
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float,
        help="Minimum acceptable price",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,
        help="Maximum acceptable price",
        required=True
    )


    args = parser.parse_args()

    go(args)
