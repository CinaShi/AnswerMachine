from nltk.parse import CoreNLPParser
from nltk import sent_tokenize
# parser = CoreNLPParser(url='http://localhost:9000')

# print(list(parser.parse('Jack is a boy . He is handsome .'.split())))

# print(list(parser.raw_parse('Jack is a boy . He is handsome .')))

from nltk.parse.corenlp import CoreNLPDependencyParser

dep_parser = CoreNLPDependencyParser(url='http://localhost:9000')


print('I am your dad , he is also your dad .'.split())
parses = dep_parser.parse('I am your dad , he is also your dad .'.split())

print([[(governor, dep, dependent) for governor, dep, dependent in parse.triples()] for parse in parses])

# parser = CoreNLPParser(url='http://localhost:9000')

# print(list(parser.tokenize('What is the airspeed of an unladen swallow?')))

# pos_tagger = CoreNLPParser(url='http://localhost:9000', tagtype='pos')

# print(list(pos_tagger.tag('What is the airspeed of an unladen swallow ?'.split())))

# ner_tagger = CoreNLPParser(url='http://localhost:9000', tagtype='ner')

# print(list(ner_tagger.tag(('Rami Eid is studying at Stony Brook University in NY'.split()))))

# tagger = CoreNLPParser(url='http://localhost:9000')

# tagger.parser_annotator='tokenize,ssplit,pos,lemma,ner,depparse,coref'

# text = "Barack Obama was born in Hawaii.  He is the president. Obama was elected in 2008. His dog is red."

# output = tagger.api_call(text)

def resolve(corenlp_output):
    """ Transfer the word form of the antecedent to its associated pronominal anaphor(s) """
    for coref in corenlp_output['corefs']:
        mentions = corenlp_output['corefs'][coref]
        antecedent = mentions[0]  # the antecedent is the first mention in the coreference chain
        for j in range(1, len(mentions)):
            mention = mentions[j]
            if mention['type'] == 'PRONOMINAL':
                # get the attributes of the target mention in the corresponding sentence
                target_sentence = mention['sentNum']
                target_token = mention['startIndex'] - 1
                # transfer the antecedent's word form to the appropriate token in the sentence
                corenlp_output['sentences'][target_sentence - 1]['tokens'][target_token]['word'] = antecedent['text']


def print_resolved(corenlp_output):
    """ Print the "resolved" output """
    output = ""
    possessives = ['hers', 'his', 'their', 'theirs']
    for sentence in corenlp_output['sentences']:
        for token in sentence['tokens']:
            output_word = token['word']
            # check lemmas as well as tags for possessive pronouns in case of tagging errors
            if token['lemma'] in possessives or token['pos'] == 'PRP$':
                output_word += "'s"  # add the possessive morpheme
            output_word += token['after']
            # print(output_word, end='')
            # print("debug")
            output += output_word
    return output
# resolve(output)

# print('Original:', text)
# print('Resolved: ', end='')

# print_resolved(output)
# print('\n')

def preprocessing(input_file):
	tagger = CoreNLPParser(url='http://localhost:9000')
	dep_parser = CoreNLPDependencyParser(url='http://localhost:9000')
	results = []
	with open(input_file, 'r') as f:
		i = 0
		for line in f:
			print("line " + str(i))
			print(len(line))
			if not line or line == "\n":
				continue
			tagger.parser_annotator='tokenize,ssplit,pos,lemma,ner,depparse,coref'
			output = tagger.api_call(line)
			resolve(output)
			output = print_resolved(output)
			tokens = sent_tokenize(output)
			for token in tokens:
				parses = dep_parser.parse(list(tokens))
				print(parses)
				results.append(parses)
			i += 1

preprocessing("../data/set1/a1.txt")


