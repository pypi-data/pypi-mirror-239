# SentenceSplitter

SentenceSplitter is a Python library for splitting text into sentences. It provides a simple and efficient way to tokenize text paragraphs into individual sentences.

## Installation

You can install SentenceSplitter using pip:

```bash
pip install sentencesplitter
```

## Usage
Here's how you can use SentenceSplitter in your Python code:

```python
from sentencesplitter import split_sentences

text = "This is a sample paragraph. It contains multiple sentences. SentenceSplitter will split it into individual sentences."
sentences = split_sentences(text)

for sentence in sentences:
    print(sentence)
```

## Features
* Splits text paragraphs into sentences.
* Handles various punctuation marks and edge cases.
* Easy integration into your projects.

## License
SentenceSplitter is licensed under the MIT License. See the LICENSE file for details.

## Contributing
Contributions are welcome! If you'd like to contribute to SentenceSplitter, please open an issue or a pull request on the GitHub repository.

## Support and Feedback
If you have any questions, feedback, or encounter issues while using SentenceSplitter, please feel free to open an issue on the GitHub repository.

## Credits
SentenceSplitter is maintained by [Your Name].

## Acknowledgments
SentenceSplitter makes use of the spaCy library for natural language processing.

## Related Projects
spaCy: The library used for tokenization in SentenceSplitter.