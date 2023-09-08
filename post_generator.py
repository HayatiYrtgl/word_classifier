import os.path

from PIL import Image, ImageDraw, ImageFont


# create class for read the post template
class PostGenerator:

    # override
    def __init__(self, filename, x=45, y=280):

        # def for vars
        # image read and resize
        self.image = Image.open("post_template/temp.jpg")

        # wordlist
        with open(filename, "r", encoding="utf-8") as file:

            self.wordlist = file.readlines()

        # identifier number word
        self.word_index_num = 0

        # x dimension identifier
        self.x = x

        # y dimension
        self.y = y

    # function to process word to image
    def image_process(self, post_dir_name):

        # if post names dir is not exists create else pass
        if os.path.exists(post_dir_name):
            pass

        # else create it
        else:
            os.mkdir(post_dir_name)

        # with for loop try
        for word in self.wordlist:

            # process and put text to image and get line
            processed_image = ImageDraw.Draw(self.image)

            font = ImageFont.truetype("pil fonts/Castal_Street.ttf", 60, encoding="utf-8")

            processed_image.text(text=word, xy=(self.x, self.y), font=font, fill=(0, 0, 0))

            processed_image.line(xy=((45, self.y+80), (1020, self.y+80)), fill="black", width=5)

            # increase the number to save image
            self.word_index_num += 1

            # increase the y dimension
            self.y += 190

            # if file identifier is divisible by 4, save the processed image
            if self.word_index_num % 4 == 0:

                # save image
                self.image.save(f"{post_dir_name}/{self.word_index_num/4}.Post.jpg")

                # y dimension
                self.y = 280

                # reset image
                # image read and resize
                self.image = Image.open("post_template/temp.jpg")

        # after the process reset values

        # identifier number word
        self.word_index_num = 1

        # x dimension identifier
        self.x = 45


