import argparse
import moviepy.editor as mp


def main():
    parser = argparse.ArgumentParser(
        prog="CutClip", description="Cuts a video to a shorter clip"
    )

    parser.add_argument("-i", "--input", help="Input file", required=True)
    parser.add_argument(
        "-s", "--start", default=0.0, type=float, help="Start time", required=True
    )
    parser.add_argument("-e", "--end", type=float, help="End time", required=True)

    args = parser.parse_args()

    vidfile = args.input
    start = args.start
    end = args.end

    video = mp.VideoFileClip(vidfile)
    clip = video.subclip(start, end)
    clip.write_videofile("output.mp4")
