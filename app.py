import streamlit as st
import os
import glob


#Boolean Model Code
st.set_page_config(
    page_title = "Boolean Retrieval System",
    page_icon = "🔍",
)

path = "./"
files_count = len(glob.glob1(path,"*.txt"))

terms = dict()

file_list = []
file_counter = -1
for files in os.listdir(path):
    if files.endswith(".txt"):
        with open(os.path.join(path, files),'r') as file:
            file_counter += 1
            file_list.append(files)
            word_counter=0           
            for line in file:
                for word in line.split():
                    word = word.lower()
                    if len(word)==0:
                        continue
                    if word[-1] in ".?/,;:!)(":
                        word = word[0:-1]
                    if len(word)==0:
                        continue
                    if word[0] in ".?/,;:!)(" and len(word)>1:
                        word = word[1:]
                    word = word.strip()
                    terms[word] = terms.get(word,[0]*files_count)
                    terms[word][file_counter] = 1

def get_answer(cm,ncm,rbits,crbits):
    all_result = []
    for words in cm:
        result = [1]*files_count
        all_words = words.split(" ")
        for words in all_words:
            words = words.lower()
            try:
                word_list = terms[words]
                for i in range(0,len(word_list)):
                    if word_list[i]==0:
                        result[i] = 0
            except:
                for i in range(0,files_count):
                    result[i] = 0
        all_result.append(result)



    for line in rbits:
        for words in line.split():
            words = words.lower()
            words = words.strip()
            word_list = []
            try:
                word_list = terms[words]
            except:
                word_list = [0]*files_count
            for i in range(len(word_list)):
                if word_list[i]==0:
                    word_list[i] = 1
                else:
                    word_list[i] = 0
            all_result.append(word_list)
    for line in ncm:
        for words in line.split():
            words = words.lower()
            words = words.strip()
            word_list = []
            try:
                word_list = terms[words]
            except:
                word_list = [0]*files_count
            all_result.append(word_list)

    final_result = [0]*files_count

    ran = 0

    for result in all_result:
        ran=1
        for i in range(len(result)):
            if result[i]==1:
                
                final_result[i] = 1

    if ran==0:
        final_result = [1]*files_count
    for line in crbits:
        for words in line.split():
            words = words.lower()
            words = words.strip()
            word_list = []
            try:
                word_list = terms[words]
            except:
                word_list = [0]*files_count
            for i in range(len(word_list)):
                if word_list[i]==1:
                    final_result[i] = 0
                    
    return final_result

def solve(query):
    compulsory = ""
    not_compulsory = ""
    reverse_bits = ""
    cm = []
    ncm = []
    rbits = []
    crbits = []
    f=0

    for c in query:
        if c=='<' and f==2:
            f=3
        elif c=='>' and f==3:
            f=2
            crbits.append(reverse_bits)
            reverse_bits = ""
            continue
        elif c=='<' and f!=2:
            f=2
        elif c=='>' and f==2:
            f=0
            rbits.append(reverse_bits)
            reverse_bits = ""
            continue
        elif f==3:
            reverse_bits+=c
        elif f==2:
            reverse_bits+=c
        if f==0 and c not in '"<':
            not_compulsory += c
            continue
        elif c=='"' and f==0:
            f=1
            if len(not_compulsory) > 0:
                ncm.append(not_compulsory)
                not_compulsory = ""
            continue
        elif c=='"' and f==1:
            f=0
            if len(compulsory) > 0:
                cm.append(compulsory)
                compulsory = ""
            continue
        elif f==1:
            compulsory+=c
        
    if len(not_compulsory) > 0:
        ncm.append(not_compulsory)
        not_compulsory = ""
    return get_answer(cm,ncm,rbits,crbits)


#Streamlit code

st.title('Boolean Retrieval System')

query = st.text_input("Please enter your query below.")
col1,col2,col3,col4,col5,col6,col7,col8 = st.columns(8)
with col4:
    search = st.button('Search')

with col5:
    corpus = st.button('Corpus')

