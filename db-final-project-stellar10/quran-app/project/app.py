from flask import Flask, render_template, request, redirect, url_for
import pymysql
pymysql.install_as_MySQLdb()
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

app.config["MYSQL_USER"]="flask_user"
app.config["MYSQL_PASSWORD"]="secure_password_123"
app.config["MYSQL_DB"]="qclass"
app.config["MYSQL_CURSORCLASS"]="DictCursor"

mysql = MySQL(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/students')
def show_students():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Students')
    students = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('students.html', students=students)

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        birth_date = request.form['birth_date']
        ph_num = request.form['ph_num']
        
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Students (FirstName, LastName, BirthDate, PhNum) VALUES (%s, %s, %s, %s)',
                       (first_name, last_name, birth_date, ph_num))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('show_students'))
    return render_template('add_student.html')

@app.route('/update_student/<int:student_id>', methods=['GET', 'POST'])
def update_student(student_id):
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        birth_date = request.form['birth_date']
        ph_num = request.form['ph_num']
        
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('UPDATE Students SET FirstName=%s, LastName=%s, BirthDate=%s, PhNum=%s WHERE StudentId=%s',
                       (first_name, last_name, birth_date, ph_num, student_id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('show_students'))
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Students WHERE StudentId = %s', (student_id,))
    student = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('update_student.html', student=student)

@app.route('/delete_student/<int:student_id>', methods=['GET', 'POST'])
def delete_student(student_id):
    if request.method == 'POST':
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Students WHERE StudentId = %s', (student_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('show_students'))
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Students WHERE StudentId = %s', (student_id,))
    student = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('delete_student.html', student=student)

@app.route('/progress')
def show_progress():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM Task')
    completed_tasks_count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return render_template('progress.html', completed_tasks=completed_tasks_count)

def show_attendance():
    conn = mysql.connect()
    cursor = conn.cursor()
    
    # Query to fetch attendance data
    cursor.execute('SELECT Students.FirstName, Students.LastName, StudentAttendance.Presence FROM Students LEFT JOIN StudentAttendance ON Students.StudentId = StudentAttendance.StudentId')
    attendance_data = cursor.fetchall()

    cursor.close()
    conn.close()

    # Process attendance data
    attendance_dict = {}
    for first_name, last_name, presence in attendance_data:
        student_name = f"{first_name} {last_name}"
        if student_name not in attendance_dict:
            attendance_dict[student_name] = {'present': 0, 'absent': 0}
        if presence:
            attendance_dict[student_name]['present'] += 1
        else:
            attendance_dict[student_name]['absent'] += 1

    return render_template('attendance.html', attendance_data=attendance_dict)

if __name__ == '__main__':
    app.run(debug=True)