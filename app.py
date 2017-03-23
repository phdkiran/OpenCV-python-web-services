import os
from flask import send_from_directory, abort, request,render_template
from eve import Eve
import cv2, numpy

app = Eve(__name__)
UPLOAD_FOLDER = os.getcwd()+'/images'
PORT = int(os.environ.get("PORT", 5000))#5000
HOST = '0.0.0.0'#'127.0.0.1'

TMP_NAME='tmp.png'

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')


def file2img(file,flags = cv2.IMREAD_UNCHANGED):
    buf = numpy.fromstring(file.read(), numpy.uint8)
    return cv2.imdecode(buf, flags)

@app.route('/demo')
def hello_world():
    return render_template('demo.html')

@app.route('/grayscale', methods=['POST'])
def grayscale():
    file = request.files['img']
    img = file2img(file)
    img = cv2.cvtColor( img, cv2.COLOR_RGB2GRAY )

    cv2.imwrite(os.path.join(UPLOAD_FOLDER,'tmp.jpg'),img)
    return send_from_directory(UPLOAD_FOLDER,'tmp.jpg', as_attachment=False)

@app.route('/threshold', methods=['POST'])
def threshold():
    file = request.files['img']
    img = file2img(file,cv2.CV_8UC1)
    img = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)

    cv2.imwrite(os.path.join(UPLOAD_FOLDER,TMP_NAME),img)
    return send_from_directory(UPLOAD_FOLDER,TMP_NAME, as_attachment=False)


@app.route('/blur', methods=['POST'])
def blur():
    file = request.files['img']
    img = file2img(file)
    size = int(request.form['size'])
    img = cv2.GaussianBlur(img,(size,size),0)

    cv2.imwrite(os.path.join(UPLOAD_FOLDER,TMP_NAME),img)
    return send_from_directory(UPLOAD_FOLDER,TMP_NAME, as_attachment=False)


@app.route('/edges', methods=['POST'])
def edges():
    file = request.files['img']
    img = file2img(file)
    img = cv2.Canny(img,120,200)

    cv2.imwrite(os.path.join(UPLOAD_FOLDER,TMP_NAME),img)
    return send_from_directory(UPLOAD_FOLDER,TMP_NAME, as_attachment=False)


@app.route('/fourier', methods=['POST'])
def fourier():
    file = request.files['img']
    img = file2img(file)
    f = numpy.fft.fft2(img)
    fshift = numpy.fft.fftshift(f)
    img = 20*numpy.log(numpy.abs(fshift))

    cv2.imwrite(os.path.join(UPLOAD_FOLDER,TMP_NAME),img)
    return send_from_directory(UPLOAD_FOLDER,TMP_NAME, as_attachment=False)

@app.route('/harris', methods=['POST'])
def harris():
    file = request.files['img']
    img = file2img(file)

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    gray = numpy.float32(gray)
    dst = cv2.cornerHarris(gray,2,3,0.04)
    dst = cv2.dilate(dst,None)
    img[dst>0.01*dst.max()]=[0,0,255]

    cv2.imwrite(os.path.join(UPLOAD_FOLDER,TMP_NAME),img)
    return send_from_directory(UPLOAD_FOLDER,TMP_NAME, as_attachment=False)


@app.route('/sift', methods=['POST'])
def sift():
    file = request.files['img']
    img = file2img(file)
    
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    sift = cv2.xfeatures2d.SIFT_create()
    kp = sift.detect(gray,None)

    img=cv2.drawKeypoints(gray,kp,cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    cv2.imwrite(os.path.join(UPLOAD_FOLDER,TMP_NAME),img)
    return send_from_directory(UPLOAD_FOLDER,TMP_NAME, as_attachment=False)

@app.route('/surf', methods=['POST'])
def surf():
    file = request.files['img']
    img = file2img(file)
    
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    sift = cv2.xfeatures2d.SURF_create()
    kp = sift.detect(gray,None)

    img=cv2.drawKeypoints(gray,kp,cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    cv2.imwrite(os.path.join(UPLOAD_FOLDER,TMP_NAME),img)
    return send_from_directory(UPLOAD_FOLDER,TMP_NAME, as_attachment=False)

@app.route('/orb', methods=['POST'])
def orb():
    file = request.files['img']
    img = file2img(file)
    
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    sift = cv2.ORB_create(nfeatures=10000, scoreType=cv2.ORB_FAST_SCORE)
    kp = sift.detect(gray,None)

    img=cv2.drawKeypoints(gray,kp,cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS)

    cv2.imwrite(os.path.join(UPLOAD_FOLDER,TMP_NAME),img)
    return send_from_directory(UPLOAD_FOLDER,TMP_NAME, as_attachment=False)



@app.route('/face', methods=['POST'])
def face():
    file = request.files['img']
    img = file2img(file)


    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

    cv2.imwrite(os.path.join(UPLOAD_FOLDER,TMP_NAME),img)
    return send_from_directory(UPLOAD_FOLDER,TMP_NAME, as_attachment=False)


@app.route('/denoise', methods=['POST'])
def denoise():
    file = request.files['img']
    img = file2img(file)

    img = cv2.fastNlMeansDenoisingColored(img,None,0,6,5,10)

    cv2.imwrite(os.path.join(UPLOAD_FOLDER,TMP_NAME),img)
    return send_from_directory(UPLOAD_FOLDER,TMP_NAME, as_attachment=False)


@app.route('/inpaint', methods=['POST'])
def inpaint():
    file = request.files['img']
    img = file2img(file)
    mask = file2img(request.files['mask'],cv2.CV_8UC1)

    img = cv2.inpaint(img,mask,3,cv2.INPAINT_TELEA)

    cv2.imwrite(os.path.join(UPLOAD_FOLDER,TMP_NAME),img)
    return send_from_directory(UPLOAD_FOLDER,TMP_NAME, as_attachment=False)



if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)

