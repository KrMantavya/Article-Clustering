from bs4 import BeautifulSoup
import urllib2
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

def getAllDoxyDonkeyPosts(url,links):
    header={'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36'}
    response=urllib2.Request(url,headers=header)
    try:
        page=urllib2.urlopen(response)
    except urllib2.HTTPError, e:
        print 'error'
        return
    print 'page obtained'
    soup=BeautifulSoup(page)
    for a in soup.find_all('a'):
        url=a.get('href')
        url=str(url)
        title=a.get('title')
        title=str(title)
        if title=="Older Posts":
            print title,url
            links.append(url)
            getAllDoxyDonkeyPosts(url,links)
    return

def getDoxyDonkeyText(testUrl,token):
    header={'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36'}
    response=urllib2.Request(testUrl,headers=header)
    try:
        page=urllib2.urlopen(response)
    except urllib2.HTTPError, e:
        print 'error'
        return (None,None)
    print 'page obtained'
    soup=BeautifulSoup(page)
    if soup is None:
        return (None,None)
    title=soup.find("title").text
    mydivs=soup.find_all("div",{"class":token})
    text=' '.join(map(lambda p: p.text, mydivs))
    return text,title

blogUrl ="https://www.doxydonkey.blogspot.in/"
links=[]
getAllDoxyDonkeyPosts(blogUrl,links)
body=getDoxyDonkeyText(blogUrl,'post-body')
#print body[0]
doxyDonkeyPosts={}
print len(links)
for link in links:
    doxyDonkeyPosts[link]=getDoxyDonkeyText(link,'post-body')
print len(doxyDonkeyPosts)
documentCorpus=[]
for onePost in doxyDonkeyPosts.values():
    documentCorpus.append(onePost[0])

vectorizer=TfidfVectorizer(max,max_df=0.5,min_df=2,stop_words='english')

x=vectorizer.fit_transform(documentCorpus)
km=KMeans(n_cluster=5,init='k-means++',max_iter=100,n_init=1,verbose=True)
km.fit(X)

testUrl="http://doxydonkey.blogspot.in/2016/02/daily-tech-snippet-monday-february-29th.html"
testArticle=getDoxyDonkeyText(testUrl,'post-body')
testCorpus=[]
testCorpus.append(testArticle)
y=vectorizer.fit_transform(testCorpus)
print km.predict(y)
