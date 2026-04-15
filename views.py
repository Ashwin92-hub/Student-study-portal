from django import contrib
from django.core.checks import messages
from django.forms.widgets import FileInput
from django.shortcuts import redirect, render
from .forms import *
from django.contrib import messages
from django.views import generic
import certifi
import ssl
import httpx
from youtubesearchpython import VideosSearch

# Create a safe SSL context with certifi
ssl_context = ssl.create_default_context(cafile=certifi.where())
httpx._client._default_ssl_context = lambda: ssl_context
response = httpx.get('https://example.com', verify=False)
import requests
import wikipedia
from django.contrib.auth import logout


def home(request):
    return render(request,'dashboard/home.html')
def notes(request):
    if request.method == "POST":
           form=NotesForm(request.POST)
           if form.is_valid():
                notes=Notes(user=request.user,title=request.POST['title'],description=request.POST['description'])
                notes.save()
           messages .success(request,f"Notes added from {request.user.username}Successfully!")
    else:
        form = NotesForm()
        notes=Notes.objects.filter(user=request.user)
        context={'notes':notes,'form': form}
        return render(request,'dashboard/notes.html',context)
def delete_note(request,pk=None):
         Notes.objects.get(id=pk).delete()
         return redirect("notes")
class NotesDetailView (generic.DetailView):
      model = Notes

def homework(request):
            if request.method == "POST":
                  form = HomeworkForm(request.POST)
                  if form.is_valid():
                        try:
                              finished = request.POST['is_finished']
                              if finished == 'on':
                                    finished = True
                              else:
                                    finished = False
                        except:
                              finished =False
                        homeworks=Homework(
                              user=request.user,
                              subject = request.POST['subject'],
                              title = request.POST['title'],
                              description = request.POST['description'],
                              due = request.POST['due'],
                              is_finished = finished
                        )                        
                        homeworks.save() 
                        messages.success(request,f'Homework Added from {request.user.username} !!')
            else:
                  form = HomeworkForm()
            homework=Homework.objects.filter(user=request.user)
            if len(homework) == 0:
                  homework_done =True
            else:
                  homework_done =False      
            context = {'homeworks':homework,'homeworks_done':homework_done,
                       'form':form}
            return render(request,'dashboard/homework.html',context)
def update_homework(request,pk=None):
      homework = Homework.objects.get(id=pk)
      if homework.is_finished == True:
            homework.is_finished == False
      else:
            homework.is_finished = True
      homework.save()
      return redirect('homework')     
      
def delete_homework(request,pk=None):
      Homework.objects.get(id=pk).delete()
      return redirect("homework")
def youtube(request):
      if request.method == "POST":
            form = DashboardForm(request.POST)
            text = request.POST['text']
            video = VideosSearch(text, limit=10)

            result_list = []
            for i in video.result()['result']:
                  result_dict={
                        'input':text,
                        'title':i['title'],
                        'duration':i['duration'],
                        'thumbnail':i['thumbnails'][0]['url'],
                        'channel':i['channel']['name'],
                        'link':i['link'],
                        'views':i['viewCount']['short'],
                        'published':i['publishedTime']
                  }
                  desc =''
                  if i['descriptionSnippet']:
                        for j in i['descriptionSnippet']:
                              desc+= j['text']
                  result_dict['description'] =desc
                  result_list.append(result_dict)
                  context={
                        'form':form,
                        'results':result_list
                  }
            return render(request,"dashboard/youtube.html",context)
      else:     
            form=DashboardForm()
            context = {'form':form}
            return render(request,"dashboard/youtube.html",context)
      
def todo(request): 
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST.get("is_finished") == 'on'
            except:
                finished = False  

            todos = Todo(
                user=request.user,
                title=request.POST['title'],
                is_finished=finished
            )  
            todos.save()
            messages.success(request, f"Todo Added from {request.user.username}!!")   
            return redirect('todo')  # <-- ADD THIS to return an HttpResponse
    else:                         
        form = TodoForm()

    todo = Todo.objects.filter(user=request.user)
    todos_done = len(todo) == 0

    context = {
        'todos': todo,
        'form': form,
        'todos_done': todos_done
    }
    return render(request, "dashboard/todo.html", context)
def update_todo(request,pk=None):
      todo = todo.objects.get(id=pk)
      if todo.is_finished == True:
            todo.is_finished = False
      else:
        todo.is_finished = True
        todo.save()
        return redirect('todo')

def delete_todo(request, pk=None):
      Todo.objects.get(id=pk).delete()
      return redirect("todo")

def books(request):
    result_list = []

    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST.get('text', '')

        if text:
            url = "https://www.googleapis.com/books/v1/volumes?q=" + text
            r = requests.get(url)
            answer = r.json()

            print("API Response:", answer)

            # Ensure 'items' key exists
            if 'items' in answer:
                for item in answer['items']:
                    volume_info = item.get('volumeInfo', {})
                    image_links = volume_info.get('imageLinks', {})

                    result_dict = {
                        'title': volume_info.get('title', 'No Title Available'),
                        'subtitle': volume_info.get('subtitle', 'No Subtitle Available'),
                        'description': volume_info.get('description', 'No Description Available'),
                        'count': volume_info.get('pageCount', 'Not Available'),
                        'categories': volume_info.get('categories', []),
                        'rating': volume_info.get('averageRating', 'Not Available'),
                        'thumbnail': image_links.get('thumbnail', ''),
                        'preview': volume_info.get('previewLink', '#')
                    }
                    result_list.append(result_dict)
            else:
                messages.warning(request, "No books found. Please try a different search term.")
        else:
            messages.warning(request, "Please enter a search term.")

        context = {
            'form': form,
            'results': result_list
        }
        return render(request, "dashboard/books.html", context)
    else:
        form = DashboardForm()
        return render(request, "dashboard/books.html", {'form': form})


def dictionary(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/" + text
        r = requests.get(url)
        answer = r.json()

        try:
            phonetics = answer[0]['phonetics'][0].get('text', '')
            audio = answer[0]['phonetics'][0].get('audio', '')
            meanings = answer[0]['meanings']

            # Get first meaning block
            first_meaning = meanings[0]
            part_of_speech = first_meaning.get('partOfSpeech', '')
            definitions = first_meaning.get('definitions', [])

            definition = definitions[0].get('definition', '') if definitions else ''
            example = definitions[0].get('example', '') if definitions else ''
            synonyms = definitions[0].get('synonyms', []) if definitions else []

            # Collect all parts of speech (categories)
            categories = [meaning.get('partOfSpeech', '') for meaning in meanings]

            context = {
                'form': form,
                'input': text,
                'phonetics': phonetics,
                'audio': audio,
                'definition': definition,
                'example': example,
                'synonyms': synonyms,
                'categories': categories,
            }

        except Exception as e:
            print("Error:", e)
            context = {
                'form': form,
                'input': '',
                'error': "Could not fetch data. Try another word."
            }

        return render(request, "dashboard/dictionary.html", context)

    else:
        form = DashboardForm()
        return render(request, "dashboard/dictionary.html", {'form': form})
def wiki(request):
    if request.method == 'POST':
         text = request.POST['text']
         form = DashboardForm(request.POST)
         search = wikipedia.page(text)
         context = {
              'form':form,
              'title':search.title,
              'link':search.url,
              'details':search.summary
         }
         return render(request,'dashboard/wiki.html',context)
    else: 
         form=DashboardForm()
         context = {'form':form}
         return render(request,'dashboard/wiki.html',context)
def conversion(request):
    if request.method == "POST":
        form = ConversionForm(request.POST)
        measurement_type = request.POST.get('measurement')

        if measurement_type == 'length':
            measurement_form = ConversionLengthForm()
            context = {
                'form': form,
                'm_form': measurement_form,
                'input': True
            }

            if 'input' in request.POST:
                first = request.POST.get('measure1')
                second = request.POST.get('measure2')
                input_val = request.POST.get('input')
                answer = ''

                if input_val and int(input_val) >= 0:
                    if first == 'yard' and second == 'foot':
                        answer = f'{input_val} yard = {int(input_val)*3} foot'
                    elif first == 'foot' and second == 'yard':
                        answer = f'{input_val} foot = {int(input_val)/3} yard'

                context['answer'] = answer
            return render(request, 'dashboard/conversion.html', context)

        elif measurement_type == 'mass':
            measurement_form = ConversionMassForm()
            context = {
                'form': form,
                'm_form': measurement_form,
                'input': True
            }

            if 'input' in request.POST:
                first = request.POST.get('measure1')
                second = request.POST.get('measure2')
                input_val = request.POST.get('input')
                answer = ''

                if input_val and int(input_val) >= 0:
                    if first.strip() == 'pound' and second.strip() == 'kilogram':
                        answer = f'{input_val} pound = {int(input_val)*0.453592} kilogram'
                    elif first.strip() == 'kilogram' and second.strip() == 'pound':
                        answer = f'{input_val} kilogram = {int(input_val)*2.20462} pound'

                context['answer'] = answer
            return render(request, 'dashboard/conversion.html', context)

    else:
        form = ConversionForm()
        context = {
            'form': form,
            'input': False
        }
        return render(request, 'dashboard/conversion.html', context)



def register(request):
    if request.method == 'POST':
        form = UserResgistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account Created for {username}!!")
            return redirect('login')  # or any other page after registration
    else:
        form = UserResgistrationForm()
    
    context = {
        'form': form
    }
    return render(request, "dashboard/register.html", context)

def profile(request):
     homeworks = Homework.objects.filter(is_finished=False,user=request.user)
     todos = Todo.objects.filter(is_finished=False,user=request.user)
     if len(homeworks) ==0:
          homework_done = True
     else:
          homework_done = False     
     if len(todos) ==0:
          todos_done = True
     else:
          todos_done = False  
     context = {
          'homeworks':homeworks,
          'todos':todos,
          'homework_done':homework_done,
          'todos_done':todos_done
     }
     return render(request,"dashboard/profile.html",context)

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')