import cv2
from pyzbar.pyzbar import decode
from sqlalchemy import null
from .models import MonumentTicket
from django.http import StreamingHttpResponse
from django.shortcuts import render, redirect
import numpy as np
from datetime import datetime, timedelta
from asyncio.windows_events import NULL
object=null
from django.http import response

a=False

def change_param(verified):
    print ("hii")
    global object
    global a
    object=verified
    a=True


def lcd_display(request):
    global object
    print("ard")
    try:
        if object.verified == False:
            d={
                "message":"Access Granted",
                "name":object.name,
                "bool":a

            }
            return response.JsonResponse(d)
        else:
            d={
                "message":"Access denied",
                "name":object.name,
                "bool":a
            }
            return response.JsonResponse(d)

    except:
        d={
            "bool":a
        }
        return response.JsonResponse(d)

def customscanner(request):
    id=request.GET["order_id"]
    if MonumentTicket.objects.filter(order_id=id).exists():
        change_param(MonumentTicket.objects.get(order_id=id))
        return render(request,"success.html")
    return redirect("react_app")    




def gen_frames():  
    camera = cv2.VideoCapture(0)

    while True:
        success, frame = camera.read()  
        try:
            if not success:
                break
            else:
                for barcode in decode(frame):
                    text = barcode.data.decode('utf-8')
                    text=str(text) # Order ID String
                    print(text) 
                    verified=MonumentTicket.objects.get(order_id=text) #Object Returned
                    if MonumentTicket.objects.filter(order_id=text).exists(): 
                        if verified.verified==False:
                            color=(0,255,0)
                            displaytext = "Access Granted"
                            change_param(verified)
                            verified.verified=True

                            now = datetime.now()
                            print("NOW: ",now)
                            expire = now + timedelta(minutes=0.5)

                            verified.timevalid = expire
                            verified.save()
                            print("VALID TILL: ",verified.timevalid)

                        else:
                            if datetime.now()<verified.timevalid.replace(tzinfo=None):
                                color=(0,255,0)
                                displaytext = "Access Granted"
                                change_param(verified)
                            else:
                                color=(0,0,255)
                                change_param(verified)
                                displaytext =  "Unauthorised Access"
                        
                    else:
                        color=(0,0,255)
                        displaytext =  "Unauthorised Access"
                    
                    polygon_Points = np.array([barcode.polygon], np.int32)
                    polygon_Points=polygon_Points.reshape(-1,1,2)
                    rect_Points= barcode.rect
                    cv2.polylines(frame,[polygon_Points],True,color, 3)
                    frame=cv2.putText(frame, displaytext, (rect_Points[0],rect_Points[1]), cv2.FONT_HERSHEY_PLAIN, 0.9, color, 2)
                    
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n') # concat frame one by one and show result
        except:
            color=(0,0,255)
            displaytext =  "Unauthorised Access"

            polygon_Points = np.array([barcode.polygon], np.int32)
            polygon_Points=polygon_Points.reshape(-1,1,2)
            rect_Points= barcode.rect
            cv2.polylines(frame,[polygon_Points],True,color, 3)
            frame=cv2.putText(frame, displaytext, (rect_Points[0],rect_Points[1]), cv2.FONT_HERSHEY_PLAIN, 0.9, color, 2)
                    
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n') # concat frame one by one and show result



def ScanQR(self):
    #Video streaming route. Put this in the src attribute of an img tag
    print(gen_frames())
    return StreamingHttpResponse(gen_frames(), content_type="multipart/x-mixed-replace;boundary=frame")    

def Call_Scan(request):
    displaytext=""
    vid = cv2.VideoCapture(0)
    vid.set(3,640)
    vid.set(4,740)
    counter=0
    global status
    while True:
        success, img = vid.read()
        for barcode in decode(img):
            displaytext=""
            text = barcode.data.decode('utf-8')
            text=str(text)
            print(text)
            verified=MonumentTicket.objects.get(order_id=text)
            if MonumentTicket.objects.filter(order_id=text).exists(): 
                if verified.verified==False:
                    color=(0,255,0)
                    displaytext = "Access Granted"
                    verified.verified=True

                    now = datetime.now()
                    print("NOW: ",now)
                    expire = now + timedelta(minutes=0.5)

                    verified.timevalid = expire
                    verified.save()
                    print("VALID TILL: ",verified.timevalid)

                else:
                    if datetime.now()<verified.timevalid.replace(tzinfo=None):
                        color=(0,255,0)
                        displaytext = "Access Granted"
                        status=True
                        return render(request,"sc.html",{"displaytext":displaytext,"status":status}) 

                    else:
                        color=(0,0,255)
                        displaytext =  "Unauthorised Access"
                        status=False
                        return render(request,"sc.html",{"displaytext":displaytext,"status":status})
                
            else:
                color=(0,0,255)
                displaytext =  "Unauthorised Access"
                status=False
                return render(request,"sc.html",{"displaytext":displaytext,"status":status})