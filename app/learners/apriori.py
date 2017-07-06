from apyori import apriori

def extract_apriori_association_rules(matches, max_length, min_support=0.0001):
    return list(apriori(matches, min_support=min_support, max_length=max_length))

def get_apriori_association_heroes(association, string=True):
    return str(sorted(association.items)).strip("[]") if string else sorted(association.items)

def is_apriori_counter_association(association):
    hero_ids = get_apriori_association_heroes(association, string=False)
    return len(hero_ids) == 2 and hero_ids[0] < 0 and hero_ids[1] > 0
