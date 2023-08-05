Allows easy creation of template tags that define a context variable


The "tag function" returns a value which, when called inside a template, is stored in a
variable or displayed directly.

Example:

@definition_tag(register=register)
def top_players(context):
    return TopScores.objects.order_by('-elo')[:20]

Inside the template, we could call {% top_players %} to output the data, or we could call
{% top_players as foo %} {{ foo }}.
