from howlongtobeatpy import HowLongToBeat

def game_add_hltb(game_dict):
    game_hltb = None
    game_name = game_dict["name"].replace("™", "").lower().replace("edition", "")
    game_hltb_list = HowLongToBeat().search(game_name)
    if game_hltb_list is not None and len(game_hltb_list) > 0:
        game_hltb = max(game_hltb_list, key=lambda element: element.similarity)

    if not game_hltb:
        game_dict["hltb"] = "N/A"
    else:
        game_dict["hltb"] = game_hltb.main_extra
    
    return game_dict






