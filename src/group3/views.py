from django.shortcuts import render
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
)
from .models import Word
from django.urls import reverse_lazy
import random
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.db import IntegrityError
from .secret import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
from database.query import *

# Create your views here.

def home(request):
    return render (request , 'group3.html' , {'group_number': '3'})

# manage 'learned box' view
def learned(request):
    # get words of box 9 (learned box) and render its html
    words = list(Word.objects.filter(box=9)) 
    return render(request, 'learned.html', {'words': words})


# manage view of words in a box
def box_view(request, box_num):
    # get words in chosen box
    words = list(Word.objects.filter(box=box_num))  
    
    # no word in box -> box is empty -> render empty_box.html
    if len(words) == 0:  
        return render(request, 'empty_box.html')  # Display a empty box message or view  
    
    # box is not empty -> render box.html
    return render(request , 'box.html', {'box_number': box_num, 'object_list': words, 'check_word': False})


# manage choosing box number before start learning
def choose_box(request):
    mydb = create_db_connection(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)
    # get box number from choose_box.html
    box_number = request.POST.get('box_number')
    # box_number is not specified
    if not box_number:
        # render choose_box.html
        return render(request, 'choose_box.html')  
    # start learning by redirecting to its function
    return redirect('group3:start-learning', box_num=box_number, start_index=0) 


# manage start learning
def start_learning(request, box_num, start_index):
    # get words in chosen box
    words = list(Word.objects.filter(box=box_num))  
    
    if box_num == 9:  # learning is done
        return render(request, 'completed.html')  # Display a completion message or view  

    if start_index >= len(words):  # words of this box are done. going to next box
        box_num += 1
        start_index = 0
        return redirect('group3:start-learning', box_num=box_num, start_index=start_index)

    current_word = words[start_index]  # Show the first word in the list  
    
    if request.method == 'POST':  
        action = request.POST.get('action') 
        
        if action == 'previous': # go to previous word
            if start_index == 0: # current word is the first word of box

                if box_num != 1: # current word box is not 1
                    # search for first previous box which is not empty
                    for i in range(box_num - 1, 0, -1):
                        words = list(Word.objects.filter(box=i))
                        if words != []:
                            # start from last word if that box
                            return redirect('group3:start-learning', box_num=i, start_index=len(words) - 1)
                
                # box number is 1 -> there is no previous word -> stay here
                return redirect('group3:start-learning', box_num=box_num, start_index=start_index)
            
            # current word is not the first word of the box ->
            # go to the previous word of this box
            return redirect('group3:start-learning', box_num=box_num, start_index=start_index - 1)
        
        elif action == 'next': # go to next word
            if start_index == len(words) - 1: # current word is the last word of the box
                if box_num == 8: # this is the last learning box -> learning is done
                    return render(request, 'completed.html')
                
                # this is not the last box -> go to first word of next box
                return redirect('group3:start-learning', box_num=box_num + 1, start_index = 0)
            
            # current word is not the last word of the box -> go to next word of this box
            return redirect('group3:start-learning', box_num=box_num, start_index=start_index + 1)
        
        elif action == 'know':  # check spelling when 'I know' clicked
            return redirect('group3:spelling', word_id=current_word.id, start_index=start_index)  
        
        else:  # action == 'don’t know'  
            return redirect('group3:start-learning', box_num=box_num, start_index=start_index + 1) 
        
    # otherwise, render start_learning.html and send its inputs to it
    return render(request , 'start_learning.html', {'box_number': box_num, 'object_list': words, 'word': current_word, 'check_word': current_word})


# manage word spelling after clicking 'I know' button in start_learning.html
def spelling_view(request, word_id, start_index):
    # get word by its id
    word = Word.objects.get(id=word_id)  
    old_box_num = word.box # save the word box

    if request.method == 'POST':  
        # check spelling
        entered_spelling = request.POST.get('spelling')  
        if entered_spelling.strip().lower() == word.word.lower():  

            # Correct Spelling  
            word.box = min(word.box + 1, 9)  # Move to the next box  
            word.save()  

            # spelling is correct -> go to next word in start learning
            return redirect('group3:start-learning', box_num=old_box_num, start_index=start_index + 1)  
        else:  # spelling is incorrect -> stay on this word in start learning
            return redirect('group3:start-learning', box_num=old_box_num, start_index=start_index)  

    # otherwise, render spelling.html
    return render(request, 'spelling.html', {'word': word.word})


# manage word list view in wordManagement page
class WordListView(ListView):
    model = Word
    queryset = Word.objects.order_by("box", "-date_created")


# manage add new words
class WordCreateView(CreateView):
    model = Word
    fields = ["word", "translation"]
    success_url = reverse_lazy("group3:word-list")
    

# manage updating words
class WordUpdateView(WordCreateView, UpdateView):
    success_url = reverse_lazy("group3:word-list")
    
