
import pandas as pd
from bs4 import BeautifulSoup
import requests


data = pd.read_csv("Vocab #4.csv", sep=",")
data = data[["Vocab Word"]]
list_data = data.values.tolist()
words = []
for word in list_data:
	words.append(word[0])

all_pos = []
all_definitions = []
all_conjugations = []
for word in words:
	# print(word)
	url = "https://www.merriam-webster.com/dictionary/" + word
	response = requests.get(url)
	page_contents = response.text
	doc = BeautifulSoup(page_contents, 'html.parser')
	pos_tag = doc.find('a', {'class': 'important-blue-link'})
	definition_tags = doc.find_all('span', {'class': 'dtText'})
	pos = pos_tag.text
	all_pos.append(pos)
	definitions_list = []
	for tag in definition_tags:
		definitions_list.append(tag.text)
	definition = "; ".join(definitions_list)
	definition = definition.replace(": ", "")
	all_definitions.append(definition)
	conj_tags = doc.find_all('span', {'class': 'ure'})
	conj_pos_tags = doc.find_all('span', {'class': 'fl'})
	conj_words = []
	conj_pos = []
	conjugations_list = []
	count = 0
	for tag in conj_tags:
		count+=1
		conj_words.append(tag.text)
	for tag in conj_pos_tags:
		if len(tag.find_all()) == 0:
			conj_pos.append(tag.text)
	for i in range(count):
		conjugations_list.append(conj_words[i] + " (" + conj_pos[i] + ")")
	conjugation = "; ".join(conjugations_list)
	all_conjugations.append(conjugation)


vocab_dict = {
	'Vocab Word': [],
	'part of speech': [],
	'definition': [],
	'conjugations': [],
	'Use the word in an original sentence.': []
}
for i in range(len(words)):
	vocab_dict['Vocab Word'].append(words[i])
	vocab_dict['part of speech'].append(all_pos[i])
	vocab_dict['definition'].append(all_definitions[i])
	vocab_dict['conjugations'].append(all_conjugations[i])
	vocab_dict['Use the word in an original sentence.'].append('')

df = pd.DataFrame(vocab_dict)
df.to_csv('apmc_vocab_4_filled.csv',index=False)





