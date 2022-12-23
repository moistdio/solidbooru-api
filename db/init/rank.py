import db.models.models as models

def populate_ranks():
    ranks = [
        "Member",
        "Moderator",
        "Admin"
    ]

    user_list = [models.Rank(name=i) for i in ranks]
    user_list.append(models.Migration(name="populate_ranks"))
    return user_list

