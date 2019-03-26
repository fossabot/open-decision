from django.shortcuts import render, redirect
from .forms import *
from django.forms import formset_factory
from django.utils.html import escape


def product_create_view(request):
    if request.method == 'GET':
        node_form = NodeForm
        NodeButtonFormSet = formset_factory(ButtonAnswersForm)
        context = {
        'form': node_form,
        }
        return render(request, 'product/product_create.html', context)
    elif request.method == 'POST' and request.POST.get('save'):
        print (request.POST)
        clean_data(request)
        node_form = NodeForm
        context = {
        'form': node_form
        }
        return render(request, 'product/product_create.html', context)


def load_answer_field(request):
    input_type = request.GET['input_type']
    list = set_answer_form(input_type)
    answer_form = list[0]
    expandable = list[1]
    AnswerFormSet = formset_factory(answer_form)
    answer_formset = AnswerFormSet(prefix='answer')
    context = {
    'answer_formset': answer_formset,
    'expandable': expandable,
    }
    return render(request, 'product/answer_field.html', context)

def set_answer_form(input_type):
    if input_type == 'button':
        answer_form = ButtonAnswersForm
        expandable = True
    elif input_type == 'list':
        answer_form = ListAnswersForms
        expandable = False
    elif input_type == 'multiple_select':
        answer_form = MultipleSelectAnswersForm
        expandable = True
    elif input_type == 'short_text':
        answer_form = ShortTextAnswersForm
        expandable = True
    elif input_type == 'long_text':
        answer_form = LongTextAnswersForm
        expandable = True
    elif input_type == 'number':
        answer_form = NumberAnswersForm
        expandable = False
    elif input_type == 'date':
        answer_form = DateAnswerForm
        expandable = False
    else:
        raise Exception('Invalid input type.')
        pass
    return [answer_form, expandable]

def load_logic_field(request):
    input_type = request.GET['input_type']
    LogicFormSet = formset_factory(LogicForm)
    test1 = (
    ('button', 'Buttons'),
    ('list', 'Auswahlliste'),
    ('multiple_select', 'Mehrfachauswahl'),
    ('short_text', 'Textfeld'),
    ('long_text', 'Großes Textfeld'),
    ('number', 'Nummernfeld'),
    ('date', 'Datum')
    )
    if input_type == 'button':
        logic_form = LogicFormSet(form_kwargs={'test1': test1, 'input_type': input_type}, prefix='logic')
    elif input_type == 'list':
        logic_form = LogicFormSet(form_kwargs={'test1': test1, 'input_type': input_type}, prefix='logic')
    elif input_type == 'multiple_select':
        logic_form = LogicFormSet(form_kwargs={'test1': test1, 'action': '', 'input_type': input_type}, prefix='logic')
    elif input_type == 'short_text':
        logic_form = LogicFormSet(form_kwargs={'test1': test1, 'action': '', 'input_type': input_type}, prefix='logic')
    elif input_type == 'long_text':
        logic_form = LogicFormSet(form_kwargs={'test1': test1, 'action': '', 'input_type': input_type}, prefix='logic')
    elif input_type == 'number':
        logic_form = LogicFormSet(form_kwargs={'test1': test1, 'action': '', 'input_type': input_type}, prefix='logic')
    elif input_type == 'date':
        logic_form = LogicFormSet(form_kwargs={'test1': test1, 'action': '', 'input_type': input_type}, prefix='logic')
    else:
        raise Exception('Invalid input type.')
    context = {
    'logic': logic_form
    }
    return render(request, 'product/logic_field.html', context)



def clean_data(request):
    try:
        data_node = {
            'name'      : request.POST.get('name'),
            'question'  : request.POST.get('question'),
            'example'   : request.POST.get('example'),
            'image'     : request.POST.get('image'),
            'input_type': request.POST.get('input_type'),
            }
    except ValueError:
        raise ValueError('')
    try:
        data_answer = {}
        answers_cleaned = {}
        answers_cleaned['formset'] = {
            'answer-TOTAL_FORMS'  : int(request.POST.get('answer-TOTAL_FORMS')),
            'answer-INITIAL_FORMS': int(request.POST.get('answer-INITIAL_FORMS')),
            'answer-MIN_NUM_FORMS': int(request.POST.get('answer-MIN_NUM_FORMS')),
            'answer-MAX_NUM_FORMS': int(request.POST.get('answer-MAX_NUM_FORMS'))
        }
        # Raise error, if formset management form was modified so that data cannot be parsed to int()
    except ValueError:
        raise ValueError('Answer Formset content has been tampered with')
    except TypeError:
        #Fine if no answers are given, throws TypeError during int()
        #Build handler to notify user
        pass
    for i in range(answers_cleaned['formset']['answer-TOTAL_FORMS']):
        key = 'answer-{}-answer'.format(i)
        data_answer[key] = request.POST.get(key)
    try:
        data_logic = {}
        logic_cleaned = {}
        logic_cleaned['formset'] = {
            'logic-TOTAL_FORMS'  : int(request.POST.get('logic-TOTAL_FORMS')),
            'logic-INITIAL_FORMS': int(request.POST.get('logic-INITIAL_FORMS')),
            'logic-MIN_NUM_FORMS': int(request.POST.get('logic-MIN_NUM_FORMS')),
            'logic-MAX_NUM_FORMS': int(request.POST.get('logic-MAX_NUM_FORMS'))
        }
    except ValueError:
        raise ValueError('Logic Formset has been tampered with')
    except TypeError:
            #Fine if no logic is given, throws TypeError during int()
            #Build handler to notify user
        pass
    for i in range(logic_cleaned['formset']['logic-TOTAL_FORMS']):
        data_logic[i] = {}
        data_logic[i]['operator'] = request.POST.get('logic-'+ str(i) +'-operator')
        data_logic[i]['answers_logic'] = request.POST.get('logic-'+ str(i) +'-answers_logic')
        data_logic[i]['action'] = request.POST.get('logic-'+ str(i) +'-action')
        data_logic[i]['var_to_modify'] = request.POST.get('logic-'+ str(i) +'-var_to_modify')
    node_form = NodeForm(data_node)
#Process errors properly -  build error dict, display to user
    if node_form.is_valid():
        node_cleaned = node_form.cleaned_data
        AnswerFormUsed = set_answer_form(node_form.cleaned_data['input_type'])[0]
                #Security issues:
        # - MIN and MAX forms are taken from user input -> hardcode allowances?
        # - data is not really cleaned, is int() enough?, escaping necessary?
        if (answers_cleaned['formset']['answer-MIN_NUM_FORMS'] <= answers_cleaned['formset']['answer-TOTAL_FORMS'] <= answers_cleaned['formset']['answer-MAX_NUM_FORMS']):
            if node_form.cleaned_data['input_type'] == 'list':
                try:
                    answer_form_instance = AnswerFormUsed({'answer': data_answer['answer-0-answer']})
                    answer_form_instance.is_valid()
                    answers_cleaned[0] = answer_form_instance.cleaned_data['answer']
                    answers_cleaned[0] = answers_cleaned[0].splitlines()
                except:
                    raise ValueError('Invalid answers')
            else:
                for i in range(answers_cleaned['formset']['answer-TOTAL_FORMS']):
                    key = 'answer-{}-answer'.format(i)
                    try:
                        answer_form_instance = AnswerFormUsed({'answer': data_answer[key]})
                        answer_form_instance.is_valid()
                        answers_cleaned[i] = answer_form_instance.cleaned_data
                    except:
                        raise ValueError('Invalid answers')
            if (logic_cleaned['formset']['logic-MIN_NUM_FORMS'] <= logic_cleaned['formset']['logic-TOTAL_FORMS'] <= logic_cleaned['formset']['logic-MAX_NUM_FORMS']):
                allowed_operators = ['==','!=','<','<=','>','>=']
                for i in range(logic_cleaned['formset']['logic-TOTAL_FORMS']):
                    logic_form_instance = LogicForm(data_logic[i], {'input_type': node_form.cleaned_data['input_type']})
                    logic_form_instance.is_valid()
                    logic_cleaned[i] = logic_form_instance.cleaned_data
#Quick and dirty workaround, cause validation for operators is somehow not working
                    if data_logic[i]['operator'] in allowed_operators:
                        logic_cleaned[i]['operator'] = data_logic[i]['operator']
                    else:
                    #Build error dict
                        pass
                    if node_form.cleaned_data['input_type'] == 'list':
                        data_logic[i]['answers_logic'] = data_logic[i]['answers_logic'].splitlines()
                        logic_cleaned[i]['answers_logic'] = []
                        for x in range(len(data_logic[i]['answers_logic'])):
                            logic_cleaned[i]['answers_logic'].append(escape(data_logic[i]['answers_logic'][x]))
                    else:
                        logic_cleaned[i]['answers_logic'] = escape(data_logic[i]['answers_logic'])
    print (node_cleaned, answers_cleaned, logic_cleaned)
#    return save_node(node_cleaned, answers_cleaned, logic_cleaned)

''' def save_node(node_cleaned, answers_cleaned, logic_cleaned):
    node = node_cleaned
    if node['input_type'] == 'list':
        node['answers'] = answers_cleaned[0]

    for key,value in node_cleaned:
        node[key] = value
    '''
