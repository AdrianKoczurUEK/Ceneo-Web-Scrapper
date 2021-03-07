from bs4 import BeautifulSoup as BS


class Review:
    def __init__(self,rev_block):
        self.rev_block=rev_block
        self.desc=self.getDesc()
        self.stars= self.getStars()
        self.author=self.getAuthor()
        self.recommended=self.getRecommended()
        self.rev_date=self.getRevDate()
        self.buy_date=self.getBuyDate()
        self.pros=self.getPros()
        self.cons=self.getCons()


    def getDesc(self):
        return self.rev_block.find(class_='user-post__text').text

    def getStars(self):
        return self.rev_block.find(class_='user-post__score-count').text

    def getAuthor(self):
        return self.rev_block.find(class_='user-post__author-name').text

    def getRecommended(self):
        recomendation=''
        if self.rev_block.find(class_='recommended'):
            recomendation = self.rev_block.find(class_='recommended').text
        elif self.rev_block.find(class_='not-recommended'):
            recomendation = self.rev_block.find(class_='not-recommended').text
        return recomendation

    def getRevDate(self):
        post_dates = self.rev_block.find(class_='user-post__published')
        user_dates = post_dates.find_all('time')
        return user_dates[0]['datetime']

    def getBuyDate(self):
        post_dates = self.rev_block.find(class_='user-post__published')
        user_dates = post_dates.find_all('time')
        try:
            return user_dates[1]['datetime']
        except:
            return ''

    def getPros(self):
        pros_list = []
        if self.rev_block.find(class_='review-feature'):
            col = self.rev_block.find_all(class_='review-feature__col')
            pros = col[0].find_all(class_='review-feature__item')
            for pro in pros:
                pros_list.append(pro.text)
        return pros_list

    def getCons(self):
        cons_list = []
        if self.rev_block.find(class_='review-feature'):
            col = self.rev_block.find_all(class_='review-feature__col')
            if len(col) > 1:
                cons = col[1].find_all(class_='review-feature__item')
                for con in cons:
                    cons_list.append(con.text)
        return cons_list