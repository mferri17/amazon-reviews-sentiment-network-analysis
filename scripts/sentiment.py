import argparse, sys
from loadDataset import getDF
from absa import absa

parser=argparse.ArgumentParser()

parser.add_argument('--source', help='Text review or dataset path', default='reviews_Clothing_Shoes_and_Jewelry_5.json.gz')
parser.add_argument('--threshold', help='Threshold to filter aspects', default=0, type=int)

args = parser.parse_args()

reviews = ""

# source is a dataset
if args.source.endswith('.json.gz'):
    # load dataset from disk, avoid additional download time
    df = getDF(args.source)

    # get most frequent product and extract reviews
    productID = df.asin.mode().iloc[0]
    dfProduct = df[df['asin'] == productID]

    for index, row in dfProduct.iterrows():
        reviews = reviews + row.reviewText
# source is a string, so a review
else:
    reviews = args.source

absa(reviews, args.threshold)
