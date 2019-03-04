import nltk
import string

resultf = open("counts.txt", 'w')
for i in range(10):
	filename = "noun_counting_data/a" + str(i+1) + ".txt"
	filteredNouns = []
	outputFilename = "noun_counting_data/a" + str(i+1) + "-nouns.txt"
	of = open(outputFilename, 'w')
	with open(filename, 'r') as f:
		content = f.readlines()
		content = [x.strip() for x in content]
		# function to test if something is a noun
		is_noun = lambda pos: pos[:2] == 'NN'
		# do the nlp stuff
		content = " ".join(content)
		printable = set(string.printable)
		content = filter(lambda x: x in printable, content)
		tokenized = nltk.word_tokenize(content)
		nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)]
		resultf.write("a" + str(i+1) + " noun count: " + str(len(nouns)) + "\n")
		of.write(",".join(nouns))
	of.close()
resultf.close()