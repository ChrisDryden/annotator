import blob_detection
import os
import math
import coordinatecalculation
import TSP

from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import os
 

def return_images_list(image_list):
    return_list = []
    for item in image_list:
        if '.jpg' in item:
            return_list.append(item)
    return return_list



#Required to set a static folder to show images
app = Flask(__name__)
app.config['STATIC_FOLDER'] = os.path.join('./static/try')



#Error handlers can be passed to seperate file
#If page is not found
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html')

#Main homepage
@app.route('/')
def homepage():
	return render_template('homepage.html')


#First page shown when the calibrate button is on main page
@app.route('/calibrate', methods=['POST'])
def calibrate_page():
    session['min_area'] = 0
    session['min_circ'] = 0
    session['min_conv'] = 0
    session['min_thre'] = 0
    session['min_iner'] = 0
    session['image'] = 0

    image_list = return_images_list(os.listdir('./static/try'))

    full_filename = os.path.join(app.config['STATIC_FOLDER'], image_list[0])
    return render_template('calibrate.html', test_image_flask = full_filename, saved_value=0, \
        area_value = session['min_area'], circ_value = session['min_circ']/100, conv_value = session['min_conv']/100, \
        thre_value = session['min_thre'], iner_value = session['min_iner']/100)


#To move to the next image to test calibration
@app.route('/next_image_calibration', methods=['POST'])
def next_image_calibrate_page():
    
    session['image'] = session['image'] + 1
    image_list = return_images_list(os.listdir('./static/try'))
    image_number = session['image'] 
    full_filename = os.path.join(app.config['STATIC_FOLDER'], image_list[image_number])
    return render_template('calibrate.html', test_image_flask = full_filename, \
        area_value = session['min_area'], circ_value = session['min_circ'], conv_value = session['min_conv'], \
        thre_value = session['min_thre'], iner_value = session['min_iner'])
 

@app.route('/test_calibration', methods=['POST'])
def test_calibrate_page():
    session['min_area'] = int(request.form['min_area'])
    session['min_circ'] = int(request.form['min_circ'])
    session['min_conv'] = int(request.form['min_conv'])
    session['min_thre'] = int(request.form['min_thre'])
    session['min_iner'] = int(request.form['min_iner'])

    #find code for this
    image_list = return_images_list(os.listdir('./static/try'))


    #Activated if program is calibrated
    #print(session['min_iner'])
    #if True: #session['min_iner'] == 1:
    #    print("Success")
    #    blob_detection.complete_detection(area = session['min_area'], circ = session['min_circ'], \
    #        conv = session['min_conv']/, thre = session['min_thre'], iner = session['min_iner'])

    try:
        image_number = session['image'] 
    except:
        image_number = 0

    full_filename = os.path.join(app.config['STATIC_FOLDER'], image_list[image_number])
    path = os.getcwd()
    print(full_filename)
    test_filename = os.path.join(app.config['STATIC_FOLDER'], 'test_calibration/' + image_list[image_number])

    blob_detection.tailored_detection_return(full_filename, test_filename, area = session['min_area'], circ = session['min_circ'], \
            conv = session['min_conv'], thre = session['min_thre'], iner = session['min_iner'])

    return render_template('calibrate.html', test_image_flask = test_filename, \
        area_value = session['min_area'], circ_value = session['min_circ'], conv_value = session['min_conv'], \
        thre_value = session['min_thre'], iner_value = session['min_iner'])

@app.route('/finish_calibration', methods=['POST'])
def finish_calibrate_page():
    

    return render_template('homepage.html')



#Verification must add latitude and longitude




#Code to seperate the seperate groups
#Parameter with route to image can be saved as "verify_image"
@app.route('/groupone', methods=['POST'])
def group_one_page():
    session['group'] = 1
    return redirect(url_for('next_verify_page'))
 
@app.route('/grouptwo', methods=['POST'])
def group_two_page():
    session['group'] = 2
    return redirect(url_for('next_verify_page'))

@app.route('/groupthree', methods=['POST'])
def group_three_page():
    session['group'] = 3
    return redirect(url_for('next_verify_page'))

@app.route('/groupfour', methods=['POST'])
def group_four_page():
    session['group'] = 4
    return redirect(url_for('next_verify_page'))

@app.route('/next_image', methods = ['GET', 'POST'])
def next_verify_page():

    #if button_pressed = yes, add to coordinates list
    #if button_pressed = no, go to next item on the list


    for item in os.listdir('./static/try/' + str(session['group'])):
        print(item)
        if '.jpg' in item:
            return render_template('verification.html', verify_image = './static/try/1/' + item)
    


    return render_template('verification.html')






@app.route('/return_home', methods=['POST'])
def return_home_page():
    return render_template('homepage.html')

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='127.0.0.1', port=5000)