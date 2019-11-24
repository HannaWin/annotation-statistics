# emotion dictionary
annotation statistics for emotion analysis on a small corpus

## Corpus

The corpus is made of 3-star amazon reviews for Star Wars Jedi: Fallen Order (PS4).

The data is preprocessed to only keep words which were tagged as adjevtives (JJ) or verbs (VB, VBN), using the nltk perceptron POS-Tagger.

The final corpus is made of 98 unique words. 

## Analysis

* counts of labeled emotions
* counts of labeled sentiments 
* annotator agreement according to Cohen's Kappa
* list of words whose labels differ among annotators
