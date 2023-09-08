import os
import nltk
from translators import translate_text as ts
from datetime import datetime as dt
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from PyPDF2 import PdfReader
from tkinter.filedialog import askopenfilename as fn
from tkinter import messagebox
from post_generator import PostGenerator


# starting with creating a class for Parsing a text
class TextParser:
    """this class will take a text corpus from pdf extractor and it will filter it"""
    # constructor struct
    def __init__(self, text_corpus, filter_type_word):
        # setting variable for post tag

        # file name
        self.file_name = f"{dt.now().strftime('%A %B %H %M %S')}.txt"

        # for user experience
        self.filter_type = filter_type_word

        # before one step from result
        self.classified_text_list = []

        # to process
        self.tokenized_text_list = []

        # the result
        self.wanted_text_list = []

        # get rid of duplicated values
        self.wanted_text_list_last = set()

        # set variables and add stop words in which language will u use like ("a", "an", "the", "is", "are"... etc.)
        self.stopwords_list = stopwords.words("english")

        # the text corpus will come like parameter
        self.text_corpus = text_corpus

        # tokenize the text to parse text
        self.tokenized_text = sent_tokenize(self.text_corpus)

        # run the function for debugging in the trying process

        self.tokenizer()

    # tokenize and classify to texts
    def tokenizer(self):

        # with for loop get every tokenized word to add
        for word in self.tokenized_text:

            # set variable to add list after this operation
            tokenized_wordlist = word_tokenize(word)

            # with for loop add the tokenized list
            self.tokenized_text_list = [w for w in tokenized_wordlist if w not in self.stopwords_list]

            # classified text adding
            self.classified_text_list += nltk.pos_tag(self.tokenized_text_list)

        # filtering with what you want
        for wanted_text in self.classified_text_list:

            # if word type is valid for filter type add the list wanted text
            if wanted_text[1] == self.filter_type:

                # add the list
                self.wanted_text_list.append(wanted_text[0])

            else:
                continue

        # remove duplication from list and convert into set
        self.wanted_text_list_last.update(i for i in self.wanted_text_list)

        # run other function to save file
        self.data_to_file()

    # create data from extracted filtered and classified texts
    def data_to_file(self):

        # if file is exists do not create else create
        for result_text in self.wanted_text_list_last:

            # with date function create unique file names
            with open(self.file_name, "a", encoding="utf-8") as word_file:

                # write words to txt
                word_file.write(result_text+"\n")


# second filter
class TextParser2:
    """this class will take a filtered txt file and it will re filter again and save, after that all operations
    it will produce posts"""
    # constructor struct
    def __init__(self, text_corpus, filter_type_word, post_dir_name, progress_bar_widget, f_name_no_translated, widget,):

        # setting variable for post tag
        # tkinter widget
        self.widget = widget

        # progress bar length
        self.progress_bar_length = 100

        # progres bar
        self.progress_bar = progress_bar_widget

        # to create post define the dir
        self.post_dir_name = post_dir_name

        # translator
        self.translator = None

        # file name
        self.file_name = f_name_no_translated

        # for user experience
        self.filter_type = filter_type_word

        # before one step from result
        self.classified_text_list = []

        # to process
        self.tokenized_text_list = []

        # the result
        self.wanted_text_list = []

        # get rid of duplicated values
        self.wanted_text_list_last = set()

        # set variables and add stop words in which language will u use like ("a", "an", "the", "is", "are"... etc.)
        self.stopwords_list = stopwords.words("english")

        # the text corpus will come like parameter
        self.text_corpus = text_corpus

        # tokenize the text to parse text
        self.tokenized_text = sent_tokenize(self.text_corpus)

        # run the function for debugging in the trying process

        self.tokenizer()

    # tokenize and classify to texts
    def tokenizer(self):

        # with for loop get every tokenized word to add
        for word in self.tokenized_text:

            # set variable to add list after this operation
            tokenized_wordlist = word_tokenize(word)

            # with for loop add the tokenized list
            self.tokenized_text_list = [w for w in tokenized_wordlist if w not in self.stopwords_list]

            # classified text adding
            self.classified_text_list += nltk.pos_tag(self.tokenized_text_list)

        # filtering with what you want
        for wanted_text in self.classified_text_list:

            # if word type is valid for filter type add the list wanted text
            if wanted_text[1] == self.filter_type:

                # add the list
                self.wanted_text_list.append(wanted_text[0])

            else:
                continue

        # remove duplication from list and convert into set
        self.wanted_text_list_last.update(i for i in self.wanted_text_list)

        # create turkish class
        self.translator = TranslateToTurkish()

        # run other function to save file
        self.data_to_file()

        # message
        print("Tamamlandı", "Kelimler Çevrildi")

    # create data from extracted filtered and classified texts
    def data_to_file(self):
        # according to filter type create folder
        if os.path.exists(f"{self.filter_type}"):
            pass

        else:
            os.mkdir(f"{self.filter_type}")

        # if file is exists do not create else create
        for result_text in self.wanted_text_list_last:

            # convert to turkish
            turkish_word = self.translator.translate(result_text)

            # with date function create unique file names
            with open(f"{self.filter_type}/"+self.file_name+"(TRANSLATED BY GOOGLE).txt",
                      "a", encoding="utf-8") as word_file:

                # write words to txt
                word_file.write(result_text+f" / {turkish_word.replace('ğ', 'g').replace('ş', 's')}"+"\n")

            # update widget
            self.widget.update()

            # update progress bar label, from no duplication set length
            self.progress_bar['value'] += 100 / len(self.wanted_text_list_last)

        # run the image generator
        self.create_post_function()

    # create post class and starting to creating
    def create_post_function(self):

        # create class
        generator = PostGenerator(f"{self.filter_type}/"+f"{self.file_name}(TRANSLATED BY GOOGLE).txt")

        # run function and derive from txts
        generator.image_process(self.post_dir_name)


# create class for extracting text from pdf
class TextExtractorPdf:
    """it will extract everything from pdf"""
    # constructor
    def __init__(self):

        # setting variables

        # text var
        self.text = ""

    def extract_text(self, file_path_pdf):

        # catch exceptions
        try:

            # read document
            document = PdfReader(file_path_pdf)

            # get pages
            pages_var = document.pages

            # with for loop get text from pages

            for pages in pages_var:

                self.text += pages.extract_text()

            # returning self value
            return self.text

        except FileNotFoundError:
            messagebox.showerror("HATA", "DOSYA SEÇİLEMDİ")


# class for translating turkish
class TranslateToTurkish:
    "it will translate to turkish"
    # constructor struct
    def __init__(self):
        # define vars
        self.translated_word = None

    # create func to translate
    def translate(self, text):
        # with try except block, try to translate the word, else increase awaiting sec
        try:
            # get text and translate
            self.translated_word = ts(text, from_language="en", to_language="tr", sleep_seconds=0.2)

            return self.translated_word

        # except condition
        except RuntimeError:
            # again try
            try:
                self.translated_word = ts(text, from_language="en", to_language="tr", sleep_seconds=0.7)

                return self.translated_word

            # except connection error to give message internet error
            except (ConnectionRefusedError, ConnectionError):

                messagebox.showerror("BAĞLANTI YOK", "INTERNET BAĞLANTISI KURULAMADI!!")
                exit()


# Without classes merged functions of classes (use in gui as button command)
def analyzer_function(filter_type, post_dir_name, progress_bar_label, widget):
    """all function will be merged here"""
    # create class
    text_extractor = TextExtractorPdf()

    # get filename with open file dialouge
    file_name = fn(filetypes=(("PDF", "*.pdf"),), )

    if file_name == '':
        messagebox.showerror("HATA", "DOSYA SEÇİLMEDİ")

        exit()

    # extract text
    text = text_extractor.extract_text(file_path_pdf=file_name)

    # create class to filter
    parser = TextParser(text, filter_type)

    # implementing second filter to analyze

    try:

        # open written words and read and merge
        with open(parser.file_name, "r", encoding="utf-8") as re_filtered:

            # merging
            txt = ""
            for i in re_filtered.readlines():
                txt += i+" "

            # analyze merged dict and translate to turkish
            parser2 = TextParser2(text_corpus=txt, filter_type_word=parser.filter_type, post_dir_name=post_dir_name,
                                  progress_bar_widget=progress_bar_label,
                                  f_name_no_translated=parser.file_name,
                                  widget=widget)

            # give message and absolute path
            messagebox.showinfo("BİLGİ", f"DOSYA {os.path.abspath(parser2.post_dir_name)} KAYDEDİLDİ")

            # open absolute path
            os.startfile(os.path.abspath(parser2.post_dir_name))

        # clear the cache
        os.remove(parser.file_name)

    except (FileExistsError, FileNotFoundError):
        messagebox.showerror("HATA", "DOSYA İÇRİSİNDE ARANA KELİME TÜRÜ YOK")


########################################################
# PROJECT MADE BY CODE DEM ALL RIGHT RESERVED          #
# FILTER TYPE COMES FROM OPTION MENU                   #
# DİR NAME COMES FROM USER                             #
# THERE ARE TWO FILTER, ONE FUNCTION EXTRACT TEXTS     #
# FIRST FILTER, FILTERS WORDS ACCORDİNG THEIR TYPES    #
# SECOND CONSOLIDATES THE RESULT                       #
# ONE POST GENERATOR DERIVES POSTS FROM TEMPLATE      #
########################################################
