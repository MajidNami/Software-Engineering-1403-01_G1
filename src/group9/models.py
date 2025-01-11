class Question:
    def __init__(self, id, body, answer):
        self.id = id
        self.body = body
        self.answer = answer

    def __str__(self):
        return f"Question(id={self.id}, body='{self.body}', answer='{self.answer}')"


class Exam:
    def __init__(self, id, questions, score, user):
        """
        questions: لیستی از آبجکت‌های Question
        score: نمره آزمون
        user: نام یا شناسه‌ی کاربر شرکت‌کننده
        """
        self.id = id
        self.questions = questions
        self.score = score
        self.user = user

    def __str__(self):
        return f"Exam(id={self.id}, user='{self.user}', score={self.score})"


class Report:
    def __init__(self, user, exams):
        """
        exams: لیستی از آبجکت‌های Exam
        """
        self.user = user
        self.exams = exams

    def __str__(self):
        return f"Report(user='{self.user}', exams_count={len(self.exams)})"


class Resource:
    def __init__(self, id, title, author, category):
        self.id = id
        self.title = title
        self.author = author
        self.category = category

    def __str__(self):
        return f"Resource(id={self.id}, title='{self.title}', category='{self.category}')"


class Exercise:
    def __init__(self, id, user, questions, score):
        """
        questions: لیستی از آبجکت‌های Question
        """
        self.id = id
        self.user = user
        self.questions = questions
        self.score = score

    def __str__(self):
        return f"Exercise(id={self.id}, user='{self.user}', score={self.score})"
