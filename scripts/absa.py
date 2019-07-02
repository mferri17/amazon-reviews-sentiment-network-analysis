import os
import json
import re
import nltk
import ast
import math, itertools, operator
from textblob import TextBlob
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer

def preProcessing(input):
    string = input.lower()

    stopwords = nltk.corpus.stopwords.words("english")
    stopwords.append('OMG')
    stopwords.append(':-)')

    result=(' '.join([word for word in string.split() if word not in stopwords]))
    print('Following are the Stop Words')
    print(stopwords)
    result=str(result)
    result=re.sub(r'\(.*?\)','',result)
    print(result)
    return result

def tokenizeReviews(input):
    tokenizedReviews={}
    tokenizer = nltk.tokenize.punkt.PunktSentenceTokenizer()
    id=1;
    stopwords = nltk.corpus.stopwords.words("english")
    regexp = re.compile(r'\?')
    for sentence in tokenizer.tokenize(input):
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


def posTagging(input):
    outputPost={}
    for key,value in input.items():
        outputPost[key]=nltk.pos_tag(nltk.word_tokenize(value))

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
    lemmatizer = WordNetLemmatizer()
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

def identifyOpinion(review, aspect, tokenized):
    output={}
    for aspect,no in aspect:
        count=0
        p=0
        ng=0
        n=0
        for key,value in tokenized.items():
            if(aspect in str(value).upper()):
                count=count+1
                a=TextBlob(value)
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
                    output[aspect]["neutral"]["score"]+=1
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


def absa(reviews, threshold):
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
    opinion=identifyOpinion(postagged,aspects,tokenized)
    f = open("output.json",'w')
    json.dump(opinion,f,indent=4)
    f.close()
    return opinion
