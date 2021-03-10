
class Review:
    def __init__(self, rev_block):
        self.rev_block = rev_block
        self.rev_id = rev_block['data-entry-id']
        self.desc = self.getDesc()
        self.stars = self.getStars()
        self.author = self.getAuthor()
        self.rev_positive_votes = self.getPositiveVotes()
        self.rev_negative_votes = self.getNegativeVotes()
        self.recommended = self.getRecommended()
        self.rev_date = self.getRevDate()
        self.buy_date = self.getBuyDate()
        self.pros = self.getPros()
        self.pros_count = self.getProsCount()
        self.cons = self.getCons()
        self.cons_count = self.getConsCount()
        self.bought = self.getBought()
        self.rev_block=1

    def getProsCount(self):
        return len(self.pros)

    def getConsCount(self):
        return len(self.cons)

    def getPositiveVotes(self):
        vote_button = self.rev_block.find("button", attrs={"data-review-id": self.rev_id,
                                                           "class": 'vote-yes js_product-review-vote js_vote-yes'})
        return vote_button['data-total-vote']

    def getNegativeVotes(self):
        vote_button = self.rev_block.find("button", attrs={"data-review-id": self.rev_id,
                                                           "class": 'vote-no js_product-review-vote js_vote-no'})
        return vote_button['data-total-vote']

    def getBought(self):
        return True if self.rev_block.find(class_='review-pz') else False

    def getDesc(self):
        return self.rev_block.find(class_='user-post__text').text

    def getStars(self):
        return self.rev_block.find(class_='user-post__score-count').text

    def getAuthor(self):
        return self.rev_block.find(class_='user-post__author-name').text

    def getRecommended(self):
        recomendation = ''
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
            for x in col:
                if x.find(class_='review-feature__title review-feature__title--positives'):
                    pros = x.find_all(class_='review-feature__item')
                    for pro in pros:
                        pros_list.append(pro.text)
        return pros_list

    def getCons(self):
        cons_list = []
        if self.rev_block.find(class_='review-feature'):
            col = self.rev_block.find_all(class_='review-feature__col')
            for x in col:
                if x.find(class_='review-feature__title review-feature__title--negatives'):
                    cons = x.find_all(class_='review-feature__item')
                    for con in cons:
                        cons_list.append(con.text)
        return cons_list
