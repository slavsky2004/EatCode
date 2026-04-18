from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Разрешаем запросы с фронтенда

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS foods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            weight REAL NOT NULL,
            calories_per_100 REAL NOT NULL,
            protein_per_100 REAL DEFAULT 0,
            fat_per_100 REAL DEFAULT 0,
            carbs_per_100 REAL DEFAULT 0,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    print("✅ База данных инициализирована")

init_db()

# Получить все продукты за сегодня
@app.route('/api/foods', methods=['GET'])
def get_foods():
    today = datetime.now().strftime('%Y-%m-%d')
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM foods WHERE date = ? ORDER BY id DESC', (today,))
    rows = cursor.fetchall()
    conn.close()
    
    foods = []
    for row in rows:
        foods.append({
            'id': row[0],
            'name': row[1],
            'weight': row[2],
            'caloriesPer100': row[3],
            'proteinPer100': row[4],
            'fatPer100': row[5],
            'carbsPer100': row[6],
            'date': row[7]
        })
    return jsonify(foods)

# Добавить продукт
@app.route('/api/foods', methods=['POST'])
def add_food():
    data = request.json
    today = datetime.now().strftime('%Y-%m-%d')
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO foods (name, weight, calories_per_100, protein_per_100, fat_per_100, carbs_per_100, date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (data['name'], data['weight'], data['caloriesPer100'], 
          data['proteinPer100'], data['fatPer100'], data['carbsPer100'], today))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    
    return jsonify({'id': new_id, 'message': 'Продукт добавлен'}), 201

# Удалить продукт
@app.route('/api/foods/<int:food_id>', methods=['DELETE'])
def delete_food(food_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM foods WHERE id = ?', (food_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Удалено'})

# Очистить все продукты за сегодня
@app.route('/api/foods', methods=['DELETE'])
def clear_all_foods():
    today = datetime.now().strftime('%Y-%m-%d')
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM foods WHERE date = ?', (today,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Все продукты удалены'})

# Получить историю по дням (последние 30 дней)
@app.route('/api/history', methods=['GET'])
def get_history():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT date, 
               SUM(weight * calories_per_100 / 100) as total,
               SUM(weight * protein_per_100 / 100) as protein,
               SUM(weight * fat_per_100 / 100) as fat,
               SUM(weight * carbs_per_100 / 100) as carbs
        FROM foods
        GROUP BY date
        ORDER BY date DESC
        LIMIT 30
    ''')
    rows = cursor.fetchall()
    conn.close()
    
    history = []
    for row in rows:
        history.append({
            'date': row[0], 
            'total': round(row[1], 0),
            'protein': round(row[2], 1),
            'fat': round(row[3], 1),
            'carbs': round(row[4], 1)
        })
    return jsonify(history)

# Корневой маршрут для проверки
@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'API калькулятора калорий работает!', 'status': 'ok'})

# Запуск сервера
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
