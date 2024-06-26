import CryDetection
import CaptureImage
import ChildAdultDetection
import MailSent


ParentMailAddress = "dummy1@gmail.com"
message = "Your child might be in stress!"

stress_level = 0

while True:
    #filename = "Sounds/Crying Sound Effect.wav"
    filename = "Sounds/Recording.wav"
    CryDetection.record_audio(filename, duration=3)
    is_crying = CryDetection.detect_baby_cry(filename)
    

    print("******************************************")
    if is_crying:
        stress_level += 2
        print("Baby crying detected!")
    else:
        print("No baby crying detected.")
        stress_level -= 1

    
    #image_name = "download.jpg"
    #captured = True
    image_name = "frame.jpg"
    captured = CaptureImage.Capture(image_name)
    if captured:
        val = ChildAdultDetection.detect_people(image_name)
        if val == 0 or val == 1:
            stress_level += 2
        elif val == 3:
            stress_level += 1
        else:
            stress_level -= 1
        
    if val == 2 and is_crying == False or stress_level < 0:
        stress_level = 0 
    
    if stress_level >= 10:
        stress_level = 0
        #MailSent.SendMail(ParentMailAddress, message)
        print("Mail sent")
    
    print("Current Stress Level", stress_level)
    print("******************************************")
    
