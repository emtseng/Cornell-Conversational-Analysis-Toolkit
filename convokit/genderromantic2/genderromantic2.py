from convokit.model import Corpus, User
from convokit.transformer import Transformer
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
import re

class Genderromantic2(Transformer):
    romantic_words = ["adorable","amazing","angel","babe","beau","beautiful","beloved","darling","dearest","enchanting","lover","gorgeous","handsome","heavenly","honey","life-changing","paramour","sweetheart","sweetie","swoon","wonderful","adore","admire","care","cherish","choose","daydream","delight","dream","need","prize","treasure","value","want","worship","yearn","date ","love","kiss","sex","romance","romantic","hug"]

    def __init__(self):
        pass
    
    @staticmethod
    def genderDictionary(arg):
        name_to_gender = {}
        for user in arg.iter_users():
            if user.name not in name_to_gender:
                name_to_gender[user.name] = user.meta['sex']
        return name_to_gender
        
    def transform(self, corpus: Corpus):
        name_to_gender = self.genderDictionary(corpus)
        ps = PorterStemmer()
        for utt in corpus.iter_utterances():
            speaker_name = utt.user.name
            speaker_gender = utt.user.meta['sex']
            gender_is_female = speaker_gender == 'FEMALE'
            
            contains_romantic = False
            male_about_female = False
            female_about_male = False

            for romantic_word in Genderromantic2.romantic_words:
                if romantic_word.lower() in utt.text.lower():
                    contains_romantic = True
                    break
            
            utt.add_meta('female_about_male', female_about_male)
            utt.add_meta('male_about_female', male_about_female)
            utt.add_meta('contains_romantic', contains_romantic)
        return corpus
