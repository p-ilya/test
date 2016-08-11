import numpy as np

''' ВАЖНО!
NetworkX ругается на русскоязычные комментарии.
При ошибках - удалить без жалости.'''

array = [[0,1,1,1,1,0,0,0,1,1,1,1,1,1,0,0,0,1,0,0],
         [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1],
         [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,0,1],
         [0,0,0,0,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0],
         [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,1,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0],
         [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,1,1,1,0,0,0,0,1,0,1,1,1,0,1,0]]
DICT = {0:'Obiekt',
        1:'Sviaz',
        2:'Xarakteristik',
        3:'Tzeloe',
        4:'Povidenie',
        5:'PodsFunkzionirovanie',
        6:'Struktura',
        7:'Situation',
        8:'Razvitie',
        9:'Element',
        10:'Sostoanie',
        11:'Kachestvo',
        12:'Sreda',
        13:'Svoistvo',
        14:'Podsistema',
        15:'Ypravlenie',
        16:'Tcel',
        17:'Integrativnii svoistva',
        18:'Derevo svoistv',
        19:'System'
        }
# Преобразует матрицу для работы с numpy.
matrix = np.array(array)

class MyNode():
    '''Custom class for storing node info.
name = node number, starting from 0 (int),
x,y = graph coordinates,
connected = all connected nodes (list),
level = level number (int),
label = text name (str, no russian!),
parents, children = predecessors and successors, lists.
'''
    def __init__(self,name):
        self.name = name
    def __str__(self):
        return '{}'.format(self.name)
    def set_xy(self,x,y):
        self.x = x
        self.y = y
    def connected_to(self, rel_dict):
        if self.name in rel_dict.keys():
            self.connected = rel_dict[self.name]
        else:
            self.connected = []
    def set_level(self, level):
        self.level = level
    def set_label(self,label):
        self.label = label
    def find_parents(self, dictionary):
        self.parents = dictionary[self.name]
    def find_children(self):
        self.children = []
        for node in self.connected:
            if node not in self.parents:
                self.children.append(node)

def find_edges(array):
    ''' Находим грани по исходной матрице.
    1 на пересечении строки и столбца.'''
    EDGELIST = []
    for line in array:
        for i in range(0,len(line)):
            if line[i]==1:
                EDGELIST.append((array.index(line),i))
    return EDGELIST

''' Список граней, используется при отрисовке графа.'''
EDGELIST = find_edges(array)

def find_relatives(edgelist):
    ''' Для каждой точки находит список точек, с которымти она связана.'''
    rel_dict = {}
    for node in DICT.keys():
        c_list = []
        for pair in edgelist:
            if node in pair:
                # print('{0} connected via {1}'.format(node,pair))
                for i in pair:
                    if i!=node: c_list.append(i)
        rel_dict[node]=c_list
    return rel_dict

''' Словарь, в котором для каждой точки указаны те,
с которыми она связана.'''
REL_DICT = find_relatives(EDGELIST)

def find_parents(edgelist):
    ''' Ищет в списке связей точки, которые находятся на нижних уровнях.'''
    p_dict = {}
    for node in DICT.keys():
        parents = []
        for pair in edgelist:
            if pair[1]==node:
                parents.append(pair[0])
        parents = list(set(parents))
        p_dict[node] = parents
    return p_dict

''' Словарь, в котором для каждой точки указаны те,
с которыми она связана и которые находятся на нижних уровнях.'''        
PAR_DICT = find_parents(EDGELIST)

# Создание списка уровней.
tree = []

def get_layer0(matrix):
    '''Ищет нулевой уровень - понятия, в которых не содржатся другие понятия.
    В матрице они представлены как нулевые столбцы.'''
    layer0 = []
    for i in range(0,matrix.shape[1]):
        if sum(matrix[:,i])<1:
            layer0.append(i)
    return layer0

# Добавить 0-й уровень в список уровней.
tree.append(get_layer0(matrix))

''' Копия словаря с "родителями" точек.
На каждом уровне точки, входящие в него, удаляются, чтобы не попадать в уровни выше.'''
r_dict = PAR_DICT.copy()

def find_next_layer(c_list):
    '''Ищет следующие уровни, основываясь на найденном предыдущем.
    Начинает с 1-го уровня (0-й найден выше).'''
    global r_dict
    next_layer = []
    for node in r_dict:
        trigger = True
        if len(r_dict[node])>0:
            for element in r_dict[node]:
                if element not in c_list:
                    trigger = False
        else: trigger = False
        if trigger:
            next_layer.append(node)
            r_dict[node] = []
    #print(next_layer)
    return next_layer

# Список для сравнения, пополняется с каждой итерацией.
c_list = get_layer0(matrix)
while True:
    layer_n = find_next_layer(c_list)
    if not layer_n: break
    tree.append(layer_n)
    for i in layer_n:
        c_list.append(i)

print('Level tree:\n {}'.format(tree))

# Создаем список из точек-объектов (так удобнее хранить информацию)
my_nodes_list = []
for node in DICT.keys():
    a = MyNode(node)
    a.connected_to(REL_DICT)
    for level in tree:
        if a.name in level:
            a.set_level(tree.index(level))
    a.find_parents(PAR_DICT)
    a.find_children()
    a.set_label(DICT[node])
    my_nodes_list.append(a)
'''
Выыод информации по точкам (для проверки)
for item in my_nodes_list:
    print('{0}, {1}\nParents: {2}\nLevel: {3}\n'.format(item.name,item.label,item.parents,item.level))
'''
