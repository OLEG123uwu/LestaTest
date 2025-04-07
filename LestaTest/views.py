from django.shortcuts import render
import re
from collections import Counter, defaultdict
import math

from django.shortcuts import render
import re
from collections import Counter, defaultdict
import math
import chardet

def index_view(request):
    word_data = []

    if request.method == 'POST' and request.FILES.getlist('files'):
        files = request.FILES.getlist('files')
        all_words = []
        document_word_counts = []
        document_frequencies = defaultdict(int)

        for uploaded_file in files:
            if uploaded_file.name.endswith(('.txt', '.doc')):
              
                raw_data = uploaded_file.read()


                detection = chardet.detect(raw_data)
                encoding = detection['encoding'] or 'utf-8'

                try:
                    text = raw_data.decode(encoding)
                except UnicodeDecodeError:
              
                    text = raw_data.decode('utf-8', errors='ignore')

                words = re.findall(r'\b\w+\b', text.lower())
                word_count = Counter(words)
                document_word_counts.append((len(words), word_count))
                all_words.append(set(word_count.keys()))

        total_documents = len(document_word_counts)

        for word_set in all_words:
            for word in word_set:
                document_frequencies[word] += 1

        combined_counts = defaultdict(lambda: {'count': 0, 'tf': 0.0, 'idf': 0.0})

        for total_words, word_count in document_word_counts:
            for word, count in word_count.items():
                tf = count / total_words
                combined_counts[word]['count'] += count
                combined_counts[word]['tf'] += tf

        for word in combined_counts:
            idf = math.log(total_documents / document_frequencies[word])
            combined_counts[word]['tf'] = round(combined_counts[word]['tf'], 4)
            combined_counts[word]['idf'] = round(idf, 4)

        for word, data in combined_counts.items():
            word_data.append({
                'word': word,
                'tf': data['tf'],
                'idf': data['idf'],
                'count': data['count']
            })

        word_data.sort(key=lambda x: x['count'], reverse=True)

    return render(request, 'index.html', {'word_data': word_data})
