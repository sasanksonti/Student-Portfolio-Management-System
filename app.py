from flask import Flask, render_template, request, redirect
import mysql.connector
app = Flask(__name__)

# Temporary data store for student portfolios (Replace this with a proper database)
portfolios = []
# Database connection settings
db_config = {
    'host': 'portfolio.ckqheqnch6gp.us-east-1.rds.amazonaws.com',
    'user': 'portfolio',
    'password': 'portfolio',
    'database': 'portfolio',
}

# Temporary data store for student portfolios (Remove this since we're using the database)
# portfolios = []

# Connect to the MySQL database
db_connection = mysql.connector.connect(**db_config)
db_cursor = db_connection.cursor()

@app.route('/')
def index():
    # Fetch portfolios from the database
    db_cursor.execute("SELECT name, description, skills, projects  FROM port WHERE avail='yes'")
    portfolios = db_cursor.fetchall()
    print(portfolios)
    return render_template('index.html', portfolios=portfolios)


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        description = request.form['description']
        skills = request.form['skills']
        projects = request.form['projects']

        # Insert the portfolio into the database
        insert_query = "INSERT INTO port (name, description, skills, projects, avail) VALUES (%s, %s, %s, %s, 'yes')"
        values = (name, description, skills, projects)
        db_cursor.execute(insert_query, values)
        db_connection.commit()

        # Redirect to the homepage
        return redirect('/')
    else:
        return render_template('create.html')

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        portfolio_name = request.form.get('portfolioName')
        query = "UPDATE port SET avail='no'  WHERE name = %s"
        values = (portfolio_name,)
        
        db_cursor.execute(query, values)
        db_connection.commit()
        
        return redirect('/')

    return render_template('delete.html')

if __name__ == '__main__':
   # app.run(debug=True)
   app.run(host='0.0.0.0')
