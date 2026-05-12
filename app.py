from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import sqlite3
from datetime import datetime
import database

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Initialize database
database.init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        mobile = request.form['mobile']
        password = request.form['password']
        action = request.form['action']
        
        conn = database.get_db_connection()
        
        if action == 'signin':
            user = conn.execute(
                'SELECT * FROM user WHERE mobile = ? AND password = ?',
                (mobile, password)
            ).fetchone()
            
            if user:
                session['user_id'] = user['id']
                session['name'] = user['name']
                session['mobile'] = user['mobile']
                session['email'] = user['email']
                return redirect(url_for('index'))
            else:
                flash('Invalid mobile number or password', 'error')
        
        elif action == 'signup':
            name = request.form['name']
            email = request.form['email']
            
            # Check if mobile already exists
            existing_user = conn.execute(
                'SELECT * FROM user WHERE mobile = ?', (mobile,)
            ).fetchone()
            
            if existing_user:
                flash('Mobile number already registered', 'error')
            else:
                conn.execute(
                    'INSERT INTO user (name, password, mobile, email) VALUES (?, ?, ?, ?)',
                    (name, password, mobile, email)
                )
                
                # Initialize wallet with 0 balance
                conn.execute(
                    'INSERT INTO wallet (balance, phone) VALUES (?, ?)',
                    (0.0, mobile)
                )
                
                conn.commit()
                flash('Registration successful! Please sign in.', 'success')
        
        conn.close()
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/wallet', methods=['GET', 'POST'])
def wallet():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = database.get_db_connection()
    
    if request.method == 'POST':
        amount = float(request.form['amount'])
        
        # Update wallet balance
        wallet = conn.execute(
            'SELECT * FROM wallet WHERE phone = ?', (session['mobile'],)
        ).fetchone()
        
        new_balance = wallet['balance'] + amount
        
        conn.execute(
            'UPDATE wallet SET balance = ? WHERE phone = ?',
            (new_balance, session['mobile'])
        )
        
        conn.commit()
        flash(f'₹{amount} added to wallet successfully!', 'success')
        return redirect(url_for('booking'))
    wallet = conn.execute(
        'SELECT * FROM wallet WHERE phone = ?', (session['mobile'],)
    ).fetchone()
    
    conn.close()
    return render_template('wallet.html', wallet=wallet)

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = database.get_db_connection()
    
    # Get booked slots
    booked_slots = conn.execute(
        'SELECT * FROM history WHERE status = "active"'
    ).fetchall()
    booked_num = [slot['numberplate'] for slot in booked_slots]
    booked_slots = [slot['slot'] for slot in booked_slots]
    
    if request.method == 'POST':
        slot = request.form['slot']
        numberplate = request.form['numberplate']
        print(numberplate)
        # Check if slot is available
        if slot in booked_slots:
            flash('Slot already booked!', 'error')
            return redirect(url_for('booking'))
        else:
            if numberplate in booked_num:
                flash('Slot already booked by this numberplate!', 'error')
                return redirect(url_for('booking'))
            else:
                # Check wallet balance
                wallet = conn.execute(
                    'SELECT * FROM wallet WHERE phone = ?', (session['mobile'],)
                ).fetchone()
                
                if wallet['balance'] >= 50:  # Assuming ₹50 per booking
                    # Deduct amount from wallet
                    new_balance = wallet['balance'] - 50
                    conn.execute(
                        'UPDATE wallet SET balance = ? WHERE phone = ?',
                        (new_balance, session['mobile'])
                    )
                    
                    from datetime import datetime
                    now = datetime.now()
                    Time = now.strftime("%H:%M")
                    print("Booked Time:", Time)
                    # Create booking
                    conn.execute(
                        '''INSERT INTO history (name, mobile, email, numberplate, slot) 
                        VALUES (?, ?, ?, ?, ?)''',
                        (session['name'], session['mobile'], session['email'], 
                        numberplate, slot)
                    )
                    
                    conn.commit()
                    flash(f'Slot {slot} booked successfully! ₹50 deducted from wallet.', 'success')
                    return redirect(url_for('booking'))
                else:
                    flash('Insufficient wallet balance. Minimum ₹50 required.', 'error')
    
    conn.close()
    return render_template('booking.html', booked_slots=booked_slots)

@app.route('/history')
def history():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = database.get_db_connection()
    
    # Get user's booking history
    bookings = conn.execute(
        '''SELECT * FROM history 
           WHERE mobile = ? 
           ORDER BY booked_time DESC''',
        (session['mobile'],)
    ).fetchall()
    
    conn.close()
    return render_template('history.html', bookings=bookings)

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    conn = database.get_db_connection()
    
    if request.method == 'POST':
        if 'user_id' not in session:
            flash('Please login to submit feedback', 'error')
            return redirect(url_for('login'))
        
        feed = request.form['feed']
        
        conn.execute(
            'INSERT INTO feedback (name, email, feed) VALUES (?, ?, ?)',
            (session['name'], session['email'], feed)
        )
        
        conn.commit()
        flash('Feedback submitted successfully!', 'success')
    
    # Get all feedbacks
    feedbacks = conn.execute(
        'SELECT * FROM feedback ORDER BY created_at DESC'
    ).fetchall()
    
    conn.close()
    return render_template('feedback.html', feedbacks=feedbacks)

if __name__ == '__main__':
    app.run(debug=True)