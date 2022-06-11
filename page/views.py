from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages, auth
from gtts import gTTS
import PyPDF2
import os
def index(request):
    return render(request, 'pages/index.html')


def about(request):
    return render(request, 'pages/about.html')

def pdfreader(request):
    if request.method == 'POST' and request.FILES['pdf']:
        voiceType = request.POST['voice']
        language = request.POST['language']
        pdf = request.FILES['pdf']

        if os.path.exists("media/Audio.mp3"):
            os.remove('media/Audio.mp3')
        #Create PDF Reader Object
        try:
            pdf_Reader = PyPDF2.PdfFileReader(pdf)
        except:
            messages.error(request, 'invalid pdf File Formate.')
            return redirect("pdfreader")
            
        count = pdf_Reader.numPages # counts number of pages in pdf
        textList = []
        
        #Extracting text data from each page of the pdf file
        for i in range(count):
            try:
                page = pdf_Reader.getPage(i)    
                textList.append(page.extractText())
            except:
                pass

        #Converting multiline text to single line text
        textString = " ".join(textList)

        print(textString)
        print("222222")
        #Set language to english (en)
        language = 'en'

        #Call GTTS
        myAudio = gTTS(text=textString, lang=language, slow=False)
        print("222222")
        #Save as mp3 file
        myAudio.save("media/Audio.mp3")
        messages.success(request, 'TEXT TO SPEACH CONVERTION SUCCESSFUL.')
        return redirect("pdfreader")
        
          
    return render(request, 'pages/dashboard.html')