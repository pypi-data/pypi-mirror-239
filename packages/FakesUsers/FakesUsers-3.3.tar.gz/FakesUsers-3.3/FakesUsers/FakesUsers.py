#FakesUsers 3.2 from filcher2011
import random

class Fu:
    def __init__(self):
        self.name = "FakesUsers"
        self.version = "3.3"
        self.patch = "2023.11.08R"

        self.name_m_ru = ['Андрей','Афанасий','Абдул','Антон','Архип','Анатолий','Александр','Алексей','Альберт','Аксен',
                        'Богдан','Борис','Бронислав','Буклаг',
                        'Вадим','Владислав','Виктор','Валерий','Валентин','Василий','Виталий','Всеволод',
                        'Давид','Давыд','Даниель','Данил','Даниил','Дмитрий','Доброслав',
                        'Евгений','Евсений','Ефрем','Епифан','Егор',
                        'Жан',
                        'Завид','Захар',
                        'Иван','Игнат','Игорь','Иосиф','Изяслав','Илья','Ильнар',
                        'Кирилл','Казимир','Кузьма',
                        'Ладислав',
                        'Мазай','Макар','Максим','Марат', 'Мурат', 'Матвей','Марк', 'Мирослав',
                        'Никита','Нифёд','Николай','Назар',
                        'Олимп','Олег',
                        'Павел','Пётр',
                        'Роман','Родим','Радислав','Руслан','Рюрик',
                        'Савелий','Савва','Семён','Станислав','Спартак',
                        'Фёдор','Филипп','Федот',
                        'Эдвард','Эльдар','Эдгар','Эрик',
                        'Юрий','Юлий',
                        'Якив','Яков','Ян','Ярополк','Ярослав',]
        
        self.name_m_en = ['Aaron','Abraham','Adam','Adrian','Aidan','Alan','Albert','Alejandro','Alex','Alexander','Alfred','Angel','Anthony','Austin',
                          'Benjamin','Bernard','Blake','Brandon','Brian','Bruce','Bryan',
                          'Carl','Christopher','Christian','Cody','Connor',
                          'Daniel','Diego','Devin','Dennis',
                          'Edward','Ethan','Evan','Eric'
                          'Francis','Fred',
                          'Gabriel','Gavin','George','Gilbert','Gerld',
                          'Harry','Harold','Henry','Hunter','Howard',
                          'Ian','Isaac','Isaiah',
                          'Jack','Jackson','Jacob','Jason','Jake','Jordan','Jonathan','John','Justin','Joseph',
                          'Kevin','Kyle',
                          'Lucas','Louis','Logan','Lewis',
                          'Martin','Mason','Michael','Morgan',
                          'Norman','Neil','Nathaniel','Nathan',
                          'Oscar','Oliver','Owen',
                          'Patrick','Peter','Philip',
                          'Ralph','Raymond','Reginald','Richard','Robert','Ryan','Ronald',
                          'Samuel','Stanley','Steven','Seth','Sebastian',
                          'Thomas','Timothy','Tyler',
                          'Wallace','Walter','William','Wyatt',
                          'Xavier',
                          'Zachary',]
        
        self.surname_m_ru = ['Аношкин','Апатов','Апятов','Александров','Авлипов','Анатошкин','Аримченко','Абаранов','Адамов','Авличекко',
                        'Бытряков','Битряков','Борисов','Балипин','Базякин','Бурятов','Батурин',
                        'Ветров','Ветряков','Вадмиран','Вичатов','Викрович','Взаров','Версталин','Вокупин',
                        'Демитров','Донской','Денистарин','Дуров','Дамиченко','Доброградов','Далинин',
                        'Ермаков','Ефмеич','Егоров','Екатин',
                        'Жаровцев','Жирин','Жостченко','Жипин','Жилин',
                        'Задоров','Затриков','Зосин','Зазарин','Захаров','Захаев',
                        'Ильбанов','Инитаров','Известин','Итмирин','Изаченко','Избанов','Иоритов',
                        'Кристалин','Крост','Кисмисов',
                        'Лебедев','Литартасов','Ликрасов','Лесуч','Лобиченко',
                        'Митин','Матросов','Миклин','Меривич', 'Муратов', 'Матвеев','Мустин','Маслеников',
                        'Надурин','Нифёдов','Назаров','Николаев',
                        'Останткин','Остмов',
                        'Петроградов','Подушкин','Пирин','Пиров',
                        'Рокосовский','Радимов','Рютриков','Русланов','Ралин',
                        'Сантропов','Семёнов','Семечкин','Стасин','Спартаков',
                        'Фёдоров','Филиморов','Филатов',
                        'Хитров','Хитбаров','Хабарин',
                        'Шевцов','Шитрин','Шитин',
                        'Эдринский','Эшинский','Эпченко','Эрикс',
                        'Ютропов','Юлиев',
                        'Ярков','Яковлев','Ялубин','Явилин','Яшин',]
        
        self.surname_m_en = ['Akins','Alameda','Absher','Abramson','Alexandre','Alldredge','Alvarado','Amado',
                             'Barksdale','Barnard','Barney','Barrientos','Bartholomew','Bateman','Beckmann','Behm',
                             'Caballero','Caban','Canizales','Caplinger','Cardwell','Carleton','Cashman','Caudle',
                             'Daw',]
        
        self.name_f_ru = [ 'Аглая','Арина','Арина','Анна','Августина','Аделина','Ангелина','Анжела','Анфиса','Ася', 'Анастасия', 'Александра',
                        'Валентина','Владислава','Ваннеса','Виктория','Вероника','Вера',
                        'Галина',
                        'Дария','Диана','Дора',
                        'Елена','Евгения','Ева','Екатерина','Елизавета',
                        'Жанна',
                        'Зарина','Зоя',
                        'Инна','Ива','Ирина',
                        'Калина','Кира', 'Кристина',
                        'Лариса','Любовь','Лина',
                        'Майя','Марина','Мария','Марьяна',
                        'Ника','Надежда',
                        'Олеся','Оксана','Ольга',
                        'Полина',
                        'Рая','Раиса','Роза','Рита',
                        'Сабина','София','Стефания',
                        'Таисия','Татьяна',
                        'Эля','Эльга',
                        'Яна','Ярина',]
        
        self.name_f_en = ['Ann','Adelina','Amelia','Avery','Ada',
                          'Bailey','Barbara',
                          'Chloe','Cecilia','Catherine',
                          'Daisy','Danielle','Delia','Dorothy',
                          'Elizabeth','Ella','Erin',
                          'Freda','Fiona','Faith',
                          'Gloria','Grace',
                          'Helen','Hannah','Haley','Hailey',
                          'Isabel','Isabella',
                          'Jane','Jada','Julia','Joyce',
                          'Katherine','Kayla','Kylie','Katelyn','Kaitlyn',
                          'Lucy','Luccile','Lorna','Lily','Leslie','Lillian',
                          'Maria','Madeline','Mabel','Monica','Molly','Michelle','Mia',
                          'Nancy','Natalie','Nora',
                          'Olivia',
                          'Priscilla','Penelope','Pauline','Pamela',
                          'Rita','Riley','Rachel','Rose',
                          'Sandra','Sara','Sylvia','Shirley',
                          'Trinity','Vanessa','Victoria','Violet','Virginia',
                          'Winifred',
                          'Yvonne',
                          'Zoe',]
        
        self.surname_f_ru = ['Алианна','Альяна','Атрасова','Апяткова','Авиолова','Анатошкина','Адианова','Асокина','Асотина','Алимарова',
                        'Бистибюлина','Бистинова','Бильбина','Балина','Базякина','Бурова','Батросова',
                        'Виталина','Верченко','Вистибюлина','Волчанова','Васюткина','Взирова','Ветрова','Вилина',
                        'Добровая','Дианнова','Деченко','Дякина','Дасимова','Добрич','Долинина',
                        'Етиспатова','Еровенич','Есушкина','Едурина',
                        'Жилинна','Жигулич','Житрипевич','Жигина','Жорина',
                        'Зимаидова','Зимина','Зосина','Зарецская','Замитрова','Зюсина',
                        'Ильнасова','Ирибинко','Истучева','Исшенко','Ипритова','Илизова','Иоритова',
                        'Кристальная','Кристинова','Космович',
                        'Ликрасова','Литрасова','Лобина','Логина','Лосинова',
                        'Миликанова','Мутулина','Марошина','Мертеич', 'Муратова', 'Матвеева','Мулина','Мастович',
                        'Никитова','Неримова','Настюшина','Николаева',
                        'Осенняя','Отмирова',
                        'Петрокамчатская','Полинина','Пирова','Пасутина',
                        'Роловинина','Ракусина','Рюрович','Руслаченко','Ралина','Родова',
                        'Сандалина','Семикрасова','Сачкова','Салтыкова','Спорина',
                        'Фёдорова','Филиморова','Филатова',
                        'Хирипова','Хиширина','Хочубина',
                        'Шевцова','Шитина','Шитрина',
                        'Эдолинова','Эльдарова','Эпченко','Эпистатова',
                        'Ютропова','Юлиева',
                        'Яркова','Яковлева','Ялубина','Явилина','Яшина',]
        
        self.surname_f_en = ['Butler','Bishop','Blare','Bladshaw','Brooks','Bush','Babcook',
                             'Gray',
                             'Red',]
        
        self.num_part1_ru = ['001','002','003','004','005','006','007','008','009',]

        self.num_part2_ru = ['2415537','4636643','6438943','0077543','6536673','3564575','3513355','0006559',
                       '9997590','8654581','1010853','6695888','4256343','6476754','1215467','53674367',]
        
        self.email = ['rei793h','AlexHyIO','PORAMT1K','lsui1994','4345g2aw24y',
                      'georagl:wedmak','neomeo228','fifynya','930ip42','4444ererer4444',
                      'uow54io','xxxkeepmedownxxx','tytyr1n3','fil4rok','0101hh0101','QQooyyuurrnnIIwwqqxxzzQQ','popyt1k','tyrn1k','776',
                      'heroesRusich2007','igrikoh93w','3232lisabonka3232','youtubeTheBest','goverment_the_RCX','le4ko',
                      'tribasyakin_nikoplay','godEX55','beebag','3432','botik_shotik','joj1sus','LXCVWERSI',
                      'boris_ermakov75','barbara33','poplin_goblin','leeasaANDvanesa','so2H2O',
                      'yorik1900','kidsfam78','jackPreston89','l0lGRENDY']
        
        self.login = ['georg','dotatop','fakerCCX','marii67','CMEPTb_B_KYCTAX','Pavlik9090','Zs1mpleV','TOPOLb_NA_OPYCKE','poritta','usoup53',
                      'likras','dorim_sakatov1989','kit0w0','7Andrew7UwU7Kirillov7','JacksonBest','Marin1A2A3A4','1tvista','4636745','rirorira','Zhushik1',
                      'SlengTab','Peorvits','jErR','NeoNexus','Ghost0x0x0Bust','joustin_eekn','KISSunya','tyrnado','youIbest','GerBeast',]
        
        self.email_index = ['@example.ru','@outlook.qq','@mcrs.com','@python-test.pyt', 'zimzas.yan']

        self.faddres_ru = ['Грибоедова','Ленина','Жаргонская','Сосоновая','Еловая',
                  'Пугачева','Комунистическая','Социалистическая','Дектярёва','Гагарина',
                  'Черная','Победителей','Мира','Малеева','Захарова', '20 октября']
        
        self.faddres_en = ['Green','Black','White','Red','Yellow','Purple','World War II','Heroes',
                           'Washincton','San-Alnaser','Uping','Down','Up','Technologys','Jackson','Security',
                           'Gloria','the 25th December','Carib','West','Douglas MacArthur','Violet','Labor','World',]
        
        self.fpassword = ['gpt4','aio','fake','ny_3#','reews','saVva_g0v0n','lilis','JACK','Kirill',
                          'qwerty123','bhor','1234567890abcdifg0987654321','3244310084y4','##836/@tg__inkt/**r','3t77++wwu%#!gj,_h',
                          'hhjj__++__%$43','35FFFFFPRES#4_+@$(!)','343494602UIUIH&*#__#(^&#___^#3663)256huh3',
                          '23425633','4625267','462646andrew','3678965','9686784','347264623jonh','3537767','2326567548','1234567876543292356loop',
                          '3235235','25246','6346437','5685856','23432325','5857978','098-89090','67336576','76354733',]
        
        self.fcity_ru = ['Санкт-Петербург','Москва','Великий Новгород','Тверь','Рязань','Ростов-на-дону','Владимир',
                         'Иваново','Ковров','Гусь-Хрустальный','Кострома','Плёс','Сочи','Казань','Иннополис',
                         'Ульяновск','Уфа','Шуя','Нижний Новгород','Екатеринбург','Челябинск','Омск','Краснодар',
                         'Красноярск','Томск','Новосибирск','Братск','Хабаровск','Владивосток','Южный Сахалин','Иркутск',]
        
        self.fcity_en = ['Washington','New-Your','Las-Vegas','Los-Sangeles','San-Francisco','Dallas','San-Diego','Miami','Chicago','Columbus',
                         'Portland','Phoenix','Denver','San-Antonio','Houston','Atlanta','Charlotte','Detroit','Seattle',]
        
    def genRegion(self, region):
        reg = 'ru'
        self.reg = region
    
    def info(self):
        return(f'Python library {self.name}, version {self.version}, patch {self.patch}')

    def fake_name(self, gender):
        self.gen = gender
        gn = self.reg
        if gn == 'ru':
            if self.gen == 'male':
                fakenmru = random.randint(0, len(self.name_m_ru) -1)
                fakesmru = random.randint(0, len(self.surname_m_ru) -1)
                return(f'{self.name_m_ru[fakenmru]} {self.surname_m_ru[fakesmru]}')
                
            elif self.gen == 'female':
                fakenfru = random.randint(0, len(self.name_f_ru) -1)
                fakesfru = random.randint(0, len(self.surname_f_ru) -1)
                return(f'{self.name_f_ru[fakenfru]} {self.surname_f_ru[fakesfru]}')
            else:
                return('Error №1! Enter True Value!')

        elif gn == 'en':
            if self.gen == 'male':
                fakenmen = random.randint(0, len(self.name_m_en) -1)
                fakesmen = random.randint(0, len(self.surname_m_en) -1)
                return(f'{self.name_m_en[fakenmen]} {self.surname_m_en[fakesmen]}')
            elif self.gen == 'female':
                fakenfen = random.randint(0, len(self.name_f_en) -1)
                fakesfen = random.randint(0, len(self.surname_f_en) -1)
                return(f'{self.name_f_en[fakenfen]} {self.surname_f_en[fakesfen]}')
            else:
                return('Error #001! Please, enter all value!')

    def fake_number(self):
        gn = self.reg
        if gn == 'ru':
            fakenum1ru = random.randint(0, len(self.num_part1_ru) -1)
            fakenum2ru = random.randint(0, len(self.num_part2_ru) -1)
            return(f'+7{self.num_part1_ru[fakenum1ru]}{self.num_part2_ru[fakenum2ru]}')
        elif gn == 'en':
            fakenum1en = random.randint(0, len(self.num_part1_ru) -1)
            fakenum2en = random.randint(0, len(self.num_part2_ru) -1)
            return(f'+1{self.num_part1_ru[fakenum1en]}{self.num_part2_ru[fakenum2en]}')
    
    def fake_addres(self, full):
        f = False
        self.f = full
        gn = self.reg
        if gn == 'ru':
            if self.f == False:
                fakeaddresru = random.randint(0, len(self.faddres_ru) -1)
                return(f'ул. {self.faddres_ru[fakeaddresru]} {random.randint(1, 120)}')
            elif self.f == True:
                fakecru = random.randint(0, len(self.fcity_ru) -1)
                fakeaddresru = random.randint(0, len(self.faddres_ru) -1)
                return(f'г.{self.fcity_ru[fakecru]}, ул. {self.faddres_ru[fakeaddresru]} {random.randint(1, 120)}')
            elif self.f == '':
                fakeaddresru = random.randint(0, len(self.faddres_ru) -1)
                return(f'ул. {self.faddres_ru[fakeaddresru]} {random.randint(1, 120)}')
            
        elif gn == 'en':
            if self.f == False:
                fakeaddresen = random.randint(0, len(self.faddres_en) -1)
                return(f'{random.randint(1, 120)} {self.faddres_en[fakeaddresen]} Streed')
            elif self.f == True:
                fakecen = random.randint(0, len(self.fcity_en) -1)
                fakeaddresen = random.randint(0, len(self.faddres_en) -1)
                return(f'{self.fcity_en[fakecen]} City, {random.randint(1, 120)} {self.faddres_en[fakeaddresen]} Streed')
            elif self.f == '':
                fakeaddresen = random.randint(0, len(self.faddres_en) -1)
                return(f'{random.randint(1, 120)} {self.faddres_en[fakeaddresen]} Streed')
    
    def fake_email(self):
        fakeei = random.randint(0, len(self.email_index) -1)
        fakee = random.randint(0, len(self.email) -1)
        return(f'{self.email[fakee]}{self.email_index[fakeei]}')
    
    def fake_pass(self):
        fakepass2 = random.randint(0, len(self.fpassword) -1)
        return(f'{self.fpassword[fakepass2]}fu{random.randint(10000000, 99999999)}{self.fpassword[fakepass2]}')
    
    def fake_dob(self):
        year = random.randint(1920, 2024)
        morth = random.randint(0, 12)
        if morth == 2:
            day = random.randint(0, 28)
            return(f'{day}.{morth}.{year}')
        else:
            day = random.randint(0, 30)
            return(f'{day}.{morth}.{year}')
        
    def fake_city(self):
        gn = self.reg
        if gn == 'ru':
            fakecru = random.randint(0, len(self.fcity_ru) -1)
            return(f'г.{self.fcity_ru[fakecru]}')
        elif gn == 'en':
            fakecen = random.randint(0, len(self.fcity_en) -1)
            return(f'{self.fcity_en[fakecen]} city')
        
    def fake_banknumber(self):
        return(f"{random.randint(1000, 1500)} {random.randint(1000, 3000)} {random.randint(1000, 9000)} {random.randint(1000, 9000)}")
    
    def fake_login(self):
        fakel = random.randint(0, len(self.login) -1)
        return(self.login[fakel])

if __name__ == '__main__':
    fu = Fu()
    fu.genRegion('ru')