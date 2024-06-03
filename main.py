from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
import uvicorn
from dotenv import load_dotenv
import os

app = FastAPI()
load_dotenv()

# Подключение к базе данных PostgreSQL
conn = psycopg2.connect(
    dbname=os.environ.get("DB_NAME"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD"),
    host=os.environ.get("DB_HOST"),
    port=os.environ.get("DB_PORT"),
)

# Модель данных для передачи информации о сессии в БД
class Session(BaseModel):
    session_topic: str
    date_session: str

# функция преобразования ответа GET запросов
def res_to_json(result):
    res = []
    for item in result:
        data = {"session_topic": item[0], "count_topic": item[1], "date_session": item[2]}
        res.append(data)
    return res

# Получение хранящихся в БД сессий
@app.get("/session_get")
async def get_sessions():
    with conn.cursor() as cur:
        cur.execute("SELECT session_topic, count_topic, date_session FROM table_mfc_2 order by count_topic desc, session_topic")
        result = cur.fetchall()
        return res_to_json(result)

# Добавление в БД новой сессии
@app.post("/session_create")
async def create_session(session: Session):
    with conn.cursor() as cur:
        # Выполнение операции UPDATE
        cur.execute("""
            UPDATE table_mfc_2
            SET count_topic = count_topic + 1
            WHERE session_topic = %s AND date_session = %s
        """, (session.session_topic, session.date_session))

        # Если ни одна строка не была обновлена, выполнить операцию INSERT
        if cur.rowcount == 0:
            cur.execute("""
                INSERT INTO table_mfc_2 (session_topic, count_topic, date_session)
                SELECT %s, 1, %s
                WHERE NOT EXISTS (
                    SELECT * FROM table_mfc_2 
                    WHERE session_topic = %s AND date_session = %s
                )
            """, (session.session_topic, session.date_session, session.session_topic, session.date_session))
        conn.commit()
        return {"message": "Data inserted successfully"}

if __name__ == "__main__":
    # запуск сервиса uvicorn на 8000 порту
    uvicorn.run(app, host="0.0.0.0", port=8000)