import nltk
from nltk.corpus import stopwords
nltk.download('averaged_perceptron_tagger') 


def word_tokenizer(text):
	"""tokenizes text for words"""
	from nltk.tokenize import word_tokenize
	#returns list of words:
	words = word_tokenize(text)
	return words


def nltk_pos_tagger(text):
	"""adds POS labels to tokenized sentences"""
	words = word_tokenizer(text)
	pos = nltk.pos_tag(words)
	with open("pos_tags_nltk.txt", "w") as f:
		for t in pos:
			f.write(t[0] + "\t" + t[1] + "\n")
	return pos


def remove_stop_words(text):
	"""saves content words in new list"""
	if type(text) == str:
		words = word_tokenizer(text)
	else:
		words = text
	content_words = list()
	for w in words:
		if w.lower() not in stopwords.words("english"):
			content_words.append(w)
	return content_words


def extract_nn_nd_adj(text):
	"""only keeps adjectives and verbs"""
	pos = nltk_pos_tagger(text)
	print(pos)
	jj_nn = list()
	accepted_pos = ("JJ", "VBN", "VB")
	for pair in pos:
		if pair[1] in accepted_pos:
			jj_nn.append(pair[0])
	final_words = remove_stop_words(jj_nn)
	return final_words


def unique_words(list_words):
	"""re-makes lst of words with only unique occurrences"""
	unique_words = list()
	for word in list_words:
		if word not in unique_words:
			unique_words.append(word)
	print(unique_words)
	print(len(unique_words))
	return unique_words





if __name__ == '__main__':
	with open("reviews.txt", "r") as f:
		reviews = f.read()
	print(len(reviews))
	words1 = extract_nn_nd_adj(reviews)
	words_final = unique_words(words1)
