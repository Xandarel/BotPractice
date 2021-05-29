import telebot
from Task import Task
from collocationsClass import ColocationFinder
from n_gramm_creator import Ngram
from tqdm import tqdm
import json


bot = telebot.TeleBot('1507489126:AAEGZ1rYJ-CqUDGiHpOQndN6WNmqsZRrnro')
n_best = 10
freq_filter = 5
# ngram = ''
# task = ''

colocation_lable_info_list = [
    'get top-10 collocations using simple frequency',
    'get top-10 collocations using described measures',
    'get top-10 collocations using Pointwise mutual information ',
    'get top-10 collocations using likelihood_ratio',
    'get top-10 collocations using chi_sq'
]


@bot.message_handler(content_types=['text', 'document'])
def get_text_messages(message):
    if message.text == '/history':
        get_history(message.from_user.id)
        return
    elif message.text == '/help':
        bot.send_message(message.from_user.id, '/history - история запросов\n /help - помощь\n <Запрос>,<количество статей>(минимум 1000),<длины n-граммы, через запятую> - запрос')
        return
    data = message.text.split(',')
    task = Task(data[0], int(data[1]) if int(data[1]) >= 1000 else 1000)
    try:
        task.find_request_url()
    except TypeError:
        bot.send_message(message.from_user.id, "По вашему запросу ничего не найдено")
        return
    bot.send_message(message.from_user.id, "Получение данных, пожалуйста подождите")
    task.get_text_from_article()

    ngram_size = list(map(int, data[2:]))
    ngram = Ngram(task, *ngram_size)
    ngram.create_dataframe()
    for fig in ngram.save_fig(message.from_user.id):
        with open(fig, 'rb') as f:
            bot.send_photo(message.from_user.id, f)
    collocation = ColocationFinder(task, n_best)
    bot.send_message(message.from_user.id, "обработка колокаций")
    for n_size in tqdm(ngram.n_grams_size):
        if n_size not in (2, 3):
            bot.send_message(message.from_user.id, f"данный рамер ({n_size}) не поддерживается")
            continue
        rankings = collocation.get_colocation(n_size, freq_filter)
        for index, ranking in enumerate(rankings):
            bot.send_message(message.from_user.id, colocation_lable_info_list[index])
            bot.send_message(message.from_user.id, str(ranking))
    save_request(task, ngram, message.from_user.id, message.text)


@bot.message_handler(content_types=['text', 'document'])
def get_history(user_id):
    with open("data_file.json", "r") as read_file:
        data_base = dict(json.load(read_file))
    if str(user_id) in data_base.keys():
        user_request = data_base[str(user_id)]
        request = [i['request_text'] for i in user_request]
        bot.send_message(user_id, str(request))
    else:
        bot.send_message(user_id, 'Вы ещё не делали ни одного запроса.')


def save_request(task_request: Task, ngram_request: Ngram, user_id: int, request: str):
    print(user_id)
    with open("data_file.json", "r") as read_file:
        data_base = dict(json.load(read_file))
    data_dict = {
        "Original_text":  task_request.res_text,
        "Tokenize_text": task_request.res_tokenize_text,
        "n_gram_size":  ngram_request.n_grams_size,
        "request_text": request
    }
    if str(user_id) in data_base.keys():
        data_base[str(user_id)].append(data_dict)
    else:
        data_base[str(user_id)] = [data_dict]
    with open("data_file.json", "w") as write_file:
        json.dump(data_base, write_file)


bot.polling(none_stop=True, interval=0)
