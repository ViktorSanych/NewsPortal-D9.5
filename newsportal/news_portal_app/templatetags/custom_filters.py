from django import template

register = template.Library()


@register.filter()
def censor(post_text: str):
    if not isinstance(post_text, str):
        raise ValueError('Можно применить только к строке!')  # Если строка, то в ней уже ищем плохие слова
    if 'редиск' or 'баран' in post_text:
        text = post_text.replace('редиск', 'р******')
        text = text.replace('баран', 'б****')
        return text
