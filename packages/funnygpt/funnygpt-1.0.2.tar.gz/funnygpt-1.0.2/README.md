# Contributors
[Angela Tao](https://github.com/xinrantaoangela)

[Luke Bernstein](https://github.com/lnbernstein)

[Charles Hu](https://github.com/comeom)

[James Luo](https://github.com/jamesluo802)

# [Python Package: Foo Barstein](https://pypi.org/project/funny-gpt-stuytowners/)
#### What is this package?
This package was created so you can have Professor Foo Barstein talk with you straight from your terminal. Professor Barstein can do four things - tell you a joke, tell you a haiku, tell you a compliment, and write you an email. Professor Barstein is a fictional character and powered by GPT-3.

### Features
1. gptchat: will take the role of Professor Foo Barstein and use ChatGPT to generate a joke, haiku, compliment, or an email so you don't have to be lonely in your terminal anymore. 

2. cowtalk: will take the response from ChatGPT-3 and add "moo" every 3 words so you can talk with cows!
  
3. onewordperline: onewordperline will play around with how the text is displayed. Instead of left to right, you will be reading from top to bottom. 

4. changepreset: changepreset will change how ChatGPT answers your question. Use this function to give ChatGPT a different role than Professor Foo Barstein! 


### How to Run demo
1. Set your OpenAI API Key by writing the following command in the shell:
  ```export OPENAI_API_KEY=(your key)```
2. Run demo.py with the pipfile with the following command:
  ```pipenv run python demo.py```

### How to run tests
1. go to tests folder by writing the following command in the shell:
   ```cd tests```
2. install all necessary packages by writing the following command in the shell:
   ```pip install openai```
   ```pip install pytest```
3. Set your OpenAI API Key by writing the following command in the shell:
  ```export OPENAI_API_KEY=(your key)```
4.run tests by writing the following command in the shell:
  ```pytest test_functions.py```

