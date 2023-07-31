import os
import requests
import scrapy
import datetime
import termcolor

class ImageDownloader:
    def __init__(self, url=""):
        print("Constructor called.")
        self.url = url
        self.destinationBase = "./images"

    def initialize(self):
        print("Initialize...")
        if self.url == "":
            self.askUrl()
        urlIsValid = self.checkIfUrlIsValid()
        if not urlIsValid:
            termcolor.cprint("Url is not valid.", "red", attrs=["bold"])
            exit()
        print("Initialize done.")
        pass

    def checkIfUrlIsValid(self):
        print("Check if url is valid...")
        # the url must match the pattern: http://subdomain.domain.com or https://subdomain.domain.com or http://domain.com or https://domain.com
        if not self.url.startswith("http") or not "://" in self.url or len(self.url.split("://")) < 2 or self.url.split("://")[1] == "" or not "." in self.url.split("//")[1] or len(self.url.split("//")[1].split(".")) < 1:
            return False

        # request the url
        try:
            requests.get(self.url)
        except:
            return False
        return True

    def getDomainName(self):
        print("Get domain name...")
        urlWithoutProtocol = self.url.split("//")[1]
        return urlWithoutProtocol.split("/")[0]
    
    def checkIfFoldersExist(self, domainName):
        print("Check if folders exist...")
        # check if destination folder exist
        if not os.path.exists(self.destinationBase):
            os.mkdir(self.destinationBase)

        # check if domain folder exist
        domainPath = self.destinationBase + "/" + domainName
        if not os.path.exists(domainPath):
            os.mkdir(domainPath)

        # check if date folder exist
        self.destinationPath = domainPath + "/" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        if not os.path.exists(self.destinationPath):
            os.mkdir(self.destinationPath)

        print("Check if folders exist done.")
        pass

    def downloadImage(self, image):
        # get image url
        imageUrl = image.xpath('@src').extract_first()
        if imageUrl is None:
            return

        # get image name
        imageName = imageUrl.split("/")[-1]
        if imageName is None:
            return

        # download image
        response = requests.get(imageUrl)
        if response.status_code == 200:
            with open(self.destinationPath + "/" + imageName, 'wb') as f:
                f.write(response.content)
        pass

    def startDownloading(self):
        self.initialize()
        print("Start downloading...")

        # check if destination folder exist
        self.checkIfFoldersExist(self.getDomainName())

        # request to url
        response = requests.get(self.url)
        document = scrapy.Selector(response=response)

        # get all images
        images = document.xpath('//img')
        for image in images:
            self.downloadImage(image)
            termcolor.cprint("Download " + image.xpath('@src').extract_first(), "blue", attrs=["bold"])

        termcolor.cprint("Download done.", "green", attrs=["bold"])
        pass



    def askUrl(self):
        self.url = input("Please input the url (start with http): ")
        while not self.url.startswith("http"):
            self.url = input("Please input a valida url (start with http): ")

    def kill(self):
        del self
        print("Killed.")
        pass