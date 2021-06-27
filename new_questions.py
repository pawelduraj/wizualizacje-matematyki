import db_manager

db = db_manager.DataBase()
db.delete_all_questions()
db.insert_questions('quiz_questions.txt')