from bs4 import BeautifulSoup
import urllib
import json

def get_soup(url,header):
    return BeautifulSoup(urllib.request.urlopen(urllib.request.Request(url,headers=header)),'html.parser')



def scrape_google_image(query,num = 1,address = None, name = None):
    query= query.split()
    query='+'.join(query)
    url="https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch"
    header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
    soup = get_soup(url,header)
    
    Images_Links = []
    i=0
    for a in soup.find_all("div",{"class":"rg_meta"}):
        link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
        Images_Links.append((link,Type))
        i+=1
        print("scraping google images: "+str(i)+"%",end='\r')  
            
    ActualImages = []
    
    for i in range(len(Images_Links)):
        if Images_Links[i][0].split(".")[-1] in ["png","jpeg","jpg"]:
            ActualImages.append(Images_Links[i][0])
    if name == None:
        name = query
    print("\n")
    for i in range(num):
        try:
            if num > 0:
                if name is None:
                    urllib.request.urlretrieve(ActualImages[i],str(i)+"."+ActualImages[i].split(".")[-1])
                    print("Images Downloaded: "+ str(i/num*100) + "%",end = "\r" )
                else:
                    urllib.request.urlretrieve(ActualImages[i],"./images/"+name+"_"+str(i)+"."+ActualImages[i].split(".")[-1])
                    print("Images Downloaded: "+ str(i/num*100) + "%",end = '\r' )
            else:
                break
        except:
            continue
        
if __name__ == '__main__':
    query = input("Enter the keyword: ")
    no = int(input("Enter no of images (max = 100): "))
    address = input("Enter the directory")
    name = input("Name of the file (for one image): ")
    scrape_google_image(query,no,address,name)
