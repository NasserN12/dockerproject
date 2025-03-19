def init_routes(app):
    from flask import request, jsonify
    from database import get_db_connection
    import mysql.connector

    @app.route('/student', methods=['POST'])
    def student():
        data = request.json
        connection = None
        cursor = None

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            cursor.execute('SELECT * FROM student WHERE studentID = %s', (data['studentID'],))
            existing_student = cursor.fetchone()

            if existing_student:
                return jsonify({"message": "Student already exists"}), 409


            cursor.execute('''
                INSERT INTO student (studentID, studentName, course, presentDate)
                VALUES (%s, %s, %s, %s)
            ''', (data['studentID'], data['studentName'], data['course'], data['presentDate']))
            connection.commit()

            return jsonify({"message": "Student Created Successfully"}), 201

        except mysql.connector.Error as e:
            return jsonify({"error": str(e)}), 500

        except KeyError:
            return jsonify({"error": "Invalid data format"}), 400

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    @app.route('/student/<string:studentID>', methods=['PUT'])
    def update_student(studentID):
        data = request.json
        connection = None
        cursor = None

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            # Check if student exists
            cursor.execute('SELECT * FROM student WHERE studentID = %s', (studentID,))
            existing_student = cursor.fetchone()

            if not existing_student:
                return jsonify({"message": "Student not found"}), 404

            # Update student record
            cursor.execute('''
                UPDATE student 
                SET studentName = %s, course = %s, presentDate = %s
                WHERE studentID = %s
            ''', (data['studentName'], data['course'], data['presentDate'], studentID))
            connection.commit()

            return jsonify({"message": "Student Updated Successfully"}), 200

        except mysql.connector.Error as e:
            return jsonify({"error": str(e)}), 500

        except KeyError:
            return jsonify({"error": "Invalid data format"}), 400

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    @app.route('/student/<string:studentID>', methods=['DELETE'])
    def delete_student(studentID):
        connection = None
        cursor = None

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            cursor.execute('SELECT * FROM student WHERE studentID = %s', (studentID,))
            existing_student = cursor.fetchone()

            if not existing_student:
                return jsonify({"message": "Student not exists"}), 404

            cursor.execute('DELETE FROM student WHERE studentID = %s', (studentID,))
            connection.commit()

            return jsonify({"message": "Student Deleted Successfully"}), 200

        except mysql.connector.Error as e:
            return jsonify({"error": str(e)}), 500

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    



