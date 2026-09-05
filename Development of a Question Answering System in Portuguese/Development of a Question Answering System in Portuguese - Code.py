#PLN Meta 3
#Verificar se todas as bibliotecas estão instaladas
#Ter os documentos instalados e redirecionar a pasta
import json
from matplotlib import pyplot as plt
from numpy import mean 
from nltk.corpus import wordnet as wn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.decomposition import LatentDirichletAllocation, TruncatedSVD
from sklearn.metrics import silhouette_score
from sklearn.svm import SVC
import numpy as np
from transformers import pipeline
import easygui
 
dRes = open(r"C:\Users\david\Desktop\UC\Programação\TXT\restaurantsCoimbra_db.json",encoding="utf8")
dHotels = open(r"C:\Users\david\Desktop\UC\Programação\TXT\hotelsCoimbra_db.json",encoding="utf8")
dAtr = open(r"C:\Users\david\Desktop\UC\Programação\TXT\attractionsCoimbra_db.json",encoding="utf8")
dDial = open(r"C:\Users\david\Desktop\UC\Programação\TXT\dialogosCoimbra.json",encoding="utf8")

dataRes = json.load(dRes)
dataHotels = json.load(dHotels)
dataAtr = json.load(dAtr)
dataDial = json.load(dDial)

allData =[dataRes,dataHotels,dataAtr]
listaCarc=['-',".",":",",",";",">","<","~","^","+","*","«","»","'","?","=","}","]",")","(","[","{","/","&","%","$","#","§","£","@","!","|",'']
listaAllTypesPT =['restaurante','pousada','residencial','hotel','piscina','teatro','arquitetura','discoteca','museu','barco','jardim','entretenimento','faculdade','cinema','desporto','salão']
listaAllTypesPTP = ['restaurantes','pousadas','residenciais','hotéis','piscinas','teatros','arquiteturas','discotecas','museus','barcos','jardins','entretenimentos','faculdades','cinemas','desportos','salões']
listaAllTypesI =['restaurant','guesthouse','guesthouse','hotel','swimmingpool', 'theatre', 'architecture', 'nightclub', 'museum', 'boat', 'park', 'entertainment', 'college', 'cinema', 'mutliple sports', 'concerthall']
allfoodI = ['italian', 'international', 'indian', 'chinese', 'portuguese', 'european', 'mexican', 'modern european', 'vietnamese', 'spanish', 'french', 'japanese', 'british', 'korean', 'turkish', 'asian oriental', 'gastropub', 'mediterranean', 'thai']
allfoodPT = ['italiana', 'internacional', 'indiana', 'chinesa', 'portuguesa', 'europeia', 'mexicana', 'moderna europeia', 'vietnamita', 'espanhola', 'francesa', 'japonesa', 'britanica', 'coreana', 'turca', 'asática', 'gastropub', 'mediterrânea', 'tailandêsa']
allareaI = ['centre', 'north', 'east', 'south', 'west', 'centro']
allareaPT = ['central', 'norte', 'este', 'sul', 'oeste', 'central']
outrasPIntI = ['area','food','stars']
outrasPIntPT = ['área','comida','estrelas']
allpriceI = ['cheap','moderate','expensive']
allpricePT = ['barato','moderado','caro']
#
def eCarc(s, lc): # Retira os caracteres não pretendidos
    for char in lc:
        s = s.replace(char, '')
    return s
#
def info(l): # Faz o print final dos resultados
    # Info importante: 
    # address,area,food,name,postcode,pricerange,type - Restaurantes - 1
    # address,area,internet,parking,name,postcode,pricerange,type - Hotel/Guesthouse - 2
    # address,area,name,postcode,pricerange,type - Attractions - 3
    lFInfo = []
    for t in l:
        h = None
        i = None
        b = None
        k = (" ;")
        if "type" in t:
            aux =t["type"]
            aux = verifP(aux,listaAllTypesI,listaAllTypesPT)
            a = ("Este "+str(aux))
        if "address" in t:
            aux = t["address"]
            d = (", localizado na "+str(aux)+" ")
        if "area" in t:
            aux = t["area"]
            aux = verifP(aux,allareaI,allareaPT)
            f = (", na área "+str(aux))
        if "name" in t:
            aux = t["name"]
            c = (" com o nome "+str(aux))
        if "postcode" in t:
            aux = t["postcode"]
            e = str((aux))     
        if "pricerange" in t:
            aux = t["pricerange"]
            aux = verifP(aux,allpriceI,allpricePT)
            g = (". Tem um pricerange: "+str(aux))
        if "food" in t:
            aux = t["food"]
            aux = verifP(aux,allfoodI,allfoodPT)
            b = (" de comida "+str((aux)))
        if "internet" in t:
            aux = t["internet"]
            h = (", internet: "+str(aux))
        if "parking" in t:
            aux = t["parking"]
            i = (", parque: "+str(aux))
        if "stars" in t:
            aux = t["stars"]
            j = (" de "+str(aux)+" estrelas")

        if h == None:
            if i == None:
                if b != None:
                    r = a+b+c+d+e+f+g+k
                    lFInfo.append(r)
                else:
                    r = a+c+d+e+f+g+k
                    lFInfo.append(r)
        else: 
            if i != None:
                r = a+c+j+d+e+f+g+h+i+k
                lFInfo.append(r)
    return lFInfo
#
def verifF(fU,LPI,LPPT): # Verifica e altera palavras que não estejam conforme o pretendido #Erro
    for p in range(len(fU)):
        for i in range(len(LPI)):
            if fU[p] == LPI[i]:
                fU[p] = LPPT[i]
    return fU
#
def verifP(P,LPI,LPPT): # Verifica e altera palavras que não estejam conforme o pretendido
    for i in range(len(LPI)):
        if P == LPI[i]:
            P = LPPT[i]
            break
    return P
#
def ListaFinal(lt,ln,la,laa,lfo,ls): # Adiciona todos os dicionários a uma lista, que vai ser o resultado 
    lf = []
    laux = [lt,ln,la,laa,lfo,ls]
    for l in laux:
        if len(l) != 0:
            for t in l:
                lf.append(t)
    dupl1 = [item for item in lf if lf.count(item) > 1] # Vale a pena fazer isto ou é bom ter as duas hipoteses?
    dupl2 = [item for item in lf if lf.count(item) > 2]
    if len(dupl2) != 0:
        if len(dupl1) > 3:
            dupl = dupl2
        else:
            dupl = dupl1
    else:
        dupl = dupl1
    lf = []
    for item in dupl:
        if item not in lf:
            lf.append(item)
    # Como não podemos dar mais importancia a certas palavras que outras o resultado não vai ser 100% certo
    return lf
#
def chatbot_function(user_input):
    # Lógica do chatbot
    user_input_split = user_input.split(" ")
    rF = []
    rAddr = []
    rName = []
    lAuxAddr = []
    lAuxName = []
    lAuxType = []
    lAuxArea = []
    lAuxStar = []
    lAuxFood = []
    cAuxAddr = []
    cAuxName = []

    # Limpeza e processamento da entrada do usuário

    for i in range(len(user_input_split)):
        user_input_split[i] = user_input_split[i].lower()
        user_input_split[i] = eCarc(user_input_split[i], listaCarc) # Função de remoção de caracteres indesejados
    user_input_split = verifF(user_input_split, listaAllTypesI, listaAllTypesPT) # Função de verificação e substituição de frases
    user_input_split = verifF(user_input_split, listaAllTypesPTP, listaAllTypesPT) 
    user_input_split = verifF(user_input_split, allareaI, allareaPT)
    user_input_split = verifF(user_input_split, outrasPIntI, outrasPIntPT) 

    for n in allData:
        for j in n:
            if "type" in j:
                for t in range(len(listaAllTypesPT)):
                    for f in user_input_split:
                        if listaAllTypesPT[t] == f:
                            if j["type"] == listaAllTypesI[t]:
                                lAuxType.append(j)

            if "name" in j:
                auxName = j["name"].split(" ")
                auxName = [string.lower() for string in auxName]
                for f in user_input_split:
                    if f in auxName:
                        lAuxName.append(j)
                        if f not in cAuxName:
                            cAuxName.append(f)

            if "address" in j:
                auxAddr = j["address"].split(" ")
                auxAddr = [string.lower() for string in auxAddr]
                for f in user_input_split:
                    if f in auxAddr:
                        lAuxAddr.append(j)
                        if f not in cAuxAddr:
                            cAuxAddr.append(f)
            if "area" in j:
                for t in range(len(allareaPT)):
                    for f in user_input_split:
                        if allareaPT[t] == f:
                            if j["area"] == allareaI[t]:
                                lAuxArea.append(j)
            if "food" in j:
                for t in range(len(allfoodPT)):
                    for f in user_input_split:
                        if allfoodPT[t] == f:
                            if j["food"] == allfoodI[t]:
                                lAuxFood.append(j)
            if "stars" in j:
                    for f in range(len(user_input_split)):
                        if "estrelas" == user_input_split[f]:
                            if j["stars"] == user_input_split[f-1]:
                                lAuxStar.append(j)                    


    if len(user_input_split) > 1:
        if len(cAuxAddr) > 1:
            duplicadosAddr = [item for item in lAuxAddr if lAuxAddr.count(item) > 1]
            for item in duplicadosAddr:
                if item not in rAddr:
                    rAddr.append(item)
        else:
            for item in lAuxAddr:
                if item not in rAddr:
                    rAddr.append(item)

        if len(cAuxName) > 1:
            duplicadosName = [item for item in lAuxName if lAuxName.count(item) > 1]
            for item in duplicadosName:
                if item not in rName:
                    rName.append(item)
        else:
            for item in lAuxName:
                if item not in rName:
                    rName.append(item)
        rF = ListaFinal(lAuxType, rName, rAddr,lAuxArea,lAuxFood,lAuxStar)

    else:
        for item in lAuxAddr:
            if item not in rF:
                rF.append(item)
        for item in lAuxName:
            if item not in rF:
                rF.append(item)
        for item in lAuxType:
            if item not in rF:
                rF.append(item)
        for item in lAuxArea:
            if item not in rF:
                rF.append(item)
        for item in lAuxFood:
            if item not in rF:
                rF.append(item)
        for item in lAuxStar:
            if item not in rF:
                rF.append(item)
    if len(rF) == 0:
        response = "Não há informações acerca do pedido..."
    else:
        rF = info(rF) # Resultado
        response = "\n".join(rF)

    return response
#
def extract_dados(dialog_data):
    user_inputs = []
    correct_responses = []

    for dial in dialog_data:
        aux = dial['services']
        if 'train' in aux or 'taxi' in aux:
            continue

        user_utterances = [turn['utterance'] for turn in dial['turns'] if turn['speaker'] == 'USER']
        system_responses = [turn['utterance'] for turn in dial['turns'] if turn['speaker'] == 'SYSTEM']

        if user_utterances:
            user_input = user_utterances[0]
            user_inputs.append(user_input)
        if system_responses:
            system_input = system_responses[0]
            correct_responses.append(system_input)

    return user_inputs,correct_responses
#
def calculate_precision(true_string, predicted_string):
    true_positives = 0
    true_string = true_string.lower()
    true_string = true_string.split()
    predicted_string = predicted_string.lower()
    predicted_string = predicted_string.split()

    for i in true_string:
        for j in predicted_string:
            if j == i:
                true_positives +=1

    false_positives = max(len(true_string), len(predicted_string)) - true_positives

    return true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
#
def calculate_f1_score(precision,recall):

    return ((2*precision*recall)/(precision+recall))
#
def calculate_accuracy(true_string, predicted_string):
    true_positives = 0
    true_negatives = 0

    true_string = true_string.lower()
    true_string = true_string.split()
    predicted_string = predicted_string.lower()
    predicted_string = predicted_string.split()

    for i in true_string:
        for j in predicted_string:
            if j == i:
                true_positives +=1

    for i in true_string:
        for j in predicted_string:
            if j != i:
                true_negatives +=1
    
    false_positives = len(predicted_string) - true_positives
    false_negatives = len(true_string) - true_positives

    return ((true_positives+true_negatives)/(true_positives+true_negatives+false_positives+false_negatives))
#
def calculate_recall(true_string, predicted_string):
    true_positives = 0

    true_string = true_string.lower()
    true_string = true_string.split()
    predicted_string = predicted_string.lower()
    predicted_string = predicted_string.split()

    for i in true_string:
        for j in predicted_string:
            if j == i:
                true_positives +=1

    false_negatives = len(true_string) - true_positives

    return true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
#
def evaluate_chatbot(user_utterances, system_responses):
    user_inputs = []
    correct_responses = []
    predicted_responses = []
    all_precison = []
    all_recall = []
    all_f1_score = []
    all_accuracy = []


    for i in range(100):
        user_input = user_utterances[i]
        correct_response = system_responses[i]

        predicted_response = chatbot_function(user_input)  # Use chatbot_function para obter a resposta

        user_inputs.append(user_input)
        correct_responses.append(correct_response)
        predicted_responses.append(predicted_response)

    for i in range(len(correct_responses)):
        precision = calculate_precision(correct_responses[i], predicted_responses[i])
        recall = calculate_recall(correct_responses[i], predicted_responses[i])
        if precision == 0 and recall == 0:
            f1 = 0
        else :
            f1 = calculate_f1_score(precision, recall)
        accuracy = calculate_accuracy(correct_responses[i], predicted_responses[i])

        all_precison.append(precision)
        all_recall.append(recall)
        all_f1_score.append(f1)
        all_accuracy.append(accuracy)
        
    m_precision = mean(all_precison)
    m_recall = mean(all_recall)
    m_f1_score = mean(all_f1_score)
    m_accuracy = mean(all_accuracy)

    tf_vect = TfidfVectorizer()
    dados = correct_responses
    p_tf = tf_vect.fit_transform(dados)
    novos_vects = tf_vect.transform(predicted_responses)
    r_cosine = cosine_similarity(p_tf, novos_vects) #similaridade do coseno
    m_cosine = mean(r_cosine)

    return {
        'precision': "{:.4f}".format(m_precision),
        'recall': "{:.4f}".format(m_recall),
        'f1_score': "{:.4f}".format(m_f1_score),
        'accuracy': "{:.4f}".format(m_accuracy),
        'cosine similarity': "{:.4f}".format(m_cosine),
        }
#
def k_means_O(correct_responses):
    aux = correct_responses[0:100]
    vectorizer = TfidfVectorizer()  
    X = vectorizer.fit_transform(aux)
    svd = TruncatedSVD(n_components=2)
    reduced_tfidf = svd.fit_transform(X)

    num_clusters = 3

    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    kmeans.fit(reduced_tfidf)

    labels = kmeans.labels_
    centers = kmeans.cluster_centers_

    plt.scatter(reduced_tfidf[:, 0], reduced_tfidf[:, 1], c=labels, cmap='viridis', alpha=0.5)
    plt.scatter(centers[:, 0], centers[:, 1], c='red', marker='x', s=100)
    plt.title('K-means Clustering')
    plt.show()
#
def kmeans_silhouette(user_utterances,correct_responses):
    raux = []
    aux = correct_responses[0:100]
    for i in range(100):
        r  = chatbot_function(user_utterances[i])
        raux.append(r)

    tf_vect = TfidfVectorizer()

    
    p_tf = tf_vect.fit_transform(aux)
    novos_vects = tf_vect.transform(raux)
    
    svd = TruncatedSVD(n_components=2) # redução de dimensionalidade, para encontrar uma aproximação de baixa dimensão de uma matriz original.
    reduced_tfidf = svd.fit_transform(novos_vects)

    num_clusters = 3

    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(reduced_tfidf)

    labels = kmeans.labels_

    silhouette_avg = silhouette_score(reduced_tfidf, labels)
    print(f"Silhouette Score - Kmeans: {silhouette_avg}")
#
def tf_idf_kmeans(user_utterances, correct_responses):
    raux = []
    aux = correct_responses[0:100]
    for i in range(100):
        r = chatbot_function(user_utterances[i])
        raux.append(r)

    tf_vect = TfidfVectorizer()

    p_tf = tf_vect.fit_transform(aux)
    novos_vects = tf_vect.transform(raux)

    svd = TruncatedSVD(n_components=2) # redução de dimensionalidade, para encontrar uma aproximação de baixa dimensão de uma matriz original.
    reduced_tfidf = svd.fit_transform(novos_vects)

    terms = tf_vect.get_feature_names_out()

    num_clusters = 3
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    kmeans.fit(reduced_tfidf)

    # Obter os rótulos dos clusters
    cluster_labels = kmeans.labels_

    tfidf_results = {} # armazenar os resultados do TF-IDF
    for doc_index, doc in enumerate(aux):
        cluster_label = cluster_labels[doc_index] 
        if cluster_label not in tfidf_results:
            tfidf_results[cluster_label] = {} # cria um dic para cada cluster

        feature_index = reduced_tfidf[doc_index, :].nonzero()[0]
        tfidf_scores = zip(feature_index, [reduced_tfidf[doc_index, x] for x in feature_index]) # Cria uma lista contendo os indices e scores TF-IDF não nulos.

        for term, score in [(terms[i], score) for (i, score) in tfidf_scores]:
            tfidf_results[cluster_label][term] = score # dicionário que contém os scores TF-IDF associados a cada termo em cada cluster.

    tfidf_r = []
    for cluster_label, scores in tfidf_results.items():
        for term, score in scores.items():
            tfidf_r.append(score)
    tfidf_rr = mean(tfidf_r)
    print(f"TF-IDF - Kmeans: {tfidf_rr}")
#
def svm_silhouette(user_utterances, correct_responses):
    raux = []
    aux = correct_responses[0:9]
    for i in range(9):
        r = chatbot_function(user_utterances[i])
        raux.append(r)

    tf_vect = TfidfVectorizer()

    p_tf = tf_vect.fit_transform(aux)
    novos_vects = tf_vect.transform(raux)

    svd = TruncatedSVD(n_components=2) # redução de dimensionalidade, para encontrar uma aproximação de baixa dimensão de uma matriz original.
    reduced_tfidf = svd.fit_transform(novos_vects)

    
    labels = [0, 1, 2] * 3  # labels == len(aux)

    svm_classifier = SVC(kernel='linear')
    svm_classifier.fit(reduced_tfidf, labels)

    predicted_labels = svm_classifier.predict(reduced_tfidf)

    silhouette_avg = silhouette_score(reduced_tfidf, predicted_labels)
    print(f"Silhouette Score - SVM: {silhouette_avg}")
#
def tf_idf_svm(user_utterances, correct_responses):
    raux = []
    aux = correct_responses[0:9]
    for i in range(9):
        r = chatbot_function(user_utterances[i])
        raux.append(r)

    tf_vect = TfidfVectorizer()

    p_tf = tf_vect.fit_transform(aux)
    novos_vects = tf_vect.transform(raux)

    svd = TruncatedSVD(n_components=2) # redução de dimensionalidade, para encontrar uma aproximação de baixa dimensão de uma matriz original.
    reduced_tfidf = svd.fit_transform(novos_vects)

    terms = tf_vect.get_feature_names_out()

    labels = [0, 1, 2] * 3  # labels == len(aux)

    svm_classifier = SVC(kernel='linear')
    svm_classifier.fit(reduced_tfidf, labels)

    predicted_labels = svm_classifier.predict(reduced_tfidf)

    tfidf_results = {} # armazenar os resultados do TF-IDF
    for doc_index, doc in enumerate(aux):
        cluster_label = predicted_labels[doc_index]
        if cluster_label not in tfidf_results: # cria um dic para cada cluster
            tfidf_results[cluster_label] = {}

        feature_index = reduced_tfidf[doc_index, :].nonzero()[0]
        tfidf_scores = zip(feature_index, [reduced_tfidf[doc_index, x] for x in feature_index]) # Cria uma lista contendo os indices e scores TF-IDF não nulos.

        for term, score in [(terms[i], score) for (i, score) in tfidf_scores]:
            tfidf_results[cluster_label][term] = score # dicionário que contém os scores TF-IDF associados a cada termo em cada cluster.

    tfidf_r = []
    for cluster_label, scores in tfidf_results.items():
        for term, score in scores.items():
            tfidf_r.append(score)
    tfidf_rr = mean(tfidf_r)
    print(f"TF-IDF - SVM: {tfidf_rr}")
#
def lda_silhouette(user_utterances, correct_responses):
    raux = []
    aux = correct_responses[0:100]
    for i in range(100):
        r = chatbot_function(user_utterances[i])
        raux.append(r)

    tf_vect = TfidfVectorizer() # usado para converter o conjunto de documentos (aux) em uma matriz TF-IDF
    p_tf = tf_vect.fit_transform(aux)

    # Utilizar LDA para redução de dimensionalidade
    lda = LatentDirichletAllocation(n_components=3, random_state=42) # aplicado para redução de dimensionalidade usando LDA com 3 tópicos
    lda_representation = lda.fit_transform(p_tf)

    # Calcular o Silhouette Score
    silhouette_avg = silhouette_score(lda_representation, np.argmax(lda_representation, axis=1)) #calculado usando os resultados do LDA para avaliar a qualidade da separação entre os tópicos
    
    print(f"Silhouette Score - LDA: {silhouette_avg}")
#
def lda_tfidf(user_utterances, correct_responses):
    raux = []
    aux = correct_responses[0:100]
    for i in range(100):
        r = chatbot_function(user_utterances[i])
        raux.append(r)

    tf_vect = TfidfVectorizer() # usado para converter o conjunto de documentos (aux) em uma matriz TF-IDF
    p_tf = tf_vect.fit_transform(aux)

    # Utilizar LDA para redução de dimensionalidade
    lda = LatentDirichletAllocation(n_components=3, random_state=42) # aplicado para redução de dimensionalidade usando LDA com 2 tópicos.
    lda_representation = lda.fit_transform(p_tf)

    lda_r = []
    for i in range(lda_representation.shape[0]):
        for j in range(lda_representation.shape[1]):
            lda_r.append(lda_representation[i, j])
    lda_rr = mean(lda_r) # média dos valores nos resultados do LDA é calculada e impressa
    print(f"TF-IDF - LDA: {lda_rr}")
#
def ger_text2text(pergunta, predicted_response):
    input_text = "question: "+str(pergunta)+" context: "+str(predicted_response)

    text2text1 = pipeline("text2text-generation",model = 'pierreguillou/t5-base-qa-squad-v1.1-portuguese',max_length =50)
    pred1= text2text1(input_text)

    text2text2 = pipeline("text2text-generation",model = 'castorini/afriteva_v2_base',max_length =50)
    pred2= text2text2(input_text)

    return pred1,pred2
#
def ger_question_answering(pergunta,predicted_response):
    qa1 = pipeline("question-answering" , model = 'pierreguillou/bert-base-cased-squad-v1.1-portuguese')
    resposta1 = qa1(question = pergunta , context = predicted_response)

    qa2 = pipeline("question-answering" , model = 'timpal0l/mdeberta-v3-base-squad2')
    resposta2 = qa2(question = pergunta , context = predicted_response)

    qa3 = pipeline("question-answering" , model = 'eraldoluis/faquad-bert-base-portuguese-cased')
    resposta3 = qa3(question = pergunta , context = predicted_response)

    qa4 = pipeline("question-answering" , model = 'mrm8488/bert-base-portuguese-cased-finetuned-squad-v1-pt')
    resposta4 = qa4(question = pergunta , context = predicted_response)

    return resposta1['answer'],resposta1['score'],resposta2['answer'],resposta2['score'],resposta3['answer'],resposta3['score'],resposta4['answer'],resposta4['score']
#
def metricas(pred,va_pred):
    all_precison = []
    all_recall = []
    all_f1_score = []
    all_accuracy = []
    dados = []
    novos_dados = []

    precision = calculate_precision(pred,va_pred)
    recall = calculate_recall(pred,va_pred)
    if precision == 0 and recall == 0:
        f1 = 0
    else :
        f1 = calculate_f1_score(precision, recall)
    accuracy = calculate_accuracy(pred,va_pred)

    all_precison.append(precision)
    all_recall.append(recall)
    all_f1_score.append(f1)
    all_accuracy.append(accuracy)
        
    m_precision = mean(all_precison)
    m_recall = mean(all_recall)
    m_f1_score = mean(all_f1_score)
    m_accuracy = mean(all_accuracy)

    tf_vect = TfidfVectorizer()
    dados.append(pred)
    novos_dados.append(va_pred)
    p_tf = tf_vect.fit_transform(dados)
    novos_vects = tf_vect.transform(novos_dados)
    r_cosine = cosine_similarity(p_tf, novos_vects)
    m_cosine = mean(r_cosine)

    return m_precision,m_recall,m_f1_score,m_accuracy,m_cosine
#
def kmeans_silhouette_m3(pred,va_pred):
    dados = []
    dados.append(pred)

    tf_vect = TfidfVectorizer()

    
    p_tf = tf_vect.fit_transform(dados)
    novos_vects = tf_vect.transform(va_pred)
    
    svd = TruncatedSVD(n_components=2) # redução de dimensionalidade, para encontrar uma aproximação de baixa dimensão de uma matriz original.
    reduced_tfidf = svd.fit_transform(novos_vects)

    num_clusters = 3

    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(reduced_tfidf)

    labels = kmeans.labels_

    silhouette_avg = silhouette_score(reduced_tfidf, labels)

    resul = f"Silhouette Score - Kmeans: {silhouette_avg}"

    return resul
#
def tf_idf_kmeans_m3(pred,va_pred):
    dados = []
    dados.append(pred)

    tf_vect = TfidfVectorizer()

    p_tf = tf_vect.fit_transform(dados)
    novos_vects = tf_vect.transform(va_pred)

    svd = TruncatedSVD(n_components=2) # redução de dimensionalidade, para encontrar uma aproximação de baixa dimensão de uma matriz original.
    reduced_tfidf = svd.fit_transform(novos_vects)

    terms = tf_vect.get_feature_names_out()

    num_clusters = 3
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    kmeans.fit(reduced_tfidf)

    cluster_labels = kmeans.labels_

    tfidf_results = {} # armazenar os resultados do TF-IDF
    for doc_index, doc in enumerate(dados):
        cluster_label = cluster_labels[doc_index] 
        if cluster_label not in tfidf_results:
            tfidf_results[cluster_label] = {} # cria um dic para cada cluster

        feature_index = reduced_tfidf[doc_index, :].nonzero()[0]
        tfidf_scores = zip(feature_index, [reduced_tfidf[doc_index, x] for x in feature_index]) # Cria uma lista contendo os indices e scores TF-IDF não nulos.

        for term, score in [(terms[i], score) for (i, score) in tfidf_scores]:
            tfidf_results[cluster_label][term] = score # dicionário que contém os scores TF-IDF associados a cada termo em cada cluster.

    tfidf_r = []
    for cluster_label, scores in tfidf_results.items():
        for term, score in scores.items():
            tfidf_r.append(score)
    tfidf_rr = mean(tfidf_r)

    resul = f"TF-IDF - Kmeans: {tfidf_rr}"

    return resul
#
def svm_silhouette_m3(pred,va_pred):
    dados = []
    dados.append(pred)

    tf_vect = TfidfVectorizer()

    p_tf = tf_vect.fit_transform(dados)
    novos_vects = tf_vect.transform(va_pred)

    svd = TruncatedSVD(n_components=2) # redução de dimensionalidade, para encontrar uma aproximação de baixa dimensão de uma matriz original.
    reduced_tfidf = svd.fit_transform(novos_vects)

    
    labels = [0, 1, 2] * 2  # labels == len(aux)

    svm_classifier = SVC(kernel='linear')
    svm_classifier.fit(reduced_tfidf, labels)

    predicted_labels = svm_classifier.predict(reduced_tfidf)

    silhouette_avg = silhouette_score(reduced_tfidf, predicted_labels)

    resul = f"Silhouette Score - SVM: {silhouette_avg}"

    return resul
#
def tf_idf_svm_m3(pred,va_pred):
    dados = []
    dados.append(pred)

    tf_vect = TfidfVectorizer()

    p_tf = tf_vect.fit_transform(dados)
    novos_vects = tf_vect.transform(va_pred)

    svd = TruncatedSVD(n_components=2) # redução de dimensionalidade, para encontrar uma aproximação de baixa dimensão de uma matriz original.
    reduced_tfidf = svd.fit_transform(novos_vects)

    terms = tf_vect.get_feature_names_out()

    labels = [0, 1, 2] * 2  # labels == len(aux)

    svm_classifier = SVC(kernel='linear')
    svm_classifier.fit(reduced_tfidf, labels)

    predicted_labels = svm_classifier.predict(reduced_tfidf)

    tfidf_results = {} # armazenar os resultados do TF-IDF
    for doc_index, doc in enumerate(dados):
        cluster_label = predicted_labels[doc_index]
        if cluster_label not in tfidf_results: # cria um dic para cada cluster
            tfidf_results[cluster_label] = {}

        feature_index = reduced_tfidf[doc_index, :].nonzero()[0]
        tfidf_scores = zip(feature_index, [reduced_tfidf[doc_index, x] for x in feature_index]) # Cria uma lista contendo os indices e scores TF-IDF não nulos.

        for term, score in [(terms[i], score) for (i, score) in tfidf_scores]:
            tfidf_results[cluster_label][term] = score # dicionário que contém os scores TF-IDF associados a cada termo em cada cluster.

    tfidf_r = []
    for cluster_label, scores in tfidf_results.items():
        for term, score in scores.items():
            tfidf_r.append(score)
    tfidf_rr = mean(tfidf_r)

    resul = f"TF-IDF - SVM: {tfidf_rr}"

    return resul
#
def lda_silhouette_m3(pred,va_pred):
    dados = []
    dados.append(pred)

    tf_vect = TfidfVectorizer() # usado para converter o conjunto de documentos (aux) em uma matriz TF-IDF

    p_tf = tf_vect.fit_transform(dados)
    novos_vects = tf_vect.transform(va_pred)

    # Utilizar LDA para redução de dimensionalidade
    lda = LatentDirichletAllocation(n_components=5, random_state=42) # aplicado para redução de dimensionalidade usando LDA com 3 tópicos
    lda_representation = lda.fit_transform(novos_vects)

    # Calcular o Silhouette Score
    silhouette_avg = silhouette_score(lda_representation, np.argmax(lda_representation, axis=1)) #calculado usando os resultados do LDA para avaliar a qualidade da separação entre os tópicos
    
    resul = f"Silhouette Score - LDA: {silhouette_avg}"

    return resul
#
def lda_tfidf_m3(pred,va_pred):
    dados = []
    dados.append(pred)

    tf_vect = TfidfVectorizer() # usado para converter o conjunto de documentos (aux) em uma matriz TF-IDF

    p_tf = tf_vect.fit_transform(dados)
    novos_vects = tf_vect.transform(va_pred)

    # Utilizar LDA para redução de dimensionalidade
    lda = LatentDirichletAllocation(n_components=5, random_state=42) # aplicado para redução de dimensionalidade usando LDA com 3 tópicos
    lda_representation = lda.fit_transform(novos_vects)

    lda_r = []
    for i in range(lda_representation.shape[0]):
        for j in range(lda_representation.shape[1]):
            lda_r.append(lda_representation[i, j])
    lda_rr = mean(lda_r) # média dos valores nos resultados do LDA é calculada e impressa

    return f"TF-IDF - LDA: {lda_rr}"
#
def exibir_prints():
    while True:
        user_input = easygui.enterbox("O que deseja: ", "PLN - Meta3")
        if user_input == None:
            break
        elif user_input == "":
            break
        else:
            #pergunta = "Que restaurantes posso encontrar na zona oeste?"
            pergunta = user_input
            predicted_response = chatbot_function(pergunta) 
            pt2t1,pt2t2 =ger_text2text(pergunta, predicted_response)
            pt2t1f = pt2t1[0]
            pt2t2f = pt2t2[0]

            m_precision1,m_recall1,m_f1_score1,m_accuracy1,m_cosine1 = metricas(predicted_response,pt2t1f['generated_text'])
            m_precision2,m_recall2,m_f1_score2,m_accuracy2,m_cosine2 = metricas(predicted_response,pt2t2f['generated_text'])

            R = []
            R.append(pt2t1f['generated_text'])
            R.append(pt2t2f['generated_text'])
            
            
            r1,rs1,r2,rs2,r3,rs3,r4,rs4 = ger_question_answering(pergunta,predicted_response)

            m_precision3,m_recall3,m_f1_score3,m_accuracy3,m_cosine3 = metricas(predicted_response,r1)
            m_precision4,m_recall4,m_f1_score4,m_accuracy4,m_cosine4 = metricas(predicted_response,r2)
            m_precision5,m_recall5,m_f1_score5,m_accuracy5,m_cosine5 = metricas(predicted_response,r3)
            m_precision6,m_recall6,m_f1_score6,m_accuracy6,m_cosine6 = metricas(predicted_response,r4)

            R.append(r1)
            R.append(r2)
            R.append(r3)
            R.append(r4)

            kmeans_sil = kmeans_silhouette_m3(predicted_response,R)
            kmeans_tf_idf = tf_idf_kmeans_m3(predicted_response,R)
            svm_sil = svm_silhouette_m3(predicted_response,R)
            svm_tf_idf = tf_idf_svm_m3(predicted_response,R)
            lda_sil = lda_silhouette_m3(predicted_response,R)
            lda_tf_idf = lda_tfidf_m3(predicted_response,R)


            prints_str =f"---\nPergunta: {pergunta}\n---\nRespostas:\n\n{predicted_response}\n---\nRespostas geradas ao usar text2text-generation:\n\n\
-{pt2t1f['generated_text']}\n-{pt2t2f['generated_text']}\n---\nRespostas geradas ao usar question-answering:\n\n-{r1} score:{round(rs1,6)}\n-{r2} score:{round(rs2,6)}\
\n-{r3} score:{round(rs3,6)}\n-{r4} score:{round(rs4,8)}\n---\nMétricas geradas ao usar text2text-generation:\n\n-1ªResposta:\nPrecision:{m_precision1}|Recall:{m_recall1}|F1-Score:\
{m_f1_score1}|Accuracy:{m_accuracy1}|Similaridade De Cosenos:{m_cosine1}\n-2ªResposta:\nPrecision:{m_precision2}|Recall:{m_recall2}|F1-Score:{m_f1_score2}|Accuracy:{m_accuracy2}|Similaridade De Cosenos:{m_cosine2}\n---\n\
Métricas geradas ao usar question-answering:\n\n-1ªResposta:\nPrecision:{m_precision3}|Recall:{m_recall3}|F1-Score:{m_f1_score3}|Accuracy:{m_accuracy3}|Similaridade De Cosenos:{m_cosine3}\n-2ªResposta:\n\
Precision:{m_precision4}|Recall:{m_recall4}|F1-Score:{m_f1_score4}|Accuracy:{m_accuracy4}|Similaridade De Cosenos:{m_cosine4}\n-3ªResposta:\nPrecision:{m_precision5}|Recall:{m_recall5}|F1-Score:\
{m_f1_score5}|Accuracy:{m_accuracy5}|Similaridade De Cosenos:{m_cosine5}\n-4ªResposta:\nPrecision:{m_precision6}|Recall:{m_recall6}|F1-Score:{m_f1_score6}|Accuracy:{m_accuracy6}|Similaridade De Cosenos:{m_cosine6}\n---\n\
Kmeans - Silhouette em relação às respostas geradas:\n{kmeans_sil}\n---\nKmeans - TF-IDF em relação às respostas geradas:\n{kmeans_tf_idf}\n---\nSVM - Silhouette em relação às respostas geradas:\n{svm_sil}\
\n---\nSVM - TF-IDF em relação às respostas geradas:\n{svm_tf_idf}\n---\nLDA - Silhouette em relação às respostas geradas:\n{lda_sil}\n---\nLDA - TF-IDF em relação às respostas geradas:\n{lda_tf_idf}\n---\n"
            
            easygui.buttonbox(msg=prints_str, title="PLN - Meta3", choices=["Fechar"])
#
exibir_prints()
#
#------------------------------------
#--METAS 1 E 2--
#user_utterances,correct_responses = extract_dados(dataDial)
#pergunta = "Que restaurantes posso encontrar na zona oeste?"
#predicted_response = chatbot_function(pergunta) 
#print(predicted_response)
#
#results = evaluate_chatbot(user_utterances, correct_responses)
#print(results)
#
#k_means_O(correct_responses)
#print("---")
#
#kmeans_silhouette(user_utterances,correct_responses)
#tf_idf_kmeans(user_utterances, correct_responses)
#print("---")
#svm_silhouette(user_utterances, correct_responses)
#tf_idf_svm(user_utterances, correct_responses)
#print("---")
#lda_silhouette(user_utterances, correct_responses)
#lda_tfidf(user_utterances, correct_responses)
#print("---")
#------------------------------------