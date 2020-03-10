# EngSub
Find and learn The difficult English words in your subtitles!

Wanna watch English movies but you are struggling with difficult words that you don't understand? Use EngSub to learn required words before watching a movie! There are just 3 steps:
1. Connect to Internet
2. Download the srt subtitles of your movies. you can check [yifysub](https://yifysub.net/) for English subtitles.
3. Download requirements: `pip install -r requirements.txt`
4. Run `DifficultFinder.py` with 4 arugements Subtitles directory, `en_50k_2.txt` path, ourput path, difficulty (between 0 to 10)

Example:

```sh
python DifficultFinder.py dataset/ en_50k_2.txt output.txt 7
```
 
 Your output should be with this format:
 
 ```sh
 [Word] [Difficulty]
 Meaning: [Cambridge Dictionary Link]
  [Part of Speach1]
      [Meaning1]
      [Meaning2]
      ...
 ```
 For example, this is a small chunk of the `output.txt` file:
 
![an example of expected output](https://raw.githubusercontent.com/amirmohammadkz/EngSub/master/assets/output.jpg)
