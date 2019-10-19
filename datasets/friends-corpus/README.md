# Friends Dataset

A collection of all the conversations that occurred over 10 seasons of <i>Friends</i>, parsed into ConvoKit format. Across the 10 seasons there are 236 episodes, 3,107 scenes/conversations, and 67,373 utterances.

## Dataset Details

### User-level information

Users in this dataset are characters in a given scene. The original dataset provides each character's name as a `<str>`, i.e. `"Monica Geller"`. We index Users by their names.

Note we add a dummy user named and indexed as `"TRANSCRIPT_NOTE"` for utterances that are not a character speaking, but instead a note in the transcript, i.e. "<i>[Time Lapse, Ross has entered.]</i>".

### Utterance-level information

This dataset contains a wealth of information at the utterance level.

For each Utterance we provide:

- **id:** `<int>`, the index of the utterance in the format `sAA_eBB_cCC_uDDDD`, where `AA` is the season number, `BB` is the episode number, `CC` is the scene/conversation number, and `DDDD` is the number of the utterance in the scene (e.g. `s01_e18_c05_u021`).
- **user:** `<str>`, the user who authored the utterance, or the speaker in our case (e.g., Monica Geller).
- **root:** `<int>`, the id of the conversation root of the utterance. We assume conversations begin at the start of a new scene.
- **reply_to:** `<int>`, the id of the utterance to which this utterance replies to. `None` if the utterance is the first in a conversation.
- **timestamp:** `None`. Our dataset does not contain timestamp information for utterances.
- **text:** `<str>`, the textual content of the utterance.

We include metadata as follows:

- **tokens:** `list <str>`, a tokenized representation of the text (handy for sentence separation)
- **emotion** `list <str>`, emotion labels for each token. Available for some but not all utterances; `None` if unavailable.
- **transcript_with_note:** `<str>`, a version of the text with an action note (e.g. "(to Ross) Hand me the coffee" vs. "Hand me the coffee"). Available for some but not all utterances; `None` if unavailable.
- **tokens_with_note:** `list <str>`, a tokenized representation of the above.
- **caption:** `<str>`, contains the begin time, end time, and text sans punctuation. Available for some but not all utterances; `None` if unavailable. Only available for seasons 6-9.
- **character_entities:** `list <str>`, lists of characters who the User is speaking to and/or about. For example, say we have the tokenized utterances _[["There", "'s", "nothing", "to", "tell", "!"],["He", "'s", "just", "some", "guy", "I", "work", "with", "!"]]_ and character entities _[[],[[0, 1, "Paul the Wine Guy"], [4, 5, "Paul the Wine Guy"], [5, 6, "Monica Geller"]]]_. The character entities tell us no one gets referred in the first sentence, and in the second sentence, "_He_" at index 0 and "_guy_" at index 4 refer to "_Paul the Wine Guy_", and "_I_" at index 5 refers to "_Monica Geller_". Available for some but not all utterances; `None` if unavailable.

### Conversation-level information

Conversations are indexed by the id of the first utterance that make the conversation. They contain the metadata as follows:

- **season**: `<str>`, the index of the season in the format `sXX`, where XX starts at `01` for season 1 and increments upwards to `10` for season 10.
- **episode**: `<str>`, the index of the episode in the format `eXX`, where XX starts at `01` for the first episode of the season and increments upwards.
- **scene**: `<str>`, the index of the scene in the episode in the format `cXX`, where XX starts at `01` for the first scene of the episode and increments upwards. Note that scenes are, for our intents and purposes, conversations.

### Corpus-level information

We include the following metadata:

- **name:** `<str>`, the corpus name ('Friends Dataset').

### Quick Stats

```
Number of Users: 700
Number of Utterances: 67373
Number of Conversations: 3107
```

## Usage

To download directly with ConvoKit:

```python
from convokit import Corpus, download
corpus = Corpus(filename=download("friends-corpus"))
```

## Notes

The original dataset is available [here] (https://github.com/emorynlp/character-mining) from the Emory NLP group.

## Contact

Corpus translated into ConvoKit format by Katharine Sadowski, Emily Tseng and Nianyi Wang.
