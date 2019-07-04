import os
import json
import re
import nltk
import ast
import math, itertools, operator
from textblob import TextBlob
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import word_tokenize

#nltk.download('punkt')
#nltk.download('stopwords')

contractions_dict = { 
"ain't": "am not / are not / is not / has not / have not",
"aren't": "are not / am not",
"can't": "cannot",
"can't've": "cannot have",
"'cause": "because",
"could've": "could have",
"couldn't": "could not",
"couldn't've": "could not have",
"didn't": "did not",
"doesn't": "does not",
"don't": "do not",
"hadn't": "had not",
"hadn't've": "had not have",
"hasn't": "has not",
"haven't": "have not",
"he'd": "he had / he would",
"he'd've": "he would have",
"he'll": "he shall / he will",
"he'll've": "he shall have / he will have",
"he's": "he has / he is",
"how'd": "how did",
"how'd'y": "how do you",
"how'll": "how will",
"how's": "how has / how is / how does",
"I'd": "I had / I would",
"I'd've": "I would have",
"I'll": "I shall / I will",
"I'll've": "I shall have / I will have",
"I'm": "I am",
"I've": "I have",
"isn't": "is not",
"it'd": "it had / it would",
"it'd've": "it would have",
"it'll": "it shall / it will",
"it'll've": "it shall have / it will have",
"it's": "it has / it is",
"let's": "let us",
"ma'am": "madam",
"mayn't": "may not",
"might've": "might have",
"mightn't": "might not",
"mightn't've": "might not have",
"must've": "must have",
"mustn't": "must not",
"mustn't've": "must not have",
"needn't": "need not",
"needn't've": "need not have",
"o'clock": "of the clock",
"oughtn't": "ought not",
"oughtn't've": "ought not have",
"shan't": "shall not",
"sha'n't": "shall not",
"shan't've": "shall not have",
"she'd": "she had / she would",
"she'd've": "she would have",
"she'll": "she shall / she will",
"she'll've": "she shall have / she will have",
"she's": "she has / she is",
"should've": "should have",
"shouldn't": "should not",
"shouldn't've": "should not have",
"so've": "so have",
"so's": "so as / so is",
"that'd": "that would / that had",
"that'd've": "that would have",
"that's": "that has / that is",
"there'd": "there had / there would",
"there'd've": "there would have",
"there's": "there has / there is",
"they'd": "they had / they would",
"they'd've": "they would have",
"they'll": "they shall / they will",
"they'll've": "they shall have / they will have",
"they're": "they are",
"they've": "they have",
"to've": "to have",
"wasn't": "was not",
"we'd": "we had / we would",
"we'd've": "we would have",
"we'll": "we will",
"we'll've": "we will have",
"we're": "we are",
"we've": "we have",
"weren't": "were not",
"what'll": "what shall / what will",
"what'll've": "what shall have / what will have",
"what're": "what are",
"what's": "what has / what is",
"what've": "what have",
"when's": "when has / when is",
"when've": "when have",
"where'd": "where did",
"where's": "where has / where is",
"where've": "where have",
"who'll": "who shall / who will",
"who'll've": "who shall have / who will have",
"who's": "who has / who is",
"who've": "who have",
"why's": "why has / why is",
"why've": "why have",
"will've": "will have",
"won't": "will not",
"won't've": "will not have",
"would've": "would have",
"wouldn't": "would not",
"wouldn't've": "would not have",
"y'all": "you all",
"y'all'd": "you all would",
"y'all'd've": "you all would have",
"y'all're": "you all are",
"y'all've": "you all have",
"you'd": "you had / you would",
"you'd've": "you would have",
"you'll": "you shall / you will",
"you'll've": "you shall have / you will have",
"you're": "you are",
"you've": "you have"
}

lemmatizer = WordNetLemmatizer()

contractions_re = re.compile('(%s)' % '|'.join(contractions_dict.keys()))

def expand_contractions(string, contractions_dict=contractions_dict):
    def replace(match):
        return contractions_dict[match.group(0)]
    return contractions_re.sub(replace, string)

punctuation_re = re.compile('([!,.:;?])(\w)')

def fix_punctuation(string, contractions_dict=contractions_dict):
    def replace(match):
        print(match)
        print(match.group(1) + ' ' + match.group(2))
        return match.group(1) + ' ' + match.group(2)
    return punctuation_re.sub(replace, string)

def preProcessing(input):
    string = input #.lower()
    
    string = fix_punctuation(string)
    string = expand_contractions(string)

    stopwords = nltk.corpus.stopwords.words("english")
    stopwords.append('OMG')
    stopwords.append(':-)')
    stopwords.append(':)')
    stopwords.remove('not')
    stopwords.remove('and')
    stopwords.remove('or')
    stopwords.remove('but')

    result=(' '.join([word for word in string.split() if word not in stopwords]))
    print('Following are the Stop Words')
    print(stopwords)
    result=str(result)
    result=re.sub(r'\(.*?\)','',result)
    print(result)
    return result

def tokenizeReviews(input):
    tokenizedReviews={}
    id=1
    stopwords = nltk.corpus.stopwords.words("english")
    regexp = re.compile(r'\?')
    for sentence in nltk.sent_tokenize(input):
        #logic to remove questions and errors
        if regexp.search(sentence):
            print("removed")
        else:
            sentence=re.sub(r'\(.*?\)','',sentence)
            tokenizedReviews[id]=sentence
            id+=1

    for key,value in tokenizedReviews.items():
        print(key,' ',value)
        tokenizedReviews[key]=value
    return tokenizedReviews

punctuation = '!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~'

def posTagging(input):
    outputPost={}
    for key,value in input.items():
        outputPost[key] = nltk.pos_tag(nltk.word_tokenize(value))
        outputPost[key] = list(filter(lambda x: not x[0] in punctuation, outputPost[key]))

    for key,value in outputPost.items():
        print(key,' ',value)
        return outputPost

def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return None

def lemmatize(input):
    lemmatized = {}
    for key,value in input.items():
        lemmatized[key] = []
        for word,tag in value:
            wntag = get_wordnet_pos(tag)
            if wntag is None:
                lemma = lemmatizer.lemmatize(word) 
            else:
                lemma = lemmatizer.lemmatize(word, pos=wntag) 
            lemmatized[key].append((lemma, tag))
    
    
    for key,value in lemmatized.items():
        print(key,' ',value)
        return lemmatized

def aspectExtraction(input, threshold):
    prevWord=''
    prevTag=''
    currWord=''
    aspectList=[]
    outputDict={}
    #Extracting Aspects
    for key,value in input.items():
        for word,tag in value:
            if(tag=='NN' or tag=='NNP'):
                if(prevTag=='NN' or prevTag=='NNP'):
                    currWord= prevWord + ' ' + word
                else:
                    aspectList.append(prevWord.upper())
                    currWord= word
            prevWord=currWord
            prevTag=tag
    #Eliminating aspect count less than threshold
    for aspect in aspectList:
            if(aspectList.count(aspect)>threshold):
                    if(outputDict.keys()!=aspect):
                            outputDict[aspect]=aspectList.count(aspect)
    outputAspect=sorted(outputDict.items(), key=lambda x: x[1],reverse = True)
    print(outputAspect)
    return outputAspect

#function to add upto 100 and round
def apportion_pcts(pcts, total):
    proportions = [total * (pct / 100) for pct in pcts]
    apportions = [math.floor(p) for p in proportions]
    remainder = total - sum(apportions)
    remainders = [(i, p - math.floor(p)) for (i, p) in enumerate(proportions)]
    remainders.sort(key=operator.itemgetter(1), reverse=True)
    for (i, _) in itertools.cycle(remainders):
        if remainder == 0:
            break
        else:
            apportions[i] += 1
            remainder -= 1
    return apportions

def identifyOpinion(aspect, tokenized):
    output={}
    lemmatized = {
        key: [lemmatizer.lemmatize(word) for word in word_tokenize(str(value).upper())]
        for key,value in tokenized.items()
    }
    for aspect,no in aspect:
        count=0
        p=0
        ng=0
        n=0
        for key,value in lemmatized.items():
            # check if lemmatized aspect is a subset of lemmatized sentence
            # or if aspect is present in sentece
            if(set(aspect.split(' ')) <= set(value) or aspect in tokenized[key]):
                count=count+1
                a=TextBlob(tokenized[key])
                output.setdefault(aspect, {
                    "positive": {
                        "score": 0,
                        "percent": 0,
                        "sentences": [],
                        "adjectives": []
                    },
                    "negative": {
                        "score": 0,
                        "percent": 0,
                        "sentences": [],
                        "adjectives": []
                    },
                    "neutral": {
                        "score": 0,
                        "percent": 0,
                        "sentences": [],
                        "adjectives": []
                    },
                })
                pol=a.sentiment.polarity
                print(pol)

                if (pol>0):
                    p=p+1
                    output[aspect]["positive"]["score"]+=pol
                    output[aspect]["positive"]["sentences"].append(tokenized[key])
                    for words,pos in a.tags:
                        if pos == 'JJ':
                            output[aspect]["positive"]["adjectives"].append(words)
                elif(pol<0):
                    ng=ng+1
                    output[aspect]["negative"]["score"]+=pol
                    output[aspect]["negative"]["sentences"].append(tokenized[key])
                    for words,pos in a.tags:
                        if pos == 'JJ':
                            output[aspect]["negative"]["adjectives"].append(words)
                else:
                    n=n+1
                    output[aspect]["neutral"]["sentences"].append(tokenized[key])
                    for words,pos in a.tags:
                        if pos == 'JJ':
                            output[aspect]["neutral"]["adjectives"].append(words)

        if(p>0):
            output[aspect]["positive"]["score"]=round(output[aspect]["positive"]["score"]/p,1)
            output[aspect]["positive"]["percent"]=(p/count)*100
        if(ng>0):
            output[aspect]["negative"]["score"]=round(output[aspect]["negative"]["score"]/ng,1)
            output[aspect]["negative"]["percent"]=(ng/count)*100
        if(n>0):
            output[aspect]["neutral"]["score"]=round(output[aspect]["neutral"]["score"]/n,1)
            output[aspect]["neutral"]["percent"]=(n/count)*100

        perc = apportion_pcts([
            output[aspect]["positive"]["percent"],
            output[aspect]["negative"]["percent"],
            output[aspect]["neutral"]["percent"]
        ],100)

        output[aspect]["positive"]["percent"] = perc[0]
        output[aspect]["negative"]["percent"] = perc[1]
        output[aspect]["neutral"]["percent"] = perc[2]

        # make list unique
        output[aspect]["positive"]["adjectives"] = list(set(output[aspect]["positive"]["adjectives"]))
        output[aspect]["negative"]["adjectives"] = list(set(output[aspect]["negative"]["adjectives"]))
        output[aspect]["neutral"]["adjectives"] = list(set(output[aspect]["neutral"]["adjectives"]))

    return output


def absa(reviews, threshold, out_file):
    print("\n\n\n#### Pre Processing ####\n")
    pre = preProcessing(reviews)
    print("\n\n\n#### Splitting into sentence ####\n")
    tokenized = tokenizeReviews(pre)
    print("\n\n\n#### Pos Tagging ####\n")
    postagged = posTagging(tokenized)
    print("\n\n\n#### Lemmatization ####\n")
    postagged = lemmatize(postagged)
    print("\n\n\n#### Aspect Identification ####\n")
    aspects = aspectExtraction(postagged, threshold)
    print("\n\n\n#### Opinion mining ####\n")
    opinion=identifyOpinion(aspects,tokenized)
    f = open(out_file,'w')
    json.dump(opinion,f,indent=4)
    f.close()
    return opinion
