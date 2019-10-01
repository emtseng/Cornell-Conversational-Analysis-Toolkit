# Convenience testing for genderromantic transformer

import convokit
from convokit import Corpus, Genderromantic

def run_stats(transformed_corpus: Corpus):
    male_speaking = 0
    male_speaking_about_female = 0
    male_speaking_about_female_romantic = 0

    male_speaking_not_about_female = 0

    female_speaking = 0
    female_speaking_about_male = 0
    female_speaking_about_male_romantic = 0

    female_speaking_not_about_male = 0

    romantic = 0
    not_romantic = 0

    utterance_ids = transformed_corpus.get_utterance_ids()

    for uid in utterance_ids:
        utt=transformed_corpus.get_utterance(uid)
        
        # First get whether it's a male or female speaker
        if 'gender' in utt.user.meta:
            speaker_gender = utt.user.meta['gender'].lower()
        elif 'sex' in utt.user.meta:
            speaker_gender = utt.user.meta['sex'].lower()

        if speaker_gender == "male":
            male_speaking += 1
        if speaker_gender == "female":
            female_speaking += 1
            
        # Then get whether the utterance is a male speaking about a female:
        if utt.meta["male_about_female"]:
            male_speaking_about_female += 1
            # And whether it was romantic
            if utt.meta["contains_romantic"]:
                male_speaking_about_female_romantic += 1
        else:
            male_speaking_not_about_female += 1
            
        # Then get whether the utterance is a female speaking about a male:
        if utt.meta["female_about_male"]:
            female_speaking_about_male += 1
            # And whether it was romantic
            if utt.meta["contains_romantic"]:
                female_speaking_about_male_romantic += 1
        else:
            female_speaking_not_about_male += 1
            
        # Then register whether the utt is romantic, period.
        rom=utt.meta["contains_romantic"]
        if rom:
            romantic += 1
        else:
            not_romantic += 1

    #Creating Percentages - help with graphs later
    perc_male_about_female=(float(male_speaking_about_female) / float(male_speaking))*100
    perc_male_about_female_rom=(float(male_speaking_about_female_romantic) / float(male_speaking_about_female))*100
    perc_female_about_male=(float(female_speaking_about_male) / float(female_speaking))*100
    perc_female_about_male_rom=(float(female_speaking_about_male_romantic) / float(female_speaking_about_male))*100
        
    print('male_speaking: ', male_speaking)
    print('male_speaking_about_female: ', male_speaking_about_female)
    print('male_speaking_about_female_romantic: ', male_speaking_about_female_romantic)
    print('pct male utterances about females', perc_male_about_female)
    print('pct male utterances about females that are romantic', perc_male_about_female_rom)
    print('male_speaking_not_about_female: ', male_speaking_not_about_female)
    print('\n')
    print('female_speaking: ', female_speaking)
    print('female_speaking_about_male: ', female_speaking_about_male)
    print('female_speaking_about_male_romantic: ', female_speaking_about_male_romantic)
    print('pct female utterances about males', perc_female_about_male)
    print('pct female utterances about males that are romantic', perc_female_about_male_rom)
    print('female_speaking_not_about_male: ', female_speaking_not_about_male)
    print('\n')
    print('romantic: ', romantic)
    print('not_romantic: ', not_romantic)


if __name__=="__main__":
    # corpus = Corpus(filename='./datasets/friends-corpus/corpus')
    corpus = Corpus(filename='./datasets/switchboard-corpus/corpus')
    grr = Genderromantic(verbose=True)
    transformed_corpus = grr.fit_transform(corpus)
    run_stats(transformed_corpus)
