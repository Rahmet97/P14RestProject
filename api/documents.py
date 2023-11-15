from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from elasticsearch_dsl import analyzer, tokenizer

from .models import Blog

autocomplete_analyzer = analyzer('autocomplete_analyzer',
                                 tokenizer=tokenizer('trigram', 'nGram', min_gram=1, max_gram=20),
                                 filter=['lowercase']
                                 )


@registry.register_document
class BlogDocument(Document):
    class Index:
        name = 'api'
        settings = {'number_of_shards': 1, 'number_of_replicas': 0, 'max_ngram_diff': 20}

    title = fields.TextField(
        attr='title',
        fields={
            'raw': fields.TextField(),
            'suggest': fields.CompletionField(),
        }
    )
    description = fields.TextField(
        attr='description',
        fields={
            'raw': fields.TextField()
        }
    )

    # hashtag = fields.TextField()

    class Django:
        model = Blog
