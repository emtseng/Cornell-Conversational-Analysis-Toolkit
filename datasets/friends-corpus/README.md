# Friends Dataset

A collection of all the conversations that occurred over 10 seasons of <i>Friends</i>, parsed into ConvoKit format.

## Dataset Details

### User-level information

Users in this dataset are characters in a given scene. The original dataset provides each character's name as a `<str>`, which is what we index Users by. 

We add the following as user-level metadata:

- <b>first_appearance</b>: `<str>`, the episode in which the character first appeared, i.e. 's01_e01' for season 1, episode 1.
- <b>gender</b>: `<str>`, the `gender_guesser` module's guess at the character's gender.

### Utterance-level information

This dataset contains a wealth of information at the utterance level.

For each Utterance we provide:

- **id:** `<int>`, index of the utterance
- **user:** `<str>`, the user who authored the utterance.
- **root:** `<int>`, id of the conversation root of the utterance.
- **reply_to:** `<int>`, id of the utterance to which this utterance replies to. `None` if the utterance is not a reply.
- **timestamp:** `None`. Our dataset does not contain timestamp information for utterances.
- **text:** `<str>`, The textual content of the utterance.

We include metadata as follows:

- **tokens:** `list <str>`, a tokenized representation of the text (handy for sentence separation)
- **emotion** `list <str>`, emotion labels for each token. Available for some but not all utterances; `None` if unavailable.
- **transcript_with_note:** `<str>`, a version of the text with an action note (e.g. "(to Ross) Hand me the coffee" vs. "Hand me the coffee"). Available for some but not all utterances; `None` if unavailable.
- **tokens_with_note:** `list <str>`, a tokenized representation of the above.
- **caption:** `<str>`, available for some but not all utterances; `None` if unavailable.
- **character_entities:** `list <str>`, available for some but not all utterances; `None` if unavailable.

### Conversation-level information

TODO

### Corpus-level information

We include:

- **name:** `<str>`, the corpus name ('Friends Dataset').

### Quick Stats

```
Number of Users: 699
Number of Utterances: 61338
Number of Conversations: 3099
```

## Usage

## Notes

The original dataset is available [here](https://github.com/emorynlp/character-mining) from the Emory NLP group.

## Contact

Corpus translated into ConvoKit format by Katharine Sadowski, Emily Tseng and Nianyi Wang.