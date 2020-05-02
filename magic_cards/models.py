from django.db import models

class  SetObjects(models.Model):
    """
    https://scryfall.com/docs/api/sets
    A Set object represents a group of related Magic cards. All Card objects on Scryfall belong to exactly one set.
    Due to Magic’s long and complicated history, Scryfall includes many un-official sets as a way to group promotional or outlier cards together. Such sets will likely have a code that begins with p or t, such as pcel or tori.
    Official sets always have a three-letter set code, such as zen.
    """
    id = models.UUIDField() #A unique ID for this set on Scryfall that will not change. 
    code = models.CharField(max_length = 10) #The unique three to five-letter code for this set. 
    mtgo_code = models.CharField() #The unique code for this set on MTGO, which may differ from the regular code. 
    tcgplayer_id = models.IntegerField(null=True) #This set’s ID on TCGplayer’s API, also known as the groupId. 
    name = models.CharField() #The English name of the set. 
    set_type = models.CharField() #A computer-readable classification for this set. See below. 
    released_at = models.DateTimeField() #The date the set was released or the first card was printed in the set (in GMT-8 Pacific time). 
    parent_set_code = models.CharField(null = True) #The set code for the parent set, if any. promo and token sets often have a parent set. 
    card_count = models.PositiveIntegerField() #The number of cards in this set. 
    digital = models.BooleanField(null = True) #True if this set was only released on Magic Online. 
    foil_only = models.BooleanField(null = True) #True if this set contains only foil cards. 
    scryfall_uri = models.URLField() #A link to this set’s permapage on Scryfall’s website. 
    uri = models.URLField() #A link to this set object on Scryfall’s API. 

    class Meta:
        ordering = ['id']

class CoreCardFields(models.Model):
    """
    https://scryfall.com/docs/api/cards
    Card objects represent individual Magic: The Gathering cards that players could obtain and add to their collection (with a few minor exceptions).
    Cards are the API’s most complex object. You are encouraged to thoroughly read this document and also the article about layouts and images.
    """
    arena_id = models.IntegerField(null = True) #This card’s Arena ID, if any. A large percentage of cards are not available on Arena and do not have this ID. 
    id = models.UUIDField() #A unique ID for this card in Scryfall’s database. 
    lang = models.CharField() #A language code for this printing.  #Hacer lista
    mtgo_id = models.IntegerField() #This card’s Magic Online ID (also known as the Catalog ID), if any. A large percentage of cards are not available on Magic Online and do not have this ID. 
    mtgo_foil_id = models.IntegerField() #This card’s foil Magic Online ID (also known as the Catalog ID), if any. A large percentage of cards are not available on Magic Online and do not have this ID. 
    #multiverse_ids = models.ARRAY? # Nullable 	This card’s multiverse IDs on Gatherer, if any, as an array of integers. Note that Scryfall includes many promo cards, tokens, and other esoteric objects that do not have these identifiers. 
    tcgplayer_id = models.IntegerField() #This card’s ID on TCGplayer’s API, also known as the productId. 
    object = models.CharField() #A content type for this object, always card. 
    oracle_id = models.UUIDField() #A unique ID for this card’s oracle identity. This value is consistent across reprinted card editions, and unique among different cards with the same name (tokens, Unstable variants, etc). 
    prints_search_uri = models.URLField() #A link to where you can begin paginating all re/prints for this card on Scryfall’s API. 
    rulings_uri = models.URLField() #A link to this card’s rulings list on Scryfall’s API. 
    scryfall_uri = models.URLField() #A link to this card’s permapage on Scryfall’s website. 
    uri = models.URLField() #A link to this card object on Scryfall’s API. 
    class Meta:
        ordering = ['id']

class GameplayFields(models.Model):
    """
    https://scryfall.com/docs/api/cards
    Gameplay Fields
    Cards have the following properties relevant to the game rules:

    """
    #all_parts = models.ARRAY???? # If this card is closely related to other cards, this property will be an array with Related Card Objects. 
    #card_faces = models.ARRAY??? #An array of Card Face objects, if this card is multifaced. 
    cmc = models.DecimalField() #The card’s converted mana cost. Note that some funny cards have fractional mana costs. 
    colors  = models.CharField() #https://scryfall.com/docs/api/colors #This card’s colors, if the overall card has colors defined by the rules. Otherwise the colors will be on the card_faces objects, see below. 
    color_identity = models.CharField() #https://scryfall.com/docs/api/colors #This card’s color identity. 
    color_indicator = models.CharField() #https://scryfall.com/docs/api/colors #The colors in this card’s color indicator, if any. A null value for this field indicates the card does not have one. 
    foil = models.BooleanField() #True if this printing exists in a foil version. 
    hand_modifier = models.CharField() #This card’s hand modifier, if it is Vanguard card. This value will contain a delta, such as -1. 
    layout = models.CharField() #https://scryfall.com/docs/api/layouts #A code for this card’s layout. 
    legalities = models.CharField() #A poner una lista #An object describing the legality of this card across play formats. Possible legalities are legal, not_legal, restricted, and banned. 
    life_modifier = models.CharField() #This card’s life modifier, if it is Vanguard card. This value will contain a delta, such as +2. 
    loyalty = models.CharField(null = True) #This loyalty if any. Note that some cards have loyalties that are not numeric, such as X. 
    mana_cost = models.CharField() #The mana cost for this card. This value will be any empty string "" if the cost is absent. Remember that per the game rules, a missing mana cost and a mana cost of {0} are different values. Multi-faced cards will report this value in card faces. 
    name = models.CharField() #The name of this card. If this card has multiple faces, this field will contain both names separated by ␣//␣. 
    nonfoil = models.BooleanField() #True if this printing exists in a nonfoil version. 
    oracle_text = models.CharField() #The Oracle text for this card, if any. 
    oversized = models.BooleanField() #True if this card is oversized. 
    power = models.CharField() #This card’s power, if any. Note that some cards have powers that are not numeric, such as *. 
    reserved = models.CharField() #True if this card is on the Reserved List. 
    toughness = models.CharField() #This card’s toughness, if any. Note that some cards have toughnesses that are not numeric, such as *. 
    type_line = models.CharField() # The type line of this card. 

    class Meta:
        ordering = ['name']
