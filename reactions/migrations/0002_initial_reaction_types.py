from django.db import migrations

def create_initial_reaction_types(apps, schema_editor):
    ReactionType = apps.get_model('reactions', 'ReactionType')
    initial_reactions = [
        {'name': 'Like', 'emoji': '👍', 'code': 'like'},
        {'name': 'Dislike', 'emoji': '👎', 'code': 'dislike'},
        {'name': 'Happy', 'emoji': '😀', 'code': 'happy'},
        {'name': 'Surprise', 'emoji': '😮', 'code': 'surprise'},
        {'name': 'Sad', 'emoji': '😢', 'code': 'sad'},
        {'name': 'Heart', 'emoji': '❤️', 'code': 'heart'},
    ]
    
    for reaction in initial_reactions:
        ReactionType.objects.get_or_create(**reaction)

class Migration(migrations.Migration):
    dependencies = [
        ('reactions', '0001_initial'),
    ]
    
    operations = [
        migrations.RunPython(create_initial_reaction_types),
    ]