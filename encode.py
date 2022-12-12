import ffmpeg
import json
import os
import argparse
from loguru import logger
# import subprocess


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="Input file", default="Mariokart_Meme_Mukbang.mp4")
    parser.add_argument("--output", help="Output file" , default="Mariokart_Meme_Mukbang.webm")
    parser.add_argument("--preset", help="Preset file", default="youtube.json")
    parser.add_argument("--one_pass", help="Use 2 pass encoding", action="store_true")
    parser.add_argument("--verbose", help="Verbose output", action="store_true")
    args = parser.parse_args()

    logger.info("Input: {args.input}")
    logger.info("Output: {args.output}")
    logger.info("Preset: {args.preset}")
    logger.info("One pass: {args.one_pass}")

    with open(args.preset) as f:
        preset = json.load(f)

    input_args = preset.get("input", {})
    output_args = preset.get("output", {})

    if args.one_pass:
        # Only one pass
        ffmpeg.input(args.input, **input_args).output(args.output, **output_args).run(overwrite_output=True, quiet=args.verbose)
    else:
        # First pass
        output_args["pass"] = 1
        output_args["f"] = "null"
        ffmpeg.input(args.input, **input_args).output("pipe:", **output_args).run(overwrite_output=True, quiet=args.verbose)
        # Second pass
        output_args["pass"] = 2
        output_args["f"] = args.output.split(".")[-1]
        ffmpeg.input(args.input, **input_args).output(args.output, **output_args).run(overwrite_output=True, quiet=args.verbose)
        

if __name__ == "__main__":
    main()