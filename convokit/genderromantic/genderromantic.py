from convokit.model import Corpus, User
from convokit.transformer import Transformer
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize, wordpunct_tokenize
import re
from tqdm import tqdm

class Genderromantic(Transformer):
    romantic_words = ["adorable","amazing","angel","babe","beau","beautiful","beloved","darling","dearest","enchanting","lover","gorgeous","handsome","heavenly","honey","life-changing","paramour","sweetheart","sweetie","swoon","wonderful","adore","admire","care","cherish","choose","daydream","delight","dream","need","prize","treasure","value","want","worship","yearn","date","love","kiss","sex","romance","romantic","hug","hot","cute"]

    def __init__(self, verbose=False):
        self.verbose=verbose
        ps = PorterStemmer()
        self.stemmed_romantic_words = [ps.stem(romantic_word) for romantic_word in  Genderromantic.romantic_words]
        pass
    
    @staticmethod
    def genderDictionary(arg):
        name_to_gender = {}
        for user in arg.iter_users():
            if user.name not in name_to_gender:
                if 'gender' in user.meta:
                    name_to_gender[user.name] = user.meta['gender']
                elif 'sex' in user.meta:
                    name_to_gender[user.name] = user.meta['sex']
                else:
                    raise EnvironmentError('Neither gender nor sex meta available for users.')
        return name_to_gender
        
    def transform(self, corpus: Corpus):
        # First get convenience dictionary mapping character names to genders
        name_to_gender = self.genderDictionary(corpus)
        # Also for convenience, instantiate your Porter Stemmer
        ps = PorterStemmer()
        # Init your current scene and initial gender values
        current_scene = next(corpus.iter_utterances()).id[:11]
        if 'gender' in next(corpus.iter_utterances()).user.meta:
            current_gender = next(corpus.iter_utterances()).user.meta['gender'].lower()
        elif 'sex' in next(corpus.iter_utterances()).user.meta:
            current_gender = next(corpus.iter_utterances()).user.meta['sex'].lower()
        only_male = 'female' not in current_gender and 'male' in current_gender
        only_female = 'female' in current_gender
        conversation_gender = {}

        for utt in tqdm(corpus.iter_utterances()):
            speaker_name = utt.user.name
            speaker_gender = name_to_gender[speaker_name]
            # speaker_gender = utt.user.meta['gender'].lower() or utt.user.meta['sex'].lower()
            speaker_is_female = speaker_gender == 'female'

            contains_romantic = False
            male_about_female = False
            male_about_male = False
            female_about_male = False
            female_about_female = False

            # First handle contains_romantic.
            if 'tokens' in utt.meta:
                tokens = utt.meta['tokens']
            else:
                tokens = [wordpunct_tokenize(utt.text)]
                # tokens = sent_tokenize(utt.text)

            for sentence in tokens:
                for token in sentence:
                    word = re.sub(r'[^\w\s]', '', token)
                    word = word.lower()
                    ps_stem_word = ps.stem(word)
                    if ps_stem_word in self.stemmed_romantic_words:
                        contains_romantic = True
                        break

            # Then handle gender
            if 'character_entities' in utt.meta:
                # If character entities are present, i.e. for the Friends corpus, use them to derive male_about_female, female_about_male and contains_romantic.
                character_entities = utt.meta['character_entities']
                if character_entities is not None:        
                    for ces in character_entities:
                        if len(ces) == 0:
                            continue
                        for ce in ces:
                            if len(ce) == 0 or ce[2] == speaker_name or ce[2][0] == '#':
                                continue
                            if ce[2] not in name_to_gender:
                                if ce[2].startswith('Man'):
                                    male_about_female = False
                                    female_about_male = speaker_is_female
                                    male_about_male =  not speaker_is_female
                                    female_about_female = False
                                elif ce[2].startswith('Woman'):
                                    male_about_female = not speaker_is_female
                                    female_about_male = False
                                    male_about_male = False
                                    female_about_female = speaker_is_female
                            elif 'female' in name_to_gender[ce[2]]:
                                male_about_female = not speaker_is_female
                                female_about_male = False
                                male_about_male = False
                                female_about_female = speaker_is_female
                            elif 'male' in name_to_gender[ce[2]]:
                                male_about_female = False
                                female_about_male = speaker_is_female
                                male_about_male =  not speaker_is_female
                                female_about_female = False
            else:
            # If character entities are not present, do this based on pronouns in the utterance text.
            # First look at pronouns:
                for sentence in tokens:
                    for token in sentence:
                        word = re.sub(r'[^\w\s]', '', token)
                        word = word.lower()
                        if word == 'he' or word == 'him':
                            female_about_male = speaker_is_female #true iff the speaker is a female
                            male_about_female = False #false because this is _about_male
                        elif word == 'she' or word == 'her':
                            male_about_female = not speaker_is_female #true iff the speaker is not a female
                            female_about_male = False #false because this is _about_female

            utt.add_meta('female_about_female', female_about_female)
            utt.add_meta('female_about_male', female_about_male)
            utt.add_meta('male_about_female', male_about_female)
            utt.add_meta('male_about_male', male_about_male)
            utt.add_meta('contains_romantic', contains_romantic)

            # If you've told it to be verbose, it'll print examples for debugging
            if self.verbose:
                if male_about_female:
                    if contains_romantic:
                        print('found male speaking romance and also about a female:\n{}: {}\n'.format(utt.user.name, utt.text))
                    else:
                        print('found male speaking about female:\n{}: {}\n'.format(utt.user.name, utt.text))
                elif female_about_male:
                    if contains_romantic:
                        print('found female speaking romance and also about a male:\n{}: {}\n'.format(utt.user.name, utt.text))
                    else:
                        print('found female speaking about male:\n{}: {}\n'.format(utt.user.name, utt.text))
                # else:
                #     print('nothing found:\n{}, {}: {}'.format(utt.user.name, utt.user.meta['sex'], tokens))

            # Then get the conversation-level gender attributes
            if current_scene == utt.id[:11]:
                if 'female' in speaker_gender:
                    only_male = False
                elif 'male' in speaker_gender:
                    only_female = False
                else:
                    only_female = False
                    only_male = False
            else:
                conversation_gender[current_scene] = {'only_male': only_male, 'only_female': only_female}
                current_scene = utt.id[:11]
                only_male = 'female' not in speaker_gender and 'male' in speaker_gender
                only_female = 'female' in speaker_gender

        corpus.conversations['meta'] = conversation_gender
        return corpus
