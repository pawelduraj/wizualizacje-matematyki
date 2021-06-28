class Answer():

    def __init__(self, text:str, is_good:bool):
        self.text = text
        self.is_good = is_good



class Question():

    def __init__(self, text:str, answer1:Answer, answer2:Answer, answer3:Answer):
        
        self.text = text
        self.answers = [answer1, answer2, answer3]
        for answer in self.answers:
            if answer.is_good == True:
                self.good_answer = self.answers.index(answer)

    def __str__(self):
        text = "Pytanie:\n" + self.text + "\n"
        for i in range(3):
            text += f"Odpowiedź {i+1} "
            if self.answers[i].is_good:
                text += '(Dobra)'
            text += ':\n'
            text += self.answers[i].text + '\n'
        return text

