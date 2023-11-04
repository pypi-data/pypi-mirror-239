import binascii
import argparse

def decode_hex_to_image(input_file, output_image_path):
    try:
        with open(input_file, 'r') as txt_file:
            hex_data = txt_file.read()
            image_data = binascii.unhexlify(hex_data.encode('utf-8'))

        with open(output_image_path, 'wb') as image_file:
            image_file.write(image_data)

        print(f"Decoded {input_file} to {output_image_path}.")
    except Exception as e:
        print(f"Error: {str(e)}")

def encode_image_to_hex(image_path, output_file):
    try:
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()
            hex_data = binascii.hexlify(image_data).decode('utf-8')

        with open(output_file, 'w') as txt_file:
            txt_file.write(hex_data)

        print(f"Encoded {image_path} to {output_file} as hex.")
    except Exception as e:
        print(f"Error: {str(e)}")

class ImageEncoderDecoder:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Encode and decode PNG images to/from hex in a text file.")
        self.parser.add_argument("input", help="Input PNG image file for encoding or input text file for decoding.")
        self.parser.add_argument("-o", "--output",
                                 help="Output text file for encoding or output image file for decoding.")
        self.parser.add_argument("-d", "--decode", action="store_true", help="Flag to enable decoding.")

    def run(self):
        args = self.parser.parse_args()

        if args.decode:
            if args.output:
                decode_hex_to_image(args.input, args.output)
            else:
                print("Please specify an output image file with -o for decoding.")
        else:
            if args.output:
                encode_image_to_hex(args.input, args.output)
            else:
                print("Please specify an output text file with -o for encoding.")

def run_hexapixl():
    encoder_decoder = ImageEncoderDecoder()
    encoder_decoder.run()

if __name__ == "__main__":
    run_hexapixl()
