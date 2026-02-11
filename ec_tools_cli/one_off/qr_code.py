import argparse
from typing import Generator

import qrcode
from PIL import Image
from pyzbar.pyzbar import decode


class QrCodeProcessor:

    @classmethod
    def generate_qr_code(cls, message: str, size: int) -> Image.Image:
        img = qrcode.make(message, box_size=size)
        return img

    @classmethod
    def read_qr_code(cls, image: Image.Image) -> Generator[str, None, None]:
        results = decode(image)
        for result in results:
            yield result.data.decode("utf-8")
        return None


def get_args():
    parser = argparse.ArgumentParser(description="QR Code Processor")
    subparsers = parser.add_subparsers(dest="action", required=True)
    generate_parser = subparsers.add_parser("generate", help="Generate a QR code from a message")
    scan_parser = subparsers.add_parser("scan", help="Read a QR code from an image file")

    generate_parser.add_argument(
        "-m",
        "--message",
        required=True,
        type=str,
        help="The message to encode in the QR code",
    )
    generate_parser.add_argument(
        "-s",
        "--size",
        type=int,
        default=20,
        help="The size of each QR code box",
    )
    generate_parser.add_argument(
        "-o",
        "--output_path",
        type=str,
        help="The path to save the generated QR code image",
    )
    scan_parser.add_argument(
        "-i",
        "--image_path",
        required=True,
        type=str,
        help="The path to the image file containing the QR code",
    )
    scan_parser.add_argument(
        "-o",
        "--output_path",
        type=str,
        help="The path to save the generated QR code image",
    )
    return parser.parse_args()


def main():
    args = get_args()
    processor = QrCodeProcessor()

    if args.action == "generate":
        qr_image = processor.generate_qr_code(args.message, args.size)
        if args.output_path:
            qr_image.save(args.output_path)
        else:
            qr_image.show()
    elif args.action == "scan":
        image = Image.open(args.image_path)
        messages = list(processor.read_qr_code(image))
        if args.output_path:
            with open(args.output_path, "w") as f:
                for message in messages:
                    f.write(message + "\n")
        else:
            print("Decoded message:", messages)


if __name__ == "__main__":
    main()
