import csv
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.externals import joblib
from sklearn.feature_extraction import DictVectorizer
import sys

corpus1 = []
impact1 = []

corpus2 = {}

impact2 = []

range1 = 120000
range2 = 128000
input1 = ""
if len(sys.argv) > 1:
    input1 = sys.argv[1]
else:
    sys.exit(0)

labels = ["CB_PROB", "CLOUDCEILING", "TEMPO_CLOUDCEILING", "ICE_HIGH", "ICE_INTENSITY", "ICE_LOW", "INVERSION", "LVP_PROB", "RAIN", "SNOW", "TEMPERATURE", "DEW_POINT", "SHEAR_HIGH", "SHEAR_INTENSITY", "SHEAR_LOW", "TURB_HIGH", "TURB_INTENSITY", "TURB_LOW", "VIS", "VIS_TEMPO", "WW", "WW_TEMPO", "WD", "WD_1000", "WD_2000", "WD_050", "WD_100", "WG", "WS", "WS_1000", "WS_2000", "WS_050", "WS_100", "RWY04_CROSSWIND", "RWY04_TAILWIND", "RWY04_1000FT_TAILWIND", "RWY22_CROSSWIND", "RWY22_TAILWIND", "RWY22_1000FT_TAILWIND", "RWY15_CROSSWIND", "RWY15_TAILWIND", "RWY15_1000FT_TAILWIND", "RWY33_CROSSWIND", "RWY33_TAILWIND", "RWY33_1000FT_TAILWIND"]
# input1 = "0,0,9900,,,,,,0,0,0,,,,,,,,,9900,9900,CAVOK,,300,330,330,310,310,11,6,25,25,20,25,6,2,0,6,0,5,3,5,25,3,0,0"

clf = joblib.load('ForestClassifierModel.pkl')

transformer = TfidfTransformer(smooth_idf=False)
vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.8)

dictVectorizer = DictVectorizer(sparse=False)

with open('labeled_weather_data__vol2.csv', 'rb') as csvfile:
    reader = csv.DictReader(csvfile)
    for i in range(0, range1):
        row = reader.next()
        if 'IMPACT' in row:
            if row['IMPACT'] == "2" or row['IMPACT'] == "1" or row['IMPACT'] == "-1" or row['IMPACT'] == "-2":
                corpus1.append(row)
                impact1.append(row['IMPACT'])
        impact1.append(row['IMPACT'])
        if 'IMPACT' in row:
            del row['IMPACT']
        corpus1.append(row)
input1list = input1.split(",")


for i in range(0, len(input1list)):
    corpus2[labels[i]] = input1list[i]
    if 'IMPACT' in corpus2:
        del corpus2['IMPACT']
    # print corpus2[labels[i]]

# print corpus2

# print "Start frequency counting.."
frequencyCountTransformArray = dictVectorizer.fit_transform(corpus1)
# print "Finish frequency counting.."

newTfidf = dictVectorizer.transform(corpus2)
predicted = clf.predict(newTfidf)

print predicted
